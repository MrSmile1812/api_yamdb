from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "role",
        "bio",
        "first_name",
        "last_name",
    )
    search_fields = (
        "username",
        "role",
    )
    list_filter = ("username",)
    empty_value_display = "-пусто-"