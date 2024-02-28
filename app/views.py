from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserLoginForm, UserRegisterForm
from .models import Book
from .serializers import UserSerializer, BookSerializer

User = get_user_model()


class CreateUserView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def login_view(request):
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
                form.add_error(None, "Adresse e-mail ou mot de passe incorrect.")
    else:
        form = UserLoginForm()
    return render(request, "app/login.html", {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('account')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, "app/register.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    return render(request, "app/account.html")


def home(request):
    query: object = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    return render(request, "app/home.html", {'books': books, 'query': query})


def custom_404(request, exception):
    return redirect('home')
