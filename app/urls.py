from django.urls import path
from .views import CreateUserView

urlpatterns = [
    path('api/signup/', CreateUserView.as_view(), name='signup'),
]
