# inventory/models.py

`inventory/models.py` defines the Django data models and business rules for the warehouse application.

## Overview

This module imports `date` from the standard library and `Decimal` for currency-safe arithmetic.
It also imports Django model helpers from `django.db` and `Sum` from `django.db.models`.
The module defines the following models:

- `Customer`: contact and tax details for a wholesale customer.
- `Product`: inventory items with purchase and sale price and stock quantity.
- `Purchase`: purchase order records.
- `Bill`: sales invoices linked to a customer and product.
- `Payment`: payments applied to a bill with a remaining balance.

## Syntax explained

- `from datetime import date`: imports `date` to set default values for date fields.
- `from decimal import Decimal`: imports `Decimal` for precise monetary calculation.
- `class Customer(models.Model):`: defines a Django model class representing a database table.
- `models.CharField(max_length=100)`: declares a text column with a maximum length.
- `blank=True`: allows the field to be empty in forms.
- `class Product(models.Model):` and `models.DecimalField(max_digits=10, decimal_places=2)`: define currency fields.
- `models.DateField(default=date.today)`: uses a callable default so each model instance gets the current date at creation.
- `models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bills")`: creates a one-to-many relationship from `Bill` to `Customer`.
- `related_name`: specifies the reverse relationship name used by Django to access related objects.
- `@property`: exposes Python methods as computed read-only attributes.

## Business logic and methods

### Bill model

- `total_amount`: returns `quantity * rate` for the bill.
- `amount_paid`: aggregates related payment amounts using `self.payments.aggregate(total=Sum("amount"))` and returns `0.00` when there are no payments.
- `amount_due`: subtracts `amount_paid` from `total_amount` and clamps the result at zero.
- `save(self, *args, **kwargs)`: overrides the model save method to update product inventory.
  - It checks whether a new bill is being created with `self.pk is None`.
  - It validates stock availability and decrements `stored_product.quantity`.
  - It saves the product before calling `super().save(*args, **kwargs)` to persist the bill.

### Payment model

- `balance`: stores the remaining due amount after the payment.
- `save(self, *args, **kwargs)`: validates the payment amount and computes the new balance before saving.
  - `if self.amount <= 0:` prevents zero or negative payments.
  - `unpaid = self.bill.amount_due`: calculates the current amount still due on the bill.
  - `self.balance = unpaid - self.amount`: stores the remaining balance after the payment.

## Teaching notes

This module is useful for teaching:

- how Django models map to database tables,
- how to define relationships with `ForeignKey`,
- how to use `@property` for computed values,
- and how to override `save()` to enforce business rules such as inventory updates and payment validation.
