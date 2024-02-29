"""Module for defining authentication-related forms for the app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from app.models import Book

User = get_user_model()


class UserLoginForm(forms.Form):
    """Form for handling user login."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    """
    Form for handling new user registration.

    Extends Django's UserCreationForm to include email field and custom validation.
    """

    email = forms.EmailField(required=True, help_text="Required. Add a valid email address.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        """Validate that the submitted email is not already in use."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email

    def save(self, commit=True):
        """
        Save the new user instance. Overridden to set username as email.

        :param commit: Whether to commit the save to the database.
        :return: The newly created user instance.
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.

    Uses custom widgets to enhance the user interface, including a date picker for the 'date' field,
    and number inputs for 'price' and 'rate' fields to ensure proper data formatting.
    """

    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'price': forms.NumberInput(),
            'rate': forms.NumberInput(attrs={'step': "0.01"}),
        }
