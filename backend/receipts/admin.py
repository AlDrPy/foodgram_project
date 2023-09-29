from django.contrib import admin

from receipts.models import (Tag, Ingredient,
                             Receipt, IngredientInReceipt,
                             Favorite, Cart)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
admin.site.register(IngredientInReceipt)
admin.site.register(Favorite)
admin.site.register(Cart)
