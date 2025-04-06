from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=100)
    birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=10)

    REQUIRED_FIELDS = ['email', 'name']
    USERNAME_FIELD = 'username'