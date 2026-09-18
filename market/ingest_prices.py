import os
import sys
import pandas as pd

# Add project root to sys.path so Django can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmer_market.settings')

import django
django.setup()

from market.models import PriceData
from django.conf import settings

def run():
    """Ingest sample price data from CSV into PriceData model.
    Expected CSV at 'datasets/sample_prices.csv' with columns:
    - crop_name (string)
    - price (numeric)
    - date (YYYY-MM-DD)
    """
    csv_path = os.path.join(settings.BASE_DIR, 'datasets', 'sample_prices.csv')
    if not os.path.exists(csv_path):
        print(f'CSV file not found: {csv_path}')
        return

    df = pd.read_csv(csv_path)
    expected = {'crop_name', 'price', 'date'}
    if not expected.issubset(set(df.columns)):
        print('CSV missing required columns. Expected:', expected)
        return

    records = []
    for _, row in df.iterrows():
        records.append(PriceData(
            commodity=row['crop_name'],
            date=row['date'],
            price=row['price']
        ))
    PriceData.objects.bulk_create(records)
    print(f'Imported {len(records)} price records into PriceData.')

if __name__ == '__main__':
    run()
