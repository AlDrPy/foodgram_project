from django.db import models
from django.core.validators import MinValueValidator

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=200)
    color = models.CharField(
        blank=False,
        null=True,
        unique=True,
        max_length=7,
        default='#ffffff',
    )
    slug = models.SlugField(blank=False, unique=True, max_length=200)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        blank=False,
        unique=True,
        max_length=200,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        blank=False,
        max_length=200,
        verbose_name='Ед.измерения'
    )

    def __str__(self):
        return self.name


class Receipt(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Автор рецепта',
        related_name='receipts'
    )
    name = models.CharField(
        blank=False,
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        blank=True,
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(blank=False, verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInReceipt',
        blank=False,
        verbose_name='Ингредиенты',
        related_name='receipts',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='receipts',
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, 'Время готовки не менее 1 минуты')]
    )

    def __str__(self):
        return self.name


class IngredientInReceipt(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ing_in_rcpt'
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='ing_in_rcpt'
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиента'
    )

    def __str__(self):
        return (
            f'Рецепт {self.receipt} содержит '
            f'{self.ingredient} в количестве '
            f'{self.amount} {self.ingredient.measurement_unit} '
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'receipt'],
                name='unique_user_receipt_favorite'
            )
        ]

    def __str__(self):
        return f'{self.receipt.name} в избраннном у {self.user.username}'


class Cart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'receipt'],
                name='unique_user_receipt_cart'
            )
        ]

    def __str__(self):
        return f'{self.receipt.name} в корзине у {self.user.username}'
