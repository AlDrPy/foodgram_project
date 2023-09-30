from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Subscription


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.fav_authors.filter(id=obj.id).exists())

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed'
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()   # Нужен только, если read_only=False
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

    def to_representation(self, instance):
        return CustomUserSerializer(instance.author, context=self.context).data
