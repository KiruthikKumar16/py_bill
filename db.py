import sqlite3
from datetime import date
from typing import Dict, List, Optional

DB_PATH = "warehouse.db"


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


class Database:
    def __init__(self, path: str = DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = dict_factory
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Customer (
                Customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Location TEXT,
                Phone_No TEXT,
                GST TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Product (
                Product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Date_of_Purchase TEXT,
                Purchase_Rate REAL,
                Sale_Rate REAL,
                Quantity INTEGER DEFAULT 0
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Purchase (
                Purchase_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Location TEXT,
                Phone_No TEXT,
                Date TEXT
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Bill (
                Bill_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT NOT NULL,
                Customer_ID INTEGER NOT NULL,
                Product_ID INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                Rate REAL NOT NULL,
                FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
                FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Payments (
                Payment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Bill_ID INTEGER NOT NULL,
                Amount REAL NOT NULL,
                Balance REAL NOT NULL,
                Date TEXT,
                FOREIGN KEY (Bill_ID) REFERENCES Bill(Bill_ID)
            );
            """
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    # Customer helpers
    def add_customer(self, name: str, location: str, phone: str, gst: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Customer (Name, Location, Phone_No, GST) VALUES (?, ?, ?, ?)",
            (name, location, phone, gst),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_customers(self) -> List[Dict]:
        return self.conn.execute("SELECT * FROM Customer ORDER BY Customer_ID").fetchall()

    def update_customer(self, customer_id: int, name: str, location: str, phone: str, gst: str):
        self.conn.execute(
            "UPDATE Customer SET Name = ?, Location = ?, Phone_No = ?, GST = ? WHERE Customer_ID = ?",
            (name, location, phone, gst, customer_id),
        )
        self.conn.commit()

    def delete_customer(self, customer_id: int):
        self.conn.execute("DELETE FROM Customer WHERE Customer_ID = ?", (customer_id,))
        self.conn.commit()

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        return self.conn.execute("SELECT * FROM Customer WHERE Customer_ID = ?", (customer_id,)).fetchone()

    # Product helpers
    def add_product(self, name: str, purchase_rate: float, sale_rate: float, quantity: int, date_of_purchase: Optional[str] = None) -> int:
        if date_of_purchase is None:
            date_of_purchase = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Product (Name, Date_of_Purchase, Purchase_Rate, Sale_Rate, Quantity) VALUES (?, ?, ?, ?, ?)",
            (name, date_of_purchase, purchase_rate, sale_rate, quantity),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_products(self) -> List[Dict]:
        return self.conn.execute("SELECT * FROM Product ORDER BY Product_ID").fetchall()

    def update_product(self, product_id: int, name: str, purchase_rate: float, sale_rate: float, quantity: int, date_of_purchase: str):
        self.conn.execute(
            "UPDATE Product SET Name = ?, Date_of_Purchase = ?, Purchase_Rate = ?, Sale_Rate = ?, Quantity = ? WHERE Product_ID = ?",
            (name, date_of_purchase, purchase_rate, sale_rate, quantity, product_id),
        )
        self.conn.commit()

    def delete_product(self, product_id: int):
        self.conn.execute("DELETE FROM Product WHERE Product_ID = ?", (product_id,))
        self.conn.commit()

    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        return self.conn.execute("SELECT * FROM Product WHERE Product_ID = ?", (product_id,)).fetchone()

    def change_product_quantity(self, product_id: int, quantity_change: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE Product SET Quantity = Quantity + ? WHERE Product_ID = ?",
            (quantity_change, product_id),
        )
        self.conn.commit()

    # Purchase helpers
    def add_purchase(self, name: str, location: str, phone: str, purchase_date: Optional[str] = None) -> int:
        if purchase_date is None:
            purchase_date = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Purchase (Name, Location, Phone_No, Date) VALUES (?, ?, ?, ?)",
            (name, location, phone, purchase_date),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_purchases(self) -> List[Dict]:
        return self.conn.execute("SELECT * FROM Purchase ORDER BY Purchase_ID").fetchall()

    # Bill helpers
    def add_bill(self, customer_id: int, product_id: int, quantity: int, rate: float, bill_date: Optional[str] = None) -> int:
        if bill_date is None:
            bill_date = date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Bill (Date, Customer_ID, Product_ID, Quantity, Rate) VALUES (?, ?, ?, ?, ?)",
            (bill_date, customer_id, product_id, quantity, rate),
        )
        bill_id = cursor.lastrowid
        self.conn.commit()
        self.change_product_quantity(product_id, -quantity)
        return bill_id

    def get_bills(self) -> List[Dict]:
        return self.conn.execute(
            "SELECT b.*, c.Name AS CustomerName, p.Name AS ProductName "
            "FROM Bill b "
            "LEFT JOIN Customer c ON b.Customer_ID = c.Customer_ID "
            "LEFT JOIN Product p ON b.Product_ID = p.Product_ID "
            "ORDER BY b.Bill_ID"
        ).fetchall()

    def get_bill_by_id(self, bill_id: int) -> Optional[Dict]:
        return self.conn.execute("SELECT * FROM Bill WHERE Bill_ID = ?", (bill_id,)).fetchone()

    # Payment helpers
    def add_payment(self, bill_id: int, amount: float, payment_date: Optional[str] = None) -> int:
        if payment_date is None:
            payment_date = date.today().isoformat()
        current_balance = self.get_balance_for_bill(bill_id)
        new_balance = max(0.0, current_balance - amount)
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Payments (Bill_ID, Amount, Balance, Date) VALUES (?, ?, ?, ?)",
            (bill_id, amount, new_balance, payment_date),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_payments(self) -> List[Dict]:
        return self.conn.execute("SELECT * FROM Payments ORDER BY Payment_ID").fetchall()

    def get_payments_for_bill(self, bill_id: int) -> List[Dict]:
        return self.conn.execute("SELECT * FROM Payments WHERE Bill_ID = ? ORDER BY Payment_ID", (bill_id,)).fetchall()

    def get_total_paid_for_bill(self, bill_id: int) -> float:
        result = self.conn.execute("SELECT SUM(Amount) AS total FROM Payments WHERE Bill_ID = ?", (bill_id,)).fetchone()
        return float(result["total"] or 0.0)

    def get_amount_due_for_bill(self, bill_id: int) -> float:
        bill = self.get_bill_by_id(bill_id)
        if not bill:
            return 0.0
        total = bill["Quantity"] * bill["Rate"]
        paid = self.get_total_paid_for_bill(bill_id)
        return max(0.0, total - paid)

    def get_balance_for_bill(self, bill_id: int) -> float:
        return self.get_amount_due_for_bill(bill_id)

    def get_next_bill_id(self) -> int:
        row = self.conn.execute("SELECT MAX(Bill_ID) AS max_id FROM Bill").fetchone()
        return int(row["max_id"] or 0) + 1
