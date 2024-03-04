"""Module for defining authentication-related forms for the app."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import NumberInput, DateInput, CheckboxSelectMultiple, \
    CheckboxInput, FileInput, RadioSelect, EmailField, CharField, \
    PasswordInput, ModelMultipleChoiceField
from django.contrib.auth import get_user_model

from app.models import Book, Category

User = get_user_model()


class CustomFormMixin:
    """Mixin to add 'form-control' class to all fields in a form, excluding
    certain types of fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude_widgets = (
            RadioSelect,
            CheckboxSelectMultiple,
            CheckboxInput,
            FileInput
        )
        for field_name, field in self.fields.items():
            # Vérifie si le widget du champ actuel est dans la liste des
            # widgets à exclure
            if not isinstance(field.widget, exclude_widgets):
                css_class = field.widget.attrs.get('class', '')
                field.widget.attrs[
                    'class'] = f'{css_class} form-control'.strip()


class UserLoginForm(CustomFormMixin, forms.Form):
    """Form for handling user login."""
    email = EmailField()
    password = CharField(widget=PasswordInput())


class UserRegisterForm(CustomFormMixin, UserCreationForm):
    """
    Form for handling new user registration.

    Extends Django's UserCreationForm to include email field and custom
    validation.
    """
    email = EmailField(required=True,
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


class BookForm(CustomFormMixin, forms.ModelForm):
    """
    Form for creating and updating Book instances.

    Uses custom widgets to enhance the user interface, including a date
    picker for the 'date' field, and number inputs for 'price' and 'rate'
    fields to ensure proper data formatting.
    """
    categories = ModelMultipleChoiceField(
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
