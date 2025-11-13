from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
