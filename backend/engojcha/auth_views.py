from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User, Seller
from .serializers import UserSerializer


# -----------------------------
# Signup View (role-based)
# -----------------------------
class SignupView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        role = request.data.get("role")
        if role not in ["buyer", "seller"]:
            return Response({"error": "Role must be buyer or seller."}, status=400)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            user.save()

            # If seller, create linked Seller profile
            if role == "seller":
                Seller.objects.create(user=user, business_name=request.data.get("business_name", f"{user.username}'s Injera Shop"))

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": f"{role.capitalize()} registered successfully.",
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)


# -----------------------------
# Login View (JWT)
# -----------------------------
# class LoginView(generics.GenericAPIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if not email or not password:
#             return Response({"error": "Email and password are required."}, status=400)

#         user = authenticate(username=email, password=password)
#         if not user:
#             return Response({"error": "Invalid credentials."}, status=401)

#         refresh = RefreshToken.for_user(user)
#         return Response({
#             "message": "Login successful.",
#             "user": {
#                 "id": user.id,
#                 "username": user.username,
#                 "email": user.email,
#                 "role": user.role,
#             },
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         })

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)