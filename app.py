import tkinter as tk

from db import Database
from ui import WarehouseApp


def main():
    database = Database()
    root = tk.Tk()
    app = WarehouseApp(root, database)
    try:
        app.run()
    finally:
        database.close()


if __name__ == "__main__":
    main()
