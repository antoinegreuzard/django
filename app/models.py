from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Ajoutez des champs supplémentaires ici
    role = models.CharField(max_length=30)
