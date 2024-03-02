# Django Book Library

This Django project is a simple book library system that allows users to manage books and user accounts. It includes
functionalities for user registration, login, and the ability to add, update, and delete book entries by superusers.

## Installation

To set up this project locally, follow these steps:

```bash
git clone https://github.com/antoinegreuzard/django.git library
cd library
pip install -r requirements.txt
npm install
python manage.py migrate
npm run build
python manage.py collectstatic
```

## Usage

### Running the Project

After installation, you can run the project locally:

```bash
npm run dev
python manage.py runserver
```

This command starts a development server at http://127.0.0.1:8000 where you can interact with the application.

### Managing Users

- **Registration**: New users can register through the `/register/` endpoint.
- **Login**: Registered users can log in through the `/login/` endpoint.
- **Logout**: Authenticated users can log out through the `/logout/` endpoint.

### Managing Books (Superuser Only)

- **Add a Book**: Superusers can add new books by navigating to `/account/books/create/`.
- **Update a Book**: Superusers can update book details by navigating to `/account/books/<int:pk>/update/`.
- **Delete a Book**: Superusers can delete books by navigating to `/account/books/<int:pk>/delete/`.

## Features

- **User Authentication**: Supports user registration, login, and logout.
- **Book Management**: Superusers can add, update, and delete book entries. Each book has a title, description, price,
  author, publication date, and rating.
- **Responsive Design**: The project uses Django forms and templates, which are styled to be responsive and
  user-friendly.

## License

This project is licensed under the [MIT License](LICENSE).
