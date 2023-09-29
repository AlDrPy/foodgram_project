from rest_framework import serializers

from receipts.models import Tag, Ingredient, Receipt, Favorite


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

    class Meta:
        model = Receipt
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            # 'image',
            'text',
            'cooking_time'
        )


class ReceiptMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = (
            'id',
            'name',
            # 'image',
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
