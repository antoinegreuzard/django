"""
Defines models for the custom user and book entities.

This module extends Django's default user model
to use email as the primary user identifier instead of a username
and defines a Book model with several fields.
"""

from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


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
            raise ValueError('L\'adresse email doit être définie')
        email = self.normalize_email(email)
        username = extra_fields.get('username', email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email,
        password, and is_staff and is_superuser set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom User model that uses email
    as the unique identifier for authentication instead of a username.
    """

    role = models.CharField(max_length=30, default='client')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Book(models.Model):
    """
    Model representing a book with title,
    description, price, author, publication date, and rating.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.CharField(max_length=255)
    date = models.DateField()
    rate = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.title


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Administration object for Book models.
    Defines:
     - fields to be displayed in list view (list_display)
     - fields to be searched in list view (search_fields)
    """

    list_display = ('title', 'author', 'price', 'date', 'rate')
    search_fields = ('title', 'author')

    def formatted_date(self, obj):
        """
        Returns the date formatted in 'd F Y'.
        """
        return format(obj.date, 'd F Y')

    formatted_date.short_description = 'Date'
