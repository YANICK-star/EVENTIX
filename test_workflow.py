import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eventix_project.settings')
django.setup()

from django.test import Client
from django.utils import timezone
from events.models import CustomUser, Event, Booking

def test_full_system():
    print("[*] Running End-to-End System Integration Test...")
    client = Client()

    # 1. Login as attendee
    logged_in = client.login(username='paul_biya_student', password='pass12345')
    assert logged_in, "Attendee login failed"
    print("[OK] Attendee authenticated successfully.")

    # 2. Check event capacity before booking
    event = Event.objects.get(title="Yaoundé National Tech & AI Summit 2026")
    initial_seats = event.remaining_seats
    print(f"[*] Initial seats for '{event.title}': {initial_seats}/{event.max_capacity}")

    # 3. Post atomic booking
    response = client.post(f'/event/{event.slug}/book/', {
        'seats_booked': 2,
        'notes': 'Test Automated Booking'
    }, follow=True)
    assert response.status_code == 200, f"Booking failed with code {response.status_code}"

    # 4. Verify seats decremented in DB
    event.refresh_from_db()
    assert event.remaining_seats == initial_seats - 2, f"Atomic seat decrement mismatch: {event.remaining_seats} vs {initial_seats - 2}"
    print(f"[OK] Atomic booking confirmed! Remaining seats properly updated to {event.remaining_seats}.")

    # 5. Fetch newly generated booking
    new_booking = Booking.objects.filter(attendee__username='paul_biya_student', event=event).order_by('-booking_date').first()
    assert new_booking is not None
    assert new_booking.qr_code, "QR code image not generated!"
    print(f"[OK] Cryptographic pass generated: #{new_booking.ticket_code}")

    # 6. Test Door Check-in API as Event Organizer
    org_client = Client()
    org_logged_in = org_client.login(username='iai_organizer', password='pass12345')
    assert org_logged_in, "Organizer login failed"

    # First check-in scan: Should succeed
    res = org_client.post('/api/verify-ticket/', {
        'token': str(new_booking.ticket_code),
        'event_id': str(event.id)
    }, content_type='application/json')
    data = res.json()
    assert res.status_code == 200
    assert data.get('success') is True and data.get('status') == 'CONFIRMED'
    print(f"[OK] Gate QR Scan 1: {data.get('status')} - Success: {data.get('success')}")

    # Second check-in scan with same pass: Should detect duplicate entry attempt!
    res2 = org_client.post('/api/verify-ticket/', {
        'token': str(new_booking.ticket_code),
        'event_id': str(event.id)
    }, content_type='application/json')
    data2 = res2.json()
    assert data2.get('status') == 'ALREADY_CHECKED_IN'
    print(f"[OK] Gate QR Scan 2: Anti-Gate-Crash detection verified! Status: {data2.get('status')}")

    # Fraudulent check-in attempt with fake UUID
    res3 = org_client.post('/api/verify-ticket/', {
        'token': '00000000-0000-0000-0000-000000000000',
        'event_id': str(event.id)
    }, content_type='application/json')
    assert res3.status_code == 404
    print("[OK] Gate QR Scan 3: Fraudulent token successfully rejected (404 Not Found).")

    print("\n[SUCCESS] ALL INTEGRATION TESTS PASSED WITH 100% ACCURACY!")

if __name__ == '__main__':
    test_full_system()
