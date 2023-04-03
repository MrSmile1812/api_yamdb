from django.urls import path
from .views import create_user, create_token


urlpatterns = [
    path(
        "v1/auth/signup/",
        create_user,
        name='signup'),
    path(
        "v1/auth/token/",
        create_token,
        name='token_obtain_pair'),
]
