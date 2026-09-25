from rest_framework import serializers
from .models import Auction
from bids.models import Bid


class AuctionSerializer(serializers.ModelSerializer):
    seller_name = serializers.SerializerMethodField()
    highest_bidder_name = serializers.SerializerMethodField()
    seller_username = serializers.SerializerMethodField()
    highest_bidder_username = serializers.SerializerMethodField()
    bid_count = serializers.SerializerMethodField()
    current_highest_bid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Auction
        fields = (
            'id', 'title', 'description', 'category', 'condition',
            'base_price', 'current_highest_bid', 'highest_bidder',
            'start_time', 'end_time', 'status', 'seller_name',
            'highest_bidder_name', 'seller_username', 'highest_bidder_username',
            'image', 'bid_count', 'created_at', 'seller'
        )
        read_only_fields = (
            'id', 'seller', 'current_highest_bid', 'highest_bidder',
            'created_at', 'seller_name', 'highest_bidder_name',
            'seller_username', 'highest_bidder_username', 'bid_count'
        )

    def validate_base_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Base price must be greater than zero.')
        return value

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({'end_time': 'End time must be later than the start time.'})

        return attrs

    def get_seller_name(self, obj):
        return obj.seller.username if obj.seller else None

    def get_highest_bidder_name(self, obj):
        return obj.highest_bidder.username if obj.highest_bidder else None

    def get_seller_username(self, obj):
        return self.get_seller_name(obj)

    def get_highest_bidder_username(self, obj):
        return self.get_highest_bidder_name(obj)

    def get_bid_count(self, obj):
        return obj.bids.count()


class AuctionDetailSerializer(AuctionSerializer):
    bid_history = serializers.SerializerMethodField()

    class Meta(AuctionSerializer.Meta):
        fields = AuctionSerializer.Meta.fields + ('bid_history',)

    def get_bid_history(self, obj):
        return [
            {
                'bidder_name': bid.bidder.username,
                'bidder': bid.bidder.username,
                'amount': str(bid.bid_amount),
                'timestamp': bid.created_at.isoformat(),
                'created_at': bid.created_at.isoformat(),
            }
            for bid in Bid.objects.filter(auction=obj).order_by('-created_at')[:25]
        ]
