# db.py

`db.py` contains the legacy SQLite database wrapper used by the old Tkinter desktop version of the warehouse app.

## Overview

This module imports `sqlite3` for SQLite access, `date` for default timestamps, and type hints for improved clarity.
It defines a `Database` class that opens a connection, creates tables, and exposes CRUD methods for customers, products, purchases, bills, and payments.

## Syntax explained

- `import sqlite3`: imports the standard library SQLite module for database access.
- `from datetime import date`: imports the `date` class for default date values.
- `from typing import Dict, List, Optional`: imports type annotation helpers.
- `DB_PATH = "warehouse.db"`: defines the default path for the SQLite file.
- `def dict_factory(cursor, row):`: defines a helper that transforms database rows into dictionaries.
- `self.conn = sqlite3.connect(self.path)`: opens a SQLite connection.
- `self.conn.row_factory = dict_factory`: ensures query results are returned as dictionaries instead of tuples.
- `cursor.execute("CREATE TABLE IF NOT EXISTS ...")`: executes SQL that creates tables only when they do not already exist.
- `self.conn.commit()`: commits transactions to the database.

## Database class syntax

- `class Database:`: defines the database wrapper class.
- `def __init__(self, path: str = DB_PATH):`: initializes the connection and sets up the schema.
- `def close(self):`: closes the SQLite connection.
- `def add_customer(self, ...):`: inserts a new customer record and returns the new row id.
- `def get_customers(self) -> List[Dict]:`: retrieves all customers ordered by ID.
- `def update_customer(self, ...):`: updates an existing customer record.
- `def delete_customer(self, customer_id: int):`: deletes a customer by ID.
- `def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:`: fetches one customer or returns `None`.
- `def add_product(...):`: inserts a product row using parameter substitution to prevent SQL injection.
- `def change_product_quantity(self, product_id: int, quantity_change: int):`: updates stock quantity using arithmetic in SQL.
- `def add_bill(...)`: inserts a bill and then reduces the product quantity by calling `change_product_quantity`.
- `def get_bills(self) -> List[Dict]:`: performs a `LEFT JOIN` query to fetch bill records with customer and product names.
- `def add_payment(...)`: calculates the current balance, inserts the payment, and stores the remaining balance.
- `def get_total_paid_for_bill(...)`: computes the sum of payments for a bill using `SUM(Amount)`.
- `def get_amount_due_for_bill(...)`: calculates bill total, reads paid amount, and returns remaining due with `max(0.0, total - paid)`.

## Teaching notes

This module is ideal for teaching:

- how to use raw SQL from Python,
- how to define helper functions and methods for CRUD operations,
- how to use `dict_factory` to make results easier to work with,
- and how to implement simple business rules in a database wrapper.
