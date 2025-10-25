from django.db.models import Avg
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User, Seller, Injera, Rating, Order
from .serializers import (
    UserSerializer,
    SellerSerializer,
    InjeraSerializer,
    RatingSerializer,
    OrderSerializer,
)


# -----------------------------
# 1. User ViewSet
# -----------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Public registration/view


# -----------------------------
# 2. Seller ViewSet
# -----------------------------
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Auto-link to logged-in user
        serializer.save(user=self.request.user)


# -----------------------------
# 3. Injera ViewSet
# -----------------------------
class InjeraViewSet(viewsets.ModelViewSet):
    queryset = Injera.objects.all().order_by("-created_at")
    serializer_class = InjeraSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Only sellers can add Injera
        if hasattr(self.request.user, "seller_profile"):
            serializer.save(seller=self.request.user.seller_profile)
        else:
            raise PermissionError("Only sellers can add injera products.")

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def my_injeras(self, request):
        """View all injeras by the current seller"""
        if hasattr(request.user, "seller_profile"):
            injeras = Injera.objects.filter(seller=request.user.seller_profile)
            serializer = self.get_serializer(injeras, many=True)
            return Response(serializer.data)
        return Response({"error": "You are not a seller."}, status=403)


# -----------------------------
# 4. Rating ViewSet
# -----------------------------
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all().order_by("-created_at")
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        buyer = self.request.user
        injera = serializer.validated_data["injera"]

        # Prevent duplicate ratings
        if Rating.objects.filter(buyer=buyer, injera=injera).exists():
            raise ValueError("You have already rated this injera.")

        # Save rating
        serializer.save(buyer=buyer)

        # Update Injera average rating
        avg = Rating.objects.filter(injera=injera).aggregate(
            avg=Avg("overall_rating")
        )["avg"]
        injera.avg_rating = avg
        injera.save()


# -----------------------------
# 5. Order ViewSet
# -----------------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        buyer = self.request.user
        serializer.save(buyer=buyer)

