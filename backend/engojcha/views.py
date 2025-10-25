# from django.shortcuts import render
# from rest_framework import viewsets, permissions
# from .models import User, Seller, Injera, Rating
# from .serializers import UserSerializer, SellerSerializer, InjeraSerializer, RatingSerializer

# # Optional: Allow anyone to read but only authenticated users to modify
# class IsSellerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return hasattr(request.user, 'seller_profile') and obj.seller.user == request.user


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class SellerViewSet(viewsets.ModelViewSet):
#     queryset = Seller.objects.all()
#     serializer_class = SellerSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class InjeraViewSet(viewsets.ModelViewSet):
#     queryset = Injera.objects.all()
#     serializer_class = InjeraSerializer
#     permission_classes = [IsSellerOrReadOnly]

#     def perform_create(self, serializer):
#         seller = self.request.user.seller_profile
#         serializer.save(seller=seller)


# class RatingViewSet(viewsets.ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(buyer=self.request.user)

