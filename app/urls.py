"""
URL Configuration for the app.

This module defines URL patterns for user authentication
and interaction with the Book model through the web API and views.
"""

from django.urls import path
from app.views import CreateUserView, \
    logout_view, \
    account_view, \
    BookListCreateAPIView, \
    home, \
    BookCreateView, \
    BookUpdateView, \
    BookDeleteView, \
    search_autocomplete, add_category, AuthorCreateView, \
    AuthorUpdateView, LoginView, RegisterView

urlpatterns = [
    path('api/signup/', CreateUserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', account_view, name='account'),
    path('api/books/', BookListCreateAPIView.as_view(), name='book'),
    path('account/book/create/', BookCreateView.as_view(),
         name='book-create'),
    path('account/book/<int:pk>/update/', BookUpdateView.as_view(),
         name='book-update'),
    path('account/book/<int:pk>/delete/', BookDeleteView.as_view(),
         name='book-delete'),
    path('api/search-autocomplete/', search_autocomplete,
         name='search-autocomplete'),
    path('api/category/', add_category, name='category'),
    path('account/author/edit/<int:pk>/', AuthorUpdateView.as_view(),
         name='author-update'),
    path('account/author/create/', AuthorCreateView.as_view(),
         name='author-create'),
    path('', home, name='home'),
]
