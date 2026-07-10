from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

# --- 1. Corrected Registration Form ---
# We add 'year' and 'department' here as extra fields that are NOT part of the model.
# This allows us to collect the data during registration.
class CustomUserCreationForm(UserCreationForm):
    year = forms.CharField(max_length=10, help_text='Enter your current academic year.')
    department = forms.CharField(max_length=50, help_text='Enter your department (e.g., IT, CSE).')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # The fields for the model itself are just username and email.
        fields = ('username', 'email')

# --- 2. Forms for the "Edit Profile" Page ---
# These are the forms we'll use for the profile editing page.
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['department', 'year']