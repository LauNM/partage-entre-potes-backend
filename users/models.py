from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):

    def create_user(self, first_name: str, last_name: str, surname: str, email: str,  password: str = None,
                    is_staff=False, is_superuser=False) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have an first name")
        if not last_name:
            raise ValueError("User must have an last name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.surname = surname
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, email, first_name, last_name, surname=None, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            surname=surname,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save()

        return user


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, blank=True, unique=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def save(self, *args, **kwargs):
        if not self.surname:
            base_surname = self.surname = f"{self.first_name}_{self.last_name}".strip()
            suffix = 1
            generated_surname = base_surname

            while User.objects.filter(surname=generated_surname).exists():
                generated_surname = f"{base_surname}_{suffix}"
                suffix += 1

            self.surname = generated_surname

        super().save(*args, **kwargs)


