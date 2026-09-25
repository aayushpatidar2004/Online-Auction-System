from django.conf import settings
from django.db import models


class Bid(models.Model):
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    auto_bid_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.bidder.username} - {self.bid_amount}'
