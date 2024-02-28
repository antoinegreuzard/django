"""
Module containing test cases for the app.
It includes tests for user views, book views, and login functionality.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from app.models import CustomUser, Book


class UserViewTests(TestCase):
    """Test cases for user-related views."""

    def test_create_user(self):
        """Ensure that a user can be created successfully."""
        url = reverse('signup')
        data = {'email': 'test@example.com',
                'password': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CustomUser.objects.filter(
                email='test@example.com'
            ).exists()
        )


class BookViewTests(TestCase):
    """Test cases for book-related views."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for the book tests."""
        Book.objects.create(title="Test Book",
                            description="Test Description",
                            price=10,
                            author="Test Author",
                            date="2023-01-01", rate=4.5)

    def test_book_list(self):
        """Ensure the book list view returns a successful response and correct book data."""
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        """Ensure that a book can be created successfully."""
        url = reverse('book-list-create')
        data = {'title': "Another Test Book",
                'description': "Another Test Description",
                'price': 15,
                'author': "Another Test Author",
                'date': "2023-01-02",
                'rate': 4.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Book.objects.filter(
                title="Another Test Book"
            ).exists()
        )


class LoginViewTests(TestCase):
    """Test cases for the login view."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for the login tests."""
        user = get_user_model()
        user.objects.create_user(email='testlogin@example.com', password='testpassword')

    def test_login_view_success(self):
        """Ensure that a user can log in successfully."""
        url = reverse('login')
        data = {'email': 'testlogin@example.com',
                'password': 'testpassword'}
        response = self.client.post(url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
