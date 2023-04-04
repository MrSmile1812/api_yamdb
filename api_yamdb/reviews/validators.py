from django.core import validators
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class MaxValueValidator(BaseValidator):
    message = _("Ensure this value is less than or equal to %(limit_value)s.")
    code = "max_value"

    def compare(self, a, b):
        return a > b


@deconstructible
class UnicodeCategoryOrGenreNameValidator(validators.RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = _(
        "Enter a valid name. This value may contain only letters and numbers."
    )
    flags = 0


@deconstructible
class MinValueValidator(BaseValidator):
    message = _(
        "Ensure this value is greater than or equal to %(limit_value)s."
    )
    code = "min_value"

    def compare(self, a, b):
        return a < b
