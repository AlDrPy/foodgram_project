from django.db.models import Sum
from django.shortcuts import get_object_or_404, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from receipts.models import (Tag, Ingredient, Receipt,
                             Favorite, Cart, IngredientInReceipt)
from api.serializers import (CustomUserSerializer, SubscriptionSerializer,
                             FavAuthorsSerializer,
                             TagSerializer, IngredientSerializer,
                             ReceiptListSerializer, ReceiptPostPatchSerializer,
                             ReceiptFavoriteSerializer, ReceiptCartSerializer)
from api.permissions import IsAdminOrAuthorOrReadOnly
from api.filters import IngredientFilter, ReceiptFilter
from users.models import Subscription


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @action(detail=False,
            permission_classes=(permissions.IsAuthenticated, ),
            )
    def subscriptions(self, request):
        favourive_authors = request.user.fav_authors.all()
        serializer = CustomUserSerializer(
            favourive_authors,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(permissions.IsAuthenticated, ),
            url_path=r'subscribe',
            )
    def subscribe_unsubscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            sub_serializer = SubscriptionSerializer(
                data={'author': author},
                context={'request': request}
            )
            sub_serializer.is_valid(raise_exception=True)
            sub_serializer.save(user=request.user)
            return Response(
                sub_serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscription,
                user=request.user,
                author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class FavAuthorsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FavAuthorsSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscription_of_author__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly, )
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReceiptFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReceiptListSerializer
        return ReceiptPostPatchSerializer

    @action(methods=['POST', 'DELETE'],
            detail=True,
            url_path=r'favorite',
            permission_classes=(IsAuthenticated, ),
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
            favorite = receipt.favorites.all()
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
        permission_classes=(IsAuthenticated, )
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
            cart_item = receipt.carts.all()
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
        permission_classes=(IsAuthenticated, ),
        url_path=r'download_shopping_cart',
    )
    def download_ingredients_from_cart(self, request):
        ingredients = IngredientInReceipt.objects.filter(
            receipt__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))

        shopping_list = ['Ваши покупки:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response
