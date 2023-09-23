from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.settings import (
    EMAIL_MAX_LEN,
    NAME_MAX_LEN,
    PASSWORD_MAX_LEN
)


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = [
        'password', 'first_name', 'last_name', 'email',
    ]

    username = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        blank=False,
        error_messages={
            'unique': 'Пользователь с таким логином уже существует',
        },
        verbose_name='Логин'
    )

    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        unique=True,
        blank=False,
        error_messages={
            'unique': 'Пользователь с таким e-mail адресом уже существует',
        },
        verbose_name='Email адрес'
    )
    first_name = models.CharField(
        max_length=NAME_MAX_LEN,
        blank=False,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=NAME_MAX_LEN,
        blank=False,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=PASSWORD_MAX_LEN,
        blank=False,
        verbose_name='Пароль'
    )

    @property
    def is_admin(self):
        return self.is_superuser or self.is_staff

    class Meta:
        ordering = ('username',)

    def __str__(self) -> str:
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    def __str__(self):
        return (
            f'{self.user} подписан '
            f'на {self.author}'
        )
