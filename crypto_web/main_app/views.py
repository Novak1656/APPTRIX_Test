from django.db.models import Q
from django.views.generic import TemplateView
from .utils import CryptoMixin


class CryptoListView(TemplateView, CryptoMixin):
    """
        Cryptocurrencies list page
    """
    template_name = 'main_app/crypto_list.html'
    extra_context = {'page_title': 'Cryptocurrencies'}

    def get_context_data(self, **kwargs):
        context = super(CryptoListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['user_favorites'] = user.favorites.values_list('crypto_id', flat=True)
        context['crypto_info'] = self.gather_crypto_info(with_save=True)
        if search_value := self.request.GET.get('search_value'):
            crypto_info = context.get('crypto_info')
            context['search_value'] = search_value
            context['page_title'] = f'Search Results | {search_value}'
            context['crypto_info'] = (
                crypto_info.filter(Q(name__icontains=search_value) | Q(symbol__icontains=search_value))
            )
        return context


class CryptoNewsView(TemplateView, CryptoMixin):
    """
        Cryptocurrencies News page
    """
    template_name = 'main_app/crypto_news.html'

    def get_context_data(self, **kwargs):
        context = super(CryptoNewsView, self).get_context_data(**kwargs)
        context['news'] = self.gather_crypto_news()
        return context
