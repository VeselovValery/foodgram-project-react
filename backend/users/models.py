from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin')
    ]
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'password',
        'username',
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


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    authors = models.ManyToManyField(
        User,
        related_name='sub_authors',
        verbose_name='На кого подписан'
    )

    class Meta:
        ordering = ['-authors__id']
        verbose_name = 'На кого подписан'
