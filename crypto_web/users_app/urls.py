from django.urls import path
from .views import RegistrationView, logout_view, login_view, add_in_favorite, delete_from_favorite, UserFavoritesView

urlpatterns = [
    path('registration', RegistrationView.as_view(), name='user_register'),
    path('logout', logout_view, name='user_logout'),
    path('login', login_view, name='user_login'),
    path('favorites/add', add_in_favorite, name='add_in_favorite'),
    path('favorites/delete', delete_from_favorite, name='delete_from_favorite'),
    path('favorites', UserFavoritesView.as_view(), name='user_favorites')
]
