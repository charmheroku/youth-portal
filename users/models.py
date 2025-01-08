from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with email as the unique identifier instead of username.

    """

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female")],
        blank=True,
    )
    telegram = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email
