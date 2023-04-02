from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import create_user


urlpatterns = [
    path(
        "v1/auth/signup/",
        create_user,
        name='signup'),
    path(
        "v1/auth/token/",
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
]

#path(
       # "v1/users/me/", 
       # UserEditViewSet.as_view(),
       # name='edit_user'
        #),
