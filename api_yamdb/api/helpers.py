from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def get_confirmation_code(user):
    """Получить confirmation_code для user."""

    return default_token_generator.make_token(user)


def send_email(user, title="Код регистраци"):
    """Отправка кода на email при регистрации."""

    code = get_confirmation_code(user)
    send_mail(
        title,
        code,
        settings.EMAIL_HOST_USER,
        [
            user.email,
        ],
    )
