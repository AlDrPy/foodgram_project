from django.db.models import Sum
from django.shortcuts import get_object_or_404, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from receipts.models import (Tag, Ingredient, Receipt,
                             Favorite, Cart, IngredientInReceipt)
from api.serializers import (TagSerializer, IngredientSerializer,
                             ReceiptListSerializer,
                             ReceiptFavoriteSerializer, ReceiptCartSerializer)


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
            url_path=r'favorite',
            # permission_classes=(permissions.IsAuthenticated, ),
            )
    def like_dislike(self, request, pk):
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
                return Response(
                    {'errors': 'В Избранном нет такого рецепта.'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path=r'shopping_cart',
        # permission_classes=[IsAuthenticated, ]
    )
    def add_to_cart_or_remove(self, request, pk):
        receipt = get_object_or_404(Receipt, id=pk)
        if request.method == 'POST':
            serializer = ReceiptCartSerializer(
                data={'user': request.user.id, 'receipt': receipt.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            cart_item = Cart.objects.filter(receipt=receipt)
            if not cart_item.exists():
                return Response(
                    {'errors': 'В Корзине нет такого рецепта.'},
                    status=status.HTTP_400_BAD_REQUEST)
            cart_item.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        detail=False,
        # permission_classes=[IsAuthenticated, ]
        url_path=r'download_shopping_cart',
    )
    def download_ingredients_from_cart(self, request):
        ingredients = IngredientInReceipt.objects.filter(
            receipt__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('ingr_amount'))

        shopping_list = ['Ваши покупки:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response
