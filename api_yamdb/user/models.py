from user.constants import TYPE_OF_USER
from user.validators import UnicodeUsernameValidator

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
        error_messages={
            "unique": ("A user with that username already exists."),
        },
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        verbose_name="Роль",
        choices=TYPE_OF_USER,
        default="user",
        max_length=9,
        blank=True,
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    first_name = models.CharField(
        verbose_name="Имя", blank=True, max_length=150
    )
    last_name = models.CharField(
        verbose_name="Фамилия", blank=True, max_length=150
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    @property
    def is_user(self):
        return self.role == "user"

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.username
