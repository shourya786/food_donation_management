from django.db import models
from django.contrib.auth.models import User

# 1. User Profile Model (Extends default Django User with roles & contact info)
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('donor', 'Food Donor'),
        ('ngo', 'NGO / Organization'),
        ('recipient', 'Recipient / Individual'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"


# 2. Food Donation Model (Stores items available for donation)
class FoodDonation(models.Model):
    FOOD_TYPE_CHOICES = (
        ('raw', 'Raw Food / Ingredients'),
        ('cooked', 'Prepared / Cooked Food'),
        ('packaged', 'Packaged / Sealed Food'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    title = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.CharField(max_length=100, help_text="e.g. 5 kg, 10 meals, 3 boxes")
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES, default='cooked')
    expiry_time = models.DateTimeField(null=True, blank=True)
    pickup_address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    claimed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='claimed_donations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

# Create your models here.
