from django.db import models


class Cryptocurrency(models.Model):
    name = models.CharField(
        verbose_name='Name',
        unique=True,
        max_length=255
    )
    rank = models.IntegerField(
        verbose_name='CMC Rank'
    )
    max_supply = models.DecimalField(
        verbose_name='Max Supply',
        max_digits=19,
        decimal_places=2,
        null=True
    )
    supply = models.DecimalField(
        verbose_name='Total Supply',
        max_digits=19,
        decimal_places=2,
        null=True
    )
    symbol = models.CharField(
        verbose_name='Symbol',
        max_length=100,
    )
    market_cap = models.DecimalField(
        verbose_name='Market Cap',
        max_digits=19,
        decimal_places=2,
        null=True
    )
    percent_change_1h = models.DecimalField(
        verbose_name='Change in 1h',
        max_digits=5,
        decimal_places=2,
        null=True
    )
    percent_change_24h = models.DecimalField(
        verbose_name='Change in 24h',
        max_digits=5,
        decimal_places=2,
        null=True
    )
    percent_change_7d = models.DecimalField(
        verbose_name='Change in 7d',
        max_digits=5,
        decimal_places=2,
        null=True
    )
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=10,
        decimal_places=2,
    )
    volume_24h = models.DecimalField(
        verbose_name='Volume in 24h',
        max_digits=19,
        decimal_places=2,
        null=True
    )

    class Meta:
        verbose_name = 'Cryptocurrency'
        verbose_name_plural = 'Cryptocurrencies'
        ordering = ['rank']

    def __str__(self):
        return self.name
