from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet, SubscriptionViewSet


app_name = 'api'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'users/subscriptions', SubscriptionViewSet)

# router.register(r'cats', CatViewSet)
# router.register(r'achievements', AchievementViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
