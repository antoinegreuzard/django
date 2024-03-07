import os
import random
from datetime import datetime

import requests
import django
from faker import Faker

# Configuring Django to execute commands outside of a server environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book, Category

fake = Faker()


def generate_random_date(year):
    """
    Generates a random date for a given year.
    """
    start_date = datetime(year, 1, 1).toordinal()
    end_date = datetime(year, 12, 31).toordinal()
    random_day = datetime.fromordinal(random.randint(start_date, end_date))
    return random_day.strftime('%Y-%m-%d')


def calculate_price_based_on(year, editions):
    """
    Calculates the price of a book based on its year of publication and the
    number of editions.
    """
    base_price = 20
    year_modifier = 0.5
    editions_modifier = 2
    year_difference = max(0, year - 2000)
    price = base_price + year_difference * year_modifier + (
            editions - 1) * editions_modifier

    return round(price, 2)


def calculate_rating_based_on(year, editions):
    """
    Assigns a random rate to each book, with a slight preference
    for average values.
    """
    base_rating = random.uniform(2, 4)
    edition_bonus = min(editions / 10, 0.5)
    return round(min(base_rating + edition_bonus, 5), 1)


def generate_description(title, year, authors, subjects=None):
    """
    Generates a description for a book using its title, year of
    first publication, authors and subjects.

    :param title: Title of the book
    :param year: Year of first publication
    :param authors: Author names
    :param subjects: List ofsubjects/categories associated with the book
    :return: A string containing the generated description
    """
    description = (f"Publié pour la première fois en {year}, '{title}' est "
                   f"une œuvre remarquable de {authors}, explorant des "
                   f"thèmes complexes et captivants.")

    if subjects:
        subjects_formatted = ", ".join(subjects)
        description += f" Ce livre aborde divers sujets tels que {subjects_formatted},"
        f"le rendant indispensable pour les passionnés du domaine."

    description += ("Une lecture incontournable pour ceux qui s'intéressent "
                    "profondément à ce sujet.")

    return description


def fetch_books():
    """
    Fetches books data from the Open Library API.
    """
    response = requests.get(
        'http://openlibrary.org/subjects/programming.json?published_in=2010'
        '-2024&limit=1000&details=true')
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

        category_names = [category.name for category in categories]

        authors_names = ', '.join(
            author['name'] for author in data.get('authors', []))
        first_publish_year = data.get('first_publish_year', None)

        if first_publish_year:
            date_str = generate_random_date(first_publish_year)
        else:
            date_str = fake.date_between(
                start_date='-10y', end_date='today'
            ).isoformat()

        description = generate_description(data['title'], first_publish_year,
                                           authors_names, category_names)

        price = calculate_price_based_on(first_publish_year,
                                         data.get('edition_count', 1))
        rating = calculate_rating_based_on(first_publish_year,
                                           data.get('edition_count', 1))

        book, created = Book.objects.get_or_create(
            title=data['title'],
            defaults={
                'description': description,
                'price': price,
                'author': authors_names,
                'date': date_str,
                'rate': rating,
            }
        )
        if created:
            book.categories.set(categories)
            print(f'Book "{book.title}" added with categories.')
        else:
            print(f'Book "{book.title}" already exists.')


if __name__ == '__main__':
    add_books_and_categories()
