from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SellerViewSet, InjeraViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sellers', SellerViewSet)
router.register(r'injeras', InjeraViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
