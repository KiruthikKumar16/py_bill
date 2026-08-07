# warehouse/settings.py

`warehouse/settings.py` configures the global Django settings for the project.

## Overview

This module defines application configuration, database settings, template loading, middleware, internationalization, and static file settings.
It is loaded automatically by Django when running management commands or starting the server.

## Syntax explained

- `from pathlib import Path`: imports the `Path` class for working with filesystem paths.
- `BASE_DIR = Path(__file__).resolve().parent.parent`: computes the project root directory relative to this file.
- `SECRET_KEY`: stores a secret string used to sign cryptographic data in Django.
- `DEBUG = True`: enables detailed error pages and other developer features.
- `ALLOWED_HOSTS = []`: lists valid hostnames for production deployments.
- `INSTALLED_APPS = [...]`: registers built-in Django applications and the custom `inventory` app.
- `MIDDLEWARE = [...]`: defines middleware components that process each HTTP request and response.
- `ROOT_URLCONF = 'warehouse.urls'`: points Django to the root URL configuration module.
- `TEMPLATES = [...]`: configures template backends, template directories, and context processors.
- `WSGI_APPLICATION = 'warehouse.wsgi.application'`: defines the WSGI callable for deployment.
- `DATABASES = {...}`: selects SQLite as the default database engine and sets the database file path.
- `AUTH_PASSWORD_VALIDATORS`: lists validators that enforce secure password rules.
- `LANGUAGE_CODE`, `TIME_ZONE`, `USE_I18N`, `USE_TZ`: configure localization and timezone handling.
- `STATIC_URL = 'static/'`: defines the base URL for static assets.

## Teaching notes

This file is useful for teaching:

- how Django uses a Python module for project configuration,
- how to reference `BASE_DIR` safely with `pathlib.Path`,
- and how to wire together installed apps, templates, and middleware.
