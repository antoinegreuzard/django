"""
Module containing test cases for the app.

This module includes classes and methods for testing user authentication,
book management functionalities, view responses, and image uploads to ensure
that the application behaves as expected under various conditions.
"""

import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.models import Book, Category, Author

User = get_user_model()


def create_temporary_image():
    """
    Creates a temporary image and returns a SimpleUploadedFile
    """
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        image = Image.new("RGB", (100, 100), "red")
        image.save(tmp_file, format='JPEG')
        tmp_file.seek(0)
        tmp_file_name = tmp_file.name
    with open(tmp_file_name, mode='rb') as f:
        file = SimpleUploadedFile('temp_image.jpg', f.read(),
                                  content_type='image/jpeg')
    return file


class UserViewTests(TestCase):
    """Test cases for user-related views."""

    def test_create_user(self):
        """Ensure that a user can be created successfully."""
        url = reverse('signup')
        data = {'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


class BookViewTests(APITestCase):
    """Test cases for book-related views."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            'admin@example.com',
            'password123'
        )
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)

        cls.author_image = create_temporary_image()
        cls.author = Author.objects.create(
            name="Test Author",
            photo=cls.author_image
        )

        cls.category = Category.objects.create(name='Category 1')

        cls.book_image = create_temporary_image()
        cls.book = Book.objects.create(
            title="Test Book",
            description="A test description",
            price=19.99,
            author=cls.author,
            date="2023-01-01",
            rate=4.5,
            cover_image=cls.book_image
        )
        cls.book.categories.add(cls.category)

    def test_book_list(self):
        url = reverse('book')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_book_with_categories(self):
        self.client.login(email='admin@example.com', password='password123')

        url = reverse('book-create')
        temp_image = create_temporary_image()
        data = {
            'title': "New Book with Categories",
            'description': "A detailed description.",
            'price': 25.99,
            'author': self.author.id,
            'date': "2023-01-02",
            'rate': 4.5,
            'categories': [self.category.id],
            'cover_image': temp_image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(
            Book.objects.filter(title="New Book with Categories").exists())


class AuthorViewTests(APITestCase):
    """Test cases for author-related views."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            'admin@example.com',
            'password123'
        )
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)

        cls.author_image = create_temporary_image()
        cls.author = Author.objects.create(
            name="Initial Author",
            photo=cls.author_image
        )

    def test_author_update(self):
        self.client.login(email='admin@example.com', password='password123')

        url = reverse('author-update', kwargs={'pk': self.author.pk})
        new_temp_image = create_temporary_image()
        data = {
            'name': "Updated Author",
            'photo': new_temp_image
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND
        )
        self.author.refresh_from_db()
        self.assertEqual(self.author.name, "Updated Author")


class LoginViewTests(TestCase):
    """Test cases for the login view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='testlogin@example.com',
            password='testpassword'
        )

    def test_login_view_success(self):
        url = reverse('login')
        data = {'email': 'testlogin@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
