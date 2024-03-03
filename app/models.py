"""
Defines models for the custom user and book entities.

This module extends Django's default user model
to use email as the primary user identifier instead of a username
and defines a Book model with several fields.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model that uses email as the unique identifier for
    authentication.
    """
    email = models.EmailField(_('email address'), unique=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.CharField(max_length=255)
    date = models.DateField()
    rate = models.DecimalField(max_digits=3, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='books')

    def __str__(self):
        return self.title


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin view for Book.
    """
    list_display = ('title', 'author', 'price', 'date', 'rate')
    search_fields = ('title', 'author')
