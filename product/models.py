from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    """ Модель продукта """
    name = models.CharField(max_length=200, verbose_name='наименование')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='пользователь'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'продукты'
        verbose_name = 'продукт'


class AccessModel(models.Model):
    """ Модель доступа """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='acc'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='acc'
    )
    value = models.BooleanField(default=False, verbose_name='доступ')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'product',)
        verbose_name = 'Модель доступа'
        verbose_name_plural = 'Модели доступа'
