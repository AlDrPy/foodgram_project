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
        verbose_name='Логин'
    )

    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        unique=True,
        blank=False,
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
    fav_authors = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Subscription',
        verbose_name='Подписки на авторов',
        related_name='subscribers',
    )

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
        related_name='subscription_of_user',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscription_of_author',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique subscription'
            )
        ]

    def __str__(self):
        return (
            f'{self.user} подписан '
            f'на {self.author}'
        )
