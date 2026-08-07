# warehouse/urls.py

`warehouse/urls.py` defines the root URL patterns for the Django project.

## Overview

This module imports Django's admin module and the `include` and `path` functions from `django.urls`.
It tells Django which URL patterns are handled by the admin application and which are forwarded to the inventory app.

## Syntax explained

- `from django.contrib import admin`: imports the built-in Django admin site instance.
- `from django.urls import include, path`: imports helpers for defining URL mappings.
- `urlpatterns = [...]`: a list of `path()` calls that Django uses to match incoming requests.
- `path('admin/', admin.site.urls)`: routes URLs under `/admin/` to Django's admin application.
- `path('', include('inventory.urls', namespace='inventory'))`: forwards the root URL space to the `inventory` app's URL configuration and assigns it a namespace.

## Teaching notes

This file is useful for teaching Django's URL dispatcher and how one project can delegate routing to reusable apps.
