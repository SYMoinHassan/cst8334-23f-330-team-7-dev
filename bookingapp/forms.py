
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import CustomUser

from datetime import timedelta

class WorkstationBookingForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    workstation_number = forms.IntegerField()
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.TimeField()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        # Remove the help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        # Do the same for any other fields where you want to remove the help text
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', ]


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateLabForm(forms.Form):
    lab_name = forms.CharField(max_length=100)
    lab_room_number = forms.CharField(max_length=100, required=False)  # Assuming this can be optional
    number_of_workstations = forms.IntegerField(min_value=1, max_value=32)
    description = forms.CharField(widget=forms.Textarea, required=False)
    # For availability, you might want to allow for multiple selections for days of the week
    availability_days = forms.MultipleChoiceField(
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False  # Assuming this can be optional
    )
    # For simplicity, let's use CharField, but you could use a more complex approach for time slots
    availability_time = forms.CharField(
        max_length=100,
        help_text='Enter the times of availability (e.g., "Tuesday 1-3pm")',
        required=False  # Assuming this can be optional
    )