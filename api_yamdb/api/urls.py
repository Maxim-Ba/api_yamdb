from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, signup, token, CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')
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
