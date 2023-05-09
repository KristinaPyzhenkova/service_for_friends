from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Application(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user',
    )
    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Кандидат',
        related_name='applicant',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.user} - {self.applicant}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь1',
        related_name='friendship1',
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь2',
        related_name='friendship2',
    )

    def __str__(self):
        return f'{self.user1} - {self.user2}'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Дружеское отношение'
        verbose_name_plural = 'Дружеские отношения'
