import os
import random
from datetime import datetime

import django
import requests
from faker import Faker

from server.settings import BASE_DIR

# Ensure the correct Django settings module is set.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from app.models import Book, Category, Author

fake = Faker()


def generate_random_date(year):
    start_date = datetime(year, 1, 1).toordinal()
    end_date = datetime(year, 12, 31).toordinal()
    random_day = datetime.fromordinal(random.randint(start_date, end_date))
    return random_day.strftime('%Y-%m-%d')


def calculate_price_based_on(year, editions):
    base_price = 20
    year_modifier = 0.5
    editions_modifier = 2
    year_difference = max(0, year - 2000)
    price = base_price + year_difference * year_modifier + (
        editions - 1) * editions_modifier
    return round(price, 2)


def calculate_rating_based_on(year, editions):
    base_rating = random.uniform(2, 4)
    edition_bonus = min(editions / 10, 0.5)
    return round(min(base_rating + edition_bonus, 5), 1)


from PIL import Image
from io import BytesIO


def download_image(image_url, save_folder="images", save_name=None):
    """
    Download image from `image_url` and save it within `save_folder` with
    `save_name`. If `save_name` is None, the basename of the URL will be used.
    Also checks if the image is larger than 1x1 pixels.
    """
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            if image.size[0] <= 1 or image.size[1] <= 1:
                print(f"Image from {image_url} is too small, skipping.")
                return None

            if not save_name:
                save_name = os.path.basename(image_url)
            save_path = os.path.join(
                os.path.join(BASE_DIR, 'static/images'),
                save_folder,
                save_name
            )
            with open(save_path, 'wb') as out_file:
                out_file.write(response.content)
            return os.path.join('/static/images/', save_folder, save_name)
    except Exception as e:
        print(f"Failed to download {image_url}. Error: {e}")
    return None


def fetch_books():
    response = requests.get(
        'http://openlibrary.org/subjects/programming.json?published_in=2010'
        '-2024&limit=1000&details=true')
    if response.status_code == 200:
        return response.json()['works']
    else:
        print("Failed to fetch data")
        return []


def generate_description(title, year, authors, subjects=None):
    description = (f"Publié pour la première fois en {year}, '{title}' est "
                   f"une œuvre remarquable de {authors}, explorant des "
                   f"thèmes complexes et captivants.")
    if subjects:
        subjects_formatted = ", ".join(subjects)
        description += (
            f" Ce livre aborde divers sujets tels que {subjects_formatted}, "
            f"le rendant indispensable pour les passionnés du domaine."
        )
        description += (
            "Une lecture incontournable pour ceux qui s'intéressent "
            "profondément à ce sujet.")
    return description


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
    books_data = fetch_books()
    for data in books_data:
        book_subjects = data.get('subject', [])
        categories = []
        for subject_name in book_subjects:
            if is_french(subject_name):
                category, _ = Category.objects.get_or_create(name=subject_name)
                categories.append(category)

        # Download author photo.
        author_data = data['authors'][0]
        author_name = author_data.get('name', 'Unknown Author')
        author_key = author_data['key'].split('/')[-1]
        author_photo_url = f"https://covers.openlibrary.org/a/olid/{author_key}-M.jpg"
        author_photo_path = download_image(
            author_photo_url,
            "authors",
            f"{author_key}.jpg"
        )

        # Create or update author with downloaded photo.
        author, _ = Author.objects.update_or_create(
            name=author_data['name'],
            defaults={
                'photo': author_photo_path if author_photo_path else 'static/images/auteur.jpg'}
        )

        # Download book cover.
        cover_image_url = f"http://covers.openlibrary.org/b/id/{data['cover_id']}-L.jpg"
        cover_image_path = download_image(
            cover_image_url,
            "covers",
            f"cover_{data['cover_id']}.jpg"
        )

        category_names = [category.name for category in categories]

        title = data.get('title', 'Titre inconnu')
        description = generate_description(
            title,
            data.get('first_publish_year', 2020),
            author_name,
            category_names
        )
        price = calculate_price_based_on(
            data.get('first_publish_year', 2020),
            data.get('edition_count', 1)
        )
        rate = calculate_rating_based_on(
            data.get('edition_count', 1),
            data.get('edition_count', 1)
        )
        date = generate_random_date(data.get('first_publish_year', 2020))

        # Create book instance.
        book, created = Book.objects.update_or_create(
            title=data['title'],
            defaults={
                'description': description,
                'price': price,
                'author': author,
                'date': date,
                'rate': rate,
                'cover_image': cover_image_path if cover_image_path else 'static/images/auteur.jpg',
            }
        )
        if created:
            book.categories.set(categories)
            print(
                f'Book "{book.title}" added with categories and cover image.')
        else:
            print(f'Book "{book.title}" already exists.')


if __name__ == '__main__':
    add_books_and_categories()
