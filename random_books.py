import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book


def add_books():
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
