from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin')
    ]
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=255
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=255
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    REQUIRED_FIELDS = [
        'password',
        'email',
        'first_name',
        'last_name'
    ]

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Последователь'
    )

    class Meta:
        ordering = ['author']
        verbose_name = 'Подписчик'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'following'], name="unique_user_following"
            )
        ]

    def __str__(self):
        return f'Пользователь {self.following} подписан на {self.author}'
