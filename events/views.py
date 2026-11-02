import csv
import json
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum, Count, F
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import CustomUser, Category, Event, Booking
from .forms import (
    CustomUserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    EventForm,
    BookingForm
)

# ----------------------------------------------------
# 1. PUBLIC DISCOVERY & EVENT VIEWS
# ----------------------------------------------------

def home_view(request):
    """Event catalog discovery page with search and multi-facet filters"""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    city = request.GET.get('city', '').strip()
    event_type = request.GET.get('type', '').strip()

    events = Event.objects.filter(status='PUBLISHED').select_related('category', 'organizer')

    if query:
        events = events.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(venue_address__icontains=query) |
            Q(organizer__organization__icontains=query)
        )

    if category_slug:
        events = events.filter(category__slug=category_slug)

    if city and city != 'All':
        events = events.filter(city=city)

    if event_type:
        events = events.filter(event_type=event_type)

    # Highlight featured events (e.g., upcoming soonest with high capacity)
    now = timezone.now()
    upcoming_events = events.filter(end_datetime__gte=now).order_by('start_datetime')
    past_events = events.filter(end_datetime__lt=now).order_by('-start_datetime')[:6]

    # Quick metrics for Cameroonian ecosystem landing banner
    total_events_count = Event.objects.filter(status='PUBLISHED').count()
    total_attendees_count = Booking.objects.filter(status__in=['CONFIRMED', 'CHECKED_IN']).aggregate(
        total=Sum('seats_booked')
    )['total'] or 0
    total_organizers_count = CustomUser.objects.filter(role='ORGANIZER').count()

    context = {
        'events': upcoming_events,
        'past_events': past_events,
        'query': query,
        'selected_category': category_slug,
        'selected_city': city,
        'selected_type': event_type,
        'total_events_count': total_events_count,
        'total_attendees_count': total_attendees_count,
        'total_organizers_count': total_organizers_count,
    }
    return render(request, 'events/home.html', context)


def event_detail_view(request, slug):
    """Full detail view for a specific event with live seat availability"""
    event = get_object_or_404(Event.objects.select_related('category', 'organizer'), slug=slug)
    user_booking = None
    if request.user.is_authenticated:
        user_booking = Booking.objects.filter(attendee=request.user, event=event, status__in=['CONFIRMED', 'CHECKED_IN']).first()

    booking_form = BookingForm()
    related_events = Event.objects.filter(category=event.category, status='PUBLISHED').exclude(id=event.id)[:3]

    context = {
        'event': event,
        'user_booking': user_booking,
        'booking_form': booking_form,
        'related_events': related_events,
    }
    return render(request, 'events/event_detail.html', context)


# ----------------------------------------------------
# 2. ATOMIC BOOKING ENGINE (CONCURRENCY-SAFE)
# ----------------------------------------------------

