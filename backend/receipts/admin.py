from django.contrib import admin

from receipts.models import Tag, Ingredient, Receipt, IngredientInReceipt


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Receipt)
admin.site.register(IngredientInReceipt)
