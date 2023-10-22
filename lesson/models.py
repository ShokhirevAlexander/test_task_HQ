from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Lesson(models.Model):
    """ Модель урока"""
    name = models.CharField(max_length=200, verbose_name='урок')
    product = models.ManyToManyField(
        Product,
        verbose_name='продукт',
        related_name='lessons',
    )
    video_link = models.URLField(unique=True, verbose_name='ссылка на видео')
    duration = models.IntegerField(verbose_name='продолжительность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'уроки'
        verbose_name = 'урок'


class ViewModel(models.Model):
    """ Модель просмотра уроков """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='viewmodels',
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='viewmodels'
    )
    duration_view = models.IntegerField(default=0, verbose_name='просмотренно')
    start_view = models.DateTimeField(auto_now_add=True)
    last_viewed = models.DateTimeField(auto_now=True, auto_now_add=False,
                                       verbose_name='дата последнего '
                                                    'просмотра')
    status = models.CharField(default='Не просмотренно', max_length=20)

    def save(self, *args, **kwargs):
        if self.duration_view >= self.lesson.duration * 0.8:
            self.status = 'Просмотренно'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'lesson',)
        verbose_name = 'модель просмотра'
        verbose_name_plural = 'модели просмотра'
