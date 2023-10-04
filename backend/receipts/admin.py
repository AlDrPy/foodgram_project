from django.contrib import admin

from backend.settings import EMPTY_VALUE
from receipts.models import (Tag, Ingredient,
                             Receipt, IngredientInReceipt,
                             Favorite, Cart)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = EMPTY_VALUE


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VALUE


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientInReceipt
    min_num = 1


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'total_in_favorites')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = EMPTY_VALUE
    inlines = (RecipeIngredientInline, )

    def total_in_favorites(self, obj):
        return obj.favorites.count()


class IngredientInReceiptAdmin(admin.ModelAdmin):
    list_display = ('pk', 'receipt', 'ingredient', 'amount')
    empty_value_display = EMPTY_VALUE


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'receipt')
    search_fields = ('user', 'receipt')
    empty_value_display = EMPTY_VALUE


class CartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'receipt')
    search_fields = ('user', 'receipt')
    empty_value_display = EMPTY_VALUE


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(IngredientInReceipt, IngredientInReceiptAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
