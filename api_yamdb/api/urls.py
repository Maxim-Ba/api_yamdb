from rest_framework import routers
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt


from .views import UserViewSet, signup, token

router_v1 = routers.SimpleRouter()
# router_v1.register(
#     r"users/(?P<username>\w+)/", UserViewSet, basename="user-retrieve"
# )
router_v1.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", csrf_exempt(signup)),
    path("v1/auth/token/", csrf_exempt(token)),
]
