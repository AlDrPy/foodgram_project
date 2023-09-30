from rest_framework import serializers

from receipts.models import Tag, Ingredient, Receipt, Favorite, Cart
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# Поиск по частичному вхождению в начале названия (name) ингредиента.
class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ReceiptListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        return self.context['request'].user.favorites.filter(
            receipt__id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        return self.context['request'].user.carts.filter(
            receipt__id=obj.id).exists()

    class Meta:
        model = Receipt
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


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
