# app.py

`app.py` is the legacy desktop application entry point for the warehouse management system.

## Overview

This module imports `tkinter` and the `Database` and `WarehouseApp` components from local modules.
It creates the database connection, builds the application window, and starts the event loop.

## Syntax explained

- `import tkinter as tk`: imports the Tkinter GUI library and aliases it as `tk`.
- `from db import Database`: imports the local `Database` wrapper class.
- `from ui import WarehouseApp`: imports the Tkinter user interface class.
- `def main():`: defines the main application bootstrap function.
- `database = Database()`: creates a database instance and opens the SQLite file.
- `root = tk.Tk()`: creates the root window for the Tkinter application.
- `app = WarehouseApp(root, database)`: initializes the UI with the window and database.
- `try: ... finally: database.close()`: ensures the database connection closes even if an error occurs.
- `if __name__ == "__main__": main()`: runs `main()` when the file is executed as a script.

## Responsibilities

- Opens the SQLite database.
- Instantiates the Tkinter root window.
- Creates the warehouse GUI application.
- Starts and manages the Tkinter event loop.
- Closes the database cleanly on exit.

## Teaching notes

This file is a simple example of application startup logic in Python and shows how to use `try/finally` for cleanup.
