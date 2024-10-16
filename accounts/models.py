from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from .managers import UserModelManager


# Create your models here.
class UserModel(AbstractUser):
    """
    This model will serve as the default authentication model via AUTH_USER_MODEL in settings.py
    """
    username = None
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    organization = models.CharField(max_length=5)
    branch = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(verbose_name="Active")
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserModelManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-date_joined']
