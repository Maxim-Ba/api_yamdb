from rest_framework import routers
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from .views import (
    UserViewSet,
    signup,
    token,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)

router_v1 = routers.SimpleRouter()

router_v1.register(
    r"users",
    UserViewSet,
    basename="users"
)
router_v1.register(
    r"categories",
    CategoryViewSet,
    basename="categories"
)
router_v1.register(
    r"genres",
    GenreViewSet,
    basename="genres"
)
router_v1.register(
    'titles',
    TitleViewSet,
    'titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", csrf_exempt(signup)),
    path("v1/auth/token/", csrf_exempt(token)),
]
