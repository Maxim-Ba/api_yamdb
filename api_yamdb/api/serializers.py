import re
import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email

from reviews.models import User, Category, Genre, Title, Comment, Review


# Использовать имя 'me' в качестве username запрещено
# Поля email и username должны быть уникальными.
# username string <= 150 characters ^[\w.@+-]+\z
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = User
        validators = [UniqueValidator(queryset=User.objects.all())]


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError(detail="Данное имя запрещено")
        pattern = re.compile(r"^[\w.@+-]+$")
        if not pattern.match(value):
            raise ValidationError(
                detail="Можно использовать латинские символы, цифры, @, +, -"
            )
        return value

    def validate_email(self, value):
        if validate_email(value.lower()):
            raise ValidationError(detail="Не корректный емайл")
        return value


class CategorySerialiser(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    model = Category
    exclude = ('id', )
    lookup_field = 'slug'


class GenreSerialiser(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    model = Genre
    exclude = ('id', )
    lookup_field = 'slug'


class WriteTitleSerializer():
    """Сериализатор, срабатывающий при методе POST и PATCH"""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        allow_null=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        allow_null=False
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год больше текущего'
            )
        return value


class ReadTitleSerializer():
    """Сериализатор, срабатывающий при методе GET"""
    genre = GenreSerialiser(
        read_only=True,
        many=True
    )
    category = CategorySerialiser(
        read_only=True
    )
    rating = serializers.IntegerField(
        read_only=True,
        required=False
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context.get['request']
        if request.method == 'POST':
            title = data['title']
            if title.reviews.filter(author=request.user).exists():
                raise serializers.ValidationError(
                    'На это произведение вы уже оставляли отзыв.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
