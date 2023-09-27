from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
# router.register(
#     r'users/subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register(r'users', CustomUserViewSet, basename='user')
router.register(
    r'users/(?P<user_id>\d+)/subscribe', CustomUserViewSet, basename='subscribe'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
