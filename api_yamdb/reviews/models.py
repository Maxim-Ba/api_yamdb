from rest_framework_simplejwt.tokens import AccessToken


from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    role = models.TextField(choices=ROLES, default="user", null=False)

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        access = AccessToken.for_user(self)
        return str(access)
