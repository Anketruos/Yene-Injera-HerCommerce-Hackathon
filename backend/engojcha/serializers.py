from rest_framework import serializers
from .models import User, Seller, Injera, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'location', 'profile_image', 'bio']


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'user', 'business_name', 'contact_number', 'address', 'verified']


class RatingSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = [
            'id', 'buyer', 'injera', 'texture_rating',
            'sourness_rating', 'color_rating', 'overall_rating',
            'comment', 'created_at'
        ]


class InjeraSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Injera
        fields = [
            'id', 'seller', 'name', 'type', 'description',
            'price', 'image', 'avg_rating', 'created_at', 'ratings'
        ]
