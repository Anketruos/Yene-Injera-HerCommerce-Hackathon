# # from django.urls import path, include
# # from rest_framework.routers import DefaultRouter
# # from .views import UserViewSet, SellerViewSet, InjeraViewSet, RatingViewSet

# # router = DefaultRouter()
# # router.register(r'users', UserViewSet)
# # router.register(r'sellers', SellerViewSet)
# # router.register(r'injeras', InjeraViewSet)
# # router.register(r'ratings', RatingViewSet)

# # urlpatterns = [
# #     path('', include(router.urls)),
# # ]
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, SellerViewSet, InjeraViewSet, RatingViewSet, OrderViewSet
# from .auth_views import SignupView, LoginView

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'sellers', SellerViewSet)
# router.register(r'injeras', InjeraViewSet)
# router.register(r'ratings', RatingViewSet)
# router.register(r'orders', OrderViewSet)

# urlpatterns = [
#     path('auth/signup/', SignupView.as_view(), name='signup'),
#     path('auth/login/', LoginView.as_view(), name='login'),
#     path('', include(router.urls)),
# ]
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
#     path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

#     path('injeras/', views.InjeraListCreateView.as_view(), name='injera-list-create'),
#     path('injeras/<int:pk>/', views.InjeraDetailView.as_view(), name='injera-detail'),

#     path('ratings/', views.RatingListCreateView.as_view(), name='rating-list-create'),
#     path('ratings/<int:pk>/', views.RatingDetailView.as_view(), name='rating-detail'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SellerViewSet, InjeraViewSet, RatingViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sellers', SellerViewSet, basename='seller')
router.register(r'injeras', InjeraViewSet, basename='injera')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

