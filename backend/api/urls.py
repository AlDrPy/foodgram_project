from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (TagViewSet, IngredientViewSet, ReceiptViewSet,
                       CustomUserViewSet, FavAuthorsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipes', ReceiptViewSet, basename='recipe')


urlpatterns = [
    path('users/subscriptions/',
         FavAuthorsViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
