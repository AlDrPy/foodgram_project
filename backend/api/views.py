from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from receipts.models import Tag, Ingredient, Receipt, Favorite
from api.serializers import (TagSerializer, IngredientSerializer,
                             ReceiptListSerializer, ReceiptMiniSerializer,
                             ReceiptFavoriteSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptListSerializer

    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


    @action(methods=['POST', 'DELETE'],
            detail=True,
            # permission_classes=(permissions.IsAuthenticated, ),
            )
    def favorite(self, request, pk):
        receipt = get_object_or_404(Receipt, id=pk)
        if request.method == 'POST':
            serializer = ReceiptFavoriteSerializer(
                data={'user': request.user.id, 'receipt': receipt.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(receipt=receipt)
            if not favorite.exists():
                return Response({'errors': 'В Избранном нет такого рецепта.'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
