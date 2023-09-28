from django.contrib import admin

from receipts.models import Tag, Ingredient, Measurement, Receipt


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Measurement)
admin.site.register(Receipt)
