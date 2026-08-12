# Warehouse Management and Billing App

A Django web application for managing customers, products, purchases, invoices, and payments in a wholesale shop.

## Project files

- `manage.py`: entry point for Django management commands.
- `warehouse/`: contains Django project configuration and root URL routing.
- `inventory/`: contains the inventory app, including models, views, forms, URLs, and admin registration.
- `templates/inventory/`: HTML templates used to render the app UI.
- `requirements.txt`: Python dependencies required to run the project.
- `*.md`: markdown documentation files explaining each Python module and its syntax.

## Requirements

- Python 3.8 or newer.
- Django 6.x.

## Run the app locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Apply migrations to create the database schema:

```bash
python manage.py migrate
```

3. Start the development server:

```bash
python manage.py runserver
```

4. Open `http://127.0.0.1:8000/` in your browser.

## How the code is organized

- `warehouse/settings.py` configures the Django project, database, installed apps, templates, middleware, and static files.
- `warehouse/urls.py` routes the root site URLs to the `inventory` app and the admin interface.
- `inventory/models.py` defines the database schema and business logic for customers, products, bills, and payments.
- `inventory/forms.py` creates Django forms and validation rules for the models.
- `inventory/views.py` contains the request handlers that render pages and process form submissions.
- `inventory/urls.py` maps app-specific URL patterns to view functions.
- `inventory/admin.py` registers models with Django admin and customizes admin display options.

## Notes

- The project uses SQLite as its default database.
- Billing decreases product stock and tracks outstanding balances.
- Payments record the paid amount and update remaining balances.
- Chart data is prepared in views and rendered with Chart.js in the dashboard.
- The Django web project can be packaged into a Windows executable using PyInstaller.

## Windows packaging for the Django app

This project includes a simple launcher and build helper for Windows:

- `launcher.py` starts the Django development server and opens the browser automatically.
- `build_windows_exe.py` runs PyInstaller to produce a single executable bundle.

### Build instructions

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Build the executable:

```bash
python build_windows_exe.py
```

3. Run the packaged app:

```bash
dist\warehouse_management.exe
```

### Notes

- Use Python 3.8 through 3.14 for best compatibility.
- `PyInstaller` 6.x is required for Python 3.14 and later.
- The packaged executable runs the Django app as a local web server.
- If `pywebview` is installed, the app opens inside a native application window instead of the browser.
- If `pywebview` is missing, `launcher.py` falls back to opening the system browser.
- This is still a desktop packaging wrapper for a web app, not a full native Win32 redesign.
- The dashboard is styled for a polished app-like experience with responsive cards, modern metrics, and charts.
