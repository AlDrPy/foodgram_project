from django.db import models
from django.utils.html import format_html


class Tag(models.Model):
    name = models.CharField(blank=False, unique=True, max_length=50)
    color = models.CharField(
        blank=False,
        unique=True,
        max_length=7,
        default='#ffffff'
    )
    slug = models.SlugField(blank=False, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(blank=False, max_length=50)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return self.name, f'количество {self.amount}'


class Measurement(models.Model):
    measurement_unit = models.CharField(blank=False, unique=True, max_length=50)

    def __str__(self):
        return f'Единица измерения: {self.name}'


class Receipt(models.Model):
    author = models.CharField(blank=False, max_length=50)
    name = models.CharField(blank=False, max_length=50)
    image = models.CharField(max_length=50)
    text = models.TextField(blank=False)
    ingredients = models.CharField(max_length=50)
    tag = models.ForeignKey(
        Tag,
        verbose_name="Тег",
        on_delete=models.CASCADE)
    cooking_time = models.IntegerField(blank=False)

    def __str__(self):
        return f'Рецепт {self.name}'
