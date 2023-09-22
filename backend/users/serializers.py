from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_admin = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_admin'
        )