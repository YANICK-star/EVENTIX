from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Event, Booking

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'city', 'phone_number', 'is_staff')
    list_filter = ('role', 'city', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'organization')
    fieldsets = UserAdmin.fieldsets + (
        ('Eventix Profile Details', {
            'fields': ('role', 'phone_number', 'city', 'organization', 'profile_picture')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Eventix Profile Details', {
            'fields': ('role', 'phone_number', 'city', 'organization', 'profile_picture')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'city', 'category', 'event_type', 'remaining_seats', 'max_capacity', 'price', 'status', 'start_datetime')
    list_filter = ('status', 'city', 'category', 'event_type', 'start_datetime')
    search_fields = ('title', 'description', 'venue_address', 'organizer__username', 'organizer__organization')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-start_datetime',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('ticket_code', 'attendee', 'event', 'seats_booked', 'total_price', 'status', 'booking_date', 'check_in_time')
    list_filter = ('status', 'event__city', 'booking_date', 'check_in_time')
    search_fields = ('ticket_code', 'attendee__username', 'attendee__email', 'event__title')
    readonly_fields = ('ticket_code', 'booking_date', 'qr_code')
    ordering = ('-booking_date',)
