"""
Views module for handling requests related to
user authentication and application functionality.
"""
import json
import logging

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import CreateView, UpdateView, DeleteView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from app.forms import UserLoginForm, UserRegisterForm, BookForm
from app.models import Book, Category
from app.serializers import UserSerializer, BookSerializer

logger = logging.getLogger(__name__)


class IsAdminOrReadOnly(IsAdminUser):
    """
    Custom permission to only allow admin users to edit or delete objects.
    """

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class CreateUserView(APIView):
    """API view for creating new users."""

    @staticmethod
    def post(request):
        """
        Create a new user instance.

        Validates the request data using the UserSerializer and creates a
        new user if the data is valid. Returns HTTP 201 Created on success,
        or HTTP 400 Bad Request if the data is invalid.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating books."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]


def login_view(request):
    """Handle user login requests."""
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('account')
            form.add_error(None, "Invalid credentials")
    else:
        form = UserLoginForm()
    return render(request, "app/login.html", {'form': form})


def register_view(request):
    """Handle user registration requests."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "app/register.html", {'form': form})


@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    """Display the account page for logged-in users."""
    books = Book.objects.filter(
        author=request.user
    ) if not request.user.is_superuser else Book.objects.all()
    return render(request, "app/account.html", {'books': books})


def home(request):
    """Display the home page with an optional search query and sorting."""
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort_by', '')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(
                author__icontains=query))

    if sort_by == 'price_asc':
        books = books.order_by('price')
    elif sort_by == 'price_desc':
        books = books.order_by('-price')
    elif sort_by == 'date_asc':
        books = books.order_by('date')
    elif sort_by == 'date_desc':
        books = books.order_by('-date')
    elif sort_by == 'rating_asc':
        books = books.order_by('rate')
    elif sort_by == 'rating_desc':
        books = books.order_by('-rate')

    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "app/home.html",
                  {'page_obj': page_obj, 'query': query})


class BookCRUDMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to check user permissions for book CRUD operations."""
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('account')

    def test_func(self):
        return self.request.user.is_superuser


class BookCreateView(BookCRUDMixin, CreateView):
    """A view for creating a new book instance."""


class BookUpdateView(BookCRUDMixin, UpdateView):
    """A view for updating an existing book instance."""


class BookDeleteView(BookCRUDMixin, DeleteView):
    """A view for deleting an existing book instance."""
    template_name = 'app/book_confirm_delete.html'


@require_http_methods(["GET"])
def search_autocomplete(request):
    """Provide autocomplete suggestions for book search."""
    if 'term' in request.GET:
        qs = Book.objects.filter(title__icontains=request.GET['term'])
        titles = list(qs.values_list('title', flat=True))
        return JsonResponse(titles, safe=False)
    return JsonResponse([], safe=False)


@ensure_csrf_cookie
@require_POST
@login_required
def add_category(request):
    """Add a new book category."""
    if not request.user.is_superuser:
        return JsonResponse({"error": "Authorization denied."}, status=403)

    try:
        data = json.loads(request.body)
        category_name = data.get('categoryName', '').strip()
        if not category_name:
            return JsonResponse({"error": "Category name cannot be empty."},
                                status=400)

        Category.objects.create(name=category_name)
        return JsonResponse({"success": "Category successfully added."},
                            status=201)
    except IntegrityError:
        return JsonResponse(
            {"error": "A category with that name already exists."}, status=400)
    except ValidationError as e:
        logger.error("Validation error while adding a new category: %s", e)
        return JsonResponse({"error": "Invalid data provided."}, status=400)
    except json.JSONDecodeError:
        logger.error("JSON decode error in add_category")
        return JsonResponse({"error": "Invalid JSON data."}, status=400)


def custom_404(request, exception):
    """Redirect to home page on 404 errors."""
    return redirect('home')