@login_required
def book_event_view(request, slug):
    """
    Capacity-controlled booking view with @transaction.atomic & select_for_update()
    Guarantees that tickets never overbook under high concurrent demand.
    """
    if request.method != 'POST':
        return redirect('event_detail', slug=slug)

    form = BookingForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid booking request. Please select a valid number of seats.")
        return redirect('event_detail', slug=slug)

    seats_requested = form.cleaned_data['seats_booked']
    notes = form.cleaned_data.get('notes', '')

    try:
        with transaction.atomic():
            # Lock the event row for update to prevent race conditions
            event = Event.objects.select_for_update().get(slug=slug)

            # Check if event is active and has enough capacity
            if event.status != 'PUBLISHED':
                messages.error(request, "This event is not currently accepting bookings.")
                return redirect('event_detail', slug=slug)

            if event.is_past:
                messages.error(request, "This event has already ended.")
                return redirect('event_detail', slug=slug)

            if event.remaining_seats < seats_requested:
                messages.error(
                    request, 
                    f"Booking failed! Only {event.remaining_seats} seat(s) remaining, but you requested {seats_requested}."
                )
                return redirect('event_detail', slug=slug)

            # Decrement seats safely
            event.remaining_seats -= seats_requested
            event.save(update_fields=['remaining_seats'])

            # Calculate pricing
            unit_price = event.price
            total_price = unit_price * seats_requested

            # Create Booking and generate cryptographic QR ticket
            booking = Booking.objects.create(
                attendee=request.user,
                event=event,
                seats_booked=seats_requested,
                unit_price=unit_price,
                total_price=total_price,
                notes=notes,
                status='CONFIRMED'
            )

        messages.success(
            request, 
            f"Félicitations! Your booking for {event.title} is confirmed ({seats_requested} pass). Access your QR pass below."
        )
        return redirect('ticket_detail', ticket_code=booking.ticket_code)

    except Event.DoesNotExist:
        messages.error(request, "Event not found.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"An unexpected error occurred during reservation: {str(e)}")
        return redirect('event_detail', slug=slug)


@login_required
def ticket_detail_view(request, ticket_code):
    """Digital Boarding Pass / QR Ticket View"""
    booking = get_object_or_404(
        Booking.objects.select_related('event', 'event__organizer', 'attendee'),
        ticket_code=ticket_code
    )

    # Permission check: Attendee, Organizer of the event, or Admin can view
    is_owner = booking.attendee == request.user
    is_event_organizer = booking.event.organizer == request.user
    if not (is_owner or is_event_organizer or request.user.is_superuser):
        messages.error(request, "You do not have permission to view this ticket.")
        return redirect('home')

    context = {
        'booking': booking,
        'event': booking.event,
        'is_owner': is_owner,
        'is_event_organizer': is_event_organizer,
    }
    return render(request, 'events/ticket_detail.html', context)


@login_required
def my_tickets_view(request):
    """Attendee dashboard showing booked passes and RSVP history"""
    bookings = Booking.objects.filter(attendee=request.user).select_related('event', 'event__category').order_by('-booking_date')
    now = timezone.now()

    upcoming_bookings = [b for b in bookings if b.event.end_datetime >= now and b.status != 'CANCELLED']
    past_or_cancelled = [b for b in bookings if b.event.end_datetime < now or b.status == 'CANCELLED']

    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_or_cancelled': past_or_cancelled,
    }
    return render(request, 'events/my_tickets.html', context)


@login_required
def cancel_booking_view(request, ticket_code):
    """Cancels a booking and safely releases reserved seats back to the event pool"""
    if request.method != 'POST':
        return redirect('ticket_detail', ticket_code=ticket_code)

    booking = get_object_or_404(Booking.objects.select_related('event'), ticket_code=ticket_code)

    if booking.attendee != request.user and not request.user.is_superuser:
        messages.error(request, "You do not have permission to cancel this booking.")
        return redirect('my_tickets')

    if booking.status == 'CANCELLED':
        messages.info(request, "This booking has already been cancelled.")
        return redirect('my_tickets')

    if booking.status == 'CHECKED_IN':
        messages.error(request, "Cannot cancel a ticket that has already been checked in at the door.")
        return redirect('ticket_detail', ticket_code=ticket_code)

    try:
        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=booking.event.id)
            event.remaining_seats += booking.seats_booked
            if event.remaining_seats > event.max_capacity:
                event.remaining_seats = event.max_capacity
            event.save(update_fields=['remaining_seats'])

            booking.status = 'CANCELLED'
            booking.save(update_fields=['status'])

        messages.success(request, f"Your reservation for {booking.event.title} has been cancelled and {booking.seats_booked} seat(s) released.")
    except Exception as e:
        messages.error(request, f"Error cancelling reservation: {str(e)}")

    return redirect('my_tickets')


# ----------------------------------------------------
# 3. ORGANIZER WORKSPACE & DASHBOARD
# ----------------------------------------------------

@login_required
def organizer_dashboard_view(request):
    """Organizer Command Center: Stats, occupancy rates, and quick controls"""
    if not (request.user.is_organizer or request.user.is_superuser):
        messages.warning(request, "Please register or upgrade as an Event Organizer to access the Organizer Dashboard.")
        return redirect('home')

    organizer_events = Event.objects.filter(organizer=request.user).select_related('category').annotate(
        attendees_count=Sum('bookings__seats_booked', filter=Q(bookings__status__in=['CONFIRMED', 'CHECKED_IN'])),
        checked_in_count=Sum('bookings__seats_booked', filter=Q(bookings__status='CHECKED_IN')),
        revenue=Sum('bookings__total_price', filter=Q(bookings__status__in=['CONFIRMED', 'CHECKED_IN']))
    ).order_by('-created_at')

    total_events = organizer_events.count()
    total_revenue = sum(e.revenue or 0 for e in organizer_events)
    total_attendees = sum(e.attendees_count or 0 for e in organizer_events)
    total_checked_in = sum(e.checked_in_count or 0 for e in organizer_events)

    context = {
        'events': organizer_events,
        'total_events': total_events,
        'total_revenue': total_revenue,
        'total_attendees': total_attendees,
        'total_checked_in': total_checked_in,
    }
    return render(request, 'events/organizer_dashboard.html', context)


