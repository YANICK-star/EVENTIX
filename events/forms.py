from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import CustomUser, Event, Booking, Category

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition shadow-sm'

class CustomUserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': 'Last Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': 'your.email@example.com'
    }))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': '+237 6XX XXX XXX'
    }))
    city = forms.ChoiceField(choices=Event.CITY_CHOICES, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    role = forms.ChoiceField(
        choices=[('ATTENDEE', 'Attendee / Participant'), ('ORGANIZER', 'Event Organizer / Host')],
        widget=forms.Select(attrs={
            'class': INPUT_CLASS
        }),
        help_text="Select 'Event Organizer' if you plan to create and manage events."
    )
    organization = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'placeholder': 'Company, Institution, or Host Name (optional)'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'city', 'role', 'organization')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['first_name', 'last_name', 'email', 'phone_number', 'city', 'role', 'organization']:
                field.widget.attrs.update({
                    'class': INPUT_CLASS
                })


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': INPUT_CLASS,
            'placeholder': 'Username or Email'
        })
        self.fields['password'].widget.attrs.update({
            'class': INPUT_CLASS,
            'placeholder': 'Password'
        })


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'city', 'organization', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
            'phone_number': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'city': forms.Select(attrs={'class': INPUT_CLASS}),
            'organization': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }


class EventForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': INPUT_CLASS
        })
    )
    end_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': INPUT_CLASS
        })
    )

    class Meta:
        model = Event
        fields = [
            'title', 'category', 'event_type', 'description', 
            'venue_address', 'city', 'start_datetime', 'end_datetime', 
            'max_capacity', 'price', 'banner_image', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g., Yaoundé Tech Summit 2026'
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASS
            }),
            'event_type': forms.Select(attrs={
                'class': INPUT_CLASS
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': INPUT_CLASS,
                'placeholder': 'Full event details, schedule, special guest speakers, dress code, etc.'
            }),
            'venue_address': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g., Palais des Congrès, Salle Polyvalente'
            }),
            'city': forms.Select(attrs={
                'class': INPUT_CLASS
            }),
            'max_capacity': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': '1'
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': '0',
                'step': '500'
            }),
            'status': forms.Select(attrs={
                'class': INPUT_CLASS
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_datetime')
        end = cleaned_data.get('end_datetime')
        if start and end and end <= start:
            raise forms.ValidationError("End date and time must be after start date and time.")
        return cleaned_data


class BookingForm(forms.Form):
    seats_booked = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-100 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white font-bold text-lg text-center focus:outline-none focus:ring-2 focus:ring-sky-500 transition shadow-sm',
            'id': 'seats-count-input'
        }),
        help_text="Maximum 10 tickets per transaction"
    )
    notes = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/70 border border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 transition shadow-sm',
            'placeholder': 'Guest names or special requests (optional)'
        })
    )
