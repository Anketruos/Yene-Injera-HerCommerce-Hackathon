from rest_framework import serializers
from .models import User, Seller, Injera, Rating, Order


# 1️⃣ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "location",
            "profile_image",
            "phone_number",
            "created_at",
        ]


# 2️⃣ Seller Serializer
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # to display basic user info

    class Meta:
        model = Seller
        fields = [
            "id",
            "user",
            "business_name",
            "contact_number",
            "address",
        ]


# 3️⃣ Injera Serializer
class InjeraSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Injera
        fields = [
            "id",
            "seller",
            "type",
            "type_of_grain",
            "price",
            "stock_quantity",
            "avg_rating",
            "created_at",
        ]


# 4️⃣ Rating Serializer
class RatingSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    injera = serializers.PrimaryKeyRelatedField(queryset=Injera.objects.all())

    class Meta:
        model = Rating
        fields = [
            "id",
            "buyer",
            "injera",
            "texture_rating",
            "quality_rating",
            "freshness_rating",
            "on_time_delivery_rating",
            "overall_rating",
            "created_at",
        ]


# 5️⃣ Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    injera = serializers.PrimaryKeyRelatedField(queryset=Injera.objects.all())

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "injera",
            "quantity",
            "created_at",
        ]

    def create(self, validated_data):
        """
        Ensure stock is reduced when an order is created.
        """
        buyer = self.context["request"].user
        validated_data["buyer"] = buyer
        order = Order.objects.create(**validated_data)
        return order
