from django.conf import settings
from requests import Session
from ..models import Cryptocurrency
import json
from newsapi import NewsApiClient


class CryptoMixin:
    def gather_crypto_info(self, with_save=False):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

        parameters = {
            'convert': 'USD',
            'limit': 100,
            'sort': 'market_cap',
            'sort_dir': 'desc'
        }

        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': settings.COINMARKETCAP_API_KEY,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            crypto_info = self.__struct_data(raw_data=data.get('data'))
            if with_save:
                return self.__save_info_in_db(crypto_info)
            return crypto_info

        except Exception as error:
            print(f'Error while gathering info: {error}')

    @staticmethod
    def __struct_data(raw_data: list[dict]) -> dict:
        crypto_info = dict()
        for crypto in raw_data:
            quotes = crypto['quote']['USD']
            crypto_info[crypto.get('name')] = (
                dict(
                    rank=crypto.get('cmc_rank'),
                    max_supply=crypto.get('max_supply'),
                    supply=crypto.get('total_supply'),
                    symbol=crypto.get('symbol'),
                    market_cap=quotes.get('market_cap'),
                    percent_change_1h=quotes.get('percent_change_1h'),
                    percent_change_24h=quotes.get('percent_change_24h'),
                    percent_change_7d=quotes.get('percent_change_7d'),
                    price=quotes.get('price'),
                    volume_24h=quotes.get('volume_24h'),
                )
            )
        return crypto_info

    @staticmethod
    def __save_info_in_db(crypto_info: dict):
        crypts = Cryptocurrency.objects.all()
        cur_crypts = {crypt.name: crypt.pk for crypt in crypts}
        fields = ('rank', 'max_supply', 'symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h',
                  'percent_change_7d', 'price', 'volume_24h')
        updated_data = [
            Cryptocurrency(id=cur_crypts.get(name), **info) for name, info in crypto_info.items() if name in cur_crypts
        ]
        Cryptocurrency.objects.bulk_update(updated_data, fields)
        return crypts

    @staticmethod
    def gather_crypto_news() -> list[dict]:
        news_api = NewsApiClient(api_key=settings.NEWS_API_KEY)
        news_raw = news_api.get_everything(q='crypto').get('articles')
        if not news_raw:
            return []
        return news_raw
