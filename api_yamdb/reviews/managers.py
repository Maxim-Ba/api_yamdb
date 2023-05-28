from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, role="user", password=None, bio=""):
        """
        Create a CustomUser with email, name, password and other extra fields
        """
        if not email:
            raise ValueError("The email is required to create this user")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            password=password,
            bio=bio,
        )
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, username, password=None, role="admin", bio=""
    ):
        u = self.create_user(email, username, role, password, bio)
        u.save(using=self._db)

        return u
