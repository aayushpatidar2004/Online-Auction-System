from django.http import HttpResponse
import csv
from market.models import PriceData
from django.views import View

class PriceCsvExportView(View):
    def get(self, request, *args, **kwargs):
        # Query all price data
        qs = PriceData.objects.all().order_by('date')
        # Create the HttpResponse object with CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="price_data.csv"'
        writer = csv.writer(response)
        # Write header
        writer.writerow(['commodity', 'date', 'price'])
        # Write data rows
        for pd in qs:
            writer.writerow([pd.commodity, pd.date, pd.price])
        return response
