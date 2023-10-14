from django.contrib import admin
from django.contrib.auth import get_user_model

from backend.settings import EMPTY_VALUE
from users.models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username',
                    'first_name', 'last_name', 'is_admin')
    list_filter = ('username', 'email')
    empty_value_display = EMPTY_VALUE


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = EMPTY_VALUE


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
