from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CryptocurrencySerializer
from main_app.models import Cryptocurrency


class CryptocurrencyAPIViewSet(ModelViewSet):
    """
        Endpoint for CRUD methods of cryptocurrencies
    """
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
    lookup_field = 'symbol'
    lookup_url_kwarg = 'symbol'

    def update(self, request, *args, **kwargs):
        crypt = get_object_or_404(Cryptocurrency, symbol=self.kwargs.get('symbol'))
        serializer = self.get_serializer(instance=crypt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=200)
