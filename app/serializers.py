"""
Serializers for the app.

This module defines serializers for the User and Book models.
These serializers are used to convert complex data types such as querysets
and model instances to native Python datatypes
that can then be easily rendered into JSON, XML, or other content types.
They are also used for deserialization, i.e.,
converting parsed data back into complex types, after validating the incoming data.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

from app.models import Book

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    Converts User instances to and from Python datatypes,
    handles user creation and password setting.
    """

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates and returns a new User instance, given the validated data.
        """
        user = User.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.

    Handles serialization and deserialization of Book instances.
    """

    class Meta:
        model = Book
        fields = '__all__'
