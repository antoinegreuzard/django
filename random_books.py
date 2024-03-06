import os
import random

import requests
import django
from faker import Faker

# Configuring Django to execute commands outside of a server environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book, Category

fake = Faker()


def fetch_books():
    """
    Fetches books data from the Open Library API.
    """
    response = requests.get(
        'http://openlibrary.org/subjects/programming.json?published_in=2000'
        '-2024&limit=500')
    if response.status_code == 200:
        return response.json()['works']
    else:
        print("Failed to fetch data")
        return []


def is_french(subject):
    """
    Determines if a given subject/category name is likely to be in French.
    """
    french_keywords = ['programmation', 'ingénierie', 'logiciel', 'systèmes',
                       'informatique', 'internet', 'système', 'ordinateur',
                       'développement', 'développeur', 'algorithmes',
                       'mathematiques']
    return any(keyword in subject.lower() for keyword in french_keywords)


def add_books_and_categories():
    """
    Adds books and their categories to the database using data fetched from
    the Open Library API and generates fake price and rate for each book
    using Faker.
    """
    books_data = fetch_books()
    for data in books_data:
        book_subjects = data.get('subject', [])
        categories = []
        for subject_name in book_subjects:
            if is_french(subject_name):
                category, _ = Category.objects.get_or_create(name=subject_name)
                categories.append(category)

        authors = data.get('authors', [])
        authors_names = ', '.join([author['name'] for author in authors])
        subjects = ', '.join(book_subjects)

        first_publish_year = data.get('first_publish_year', None)

        if first_publish_year:
            random_month = random.randint(1, 12)
            random_day = random.randint(1, 28)
            date_str = f"{first_publish_year}-{random_month:02d}-{random_day:02d}"
        else:
            date_str = fake.date_between(
                start_date='-10y', end_date='today'
            ).isoformat()

        description = f"This book, titled '{data['title']}', was first published in {first_publish_year}. It covers the following subjects: {subjects}. Written by {authors}."

        book, created = Book.objects.get_or_create(
            title=data['title'],
            defaults={
                'description': description,
                'price': round(fake.pydecimal(left_digits=2, right_digits=2,
                                              positive=True, min_value=5,
                                              max_value=50), 2),
                'author': authors_names,
                'date': date_str,
                'rate': round(
                    fake.pydecimal(left_digits=1, right_digits=1, min_value=0,
                                   max_value=5), 1),
            }
        )
        if created:
            book.categories.set(categories)
            print(f'Book "{book.title}" added with categories.')
        else:
            print(f'Book "{book.title}" already exists.')


if __name__ == '__main__':
    add_books_and_categories()
