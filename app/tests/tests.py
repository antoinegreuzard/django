"""
Module containing test cases for the app.

This module includes classes and methods for testing user authentication,
book management functionalities, and view responses to ensure that the
application behaves as expected under various conditions.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from app.models import Book, Category

User = get_user_model()


class UserViewTests(TestCase):
    """Test cases for user-related views."""

    def test_create_user(self):
        """
        Ensure that a user can be created successfully.
        """
        url = reverse('signup')
        data = {'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


class BookViewTests(APITestCase):
    """
    Test cases for book-related views.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser('admin@example.com',
                                                 'password123')
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)
        cls.categories = [Category.objects.create(name=f'Category {i}') for i
                          in range(1, 6)]

        # Création d'un livre et assignation de catégories
        cls.book = Book.objects.create(
            title="Test Book",
            description="A test description",
            price=19.99,
            author="Test Author",
            date="2023-01-01",
            rate=4.5,
        )
        cls.book.categories.set(
            cls.categories[:2])

    def test_book_list(self):
        """
        Test the book list view to ensure it returns at least one book.
        """
        url = reverse('book')
        response = self.client.get(url)
        print(response.data)  # Afficher pour le diagnostic
        books_data = response.data if not isinstance(
            response.data, dict
        ) else response.data.get('results', [])
        self.assertTrue(len(books_data) >= 1)

    def test_create_book_with_categories(self):
        """
        Ensure that a book can be created with categories.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('book')
        category_ids = [category.id for category in self.categories]
        book_data = {
            'title': "New Book with Categories",
            'description': "A detailed description.",
            'price': 25.99,
            'author': "Author Name",
            'date': "2023-01-01",
            'rate': 4.5,
            'categories': category_ids
        }
        response = self.client.post(url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginViewTests(TestCase):
    """Test cases for the login view."""

    @classmethod
    def setUpTestData(cls):
        """Set up data for the login tests."""
        User.objects.create_user(email='testlogin@example.com',
                                 password='testpassword')

    def test_login_view_success(self):
        """Ensure that a user can log in successfully."""
        url = reverse('login')
        data = {'email': 'testlogin@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
