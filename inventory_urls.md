# inventory/urls.py

`inventory/urls.py` defines URL routing rules for the inventory Django app.

## Overview

This module imports Django's `path` function and the `views` module from the same app.
It defines `app_name = "inventory"` so the app can be referenced using namespaced URL names in templates and code.
The `urlpatterns` list maps path expressions to view functions.

## Syntax explained

- `from django.urls import path`: imports the routing helper used to define URL patterns.
- `from . import views`: imports the view functions that will handle requests.
- `app_name = "inventory"`: defines the application namespace for reverse URL lookups.
- `urlpatterns = [...]`: defines the list of URL patterns Django checks in order.
- `path("", views.dashboard, name="dashboard")`: maps the root path to the dashboard view and gives it the name `dashboard`.
- `path("customers/<int:pk>/edit/", views.customer_update, name="customer_update")`: captures an integer parameter named `pk` from the URL and passes it to the view.

## Routing patterns

- `path("customers/", ...)`: list customers.
- `path("customers/add/", ...)`: show the add customer form.
- `path("customers/<int:pk>/delete/", ...)`: delete the selected customer.
- Similar patterns exist for products, purchases, bills, and payments.

## Teaching notes

This file is a good example of:

- how Django uses `path()` to convert URL strings into view calls,
- how named URLs enable clean reverse lookups in templates,
- and how apps can keep their routing self-contained and reusable.
