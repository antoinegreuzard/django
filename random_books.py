"""This script is designed to populate the database with fake data for
testing purposes. It uses the Django ORM to create and add categories and
books with realistic but fake data. This facilitates testing and development
by providing a way to quickly generate data within the database without
manual input."""

import os
import random

import django
from faker import Faker

# Configuring Django to execute commands outside of a server environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book, Category

fake = Faker()


def add_categories():
    """
    Creates and adds 5 categories to the database with fake but realistic data
    """
    category_names = set()
    while len(category_names) < 5:
        category_names.add(fake.unique.word().capitalize())

    for name in category_names:
        category = Category.objects.create(name=name)
        print(f'Category {category.name} added.')


def add_books():
    """
    Creates and adds 20 books to the database with fake but realistic data.
    Each book is randomly assigned 1 to 3 categories from the existing
    categories in the database.
    """
    categories = list(Category.objects.all())

    for _ in range(20):
        book = Book.objects.create(
            title=fake.sentence(nb_words=5),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(5.99, 50.99), 2),
            author=fake.name(),
            date=fake.date_between(start_date='-10y', end_date='today'),
            rate=round(random.uniform(0, 5), 2),
        )

        # Assign 1 to 3 random categories to each book
        book_categories = random.sample(categories, k=random.randint(1, 3))
        book.categories.set(book_categories)

        print(f'Book {book.title} added.')


if __name__ == '__main__':
    add_categories()
    add_books()
