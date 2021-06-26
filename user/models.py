from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    update_time = models.DateTimeField('更新时间', auto_now=True)
