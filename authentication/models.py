from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
