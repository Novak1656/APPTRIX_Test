from django.urls import path
from .views import CryptoListView, CryptoNewsView

urlpatterns = [
    path('', CryptoListView.as_view(), name='main_page'),
    path('news', CryptoNewsView.as_view(), name='news')
]
