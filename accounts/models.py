import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from accounts.managers import UserManager
from base.models import DateTimeRecord


class User(AbstractBaseUser, DateTimeRecord):
    name = models.CharField(max_length=50)
    phone = models.BigIntegerField(unique=True)
    isd = models.CharField(max_length=4, default='')
    fcm_token = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "phone"
    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.id}"