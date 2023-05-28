import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import validate_email

from reviews.models import User


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
