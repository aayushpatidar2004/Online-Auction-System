from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from auctions.models import Auction
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(buyer=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def initiate(self, request):
        auction_id = request.data.get('auction_id')
        if not auction_id:
            return Response({'detail': 'auction_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        auction = get_object_or_404(Auction, id=auction_id)
        payment, created = Payment.objects.get_or_create(
            auction=auction,
            buyer=request.user,
            defaults={
                'amount': auction.current_highest_bid or auction.base_price,
                'status': 'pending',
                'payment_id': f'local-{auction.id}-{request.user.id}',
            },
        )

        if not created:
            payment.amount = auction.current_highest_bid or auction.base_price
            payment.status = 'pending'
            payment.save(update_fields=['amount', 'status'])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
