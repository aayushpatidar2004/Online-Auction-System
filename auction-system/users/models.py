from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    seller_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    buyer_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
