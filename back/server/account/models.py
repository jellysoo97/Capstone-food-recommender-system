from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(
        default='', max_length=100, null=False, blank=False, unique=True)
    # sex = models.BooleanField(default=False, null=False)
    # age = models.SmallIntegerField(
    #     default='', null=False, blank=False)
    vege_type = models.CharField(
        default='', max_length=50, null=False, blank=False, unique=False)
    # alle_type = models.CharField(
    #     default='', max_length=50, null=False, blank=False, unique=False)
    password = models.CharField(max_length=200)
# =======
#     sex = models.BooleanField(default=False, null=False)
#     age = models.SmallIntegerField(
#         default='', null=False, blank=False)
#     vegetype = models.CharField(
#         default='', max_length=50, null=False, blank=False, unique=False)
#     allergic = models.CharField(
#         default='', max_length=50, null=False, blank=False, unique=False)
#     password = models.CharField(max_length=200)
# >>>>>>> 3955f6c96a53d949719e0843be6a96f0191f2d49
