from django.contrib import admin

from receipts.models import (Tag, Ingredient, 
                             Receipt, IngredientInReceipt,
                             Favorite)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
admin.site.register(IngredientInReceipt)
admin.site.register(Favorite)
