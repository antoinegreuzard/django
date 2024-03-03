"""
Serializers for the app.

This module defines serializers for the User and Book models. These
serializers are used to convert complex data types such as querysets and
model instances to native Python datatypes that can then be easily rendered
into JSON, XML, or other content types. They are also used for
deserialization, i.e., converting parsed data back into complex types,
after validating the incoming data.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from app.models import Book

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    Converts User instances to and from Python datatypes,
    handles user creation and password setting securely.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Overridden create method to handle user creation with hashed password.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Overridden update method to handle password setting securely.
        Password is set only if it's included in validated_data.
        """
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.

    Handles serialization and deserialization of Book instances efficiently.
    """

    class Meta:
        model = Book
        fields = '__all__'
