from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint
from rest_framework_simplejwt.tokens import AccessToken
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = (
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    )
    username = models.CharField(max_length=150, unique=True, null=False)
    email = models.EmailField(max_length=254, unique=True, null=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.TextField(choices=ROLES, default=USER, null=False)

    class Meta:
        ordering = ["-id"]

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

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Category(models.Model):
    """Модель категорий произведений"""

    name = models.CharField("Категория", max_length=256)
    slug = models.SlugField("Слаг", max_length=50, unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField("Жанр", max_length=256)
    slug = models.SlugField("Слаг", max_length=50, unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField("Произведение", max_length=256)
    description = models.CharField("Описание произведения", max_length=300)
    year = models.IntegerField("Год выпуска произведе ния")
    genre = models.ManyToManyField(Genre, through="TitleGenre")
    category = models.ForeignKey(
        Category,
        related_name="category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Промежуточная модель произведений и жанров"""

    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-id"]


class Review(models.Model):
    MIN_SCORE = 1
    MAX_SCORE = 10

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведения",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ),
        verbose_name="Рейтинг",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-pub_date",)
        constraints = [
            UniqueConstraint(fields=("title", "author"), name="unique_review")
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("-pub_date",)
