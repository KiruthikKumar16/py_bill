import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict

from db import Database
from invoice import build_invoice_text


class WarehouseApp:
    def __init__(self, root: tk.Tk, db: Database):
        self.root = root
        self.db = db
        self.root.title("Warehouse Management and Billing")
        self.root.geometry("1100x700")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.customers_tab = ttk.Frame(self.notebook)
        self.products_tab = ttk.Frame(self.notebook)
        self.purchase_tab = ttk.Frame(self.notebook)
        self.bill_tab = ttk.Frame(self.notebook)
        self.payment_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.customers_tab, text="Customers")
        self.notebook.add(self.products_tab, text="Products")
        self.notebook.add(self.purchase_tab, text="Purchases")
        self.notebook.add(self.bill_tab, text="Billing")
        self.notebook.add(self.payment_tab, text="Payments")

        self._create_customer_tab()
        self._create_product_tab()
        self._create_purchase_tab()
        self._create_bill_tab()
        self._create_payment_tab()

        self.refresh_customers()
        self.refresh_products()
        self.refresh_purchases()
        self.refresh_bills()
        self.refresh_payments()

    def _create_customer_tab(self):
        left_frame = ttk.Frame(self.customers_tab, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = ttk.Frame(self.customers_tab, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.customer_name = ttk.Entry(left_frame, width=30)
        self.customer_name.grid(row=0, column=1, pady=4)

        ttk.Label(left_frame, text="Location:").grid(row=1, column=0, sticky=tk.W)
        self.customer_location = ttk.Entry(left_frame, width=30)
        self.customer_location.grid(row=1, column=1, pady=4)

        ttk.Label(left_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W)
        self.customer_phone = ttk.Entry(left_frame, width=30)
        self.customer_phone.grid(row=2, column=1, pady=4)

        ttk.Label(left_frame, text="GST:").grid(row=3, column=0, sticky=tk.W)
        self.customer_gst = ttk.Entry(left_frame, width=30)
        self.customer_gst.grid(row=3, column=1, pady=4)

        self.customer_id = None
        add_button = ttk.Button(left_frame, text="Add Customer", command=self.add_customer)
        update_button = ttk.Button(left_frame, text="Update Customer", command=self.update_customer)
        delete_button = ttk.Button(left_frame, text="Delete Customer", command=self.delete_customer)
        add_button.grid(row=4, column=0, pady=8)
        update_button.grid(row=4, column=1, pady=8)
        delete_button.grid(row=5, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.customer_tree = ttk.Treeview(right_frame, columns=("Name", "Location", "Phone", "GST"), show="headings", height=15)
        for heading in ["Name", "Location", "Phone", "GST"]:
            self.customer_tree.heading(heading, text=heading)
            self.customer_tree.column(heading, width=140)
        self.customer_tree.pack(fill=tk.BOTH, expand=True)
        self.customer_tree.bind("<<TreeviewSelect>>", self.on_customer_selected)

    def _create_product_tab(self):
        left_frame = ttk.Frame(self.products_tab, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = ttk.Frame(self.products_tab, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.product_name = ttk.Entry(left_frame, width=30)
        self.product_name.grid(row=0, column=1, pady=4)

        ttk.Label(left_frame, text="Purchase Rate:").grid(row=1, column=0, sticky=tk.W)
        self.product_purchase_rate = ttk.Entry(left_frame, width=30)
        self.product_purchase_rate.grid(row=1, column=1, pady=4)

        ttk.Label(left_frame, text="Sale Rate:").grid(row=2, column=0, sticky=tk.W)
        self.product_sale_rate = ttk.Entry(left_frame, width=30)
        self.product_sale_rate.grid(row=2, column=1, pady=4)

        ttk.Label(left_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W)
        self.product_quantity = ttk.Entry(left_frame, width=30)
        self.product_quantity.grid(row=3, column=1, pady=4)

        ttk.Label(left_frame, text="Purchase Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W)
        self.product_purchase_date = ttk.Entry(left_frame, width=30)
        self.product_purchase_date.grid(row=4, column=1, pady=4)

        self.product_id = None
        add_button = ttk.Button(left_frame, text="Add Product", command=self.add_product)
        update_button = ttk.Button(left_frame, text="Update Product", command=self.update_product)
        delete_button = ttk.Button(left_frame, text="Delete Product", command=self.delete_product)
        add_button.grid(row=5, column=0, pady=8)
        update_button.grid(row=5, column=1, pady=8)
        delete_button.grid(row=6, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.product_tree = ttk.Treeview(right_frame, columns=("Name", "Purchase Rate", "Sale Rate", "Quantity", "Purchase Date"), show="headings", height=15)
        for heading in ["Name", "Purchase Rate", "Sale Rate", "Quantity", "Purchase Date"]:
            self.product_tree.heading(heading, text=heading)
            self.product_tree.column(heading, width=120)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        self.product_tree.bind("<<TreeviewSelect>>", self.on_product_selected)

    def _create_purchase_tab(self):
        left_frame = ttk.Frame(self.purchase_tab, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = ttk.Frame(self.purchase_tab, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Retailer / Supplier Name:").grid(row=0, column=0, sticky=tk.W)
        self.purchase_name = ttk.Entry(left_frame, width=30)
        self.purchase_name.grid(row=0, column=1, pady=4)

        ttk.Label(left_frame, text="Location:").grid(row=1, column=0, sticky=tk.W)
        self.purchase_location = ttk.Entry(left_frame, width=30)
        self.purchase_location.grid(row=1, column=1, pady=4)

        ttk.Label(left_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W)
        self.purchase_phone = ttk.Entry(left_frame, width=30)
        self.purchase_phone.grid(row=2, column=1, pady=4)

        add_button = ttk.Button(left_frame, text="Add Purchase Record", command=self.add_purchase)
        add_button.grid(row=3, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.purchase_tree = ttk.Treeview(right_frame, columns=("Name", "Location", "Phone", "Date"), show="headings", height=18)
        for heading in ["Name", "Location", "Phone", "Date"]:
            self.purchase_tree.heading(heading, text=heading)
            self.purchase_tree.column(heading, width=180)
        self.purchase_tree.pack(fill=tk.BOTH, expand=True)

    def _create_bill_tab(self):
        left_frame = ttk.Frame(self.bill_tab, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = ttk.Frame(self.bill_tab, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Customer:").grid(row=0, column=0, sticky=tk.W)
        self.bill_customer = ttk.Combobox(left_frame, width=28, state="readonly")
        self.bill_customer.grid(row=0, column=1, pady=4)

        ttk.Label(left_frame, text="Product:").grid(row=1, column=0, sticky=tk.W)
        self.bill_product = ttk.Combobox(left_frame, width=28, state="readonly")
        self.bill_product.grid(row=1, column=1, pady=4)
        self.bill_product.bind("<<ComboboxSelected>>", self.on_bill_product_selected)

        ttk.Label(left_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W)
        self.bill_quantity = ttk.Entry(left_frame, width=30)
        self.bill_quantity.grid(row=2, column=1, pady=4)

        ttk.Label(left_frame, text="Rate (Sale Rate default):").grid(row=3, column=0, sticky=tk.W)
        self.bill_rate = ttk.Entry(left_frame, width=30)
        self.bill_rate.grid(row=3, column=1, pady=4)

        add_button = ttk.Button(left_frame, text="Create Bill", command=self.add_bill)
        add_button.grid(row=4, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.bill_tree = ttk.Treeview(right_frame, columns=("Bill ID", "Date", "Customer", "Product", "Qty", "Rate", "Total"), show="headings", height=10)
        for heading in ["Bill ID", "Date", "Customer", "Product", "Qty", "Rate", "Total"]:
            self.bill_tree.heading(heading, text=heading)
            self.bill_tree.column(heading, width=100)
        self.bill_tree.pack(fill=tk.BOTH, expand=True)
        self.bill_tree.bind("<<TreeviewSelect>>", self.on_bill_selected)

        preview_frame = ttk.LabelFrame(right_frame, text="Invoice Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.invoice_preview = tk.Text(preview_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.invoice_preview.pack(fill=tk.BOTH, expand=True)

    def _create_payment_tab(self):
        left_frame = ttk.Frame(self.payment_tab, padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        right_frame = ttk.Frame(self.payment_tab, padding=10)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(left_frame, text="Bill:").grid(row=0, column=0, sticky=tk.W)
        self.payment_bill = ttk.Combobox(left_frame, width=28, state="readonly")
        self.payment_bill.grid(row=0, column=1, pady=4)
        self.payment_bill.bind("<<ComboboxSelected>>", self.on_payment_bill_selected)

        ttk.Label(left_frame, text="Amount to Pay:").grid(row=1, column=0, sticky=tk.W)
        self.payment_amount = ttk.Entry(left_frame, width=30)
        self.payment_amount.grid(row=1, column=1, pady=4)

        self.payment_balance_label = ttk.Label(left_frame, text="Balance Due: INR 0.00")
        self.payment_balance_label.grid(row=2, column=0, columnspan=2, pady=4, sticky=tk.W)

        add_button = ttk.Button(left_frame, text="Record Payment", command=self.add_payment)
        add_button.grid(row=3, column=0, columnspan=2, pady=8, sticky=tk.EW)

        self.payment_tree = ttk.Treeview(right_frame, columns=("Payment ID", "Bill ID", "Amount", "Balance", "Date"), show="headings", height=16)
        for heading in ["Payment ID", "Bill ID", "Amount", "Balance", "Date"]:
            self.payment_tree.heading(heading, text=heading)
            self.payment_tree.column(heading, width=120)
        self.payment_tree.pack(fill=tk.BOTH, expand=True)

    def add_customer(self):
        name = self.customer_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Customer name is required.")
            return
        self.db.add_customer(name, self.customer_location.get().strip(), self.customer_phone.get().strip(), self.customer_gst.get().strip())
        self.clear_customer_form()
        self.refresh_customers()

    def update_customer(self):
        if not self.customer_id:
            messagebox.showwarning("Selection", "Choose a customer to update.")
            return
        name = self.customer_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Customer name is required.")
            return
        self.db.update_customer(self.customer_id, name, self.customer_location.get().strip(), self.customer_phone.get().strip(), self.customer_gst.get().strip())
        self.clear_customer_form()
        self.refresh_customers()

    def delete_customer(self):
        if not self.customer_id:
            messagebox.showwarning("Selection", "Choose a customer to delete.")
            return
        self.db.delete_customer(self.customer_id)
        self.clear_customer_form()
        self.refresh_customers()

    def on_customer_selected(self, event):
        selected = self.customer_tree.selection()
        if not selected:
            return
        values = self.customer_tree.item(selected[0], "values")
        self.customer_id = int(self.customer_tree.item(selected[0], "text"))
        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, values[0])
        self.customer_location.delete(0, tk.END)
        self.customer_location.insert(0, values[1])
        self.customer_phone.delete(0, tk.END)
        self.customer_phone.insert(0, values[2])
        self.customer_gst.delete(0, tk.END)
        self.customer_gst.insert(0, values[3])

    def clear_customer_form(self):
        self.customer_id = None
        self.customer_name.delete(0, tk.END)
        self.customer_location.delete(0, tk.END)
        self.customer_phone.delete(0, tk.END)
        self.customer_gst.delete(0, tk.END)

    def refresh_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        customers = self.db.get_customers()
        for customer in customers:
            self.customer_tree.insert("", tk.END, text=str(customer["Customer_ID"]), values=(customer["Name"], customer["Location"], customer["Phone_No"], customer["GST"]))
        customer_options = [f"{c['Customer_ID']} - {c['Name']}" for c in customers]
        self.bill_customer["values"] = customer_options
        self.refresh_payment_bill_combobox()

    def add_product(self):
        name = self.product_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Product name is required.")
            return
        try:
            purchase_rate = float(self.product_purchase_rate.get().strip() or 0)
            sale_rate = float(self.product_sale_rate.get().strip() or 0)
            quantity = int(self.product_quantity.get().strip() or 0)
        except ValueError:
            messagebox.showwarning("Validation", "Enter numeric values for rates and quantity.")
            return
        self.db.add_product(name, purchase_rate, sale_rate, quantity, self.product_purchase_date.get().strip() or None)
        self.clear_product_form()
        self.refresh_products()

    def update_product(self):
        if not self.product_id:
            messagebox.showwarning("Selection", "Choose a product to update.")
            return
        try:
            purchase_rate = float(self.product_purchase_rate.get().strip() or 0)
            sale_rate = float(self.product_sale_rate.get().strip() or 0)
            quantity = int(self.product_quantity.get().strip() or 0)
        except ValueError:
            messagebox.showwarning("Validation", "Enter numeric values for rates and quantity.")
            return
        self.db.update_product(self.product_id, self.product_name.get().strip(), purchase_rate, sale_rate, quantity, self.product_purchase_date.get().strip() or "")
        self.clear_product_form()
        self.refresh_products()

    def delete_product(self):
        if not self.product_id:
            messagebox.showwarning("Selection", "Choose a product to delete.")
            return
        self.db.delete_product(self.product_id)
        self.clear_product_form()
        self.refresh_products()

    def on_product_selected(self, event):
        selected = self.product_tree.selection()
        if not selected:
            return
        self.product_id = int(self.product_tree.item(selected[0], "text"))
        values = self.product_tree.item(selected[0], "values")
        self.product_name.delete(0, tk.END)
        self.product_name.insert(0, values[0])
        self.product_purchase_rate.delete(0, tk.END)
        self.product_purchase_rate.insert(0, values[1])
        self.product_sale_rate.delete(0, tk.END)
        self.product_sale_rate.insert(0, values[2])
        self.product_quantity.delete(0, tk.END)
        self.product_quantity.insert(0, values[3])
        self.product_purchase_date.delete(0, tk.END)
        self.product_purchase_date.insert(0, values[4])

    def clear_product_form(self):
        self.product_id = None
        self.product_name.delete(0, tk.END)
        self.product_purchase_rate.delete(0, tk.END)
        self.product_sale_rate.delete(0, tk.END)
        self.product_quantity.delete(0, tk.END)
        self.product_purchase_date.delete(0, tk.END)

    def refresh_products(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        products = self.db.get_products()
        for product in products:
            self.product_tree.insert("", tk.END, text=str(product["Product_ID"]), values=(product["Name"], f"{product['Purchase_Rate']:.2f}", f"{product['Sale_Rate']:.2f}", product["Quantity"], product["Date_of_Purchase"]))
        product_options = [f"{p['Product_ID']} - {p['Name']}" for p in products]
        self.bill_product["values"] = product_options
        self.refresh_payment_bill_combobox()

    def add_purchase(self):
        name = self.purchase_name.get().strip()
        if not name:
            messagebox.showwarning("Validation", "Purchase name is required.")
            return
        self.db.add_purchase(name, self.purchase_location.get().strip(), self.purchase_phone.get().strip())
        self.purchase_name.delete(0, tk.END)
        self.purchase_location.delete(0, tk.END)
        self.purchase_phone.delete(0, tk.END)
        self.refresh_purchases()

    def refresh_purchases(self):
        for item in self.purchase_tree.get_children():
            self.purchase_tree.delete(item)
        purchases = self.db.get_purchases()
        for purchase in purchases:
            self.purchase_tree.insert("", tk.END, values=(purchase["Name"], purchase["Location"], purchase["Phone_No"], purchase["Date"]))

    def add_bill(self):
        customer_selection = self.bill_customer.get().strip()
        product_selection = self.bill_product.get().strip()
        if not customer_selection or not product_selection:
            messagebox.showwarning("Validation", "Select a customer and a product.")
            return
        try:
            quantity = int(self.bill_quantity.get().strip())
            rate = float(self.bill_rate.get().strip())
        except ValueError:
            messagebox.showwarning("Validation", "Enter numeric values for quantity and rate.")
            return
        customer_id = int(customer_selection.split(" - ")[0])
        product_id = int(product_selection.split(" - ")[0])
        product = self.db.get_product_by_id(product_id)
        if product is None:
            messagebox.showwarning("Validation", "Selected product not found.")
            return
        if quantity <= 0:
            messagebox.showwarning("Validation", "Quantity must be greater than zero.")
            return
        if product["Quantity"] < quantity:
            messagebox.showwarning("Stock", "Not enough stock available for this product.")
            return
        self.db.add_bill(customer_id, product_id, quantity, rate)
        self.bill_quantity.delete(0, tk.END)
        self.bill_rate.delete(0, tk.END)
        self.refresh_bills()
        self.refresh_products()
        self.refresh_payment_bill_combobox()

    def refresh_bills(self):
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        bills = self.db.get_bills()
        for bill in bills:
            total = bill["Quantity"] * bill["Rate"]
            self.bill_tree.insert(
                "",
                tk.END,
                text=str(bill["Bill_ID"]),
                values=(bill["Bill_ID"], bill["Date"], bill.get("CustomerName", ""), bill.get("ProductName", ""), bill["Quantity"], f"{bill['Rate']:.2f}", f"{total:.2f}"),
            )

    def on_bill_selected(self, event):
        selected = self.bill_tree.selection()
        if not selected:
            return
        bill_id = int(self.bill_tree.item(selected[0], "text"))
        bill = self.db.get_bill_by_id(bill_id)
        if not bill:
            return
        customer = self.db.get_customer_by_id(bill["Customer_ID"])
        product = self.db.get_product_by_id(bill["Product_ID"])
        balance = self.db.get_balance_for_bill(bill_id)
        invoice_text = build_invoice_text(bill, customer, product, balance)
        self.invoice_preview.configure(state=tk.NORMAL)
        self.invoice_preview.delete("1.0", tk.END)
        self.invoice_preview.insert(tk.END, invoice_text)
        self.invoice_preview.configure(state=tk.DISABLED)

    def on_bill_product_selected(self, event):
        selection = self.bill_product.get().strip()
        if not selection:
            return
        product_id = int(selection.split(" - ")[0])
        product = self.db.get_product_by_id(product_id)
        if product:
            self.bill_rate.delete(0, tk.END)
            self.bill_rate.insert(0, f"{product['Sale_Rate']:.2f}")

    def refresh_payment_bill_combobox(self):
        bills = self.db.get_bills()
        bill_options = [f"{b['Bill_ID']} - {b.get('CustomerName', '')} - {b.get('ProductName', '')}" for b in bills]
        self.payment_bill["values"] = bill_options

    def on_payment_bill_selected(self, event):
        selection = self.payment_bill.get().strip()
        if not selection:
            return
        bill_id = int(selection.split(" - ")[0])
        balance = self.db.get_balance_for_bill(bill_id)
        self.payment_balance_label.configure(text=f"Balance Due: ₹ {balance:.2f}")

    def add_payment(self):
        selection = self.payment_bill.get().strip()
        if not selection:
            messagebox.showwarning("Validation", "Select a bill to pay.")
            return
        try:
            amount = float(self.payment_amount.get().strip())
        except ValueError:
            messagebox.showwarning("Validation", "Enter a valid payment amount.")
            return
        bill_id = int(selection.split(" - ")[0])
        balance_before = self.db.get_balance_for_bill(bill_id)
        if amount <= 0:
            messagebox.showwarning("Validation", "Amount must be greater than zero.")
            return
        if amount > balance_before:
            messagebox.showwarning("Validation", "Payment amount cannot exceed the due balance.")
            return
        self.db.add_payment(bill_id, amount)
        self.payment_amount.delete(0, tk.END)
        self.refresh_payments()
        self.on_payment_bill_selected(None)
        self.on_bill_selected(None)

    def refresh_payments(self):
        for item in self.payment_tree.get_children():
            self.payment_tree.delete(item)
        payments = self.db.get_payments()
        for payment in payments:
            self.payment_tree.insert(
                "",
                tk.END,
                values=(payment["Payment_ID"], payment["Bill_ID"], f"{payment['Amount']:.2f}", f"{payment['Balance']:.2f}", payment["Date"]),
            )

    def run(self):
        self.root.mainloop()
