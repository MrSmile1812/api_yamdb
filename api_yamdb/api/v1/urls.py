from rest_framework import routers

from django.urls import include, path

from api.v1.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    MeViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)


app_name = "api"

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"users/me", MeViewSet, basename="me")
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
    path("v1/", include(router.urls)),
]
