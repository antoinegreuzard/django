"""
URL Configuration for the app.

This module defines URL patterns for user authentication
and interaction with the Book model through the web API and views.
"""

from django.urls import path
from app.views import CreateUserView, \
    login_view, \
    logout_view, \
    register_view, \
    account_view, \
    BookListCreateAPIView, \
    home

urlpatterns = [
    path('api/signup/', CreateUserView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('account/', account_view, name='account'),
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('', home, name='home'),
]
