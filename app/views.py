"""
Views module for handling requests related to
user authentication and application functionality.
"""

from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, DeleteView

from rest_framework import status, generics
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.views import APIView

from app.forms import UserLoginForm, UserRegisterForm, BookForm
from app.models import Book
from app.serializers import UserSerializer, BookSerializer

User = get_user_model()


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit or delete objects.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CreateUserView(APIView):
    """API view for creating new users."""

    @staticmethod
    def post(request):
        """Handle POST request to create a new user."""
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
    if request.user.is_authenticated:
        return redirect('account')
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('account')
    else:
        form = UserLoginForm()
    return render(request, "app/login.html", {'form': form})


def register_view(request):
    """Handle user registration requests."""
    if request.user.is_authenticated:
        return redirect('account')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, "app/register.html", {'form': form})


def logout_view(request):
    """Log out the current user."""
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    """Display the account page for logged-in users."""
    books = Book.objects.all() if request.user.is_superuser else None
    return render(request, "app/account.html", {'books': books})


def home(request):
    """Display the home page with an optional search query."""
    query: object = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, "app/home.html", {'books': books, 'query': query})


def custom_404(request, exception):
    """Redirect to home page on 404 errors."""
    return redirect('home')


class BookCreateView(CreateView):
    """
    A view for creating a new book instance.
    Automatically generates a form for all fields of the `Book` model.
    Redirects to the account page (`account`) after successful creation.
    """
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('account')


class BookUpdateView(UpdateView):
    """
    A view for updating an existing book instance.
    Automatically generates a form for all fields of the `Book` model.
    Redirects to the account page (`account`) after successful update.
    """
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('account')


class BookDeleteView(DeleteView):
    """
    A view for deleting an existing book instance.
    Asks for deletion confirmation from the user before proceeding.
    Redirects to the account page (`account`) after successful deletion.
    """
    model = Book
    context_object_name = 'book'
    success_url = reverse_lazy('account')
