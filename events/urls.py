from django.urls import path
from . import views

urlpatterns = [
    # Public discovery
    path('', views.home_view, name='home'),
    path('event/<slug:slug>/', views.event_detail_view, name='event_detail'),
    path('event/<slug:slug>/book/', views.book_event_view, name='book_event'),

    # Attendee pass management
    path('my-tickets/', views.my_tickets_view, name='my_tickets'),
    path('ticket/<uuid:ticket_code>/', views.ticket_detail_view, name='ticket_detail'),
    path('ticket/<uuid:ticket_code>/cancel/', views.cancel_booking_view, name='cancel_booking'),

    # Organizer operations
    path('organizer/dashboard/', views.organizer_dashboard_view, name='organizer_dashboard'),
    path('organizer/events/new/', views.event_create_view, name='event_create'),
    path('organizer/events/<slug:slug>/edit/', views.event_edit_view, name='event_edit'),
    path('organizer/events/<slug:slug>/attendees/', views.event_attendees_view, name='event_attendees'),
    path('organizer/events/<slug:slug>/export-csv/', views.export_attendees_csv_view, name='export_attendees_csv'),
    path('organizer/scanner/', views.door_scanner_view, name='door_scanner'),
    path('organizer/scanner/<slug:slug>/', views.door_scanner_view, name='door_scanner_event'),

    # API endpoints
    path('api/verify-ticket/', views.verify_ticket_api, name='verify_ticket_api'),

    # Auth & Profile
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.profile_view, name='profile'),
]
