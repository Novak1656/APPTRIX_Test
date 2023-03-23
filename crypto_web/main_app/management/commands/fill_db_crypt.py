from django.core.management import BaseCommand
from ...utils import CryptoMixin
from ...models import Cryptocurrency


class Command(BaseCommand, CryptoMixin):
    help = 'Fill the database with preliminary records about cryptocurrencies'

    def handle(self, *args, **options):
        crypto_info = self.gather_crypto_info()
        try:
            new_crypto = [Cryptocurrency(name=name, **info) for name, info in crypto_info.items()]
            cryptos = Cryptocurrency.objects.bulk_create(new_crypto)
            print(f'{len(cryptos)} cryptocurrencies has been added in database')
        except Exception as error:
            print(f'Error while filling the database: {error}')
