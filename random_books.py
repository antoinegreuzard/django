"""
This script adds 20 books to the database using the Book model.
It is designed to be run in a Django environment.
"""

import os
import datetime
import django

# Configuring Django to execute commands outside of a server environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book


def add_books():
    """
    Creates and adds 20 books to the database with generic data.
    """
    for i in range(1, 21):
        book = Book.objects.create(
            title=f'Book Title {i}',
            description=f'Description for book {i}',
            price=19.99 + i,
            author=f'Author {i}',
            date=datetime.date.today(),
            rate=4.5
        )
        print(f'Book {book.title} added.')


if __name__ == '__main__':
    add_books()
