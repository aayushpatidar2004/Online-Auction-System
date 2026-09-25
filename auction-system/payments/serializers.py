from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    auction_title = serializers.SerializerMethodField()
    buyer_username = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('id', 'auction', 'auction_title', 'buyer', 'buyer_username', 'amount', 'payment_id', 'status', 'created_at')
        read_only_fields = ('id', 'auction', 'buyer', 'auction_title', 'buyer_username', 'created_at')

    def get_auction_title(self, obj):
        return obj.auction.title if obj.auction else None

    def get_buyer_username(self, obj):
        return obj.buyer.username if obj.buyer else None
