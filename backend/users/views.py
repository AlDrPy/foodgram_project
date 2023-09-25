from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
#from rest_framework.pagination import LimitOffsetPagination

from djoser.views import UserViewSet

from users.models import Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False,
            permission_classes=(permissions.IsAuthenticated, ),
            )
    def subscriptions(self, request):
        favourive_authors = self.request.user.fav_authors.all()
        serializer = self.get_serializer(favourive_authors, many=True)
        return Response(serializer.data) 
        


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return self.request.user.fav_authors.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
