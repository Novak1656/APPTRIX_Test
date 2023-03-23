from rest_framework.viewsets import ModelViewSet
from .serializers import CryptocurrencySerializer
from main_app.models import Cryptocurrency


class CryptocurrencyAPIViewSet(ModelViewSet):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
    lookup_field = 'symbol'
    lookup_url_kwarg = 'symbol'
