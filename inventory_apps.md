# inventory/apps.py

`inventory/apps.py` defines the application configuration for the `inventory` Django app.

## Overview

This module imports `AppConfig` from `django.apps` and defines a subclass named `InventoryConfig`.
Django uses this configuration class when the app is included in `INSTALLED_APPS`.

## Syntax explained

- `from django.apps import AppConfig`: imports the base class for Django app configuration.
- `class InventoryConfig(AppConfig):`: defines a configuration class for the app.
- `name = 'inventory'`: tells Django the Python path for this app.

## Teaching notes

This file is a simple example of Django app configuration.
It is usually generated automatically and provides a place to add app-specific settings or startup logic later.
