from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription


User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_admin = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_admin'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('author', 'user')
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('author', 'user'),
                message='Дублирование подписок запрещено.'
            )
        ]

    def validate_author(self, value):
        user = self.context['request'].user
        if value.username == user.username:
            raise serializers.ValidationError('Нельзя подписываться на себя!')
        return value
