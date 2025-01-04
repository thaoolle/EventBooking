from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        null=False,
        validators=[EmailValidator(message="Please provide a valid email address.")],
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        help_text="Required. 100 characters or fewer. Letters, digits, and @/./+/-/_ only.",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


