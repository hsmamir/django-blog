from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from typing import Callable, Tuple
from rest_framework_simplejwt.tokens import RefreshToken
from utils.models import CreationMixin
from django.core.cache import cache
from datetime import datetime
from django.contrib.auth.hashers import check_password


class UserManager(BaseUserManager):
    use_in_migrations = True


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    password = None
    last_login = None

    objects = UserManager()

    USERNAME_FIELD = 'id'

    def __str__(self):
        return str(self.pk)

    @classmethod
    def create_deferred_user(cls, **kwargs) -> Callable[[], 'User']:
        def create_user():
            return cls.objects.create(**kwargs)

        return create_user

    def api_token(self):
        refresh = RefreshToken.for_user(self)
        return str(refresh), str(refresh.access_token)


class Profile(CreationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    user_name = models.CharField(unique=True, max_length=11)
    password = models.TextField()

    def __str__(self):
        return str(self.pk)

    @classmethod
    def get_or_create(
            cls, defaults: dict = None, **kwargs) -> Tuple['Profile', bool]:

        defaults = defaults or {}
        return cls.objects.get_or_create(**kwargs, defaults={
            'user': User.create_deferred_user(),
            **defaults
        })

    @classmethod
    def update_last_sync(cls, pk):
        cache.set(f"last_sync_{pk}", int(datetime.utcnow().timestamp()))

    def get_last_sync(self):
        return cache.get(f"last_sync_{self.pk}", None)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)
