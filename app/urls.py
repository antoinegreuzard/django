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
    home, \
    BookCreateView, \
    BookUpdateView, \
    BookDeleteView, \
    search_autocomplete, add_category

urlpatterns = [
    path('api/signup/', CreateUserView.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('account/', account_view, name='account'),
    path('api/books/', BookListCreateAPIView.as_view(), name='book'),
    path('account/books/create/', BookCreateView.as_view(),
         name='book-create'),
    path('account/books/<int:pk>/update/', BookUpdateView.as_view(),
         name='book-update'),
    path('account/books/<int:pk>/delete/', BookDeleteView.as_view(),
         name='book-delete'),
    path('api/search-autocomplete/', search_autocomplete,
         name='search-autocomplete'),
    path('api/category/', add_category, name='category'),
    path('', home, name='home'),
]
