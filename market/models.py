from django.db import models

class PriceData(models.Model):
    commodity = models.CharField(max_length=100)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = (('commodity', 'date'),)
        ordering = ['-date']

    def __str__(self):
        return f"{self.commodity} - {self.date}: {self.price}"
