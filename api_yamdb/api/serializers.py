import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email

from reviews.models import User


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
