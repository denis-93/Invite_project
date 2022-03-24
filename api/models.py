from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    authorization_code = models.CharField(max_length=4, null=True, blank=True, default='xxxx')
    self_code = models.CharField(max_length=6, null=True, blank=True, unique=True)
    invite_code = models.CharField(max_length=6, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []


    def __str__(self):
        return f'{self.phone}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"
