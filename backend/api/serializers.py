from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.utils import Base64ImageField
from receipts.models import (Tag, Ingredient, Receipt,
                             Favorite, Cart, IngredientInReceipt)
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
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')


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

    def to_representation(self, instance):
        return CustomUserSerializer(instance.author, context=self.context).data


class FavAuthorsSerializer(CustomUserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = None
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.receipts.all()
        if recipes_limit:
            recipes = obj.receipts.all()[:int(recipes_limit)]
        return ReceiptMiniSerializer(recipes, many=True,
                                     context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.receipts.count()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientFromReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInReceipt
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientToReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInReceipt
        fields = ('id', 'amount')


class ReceiptListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientFromReceiptSerializer(
        many=True, read_only=True, source='ing_in_rcpt')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.favorites.filter(
                    receipt__id=obj.id
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.carts.filter(
                    receipt__id=obj.id
                ).exists())

    class Meta:
        model = Receipt
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )


class ReceiptPostPatchSerializer(serializers.ModelSerializer):
    ingredients = IngredientToReceiptSerializer(
        many=True, source='ing_in_rcpt',
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Receipt
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients_list = []
        for ingredient in data.get('ing_in_rcpt'):
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1'
                )
            ingredients_list.append(ingredient.get('id'))
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Нельзя добавить два одинаковых ингредиента в один рецепт'
            )
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ing_in_rcpt')
        receipt = Receipt.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        receipt.tags.set(tags)
        for ingr in ingredients:
            amount = ingr.get('amount')
            current_ingr = get_object_or_404(
                Ingredient, id=ingr.get('id'))
            IngredientInReceipt.objects.create(
                ingredient=current_ingr, receipt=receipt,
                amount=amount)
        return receipt

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ing_in_rcpt')
        instance.tags.clear()
        instance.tags.set(tags)
        IngredientInReceipt.objects.filter(receipt=instance).delete()
        super().update(instance, validated_data)
        for ingr in ingredients:
            amount = ingr.get('amount')
            current_ingr = get_object_or_404(
                Ingredient, id=ingr.get('id'))
            IngredientInReceipt.objects.create(
                ingredient=current_ingr, receipt=instance,
                amount=amount)
        instance.save()
        return instance

    def to_representation(self, instance):
        return ReceiptListSerializer(
            instance, context=self.context).data


class ReceiptMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class ReceiptFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = (
            'user',
            'receipt'
        )

    def to_representation(self, instance):
        return ReceiptMiniSerializer(
            instance.receipt, context=self.context).data


class ReceiptCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = (
            'user',
            'receipt'
        )

    def to_representation(self, instance):
        return ReceiptMiniSerializer(
            instance.receipt, context=self.context).data
