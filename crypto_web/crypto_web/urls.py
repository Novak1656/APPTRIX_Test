from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users_app.urls')),
    path('', include('main_app.urls')),
    path('api/v1/', include('crypto_api.urls')),
]
