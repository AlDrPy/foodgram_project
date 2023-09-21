
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
# from django.conf.urls.static import static

# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'cats', CatViewSet)
# router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

