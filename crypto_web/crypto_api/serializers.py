from rest_framework import serializers
from main_app.models import Cryptocurrency


class CryptocurrencySerializer(serializers.ModelSerializer):
    """
        Serilizer for cryptocurrencies
    """
    class Meta:
        model = Cryptocurrency
        fields = '__all__'
