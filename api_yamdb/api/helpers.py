import hashlib

from django.conf import settings
from django.core.mail import send_mail


def get_confirmation_code(user):
    m = hashlib.md5()
    m.update(user.email.encode("utf-8"))
    return m.hexdigest()


def create_confirmation_code(value: str):
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    return m.hexdigest()


def send_email(email, msg, title="Код регистраци"):
    code = create_confirmation_code(msg)
    send_mail(
        title,
        code,
        settings.EMAIL_HOST_USER,
        [
            email,
        ],
    )
