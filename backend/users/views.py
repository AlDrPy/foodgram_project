# from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import viewsets  #, permissions, filters, mixins
from django.contrib.auth import get_user_model
#from rest_framework.pagination import LimitOffsetPagination

from users.models import Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
