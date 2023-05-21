from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Имя',
        help_text='Напишите свое имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Фамилия',
        help_text='Напишите свою фамилию',
    )
    password = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Пароль',
        help_text='Укажите пароль',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Данные юзера'
        verbose_name_plural = 'Данные юзеров'
        constraints = (
            models.UniqueConstraint(fields=('email', 'username'),
                                    name='unique_user'),
        )


class Subscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Тот, кто подписывается')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
        help_text='На кого подписываются')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'follower'), name='unique_follower'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
