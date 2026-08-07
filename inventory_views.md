# inventory/views.py

`inventory/views.py` contains function-based Django views that handle HTTP requests and render templates for the warehouse app.

## Overview

This module imports helper libraries for JSON serialization, decimal math, and Django request handling.
It imports form classes and model classes from the `inventory` app and a helper function from `invoice.py`.
The views include a dashboard and standard CRUD pages for customers, products, purchases, bills, and payments.

## Syntax explained

- `import json`: imports Python's JSON library to serialize chart data for templates.
- `from decimal import Decimal`: imports `Decimal` for precise money calculations in the dashboard.
- `from django.db.models import Sum`: imports the aggregation helper used by models.
- `from django.shortcuts import get_object_or_404, redirect, render`: imports common view helpers.
- `from django.urls import reverse`: imports a function that returns URL strings from names.
- `def dashboard(request):`: defines the landing page view function.
- `Product.objects.all()`: queries all product records.
- `Bill.objects.select_related("customer", "product")`: fetches bills with their related customer and product in a single database query.
- `request.POST or None`: passes POST data into a form when the request is a POST, and `None` otherwise.
- `form.is_valid()`: checks if the submitted form data passes validation.
- `form.save()`: saves the valid form to the database.
- `redirect(reverse("inventory:customer_list"))`: redirects the browser to a named URL route.
- `get_object_or_404(Model, pk=pk)`: fetches an object or raises a 404 error if it does not exist.
- `render(request, "template.html", context)`: renders an HTML template with context data.

## Dashboard view

- It computes daily sales labels and values for charts.
- It aggregates top customers by billed amount.
- It calculates totals such as revenue, outstanding due, and inventory value.
- It prepares the top stocked products list and recent bills for the dashboard summary.
- It serializes lists to JSON for `Chart.js` in the template so the client-side script can parse them safely.

## Dashboard UI and chart data

- `json.dumps(list(daily_sales.keys()))` converts Python dates into a JSON array of labels for the sales chart.
- `json.dumps([float(value) for value in daily_sales.values()])` converts `Decimal` totals into a numeric JSON array.
- `stock_labels` and `stock_values` use the top products query results to show a product stock bar chart.
- The dashboard template renders these values in `data-labels` and `data-values` attributes on canvas elements.

## CRUD view patterns

Each create/update/delete view follows the same pattern:

- instantiate a form with POST data or the model instance,
- validate and save the form on POST,
- redirect on success,
- otherwise render the form template with the current form instance.

## Bill-specific logic

- `bill_create` uses `form.save(commit=False)` to create a `Bill` object without saving immediately.
- It validates bill quantity and stock levels before saving.
- `bill_invoice` renders a printable invoice page and converts totals to words.

## Payment-specific logic

- `payment_create` also uses `form.save(commit=False)` to allow the `Payment` model to compute the remaining balance in its `save()` method.

## Teaching notes

This file demonstrates:

- function-based views in Django,
- form validation and conditional rendering,
- using `get_object_or_404` to guard object access,
- redirecting after POST to avoid duplicate submission,
- and preparing JSON data for client-side charts.
