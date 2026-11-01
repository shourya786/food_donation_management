from django.contrib import admin
from .models import UserProfile, FoodDonation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number')
    list_filter = ('role',)

@admin.register(FoodDonation)
class FoodDonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'food_type', 'status', 'created_at')
    list_filter = ('status', 'food_type')
    search_fields = ('title', 'description', 'pickup_address')
