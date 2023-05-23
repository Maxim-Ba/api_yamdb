from django.db import models


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


class Genres(models.Model):
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
        'Год выпуска произведения'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name