@login_required
def event_create_view(request):
    """Create a new event with strict capacity limits and venue boundaries"""
    if not (request.user.is_organizer or request.user.is_superuser):
        messages.error(request, "Only Event Organizers can publish new events.")
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.remaining_seats = event.max_capacity
            event.save()
            messages.success(request, f"Event '{event.title}' created and published successfully!")
            return redirect('organizer_dashboard')
    else:
        form = EventForm()

    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'events/event_create_edit.html', context)


@login_required
def event_edit_view(request, slug):
    """Edit an existing event"""
    event = get_object_or_404(Event, slug=slug)

    if event.organizer != request.user and not request.user.is_superuser:
        messages.error(request, "You are not authorized to edit this event.")
        return redirect('organizer_dashboard')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save(commit=False)
            # Recompute remaining seats if max_capacity changed
            booked = event.max_capacity - event.remaining_seats
            updated_event.remaining_seats = max(0, updated_event.max_capacity - booked)
            updated_event.save()
            messages.success(request, f"Event '{updated_event.title}' updated successfully!")
            return redirect('organizer_dashboard')
    else:
        form = EventForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'is_edit': True,
    }
    return render(request, 'events/event_create_edit.html', context)


@login_required
def event_attendees_view(request, slug):
    """View real-time attendee roster for a specific event with manual check-in toggle"""
    event = get_object_or_404(Event, slug=slug)

    if event.organizer != request.user and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('organizer_dashboard')

    bookings = Booking.objects.filter(event=event).select_related('attendee').order_by('-booking_date')

    search = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search:
        bookings = bookings.filter(
            Q(attendee__username__icontains=search) |
            Q(attendee__first_name__icontains=search) |
            Q(attendee__last_name__icontains=search) |
            Q(attendee__email__icontains=search) |
            Q(attendee__phone_number__icontains=search) |
            Q(ticket_code__icontains=search)
        )

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    context = {
        'event': event,
        'bookings': bookings,
        'search': search,
        'status_filter': status_filter,
    }
    return render(request, 'events/event_attendees.html', context)


@login_required
def export_attendees_csv_view(request, slug):
    """Exports attendee roster as a clean, standardized CSV file for organizers"""
    event = get_object_or_404(Event, slug=slug)

    if event.organizer != request.user and not request.user.is_superuser:
        messages.error(request, "Access denied.")
        return redirect('organizer_dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="inventix_{event.slug}_attendees.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Ticket Pass Code', 'Attendee Name', 'Username', 'Email', 
        'Phone Number', 'City', 'Seats Booked', 'Total (FCFA)', 
        'Status', 'Booking Timestamp', 'Door Check-in Time'
    ])

    bookings = Booking.objects.filter(event=event).select_related('attendee').order_by('booking_date')

    for b in bookings:
        writer.writerow([
            str(b.ticket_code),
            b.attendee.get_full_name() or b.attendee.username,
            b.attendee.username,
            b.attendee.email,
            b.attendee.phone_number or 'N/A',
            b.attendee.city,
            b.seats_booked,
            b.total_price,
            b.get_status_display(),
            b.booking_date.strftime('%Y-%m-%d %H:%M'),
            b.check_in_time.strftime('%Y-%m-%d %H:%M') if b.check_in_time else 'Pending'
        ])

    return response


# ----------------------------------------------------
# 4. DOOR SCANNER UI & REAL-TIME VERIFICATION API
# ----------------------------------------------------

