from django.contrib import admin

from .models import Auction


@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'seller', 'base_price', 'current_highest_bid',
        'status', 'end_time',
    )
    list_filter = ('status', 'category', 'condition')
    search_fields = ('title', 'description', 'seller__username')
    readonly_fields = ('created_at',)
