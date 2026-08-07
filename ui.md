# ui.py

`ui.py` contains the legacy Tkinter graphical user interface for the warehouse desktop app.

## Overview


This module imports `tkinter`, `messagebox`, and `ttk` from the standard library.
It creates a `WarehouseApp` class that builds the main window, tabs, controls, and event handlers.

## Syntax explained

- `import tkinter as tk`: imports the Tkinter module and aliases it as `tk` for convenience.
- `from tkinter import messagebox, ttk`: imports message boxes and themed widgets.
- `from typing import Dict`: imports a type alias used for dictionary-based data.
- `from db import Database`: imports the database wrapper.
- `from invoice import build_invoice_text`: imports a helper that formats invoice text.
- `class WarehouseApp:`: defines the main application class.
- `def __init__(self, root: tk.Tk, db: Database):`: initializes the app with the root window and database connection.
- `self.notebook = ttk.Notebook(root)`: creates a tabbed notebook widget.
- `self.notebook.add(...)`: adds tabs for customers, products, purchases, billing, and payments.
- `self._create_*_tab()`: helper methods that build each screen's layout.
- `ttk.Label`, `ttk.Entry`, `ttk.Button`: create labels, text boxes, and buttons.
- `.grid(...)` and `.pack(...)`: geometry managers that place widgets in the window.
- `self.customer_tree = ttk.Treeview(...)`: creates a table-like widget to display records.
- `self.customer_tree.bind("<<TreeviewSelect>>", ...)`: registers event handlers for selection changes.

## Event handling and form logic

- `add_customer`, `update_customer`, `delete_customer`: read widget values, validate them, and call database methods.
- `on_customer_selected`: reads the selected row from the tree and populates form fields.
- `refresh_customers`: reloads data from the database and updates both the tree and combobox values.
- `add_product`, `update_product`, `delete_product`: similar operations for products.
- `add_purchase`: stores purchase records and refreshes the purchase list.
- `add_bill`: validates customer/product selections, quantity, and stock before creating a bill.
- `on_bill_selected`: builds an invoice preview using `build_invoice_text` and displays it in a disabled text widget.
- `add_payment`: validates payment amount and records the payment through the database wrapper.

## Teaching notes

This file is useful for teaching:

- how to structure a Tkinter GUI with a main application class,
- how to create and arrange widgets with `ttk` and geometry managers,
- how to connect UI controls to database logic,
- and how to refresh the UI after data changes.
