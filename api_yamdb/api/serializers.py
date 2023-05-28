import re
import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from django.core.validators import validate_email

from reviews.models import User, Category, Genre, Title, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]
        model = User

    def validate_username(self, value):
        return _validate_username(value)

    def validate_email(self, value):
        return _validate_email(value)


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User
        validators = []
        extra_kwargs = {
            "username": {
                "validators": [],
            },
            "email": {
                "validators": [],
            },
        }

    def validate_username(self, value):
        print(self)
        return _validate_username(value)

    def validate_email(self, value):
        return _validate_email(value)

    def validate(self, data):
        """Общая функция валидации email"""

        email = data["email"]
        username = data["username"]
        qs = User.objects.filter(email=email)
        if qs.exists():
            if not qs.filter(username=username).exists():
                raise ValidationError("У email другой username.")
        qs = User.objects.filter(username=username)
        if qs.exists():
            if not qs.filter(email=email).exists():
                raise ValidationError("У email другой username.")
        return data


def _validate_username(value):
    """Общая функция валидации username"""

    if value.lower() == "me":
        raise ValidationError(detail="Данное имя запрещено")
    if not re.match(r"^[\w.@+-]+$", value):
        raise ValidationError(
            detail="Можно использовать латинские символы, цифры, @, +, -"
        )
    return value


def _validate_email(value):
    if validate_email(value.lower()):
        raise ValidationError(detail="Не корректный емайл")
    return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class WriteTitleSerializer(serializers.ModelSerializer):
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
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError(
                'Год больше текущего'
            )
        return value


class ReadTitleSerializer(serializers.ModelSerializer):
    """Сериализатор, срабатывающий при методе GET"""
    genre = GenreSerializer(
        many=True,
    )
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
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

    # def validate(self, data):
    #     request = self.context['request']
    #     if request.method == 'POST':
    #         title = data['title']
    #         if title.reviews.filter(author=request.user).exists():
    #             raise serializers.ValidationError(
    #                 'На это произведение вы уже оставляли отзыв.'
    #             )
    #     return data

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError(
                    'На это произведение вы уже оставляли отзыв.')
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
