from django.db import models
from datetime import datetime, timedelta
import jwt

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


ROLES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)


class User(AbstractUser):
    """Модель юзера"""
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
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.timestamp())},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token.encode("utf-8")


class Category(models.Model):
    """Модель категорий произведений"""
    name = models.CharField(
        'Категория',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(
        'Жанр',
        max_length=256
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(
        'Произведение',
        max_length=256
    )
    description = models.CharField(
        'Описание произведения',
        max_length=300
    )
    year = models.IntegerField(
        'Год выпуска произведе ния'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name
