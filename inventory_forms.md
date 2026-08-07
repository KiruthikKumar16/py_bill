# inventory/forms.py

`inventory/forms.py` defines Django form classes that map database models into HTML form fields and validate user input.

## Overview

This module imports `forms` from Django and the `Bill`, `Customer`, `Payment`, `Product`, and `Purchase` model classes from `.models`.
The forms are built on `forms.ModelForm`, which automatically creates form fields based on model fields.
A shared base class, `BootstrapModelForm`, adds the Bootstrap `form-control` CSS class to all widgets.

## Syntax explained

- `from django import forms`: imports Django's form library so the module can define form classes.
- `from .models import Bill, Customer, Payment, Product, Purchase`: imports the model classes used by the forms.
- `class BootstrapModelForm(forms.ModelForm):`: defines a reusable subclass of `forms.ModelForm`.
- `def __init__(self, *args, **kwargs):`: custom initializer that runs when a form instance is created.
- `super().__init__(*args, **kwargs)`: calls the parent `ModelForm` initializer to populate `self.fields`.
- `for field in self.fields.values():`: iterates through all form fields.
- `field.widget.attrs["class"] = ...`: updates the rendered HTML widget attributes to include Bootstrap styling.
- `class Meta:`: nested class used by Django to configure model binding, included fields, and widgets.
- `widgets = {...}`: overrides default widgets for specific fields, such as using `DateInput` with `type="date"`.
- `def clean_amount(self):`: implements a field-specific validator for the `amount` field in `PaymentForm`.
- `raise forms.ValidationError(...)`: raises a validation error when the input does not meet business rules.

## Form classes

- `CustomerForm`: includes `name`, `location`, `phone_no`, and `gst` fields. It uses `TextInput` placeholders to guide the user.
- `ProductForm`: includes purchase and sale rates, quantity, and purchase date. It renders the date field as a browser date picker.
- `PurchaseForm`: builds a purchase order form and also uses a date picker for the `date` field.
- `BillForm`: exposes the bill date, customer relationship, product relationship, quantity, and rate.
- `PaymentForm`: exposes the bill relationship, payment amount, and date.

## Validation logic

The `PaymentForm.clean_amount` method checks:

- the `amount` is not empty and is greater than zero,
- the payment does not exceed the current unpaid balance of the selected bill.

This shows how Django performs validation before saving data.

## Teaching notes

This file is ideal for teaching:

- how `ModelForm` maps models to form fields,
- how to customize widget attributes and placeholders,
- how to add reusable behavior in a base form class,
- and how to validate individual fields using `clean_<fieldname>()` methods.
