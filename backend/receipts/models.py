from django.db import models

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
    # image = models.ImageField(unique=True, blank=False, upload_to=)
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
    cooking_time = models.IntegerField(blank=False)

    def __str__(self):
        return self.name


class IngredientInReceipt(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingr_amount = models.IntegerField(
        verbose_name='Количество ингредиента'
    )

    def __str__(self):
        return (
            f'Рецепт {self.receipt} содержит '
            f'{self.ingredient} в количестве '
            f'{self.ingr_amount} {self.ingredient.measurement_unit} '
        )
