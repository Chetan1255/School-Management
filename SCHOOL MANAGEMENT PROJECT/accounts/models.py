# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


from django.contrib.auth.models import AbstractUser
from django.db import models
from .models import School   # जर वेगळ्या file मध्ये असेल तर

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ("SUPER_ADMIN", "Super Admin"),
        ("ADMIN", "Admin"),
        ("TEACHER", "Teacher"),
        ("PRINCIPAL", "Principal"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

class Teacher(models.Model):
    school = models.ForeignKey("accounts.School", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
