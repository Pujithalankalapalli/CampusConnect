# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. Leaner CustomUser Model (for Authentication) ---
# We keep only the fields needed for login and verification.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_otp_verified = models.BooleanField(default=False) # Renamed for clarity

    def __str__(self):
        return self.username

# --- 2. New Profile Model (for Profile Information) ---
# This model holds all the extra user details.
class Profile(models.Model):
    # This creates a one-to-one link with a user.
    # If a User is deleted, their Profile is deleted too (on_delete=models.CASCADE).
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    # Using PositiveIntegerField is better for a year number.
    year = models.PositiveIntegerField(null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# --- 3. Django Signals to Automate Profile Creation ---
# This code ensures that whenever a new CustomUser is created,
# a corresponding Profile is automatically created for them.

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Ensures that the profile is saved whenever the user object is saved
    instance.profile.save()