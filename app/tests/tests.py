from django.test import TestCase
from django.urls import reverse
from app.models import CustomUser, Book
from rest_framework import status
from django.contrib.auth import get_user_model


class UserViewTests(TestCase):

    def test_create_user(self):
        url = reverse('signup')
        data = {'email': 'test@example.com', 'password': 'testpassword123', 'role': 'client'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='test@example.com').exists())


class BookViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Créer un livre pour tester
        Book.objects.create(title="Test Book", description="Test Description", price=10, author="Test Author",
                            date="2023-01-01", rate=4.5)

    def test_book_list(self):
        url = reverse('book-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assurez-vous qu'un livre est retourné

    def test_create_book(self):
        url = reverse('book-list-create')
        data = {'title': "Another Test Book", 'description': "Another Test Description", 'price': 15,
                'author': "Another Test Author", 'date': "2023-01-02", 'rate': 4.0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="Another Test Book").exists())


class LoginViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        User.objects.create_user(email='testlogin@example.com', password='testpassword')

    def test_login_view_success(self):
        url = reverse('login')
        data = {'email': 'testlogin@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
