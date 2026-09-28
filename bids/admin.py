from django.contrib import admin

from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('auction', 'bidder', 'bid_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('auction__title', 'bidder__username')
    readonly_fields = ('created_at',)