@login_required
def door_scanner_view(request, slug=None):
    """
    Door Scanner Interface:
    Supports HTML5 Camera QR Code scanning and manual ticket token lookup.
    """
    if not (request.user.is_organizer or request.user.is_superuser):
        messages.error(request, "Door scanner is reserved for event organizers and authorized ushers.")
        return redirect('home')

    user_events = Event.objects.filter(organizer=request.user, status='PUBLISHED').order_by('-start_datetime')
    active_event = None

    if slug:
        active_event = get_object_or_404(Event, slug=slug, organizer=request.user)
    elif user_events.exists():
        active_event = user_events.first()

    context = {
        'events': user_events,
        'active_event': active_event,
    }
    return render(request, 'events/scanner.html', context)


@login_required
@require_POST
def verify_ticket_api(request):
    """
    Real-Time Ticket Validation Endpoint (AJAX / Scanner POST)
    Accepts QR payload or manual UUID ticket code.
    Returns JSON response with instant feedback: Valid, Already Scanned, Invalid, or Wrong Event.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    raw_token = data.get('token', '').strip()
    target_event_id = data.get('event_id')

    if not raw_token:
        return JsonResponse({'success': False, 'message': 'No ticket token provided.'}, status=400)

    # In case the raw QR code is a full JSON string
    ticket_uuid = raw_token
    if raw_token.startswith('{') and 'token' in raw_token:
        try:
            parsed = json.loads(raw_token)
            ticket_uuid = parsed.get('token', raw_token)
        except Exception:
            pass

    try:
        ticket_code = uuid.UUID(ticket_uuid)
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Invalid ticket format.'}, status=400)

    try:
        booking = Booking.objects.select_related('event', 'attendee', 'event__organizer').get(ticket_code=ticket_code)
    except Booking.DoesNotExist:
        return JsonResponse({
            'success': False,
            'status': 'INVALID',
            'message': '❌ Ticket Pass NOT FOUND. Invalid or fraudulent pass.'
        }, status=404)

    # Security check: Does this user have permission to check-in for this event?
    if booking.event.organizer != request.user and not request.user.is_superuser:
        return JsonResponse({
            'success': False,
            'status': 'UNAUTHORIZED',
            'message': '⛔ You are not authorized to check-in guests for this event.'
        }, status=403)

    # Event scope verification if an active event filter is selected
    if target_event_id and str(booking.event.id) != str(target_event_id):
        return JsonResponse({
            'success': False,
            'status': 'WRONG_EVENT',
            'message': f"⚠️ Ticket is for a DIFFERENT event: '{booking.event.title}'"
        }, status=400)

    # Status check
    if booking.status == 'CANCELLED':
        return JsonResponse({
            'success': False,
            'status': 'CANCELLED',
            'message': '⛔ TICKET CANCELLED. This reservation was previously cancelled.'
        }, status=400)

    if booking.status == 'CHECKED_IN':
        check_in_str = booking.check_in_time.strftime('%H:%M:%S') if booking.check_in_time else 'Earlier'
        return JsonResponse({
            'success': False,
            'status': 'ALREADY_CHECKED_IN',
            'message': f"⚠️ ALREADY CHECKED IN at {check_in_str}! (Possible duplicate pass attempt)",
            'attendee': booking.attendee.get_full_name() or booking.attendee.username,
            'seats': booking.seats_booked,
            'event': booking.event.title
        })

    # Legitimate first check-in
    booking.status = 'CHECKED_IN'
    booking.check_in_time = timezone.now()
    booking.checked_in_by = request.user
    booking.save(update_fields=['status', 'check_in_time', 'checked_in_by'])

    return JsonResponse({
        'success': True,
        'status': 'CONFIRMED',
        'message': f"✅ VALID PASS! Welcome {booking.attendee.get_full_name() or booking.attendee.username}",
        'attendee': booking.attendee.get_full_name() or booking.attendee.username,
        'seats': booking.seats_booked,
        'event': booking.event.title,
        'check_in_time': booking.check_in_time.strftime('%H:%M:%S')
    })


# ----------------------------------------------------
# 5. AUTHENTICATION & PROFILE VIEWS
# ----------------------------------------------------

def register_view(request):
    """Custom user registration with role selection (Attendee vs Organizer)"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue on Eventix, {user.first_name or user.username}! Your account has been created.")
            if user.is_organizer:
                return redirect('organizer_dashboard')
            return redirect('home')
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if user.is_organizer:
                return redirect('organizer_dashboard')
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required
def profile_view(request):
    """User Profile management"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'auth/profile.html', {'form': form})
