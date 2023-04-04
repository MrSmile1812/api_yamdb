from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UnicodeUsernameValidator


class User(AbstractUser):
    TYPE_OF_USER = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="Username",
        max_length=150,
        unique=True,
        help_text=(
            "Required. 150 characters or fewer. "
            "Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
    )
    email = models.EmailField(
        verbose_name="Email", max_length=254, unique=True
    )
    first_name = models.CharField(
        verbose_name="Имя", blank=True, max_length=150
    )
    last_name = models.CharField(
        verbose_name="Фамилия", blank=True, max_length=150
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    role = models.CharField(
        verbose_name="Роль", choices=TYPE_OF_USER, default="user", max_length=9
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
