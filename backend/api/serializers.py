from rest_framework import serializers

from receipts.models import Tag, Ingredient, Receipt


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


# Поиск по частичному вхождению в начале названия (name) ингредиента.
class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


# class ReceiptListSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Receipt
#         fields = ('id', 'name', 'color', 'slug')


# class ReceiptMiniSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Receipt
#         fields = ('id', 'name', 'color', 'slug')
