from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'seller_rating', 'buyer_rating', 'wallet_balance', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Auction Info', {'fields': ('phone', 'seller_rating', 'buyer_rating', 'wallet_balance', 'profile_image')}),
    )
