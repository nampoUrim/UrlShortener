# UrlShortener

A simple URL shortening web application built with Django. It allows users to convert long URLs into short, shareable links without creating an account.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Model](#database-model)
- [Error Handling](#error-handling)
- [Development Commands](#development-commands)
- [Security Notes](#security-notes)
- [Current Limitations](#current-limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

## Overview

UrlShortener is a small web application designed to simplify the sharing of long URLs by generating shorter alternatives.

The application uses Django for its backend, SQLite for data storage, and HTML, CSS, and JavaScript for its frontend.

The application is public and anonymous: users can shorten URLs and access existing short links without registering or logging in.

This project was developed as a practical backend learning project, with an emphasis on understanding Django models, views, URL routing, database operations, validation, and Git.

## Features

- **Anonymous URL shortening:** Create short links without a user account.
- **Automatic short code generation:** Generate random, six-character alphanumeric codes.
- **Unique short codes:** Prevent duplicate codes through model validation and a database uniqueness constraint.
- **URL validation:** Accept HTTP and HTTPS URLs and validate their structure.
- **Automatic redirection:** Redirect visitors to the original destination URL.
- **Click tracking:** Count the number of recorded visits to each short link.
- **Copy to clipboard:** Copy the generated short URL using the browser's Clipboard API.
- **Responsive interface:** Adapt the interface to desktop and mobile screens.
- **Custom 404 page:** Display a custom error page when a requested short code does not exist, when Django is configured to use custom error templates.
- **Django administration:** Manage stored short links through the built-in Django admin interface.

## How It Works

The application follows a simple request-response workflow.

### 1. Creating a short link

1. The user opens the homepage.
2. The user submits an original URL through the form.
3. Django receives the form submission and validates the URL.
4. The application generates a unique, random short code.
5. The original URL and its short code are stored in the database.
6. The application redirects back to the homepage and displays the generated short link.

### 2. Accessing a short link

When someone visits a URL such as:

`http://127.0.0.1:8000/abc123/`

Django extracts the short code `abc123` from the requested path.

The application searches the database for the corresponding record. If a record exists, the click counter is incremented and the visitor is redirected to the original URL.

If the code does not exist, Django raises an HTTP 404 error.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Web framework, request handling, validation, and administration |
| SQLite | Relational database |
| HTML | Page structure |
| CSS | Styling and responsive layout |
| JavaScript | Clipboard interaction |
| python-dotenv | Loading environment variables from a `.env` file |
| Git | Version control |
| GitHub | Remote repository hosting |

## Project Structure

UrlShortener/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── shortener/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── ...
│   ├── static/
│   │   └── shortener/
│   │       ├── css/
│   │       │   └── style.css
│   │       └── js/
│   │           └── copy-link.js
│   ├── templates/
│   │   ├── 404.html
│   │   └── shortener/
│   │       └── home.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md


### Main components

- `config/settings.py`: Defines Django settings, environment variables, database configuration, installed applications, and static file settings.
- `config/urls.py`: Connects the project's URL configuration to the application and Django admin.
- `shortener/models.py`: Defines the `ShortURL` database model, URL validation, short code generation, and click tracking.
- `shortener/views.py`: Handles the homepage, link creation, and redirection.
- `shortener/urls.py`: Maps URL paths to the appropriate view functions.
- `shortener/admin.py`: Configures how short links are displayed and managed in Django admin.
- `shortener/templates/`: Contains the HTML templates.
- `shortener/static/`: Contains the CSS and JavaScript files.
- `shortener/migrations/`: Contains database schema migrations.
- `manage.py`: Provides the command-line interface for Django management tasks.
- `.env`: Stores local environment variables and secrets. This file must not be committed.
- `.gitignore`: Excludes local databases, environment files, virtual environments, and generated files from Git.
- `requirements.txt`: Lists the Python dependencies required by the project.

## Requirements

Before installing the application, ensure that you have:

- Python installed.
- pip, Python's package installer.
- Git, if you want to clone the repository.
- A terminal compatible with the commands below.

The application uses SQLite, which is supported by Python and does not require a separate database server.

## Installation

### 1. Clone the repository

git clone https://github.com/nampoUrim/UrlShortener.git
cd UrlShortener

### 2. Create a virtual environment

On Windows:

python -m venv urlshortenervenv

Activate it in PowerShell:

.\urlshortenervenv\Scripts\Activate.ps1

Or in Windows Command Prompt:

urlshortenervenv\Scripts\activate.bat

### 3. Install dependencies

python -m pip install -r requirements.txt

### 4. Configure environment variables

Create a `.env` file in the project root, alongside `manage.py`.

Add the following configuration:

DJANGO_SECRET_KEY=replace-with-a-secure-random-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost


Replace the example secret with a securely generated value. Never use the example placeholder as a production secret.

The `.env` file is excluded from version control. Do not upload it to GitHub or share its contents publicly.

### 5. Apply database migrations


python manage.py migrate


This creates the database tables required by Django and the application.

### 6. Create an administrator account


python manage.py createsuperuser


Follow the prompts to create the account.

### 7. Start the development server

python manage.py runserver


Open the following address in your browser:

http://127.0.0.1:8000/

The Django administration interface is available at:

http://127.0.0.1:8000/admin/

## Configuration

The application uses environment variables to configure sensitive or environment-specific settings.

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Secret key used by Django's security-related components |
| `DJANGO_DEBUG` | Enables or disables Django debug mode |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated list of permitted hostnames |

For local development, `DJANGO_DEBUG=True` is convenient. Before deploying the application publicly, set it to `False` and configure the allowed hosts appropriately.

## Usage

### Shorten a URL

1. Navigate to the homepage.
2. Enter a valid HTTP or HTTPS URL.
3. Click **Shorten URL**.
4. Copy the generated short link.

### Follow a short link

Open the generated link in a browser. The application looks up the corresponding destination, records the click, and redirects the visitor.

### Manage links

Log in to `/admin/` using the administrator account created during installation. The administration interface allows you to inspect and manage stored short links.

## Database Model

The application uses a `ShortURL` model with the following fields:

| Field | Description |
|---|---|
| `original_url` | The original destination URL |
| `short_code` | A unique, six-character alphanumeric code |
| `created_at` | The date and time when the record was created |
| `click_count` | The number of recorded clicks |

Each short code identifies a stored destination URL.

The database's uniqueness constraint prevents two records from sharing the same short code. The application also checks for existing codes when generating a new one.

## Error Handling

The application handles several common situations:

- **Invalid URL:** Validation errors are displayed on the homepage.
- **Unknown short code:** The application raises an HTTP 404 error.
- **Custom 404 page:** Django can render the `404.html` template when debug mode is disabled and the template is available through the configured template loaders.

During development, Django may display its technical error page instead of the custom 404 template when `DEBUG=True`.

## Development Commands

Run these commands from the project root with the virtual environment activated.

Check the project configuration:

python manage.py check


Create migrations after model changes:

python manage.py makemigrations


Apply migrations:

python manage.py migrate

Check whether migrations are missing:

python manage.py makemigrations --check --dry-run

Run the automated test suite:

python manage.py test


Start the development server:

python manage.py runserver


Check the current Git status:

git status


## Security Notes

- Never commit `.env` or expose the Django secret key.
- Do not use `DEBUG=True` in a public production deployment.
- Configure `ALLOWED_HOSTS` for the intended deployment environment.
- URL validation checks the URL's format and permitted scheme; it does not guarantee that a destination is reachable or safe.
- A production deployment should include appropriate HTTPS, secure cookie settings, and additional operational security measures.
- Public URL shorteners can be abused to distribute misleading or malicious links. A public production service may require abuse prevention, rate limiting, and reporting mechanisms.

## Current Limitations

- No user accounts or authentication for regular visitors.
- No automatic link expiration.
- No custom aliases.
- No advanced analytics or per-visitor statistics.
- No built-in rate limiting or abuse reporting.
- The application is currently configured for local development and is not, by itself, a complete production deployment.

## Future Improvements

Potential improvements for future versions include:

- Link expiration dates.
- Custom short codes.
- More detailed click statistics.
- Rate limiting and abuse prevention.
- Automated tests covering validation, redirects, and click tracking.
- Production deployment with HTTPS and appropriate security settings.

These improvements are not part of the current V1 scope.

## License

No license has been specified yet.

If you intend to make this project open source, add a `LICENSE` file and update this section with the chosen license. Without an explicit license, others generally do not receive permission to reuse, modify, or redistribute the project beyond what applicable law permits.
