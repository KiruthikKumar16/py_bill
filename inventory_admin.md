# inventory/admin.py

`inventory/admin.py` registers the inventory app models with Django's admin site and configures how each model is displayed.

## Overview

This module imports `admin` from `django.contrib` and model classes from `.models`.
It uses the `@admin.register()` decorator to connect each model to a custom admin class.

## Syntax explained

- `from django.contrib import admin`: imports the Django admin registration and customization utilities.
- `from .models import Bill, Customer, Payment, Product, Purchase`: imports the models that should appear in the admin interface.
- `@admin.register(Customer)`: registers the `Customer` model with a custom admin class.
- `class CustomerAdmin(admin.ModelAdmin):`: defines options for how `Customer` records are displayed.
- `list_display = ("name", "location", "phone_no", "gst")`: defines the columns shown on the admin changelist page.
- `search_fields = ("name", "gst", "phone_no")`: enables search over these fields.
- `list_filter = ("date",)`: adds a sidebar filter on the `date` field for `Bill` and `Payment` models.

## Model admin classes

- `CustomerAdmin`: shows customer contact details and enables search by name, GST, or phone.
- `ProductAdmin`: shows product pricing, stock, and purchase date.
- `PurchaseAdmin`: displays purchase orders and allows searching by name and location.
- `BillAdmin`: displays invoice details and provides a date filter.
- `PaymentAdmin`: displays payment history and adds a date filter.

## Teaching notes

This file demonstrates:

- how to register models with the Django admin,
- how to customize admin list display and search,
- and how decorators can replace manual `admin.site.register()` calls.
