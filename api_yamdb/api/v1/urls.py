from rest_framework import routers

from django.urls import include, path

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)

from .views import create_token, create_user

app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"genres", GenreViewSet, basename="genres")
router.register(r"titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)

urlpatterns = router.urls

urlpatterns = [
    path("v1/auth/signup/", create_user, name="signup"),
    path("v1/auth/token/", create_token, name="token_obtain_pair"),
    path("v1/", include(router.urls)),
]
