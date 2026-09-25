from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from bids.models import Bid
from .models import Auction
from .serializers import AuctionDetailSerializer, AuctionSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all().order_by('-created_at')
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in {'create', 'place_bid'}:
            return [permissions.IsAuthenticated()]
        if self.action in {'update', 'partial_update', 'destroy'}:
            return [IsAdminOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = Auction.objects.all().order_by('-created_at')
        if self.action == 'my_auctions':
            return queryset.filter(seller=self.request.user)
        if self.action == 'my_bids':
            return queryset.filter(bids__bidder=self.request.user).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action in {'retrieve', 'bid_history'}:
            return AuctionDetailSerializer
        return AuctionSerializer

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_auctions(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_bids(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def bid_history(self, request, pk=None):
        auction = self.get_object()
        bids = Bid.objects.filter(auction=auction).order_by('-created_at')
        data = [
            {
                'bidder_name': bid.bidder.username,
                'bidder': bid.bidder.username,
                'amount': str(bid.bid_amount),
                'timestamp': bid.created_at.isoformat(),
                'created_at': bid.created_at.isoformat(),
            }
            for bid in bids
        ]
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def place_bid(self, request, pk=None):
        auction = self.get_object()

        # Check auction status and timeline
        if auction.status != 'active':
            return Response(
                {'detail': f'Cannot bid on an auction that is {auction.status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if auction.end_time and auction.end_time <= timezone.now():
            if auction.status == 'active':
                auction.status = 'ended'
                auction.save(update_fields=['status'])
            return Response(
                {'detail': 'This auction has already ended.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Disallow seller from bidding on their own auction
        if auction.seller == request.user:
            return Response(
                {'detail': 'You cannot bid on your own auction.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bid_amount = request.data.get('bid_amount')
        if bid_amount is None:
            return Response({'detail': 'bid_amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bid_amount = Decimal(str(bid_amount))
        except (InvalidOperation, ValueError, TypeError):
            return Response({'detail': 'Invalid bid amount.'}, status=status.HTTP_400_BAD_REQUEST)

        if bid_amount <= 0:
            return Response({'detail': 'Bid amount must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)

        if bid_amount <= auction.current_highest_bid:
            return Response(
                {'detail': f'Bid must be greater than current highest bid of {auction.current_highest_bid}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if bid_amount < auction.base_price:
            return Response(
                {'detail': f'Bid must be at least the base price of {auction.base_price}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Refresh auction row for concurrent locking if needed
            auction = Auction.objects.select_for_update().get(pk=auction.pk)

            # Re-check after lock
            if bid_amount <= auction.current_highest_bid:
                return Response(
                    {'detail': f'A higher bid of {auction.current_highest_bid} was just placed. Please increase your bid.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bid = Bid.objects.create(
                auction=auction,
                bidder=request.user,
                bid_amount=bid_amount,
                auto_bid_limit=request.data.get('auto_bid_limit'),
            )
            auction.current_highest_bid = bid_amount
            auction.highest_bidder = request.user
            auction.save(update_fields=['current_highest_bid', 'highest_bidder'])

        return Response({
            'message': 'Bid placed successfully.',
            'bid_id': bid.id,
            'bid_amount': f"{bid_amount:.2f}",
            'highest_bidder': request.user.username,
            'highest_bidder_name': request.user.username,
            'current_highest_bid': f"{auction.current_highest_bid:.2f}",
            'bid_count': auction.bids.count(),
        }, status=status.HTTP_201_CREATED)
