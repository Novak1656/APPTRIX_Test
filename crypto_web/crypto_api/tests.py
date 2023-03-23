from django.test import TestCase
from django.urls import reverse
from main_app.models import Cryptocurrency

# Так как в тз указано написать тесты только для методов API я сделал тест только для метода обновления,
# так как переопределил его. Остальные же методы не тестил так как нет смысла тестить
# то что реализованно инстументами DRF


class CryptocurrencyAPIViewSetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cryptocurrency.objects.create(name='TestCoin', rank=1, symbol='TC', price=5.00)

    def test_update_method(self):
        after_update = Cryptocurrency.objects.get(name='TestCoin')
        resp = self.client.put(
            reverse('crypto-detail', kwargs={'symbol': 'TC'}),
            data={'name': 'BestCoin'},
            follow=True,
            content_type='application/json'
        )
        self.assertEqual(resp.status_code, 200)
        after_update.refresh_from_db()
        self.assertEqual(after_update.name, 'BestCoin')
