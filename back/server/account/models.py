from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import CharField


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(
        default='', max_length=128, null=False, blank=False, unique=True)
    password = models.CharField(max_length=128)
    sex = models.BooleanField(default=False, null=False)
    age = models.SmallIntegerField(
        default='', null=False, blank=False)
    height = models.IntegerField(default=160, null=False)
    weight = models.IntegerField(default=60, null=False)
    health = models.CharField(default="없을 무", max_length=128)
    # 리스트 https://django-mysql.readthedocs.io/en/latest/model_fields/list_fields.html
    vegtype = models.TextField(default="[]", max_length=128)
    # 리스트
    allergic = models.TextField(default="[]", max_length=128)