from django.core.management import BaseCommand
from django.db import transaction

from ...utils import CryptoMixin
from ...models import Cryptocurrency


class Command(BaseCommand, CryptoMixin):
    help = 'Fill the database with preliminary records about cryptocurrencies'

    def handle(self, *args, **options):
        crypto_info = self.gather_crypto_info()
        crypts = Cryptocurrency.objects.values('name', 'symbol')
        cur_crypto = [crypto.get('name') for crypto in crypts] + [crypto.get('symbol') for crypto in crypts]
        try:
            with transaction.atomic():
                new_crypto = []
                for name, info in crypto_info.items():
                    if name in cur_crypto or info.get('symbol') in cur_crypto:
                        continue
                    new_crypto.append(Cryptocurrency(name=name, **info))
                    cur_crypto.extend([name, info.get('symbol')])
                cryptos = Cryptocurrency.objects.bulk_create(new_crypto)
            print(f'{len(cryptos)} cryptocurrencies has been added in database')
        except Exception as error:
            print(f'Error while filling the database: {error}')
