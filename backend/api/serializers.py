from rest_framework import serializers

from receipts.models import Tag, Ingredient, Measurement, Receipt


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
