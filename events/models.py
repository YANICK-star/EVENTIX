import uuid
import json
import io
import qrcode
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone
from django.core.files.base import ContentFile

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ATTENDEE', 'Attendee / Participant'),
        ('ORGANIZER', 'Event Organizer'),
        ('ADMIN', 'System Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ATTENDEE')
    phone_number = models.CharField(max_length=20, blank=True, help_text="e.g., +237 6XX XXX XXX (MTN / Orange)")
    city = models.CharField(max_length=100, default='Yaoundé')
    organization = models.CharField(max_length=150, blank=True, help_text="Company, Institution, or Host Name")
    profile_picture = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        full_name = self.get_full_name()
        display = full_name if full_name else self.username
        return f"{display} ({self.get_role_display()})"

    @property
    def is_organizer(self):
        return self.role == 'ORGANIZER' or self.is_superuser

    @property
    def is_attendee(self):
        return self.role == 'ATTENDEE'

    @property
    def is_system_admin(self):
        return self.role == 'ADMIN' or self.is_superuser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-calendar-alt', help_text="FontAwesome icon class")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('ACADEMIC', 'Academic & Professional (Conferences, Seminars)'),
        ('ENTERTAINMENT', 'Entertainment & Cultural (Concerts, Festivals)'),
        ('SPORTS', 'Recreational & Sports (Football, Basketball Matches)'),
        ('PRIVATE', 'Private Milestones (Marriages, Birthdays, RSVPs)'),
    ]
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    CITY_CHOICES = [
        ('Yaoundé', 'Yaoundé'),
        ('Douala', 'Douala'),
        ('Bafoussam', 'Bafoussam'),
        ('Bamenda', 'Bamenda'),
        ('Buea', 'Buea'),
        ('Garoua', 'Garoua'),
        ('Maroua', 'Maroua'),
        ('Kribi', 'Kribi'),
        ('Limbe', 'Limbe'),
        ('Other', 'Other'),
    ]

    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organized_events')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, default='ACADEMIC')
    description = models.TextField()
    venue_address = models.CharField(max_length=255, help_text="e.g. Palais des Congrès, Salle Polyvalente, etc.")
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default='Yaoundé')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    max_capacity = models.PositiveIntegerField(help_text="Strict maximum seat or catering capacity")
    remaining_seats = models.PositiveIntegerField(help_text="Real-time available seats")
    price = models.DecimalField(max_digits=12, decimal_places=0, default=0, help_text="Ticket price in FCFA (0 for Free/RSVP)")
    banner_image = models.ImageField(upload_to='events/banners/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PUBLISHED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_datetime']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'event'
            unique_id = uuid.uuid4().hex[:6]
            self.slug = f"{base_slug}-{unique_id}"
        if self._state.adding and self.remaining_seats is None:
            self.remaining_seats = self.max_capacity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.city}) - {self.remaining_seats}/{self.max_capacity} seats"

    @property
    def booked_seats(self):
        return max(0, self.max_capacity - self.remaining_seats)

    @property
    def occupancy_percentage(self):
        if not self.max_capacity or self.max_capacity == 0:
            return 0
        return min(100, int((self.booked_seats / self.max_capacity) * 100))

    @property
    def is_free(self):
        return self.price == 0

    @property
    def is_sold_out(self):
        return self.remaining_seats <= 0

    @property
    def is_past(self):
        return self.end_datetime < timezone.now()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CHECKED_IN', 'Checked In'),
        ('CANCELLED', 'Cancelled'),
    ]

    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    ticket_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    seats_booked = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    check_in_time = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='scanned_bookings')
    qr_code = models.ImageField(upload_to='tickets/qr/', blank=True, null=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"Pass #{str(self.ticket_code)[:8].upper()} - {self.attendee.username} ({self.event.title})"

    def generate_qr_code(self):
        """Generates a high-resolution QR code encoding the ticket validation payload"""
        payload = {
            "token": str(self.ticket_code),
            "event_id": self.event.id,
            "attendee": self.attendee.get_full_name() or self.attendee.username,
            "seats": self.seats_booked,
        }
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=3,
        )
        qr.add_data(json.dumps(payload))
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0b132b", back_color="#ffffff")
        
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        filename = f"qr_{self.ticket_code}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.unit_price * self.seats_booked
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
