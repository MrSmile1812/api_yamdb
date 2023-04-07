from django.db import models
from django.utils.translation import gettext_lazy as _


class TYPE_OF_USER(models.TextChoices):
    user = "user", _("user")
    moderator = "moderator", _("moderator")
    admin = "admin", _("admin")
