import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eventix_project.settings')
django.setup()

from events.models import CustomUser, Category, Event, Booking

def seed():
    print("[*] Seeding Eventix Cameroon Database...")

    # 1. Categories
    categories_data = [
        {"name": "Academic & Professional", "slug": "academic-professional", "description": "Conferences, Tech Symposia, Research Colloquiums", "icon": "fa-graduation-cap"},
        {"name": "Entertainment & Cultural", "slug": "entertainment-cultural", "description": "Concerts, Festivals, Galas, Fashion Shows", "icon": "fa-music"},
        {"name": "Recreational & Sports", "slug": "recreational-sports", "description": "Football Matches, Basketball Tournaments, Marathons", "icon": "fa-futbol"},
        {"name": "Private Milestones", "slug": "private-milestones", "description": "Weddings, Anniversaries, Executive RSVPs", "icon": "fa-champagne-glasses"},
    ]
    categories = {}
    for cat in categories_data:
        c, _ = Category.objects.get_or_create(slug=cat['slug'], defaults=cat)
        categories[cat['slug']] = c
    print(f"[OK] Created {len(categories)} categories")

    # 2. Users
    # Admin
    if not CustomUser.objects.filter(username='admin').exists():
        admin_user = CustomUser.objects.create_superuser('admin', 'admin@eventix.cm', 'admin12345')
        admin_user.role = 'ADMIN'
        admin_user.first_name = 'Chief'
        admin_user.last_name = 'Administrator'
        admin_user.city = 'Yaoundé'
        admin_user.organization = 'Eventix Core Tech Team'
        admin_user.save()
        print("[OK] Created Superuser: admin / admin12345")
    else:
        admin_user = CustomUser.objects.get(username='admin')

    # Organizer 1: IAI Cameroon
    organizer_iai, _ = CustomUser.objects.get_or_create(
        username='iai_organizer',
        defaults={
            'email': 'events@iai-cameroon.cm',
            'first_name': 'Alain',
            'last_name': 'Nguemo',
            'role': 'ORGANIZER',
            'city': 'Yaoundé',
            'organization': 'IAI Cameroon / CET Paul Biya',
            'phone_number': '+237 677 889 900'
        }
    )
    organizer_iai.set_password('pass12345')
    organizer_iai.save()

    # Organizer 2: Douala Live Media
    organizer_douala, _ = CustomUser.objects.get_or_create(
        username='douala_media',
        defaults={
            'email': 'contact@douala-live.cm',
            'first_name': 'Chantal',
            'last_name': 'Ewondo',
            'role': 'ORGANIZER',
            'city': 'Douala',
            'organization': 'Douala Creative Arts & Culture',
            'phone_number': '+237 699 112 233'
        }
    )
    organizer_douala.set_password('pass12345')
    organizer_douala.save()

    # Attendees
    attendee_paul, _ = CustomUser.objects.get_or_create(
        username='paul_biya_student',
        defaults={
            'email': 'paul.student@iai.cm',
            'first_name': 'Paul',
            'last_name': 'Kamga',
            'role': 'ATTENDEE',
            'city': 'Yaoundé',
            'phone_number': '+237 655 443 322'
        }
    )
    attendee_paul.set_password('pass12345')
    attendee_paul.save()

    attendee_marie, _ = CustomUser.objects.get_or_create(
        username='marie_douala',
        defaults={
            'email': 'marie.fotso@gmail.com',
            'first_name': 'Marie',
            'last_name': 'Fotso',
            'role': 'ATTENDEE',
            'city': 'Douala',
            'phone_number': '+237 688 221 100'
        }
    )
    attendee_marie.set_password('pass12345')
    attendee_marie.save()
    print("[OK] Created demo users: admin, iai_organizer, douala_media, paul_biya_student, marie_douala")

    # 3. Events
    now = timezone.now()

    events_data = [
        {
            "organizer": organizer_iai,
            "title": "Yaoundé National Tech & AI Summit 2026",
            "category": categories['academic-professional'],
            "event_type": "ACADEMIC",
            "description": "The largest gathering of software engineers, AI researchers, and digital innovators in Central Africa. Keynotes on scalable cloud computing, Fintech innovation in CEMAC, and youth empowerment. Featuring exhibitions by leading tech startups and universities.",
            "venue_address": "Palais des Congrès, Grande Salle",
            "city": "Yaoundé",
            "start_datetime": now + timedelta(days=5, hours=9),
            "end_datetime": now + timedelta(days=5, hours=17),
            "max_capacity": 250,
            "price": 2500,
            "status": "PUBLISHED"
        },
        {
            "organizer": organizer_douala,
            "title": "Douala International Afrobeat & Urban Music Fest",
            "category": categories['entertainment-cultural'],
            "event_type": "ENTERTAINMENT",
            "description": "An electric open-air celebration of Cameroonian sound, Makossa fusion, and contemporary urban music. Live performances by top local and international artists, artisan culinary stalls, and vibrant youth showcases.",
            "venue_address": "Bercy Hall Esplanade, Bonanjo",
            "city": "Douala",
            "start_datetime": now + timedelta(days=12, hours=18),
            "end_datetime": now + timedelta(days=13, hours=2),
            "max_capacity": 500,
            "price": 5000,
            "status": "PUBLISHED"
        },
        {
            "organizer": organizer_iai,
            "title": "Elite One Football Derby: Canon vs Tonnerre",
            "category": categories['recreational-sports'],
            "event_type": "SPORTS",
            "description": "The legendary capital city clash! Pre-booked verified stadium access to avoid physical ticket queues and stampedes at the gates. Instant QR code verification for Tribune d'Honneur and Virages.",
            "venue_address": "Stade Omnisports Ahmadou Ahidjo",
            "city": "Yaoundé",
            "start_datetime": now + timedelta(days=8, hours=15),
            "end_datetime": now + timedelta(days=8, hours=18),
            "max_capacity": 300,
            "price": 2000,
            "status": "PUBLISHED"
        },
        {
            "organizer": organizer_iai,
            "title": "Jean-Paul & Brenda Royal Marriage Celebration",
            "category": categories['private-milestones'],
            "event_type": "PRIVATE",
            "description": "Strict RSVP capacity locking ceremony and reception. Only guests with verified digital QR passes will be admitted by the ushers. Please confirm attendance before the seating limit is met.",
            "venue_address": "Salle Polyvalente de Tsinga",
            "city": "Yaoundé",
            "start_datetime": now + timedelta(days=15, hours=12),
            "end_datetime": now + timedelta(days=15, hours=20),
            "max_capacity": 80,
            "price": 0,  # Free RSVP
            "status": "PUBLISHED"
        },
        {
            "organizer": organizer_douala,
            "title": "Silicon Mountain Buea DevFest & Hackathon",
            "category": categories['academic-professional'],
            "event_type": "ACADEMIC",
            "description": "Hands-on coding sprints, open-source workshops, and startup pitching in the heart of Buea's Silicon Mountain ecosystem. Fast-paced mentor sessions with industry experts.",
            "venue_address": "Mountain Hotel Convention Center",
            "city": "Buea",
            "start_datetime": now + timedelta(days=20, hours=10),
            "end_datetime": now + timedelta(days=21, hours=16),
            "max_capacity": 120,
            "price": 1000,
            "status": "PUBLISHED"
        }
    ]

    created_events = []
    for ed in events_data:
        ev, created = Event.objects.get_or_create(
            title=ed['title'],
            defaults=ed
        )
        if created:
            ev.remaining_seats = ev.max_capacity
            ev.save()
        created_events.append(ev)
    print(f"[OK] Created {len(created_events)} Cameroonian showcase events")

    # 4. Sample Bookings with generated QR codes
    # Booking 1: Paul Kamga for Yaoundé Tech Summit
    ev1 = created_events[0]
    b1, _ = Booking.objects.get_or_create(
        attendee=attendee_paul,
        event=ev1,
        defaults={
            'seats_booked': 2,
            'unit_price': ev1.price,
            'total_price': ev1.price * 2,
            'status': 'CONFIRMED',
            'notes': 'Paul Kamga + 1 Student Developer'
        }
    )
    if b1.event.remaining_seats == b1.event.max_capacity:
        b1.event.remaining_seats -= b1.seats_booked
        b1.event.save()

    # Booking 2: Marie Fotso for Douala Music Fest
    ev2 = created_events[1]
    b2, _ = Booking.objects.get_or_create(
        attendee=attendee_marie,
        event=ev2,
        defaults={
            'seats_booked': 3,
            'unit_price': ev2.price,
            'total_price': ev2.price * 3,
            'status': 'CONFIRMED',
            'notes': 'VIP Table Section'
        }
    )
    if b2.event.remaining_seats == b2.event.max_capacity:
        b2.event.remaining_seats -= b2.seats_booked
        b2.event.save()

    # Booking 3: Paul Kamga for Private Marriage RSVP
    ev4 = created_events[3]
    b3, _ = Booking.objects.get_or_create(
        attendee=attendee_paul,
        event=ev4,
        defaults={
            'seats_booked': 1,
            'unit_price': 0,
            'total_price': 0,
            'status': 'CHECKED_IN',
            'check_in_time': now - timedelta(hours=1),
            'checked_in_by': organizer_iai,
            'notes': 'Table 4 - Friend of the Groom'
        }
    )
    if b3.event.remaining_seats == b3.event.max_capacity:
        b3.event.remaining_seats -= b3.seats_booked
        b3.event.save()

    print(f"[OK] Created sample bookings with QR codes: Pass #{b1.ticket_code}, Pass #{b2.ticket_code}")
    print("\n[SUCCESS] Seed completed successfully!")

if __name__ == '__main__':
    seed()
