from django.contrib.auth import get_user_model
from django.db import models


class Favorites(models.Model):
    user = models.ForeignKey(
        verbose_name='User',
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    crypto = models.ForeignKey(
        verbose_name='Cryptocurrency',
        to='main_app.Cryptocurrency',
        on_delete=models.CASCADE,
        related_name='favorites',
    )

    class Meta:
        verbose_name = 'Favorites'
        verbose_name_plural = 'Favorite',
        ordering = ['user']

    def __str__(self):
        return f'{self.user}: {self.crypto}'
