import json
from decimal import Decimal
from pathlib import Path

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BillForm, CustomerForm, PaymentForm, ProductForm, PurchaseForm
from .models import Bill, Customer, Payment, Product, Purchase
from invoice import number_to_words
from invoice_generator.invoice_generator import InvoiceGenerator


def dashboard(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    recent_bills = Bill.objects.select_related("customer", "product").order_by("-id")[:5]

    customer_count = customers.count()
    product_count = products.count()
    purchase_count = Purchase.objects.count()
    payment_count = Payment.objects.count()

    total_revenue = sum((bill.total_amount for bill in Bill.objects.all()), Decimal("0.00"))
    total_due = sum((bill.amount_due for bill in Bill.objects.all()), Decimal("0.00"))
    inventory_value = sum(
        (product.purchase_rate * product.quantity for product in products),
        Decimal("0.00"),
    )

    daily_sales = {}
    for bill in Bill.objects.select_related("customer", "product").order_by("date"):
        label = bill.date.strftime("%d %b")
        daily_sales[label] = daily_sales.get(label, Decimal("0.00")) + bill.total_amount

    sales_labels = list(daily_sales.keys())
    sales_values = [float(value) for value in daily_sales.values()]

    customer_totals = {}
    for bill in Bill.objects.select_related("customer"):
        customer_totals[bill.customer.name] = (
            customer_totals.get(bill.customer.name, Decimal("0.00")) + bill.total_amount
        )
    top_customers = sorted(customer_totals.items(), key=lambda item: item[1], reverse=True)[:5]

    stock_entries = Product.objects.order_by("-quantity")[:5]
    stock_labels = [product.name for product in stock_entries]
    stock_values = [product.quantity for product in stock_entries]

    return render(
        request,
        "inventory/dashboard.html",
        {
            "customer_count": customer_count,
            "product_count": product_count,
            "total_revenue": total_revenue,
            "total_due": total_due,
            "inventory_value": inventory_value,
            "recent_bills": recent_bills,
            "purchase_count": purchase_count,
            "payment_count": payment_count,
            "daily_sales_labels": json.dumps(sales_labels),
            "daily_sales_values": json.dumps(sales_values),
            "top_customers": top_customers,
            "stock_labels": json.dumps(stock_labels),
            "stock_values": json.dumps(stock_values),
        },
    )


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "inventory/customer_list.html", {"customers": customers})


def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Add Customer"})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Edit Customer"})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_confirm_delete.html", {"customer": customer, "title": "Delete Customer"})


def product_list(request):
    products = Product.objects.all()
    return render(request, "inventory/product_list.html", {"products": products})


def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_form.html", {"form": form, "title": "Add Product"})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_form.html", {"form": form, "title": "Edit Product"})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_confirm_delete.html", {"product": product, "title": "Delete Product"})


def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, "inventory/purchase_list.html", {"purchases": purchases})


def purchase_create(request):
    form = PurchaseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:purchase_list"))
    return render(request, "inventory/purchase_form.html", {"form": form, "title": "Add Purchase"})


def bill_list(request):
    bills = Bill.objects.select_related("customer", "product").all()
    return render(request, "inventory/bill_list.html", {"bills": bills})


def bill_create(request):
    form = BillForm(request.POST or None)
    if form.is_valid():
        bill = form.save(commit=False)
        if bill.quantity <= 0:
            form.add_error("quantity", "Quantity must be greater than zero.")
        elif bill.product.quantity < bill.quantity:
            form.add_error("quantity", "Not enough stock available for this product.")
        else:
            bill.save()
            return redirect(reverse("inventory:bill_list"))
    return render(
        request,
        "inventory/bill_form.html",
        {
            "form": form,
            "title": "Create Bill",
            "products": Product.objects.all(),
        },
    )


def bill_invoice(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    return render(
        request,
        "inventory/invoice.html",
        {
            "bill": bill,
            "amount_in_words": number_to_words(float(bill.total_amount)),
        },
    )


def payment_list(request):
    payments = Payment.objects.select_related("bill", "bill__customer").all()
    return render(request, "inventory/payment_list.html", {"payments": payments})


def payment_create(request):
    form = PaymentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("inventory:payment_list"))
    return render(request, "inventory/payment_form.html", {"form": form, "title": "Record Payment"})


def bill_invoice(request, pk):
    return bill_invoice_pdf(request, pk)


def bill_invoice_pdf(request, pk):
    bill = get_object_or_404(Bill, pk=pk)
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "invoice_generator" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"invoice_{bill.pk}.pdf"

    seller_config_path = base_dir / "invoice_generator" / "seller_config.json"
    invoice_data = {
        "invoice_no": str(bill.pk),
        "date": bill.date.strftime("%d-%m-%Y"),
        "vehicle_no": "",
        "place_of_supply": bill.customer.location or "N/A",
        "bill_type": "CASH",
        "currency": "INR",
        "buyer": {
            "name": bill.customer.name,
            "address_lines": [line for line in [bill.customer.location] if line],
            "phone": bill.customer.phone_no or "",
            "state_name": "",
            "state_code": "",
            "gstin": bill.customer.gst or "",
        },
        "items": [
            {
                "description": bill.product.name,
                "hsn_code": "",
                "qty": float(bill.quantity),
                "unit": "KG",
                "rate": float(bill.rate),
            }
        ],
    }

    generator = InvoiceGenerator(str(seller_config_path))
    generator.generate(invoice_data, str(output_path))

    response = HttpResponse(output_path.read_bytes(), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="invoice_{bill.pk}.pdf"'
    return response
