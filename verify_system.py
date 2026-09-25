import os
import sys

# Force UTF-8 for stdout/stderr on Windows
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_backend.settings')
django.setup()

from decimal import Decimal
from django.utils import timezone
from rest_framework.test import APIClient
from users.models import CustomUser
from auctions.models import Auction
from bids.models import Bid
from payments.models import Payment

def run_system_verification():
    print("=" * 60)
    print("[*] STARTING FULL SYSTEM VERIFICATION")
    print("=" * 60)

    client = APIClient()

    # 1. Clean test data
    Payment.objects.all().delete()
    Bid.objects.all().delete()
    Auction.objects.all().delete()
    CustomUser.objects.filter(username__in=['seller_test', 'bidder_alpha', 'bidder_beta']).delete()

    # 2. Test User Registration
    print("\n[1/7] Testing User Registration API...")
    seller_data = {
        'username': 'seller_test',
        'email': 'seller@example.com',
        'phone': '9876500001',
        'password': 'SellerPassword123!',
        'password2': 'SellerPassword123!'
    }
    res = client.post('/api/users/register/', seller_data)
    assert res.status_code == 201, f"Failed to register seller: {res.data}"
    print("  [PASS] Seller user registered successfully.")

    bidder1_data = {
        'username': 'bidder_alpha',
        'email': 'bidder1@example.com',
        'phone': '9876500002',
        'password': 'BidderPassword123!',
        'password2': 'BidderPassword123!'
    }
    res = client.post('/api/users/register/', bidder1_data)
    assert res.status_code == 201, f"Failed to register bidder 1: {res.data}"
    print("  [PASS] Bidder 1 registered successfully.")

    bidder2_data = {
        'username': 'bidder_beta',
        'email': 'bidder2@example.com',
        'phone': '9876500003',
        'password': 'BidderPassword123!',
        'password2': 'BidderPassword123!'
    }
    res = client.post('/api/users/register/', bidder2_data)
    assert res.status_code == 201, f"Failed to register bidder 2: {res.data}"
    print("  [PASS] Bidder 2 registered successfully.")

    # 3. Test JWT Authentication
    print("\n[2/7] Testing JWT Token Generation...")
    login_res = client.post('/api/token/', {'username': 'seller_test', 'password': 'SellerPassword123!'})
    assert login_res.status_code == 200, f"Seller login failed: {login_res.data}"
    seller_token = login_res.data['access']
    assert seller_token, "Access token missing"
    print("  [PASS] JWT Token obtained for seller.")

    login_bidder1 = client.post('/api/token/', {'username': 'bidder_alpha', 'password': 'BidderPassword123!'})
    assert login_bidder1.status_code == 200
    bidder1_token = login_bidder1.data['access']

    login_bidder2 = client.post('/api/token/', {'username': 'bidder_beta', 'password': 'BidderPassword123!'})
    assert login_bidder2.status_code == 200
    bidder2_token = login_bidder2.data['access']

    # 4. Test Create Auction
    print("\n[3/7] Testing Create Auction API...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {seller_token}')
    auction_payload = {
        'title': 'Rare Antique Kashmiri Carpet',
        'description': 'Handcrafted pure silk Kashmiri carpet from 1950s, museum grade.',
        'category': 'art',
        'condition': 'used',
        'base_price': '2500.00',
        'start_time': timezone.now().isoformat(),
        'end_time': (timezone.now() + timezone.timedelta(days=3)).isoformat()
    }
    create_res = client.post('/api/auctions/', auction_payload)
    assert create_res.status_code == 201, f"Failed to create auction: {create_res.data}"
    auction_id = create_res.data['id']
    assert create_res.data['seller_name'] == 'seller_test', f"Unexpected seller name: {create_res.data}"
    assert create_res.data['bid_count'] == 0, "bid_count should be 0 initially"
    print(f"  [PASS] Auction #{auction_id} created with base price Rs. 2500.00.")

    # 5. Test Auction List
    print("\n[4/7] Testing Auctions List & Serializer Fields...")
    client.credentials()  # Unauthenticated public browse
    list_res = client.get('/api/auctions/')
    assert list_res.status_code == 200
    results = list_res.data.get('results', list_res.data)
    created_item = next(item for item in results if item['id'] == auction_id)
    assert 'seller_name' in created_item, "seller_name missing from list serializer"
    assert 'highest_bidder_name' in created_item, "highest_bidder_name missing from list serializer"
    assert 'bid_count' in created_item, "bid_count missing from list serializer"
    print(f"  [PASS] Auction list verified with {len(results)} item(s) and all required serializer fields.")

    # 6. Test Bidding Validations
    print("\n[5/7] Testing Bidding Validations & History...")
    
    # 6a. Seller self-bidding rejected
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {seller_token}')
    self_bid = client.post(f'/api/auctions/{auction_id}/place_bid/', {'bid_amount': 3000.00})
    assert self_bid.status_code == 400, "Seller self-bid was not rejected!"
    print("  [PASS] Blocked seller from bidding on their own auction.")

    # 6b. Valid bid from Bidder 1
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {bidder1_token}')
    bid1_res = client.post(f'/api/auctions/{auction_id}/place_bid/', {'bid_amount': 2800.00})
    assert bid1_res.status_code == 201, f"Bidder 1 bid failed: {bid1_res.data}"
    assert bid1_res.data['current_highest_bid'] == '2800.00'
    assert bid1_res.data['highest_bidder'] == 'bidder_alpha'
    print("  [PASS] Bidder 1 successfully placed bid of Rs. 2800.00.")

    # 6c. Lower / equal bid rejected from Bidder 2
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {bidder2_token}')
    low_bid = client.post(f'/api/auctions/{auction_id}/place_bid/', {'bid_amount': 2800.00})
    assert low_bid.status_code == 400, "Equal bid was not rejected!"
    low_bid2 = client.post(f'/api/auctions/{auction_id}/place_bid/', {'bid_amount': 2600.00})
    assert low_bid2.status_code == 400, "Lower bid was not rejected!"
    print("  [PASS] Lower/equal bids rejected with 400 Bad Request.")

    # 6d. Valid higher bid from Bidder 2
    bid2_res = client.post(f'/api/auctions/{auction_id}/place_bid/', {'bid_amount': 3200.00})
    assert bid2_res.status_code == 201
    assert bid2_res.data['current_highest_bid'] == '3200.00'
    assert bid2_res.data['highest_bidder'] == 'bidder_beta'
    print("  [PASS] Bidder 2 outbid Bidder 1 with Rs. 3200.00.")

    # 6e. Verify Bid History
    history_res = client.get(f'/api/auctions/{auction_id}/bid_history/')
    assert history_res.status_code == 200
    assert len(history_res.data) == 2, f"Expected 2 bids, got: {history_res.data}"
    top_bid = history_res.data[0]
    assert top_bid['bidder_name'] == 'bidder_beta'
    assert top_bid['amount'] == '3200.00'
    assert 'timestamp' in top_bid
    print(f"  [PASS] Bid history verified: {len(history_res.data)} bids with bidder_name, amount, timestamp.")

    # 7. Test Payment Initiation
    print("\n[6/7] Testing Payment Processing...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {bidder2_token}')
    pay_res = client.post('/api/payments/initiate/', {'auction_id': auction_id})
    assert pay_res.status_code == 201, f"Payment initiation failed: {pay_res.data}"
    assert pay_res.data['status'] == 'pending'
    assert Decimal(str(pay_res.data['amount'])) == Decimal('3200.00')
    print("  [PASS] Payment initiated for winning amount Rs. 3200.00.")

    my_payments = client.get('/api/payments/')
    assert my_payments.status_code == 200
    assert len(my_payments.data) >= 1
    print(f"  [PASS] Payment recorded in user payment history.")

    # 8. User Profile Verification
    print("\n[7/7] Testing Profile Retrieval & Update...")
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {bidder2_token}')
    prof_res = client.get('/api/users/profile/')
    assert prof_res.status_code == 200
    assert prof_res.data['username'] == 'bidder_beta'
    assert 'wallet_balance' in prof_res.data
    assert 'seller_rating' in prof_res.data
    assert 'buyer_rating' in prof_res.data

    patch_res = client.patch('/api/users/profile/', {'phone': '9876599999'})
    assert patch_res.status_code == 200
    assert patch_res.data['phone'] == '9876599999'
    print("  [PASS] User profile verified and updated.")

    print("\n" + "=" * 60)
    print("[SUCCESS] ALL SYSTEM & API VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_system_verification()
