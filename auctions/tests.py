from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from auctions.models import Auction
from bids.models import Bid
from payments.models import Payment


class AuctionSystemAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.seller = CustomUser.objects.create_user(
            username='seller1',
            email='seller1@example.com',
            password='Password123!',
            phone='9876543210'
        )
        self.bidder1 = CustomUser.objects.create_user(
            username='bidder1',
            email='bidder1@example.com',
            password='Password123!',
            phone='9876543211'
        )
        self.bidder2 = CustomUser.objects.create_user(
            username='bidder2',
            email='bidder2@example.com',
            password='Password123!',
            phone='9876543212'
        )

        # Create active auction
        self.active_auction = Auction.objects.create(
            seller=self.seller,
            title='Vintage Brass Telescope',
            description='Authentic nautical brass telescope from 1940s in excellent condition.',
            category='art',
            condition='used',
            base_price=Decimal('100.00'),
            current_highest_bid=Decimal('100.00'),
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() + timedelta(days=2),
            status='active'
        )

        # Create ended auction
        self.ended_auction = Auction.objects.create(
            seller=self.seller,
            title='Classic Leather Watch',
            description='Rare vintage chronograph wristwatch.',
            category='fashion',
            condition='used',
            base_price=Decimal('50.00'),
            current_highest_bid=Decimal('50.00'),
            start_time=timezone.now() - timedelta(days=2),
            end_time=timezone.now() - timedelta(hours=1),
            status='ended'
        )

    def test_get_auctions_list(self):
        """Verify auctions list returns data with seller_name and bid_count"""
        response = self.client.get('/api/auctions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 2)

        first_auction = next(item for item in results if item['id'] == self.active_auction.id)
        self.assertEqual(first_auction['title'], 'Vintage Brass Telescope')
        self.assertEqual(first_auction['seller_name'], 'seller1')
        self.assertIn('bid_count', first_auction)

    def test_place_valid_bid(self):
        """Verify bidder can place a valid bid greater than current bid"""
        self.client.force_authenticate(user=self.bidder1)
        response = self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {
            'bid_amount': 150.00
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['highest_bidder'], 'bidder1')
        self.assertEqual(response.data['current_highest_bid'], '150.00')

        # Check auction updated in DB
        self.active_auction.refresh_from_db()
        self.assertEqual(self.active_auction.current_highest_bid, Decimal('150.00'))
        self.assertEqual(self.active_auction.highest_bidder, self.bidder1)
        self.assertEqual(Bid.objects.filter(auction=self.active_auction).count(), 1)

    def test_place_lower_bid_rejected(self):
        """Verify bids <= current_highest_bid are rejected"""
        self.client.force_authenticate(user=self.bidder1)
        # Bid exactly equal to current
        response = self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {
            'bid_amount': 100.00
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Bid lower than current
        response2 = self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {
            'bid_amount': 80.00
        })
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seller_cannot_bid_on_own_auction(self):
        """Verify sellers cannot bid on their own auctions"""
        self.client.force_authenticate(user=self.seller)
        response = self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {
            'bid_amount': 200.00
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('own auction', response.data['detail'].lower())

    def test_bid_on_ended_auction_rejected(self):
        """Verify bidding on ended auctions is blocked"""
        self.client.force_authenticate(user=self.bidder1)
        response = self.client.post(f'/api/auctions/{self.ended_auction.id}/place_bid/', {
            'bid_amount': 200.00
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bid_history_structure(self):
        """Verify bid_history action returns list with bidder_name, amount, and timestamp"""
        # Place two bids
        self.client.force_authenticate(user=self.bidder1)
        self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {'bid_amount': 120.00})

        self.client.force_authenticate(user=self.bidder2)
        self.client.post(f'/api/auctions/{self.active_auction.id}/place_bid/', {'bid_amount': 150.00})

        # Retrieve bid history
        response = self.client.get(f'/api/auctions/{self.active_auction.id}/bid_history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        history = response.data
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['bidder_name'], 'bidder2')
        self.assertEqual(history[0]['amount'], '150.00')
        self.assertIn('timestamp', history[0])

    def test_payment_initiation(self):
        """Verify winning/interested buyer can initiate payment"""
        self.client.force_authenticate(user=self.bidder1)
        response = self.client.post('/api/payments/initiate/', {
            'auction_id': self.active_auction.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(Decimal(str(response.data['amount'])), Decimal('100.00'))
