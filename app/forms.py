"""Module for defining authentication-related forms for the app."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import NumberInput, DateInput, CheckboxSelectMultiple
from django.contrib.auth import get_user_model

from app.models import Book, Category

User = get_user_model()


class UserLoginForm(forms.Form):
    """Form for handling user login."""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    """
    Form for handling new user registration.

    Extends Django's UserCreationForm to include email field and custom
    validation.
    """
    email = forms.EmailField(required=True,
                             help_text="Required. Add a valid email address.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        """Validate that the submitted email is not already in use."""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        """Save the new user instance. Overridden to set username as email."""
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.

    Uses custom widgets to enhance the user interface, including a date
    picker for the 'date' field, and number inputs for 'price' and 'rate'
    fields to ensure proper data formatting.
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False)

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'date': DateInput(
                attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'},
                format='%Y-%m-%d'),
            'price': NumberInput(),
            'rate': NumberInput(attrs={'step': "0.01"}),
        }
