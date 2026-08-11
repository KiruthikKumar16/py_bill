import json
from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import BillForm, CustomerForm, PaymentForm, ProductForm, PurchaseForm
from .models import Bill, Customer, Payment, Product, Purchase
from invoice import number_to_words, build_invoice_text


def dashboard(request):
    products = Product.objects.all()
    bills = Bill.objects.select_related("customer", "product").order_by("-date", "-id")

    daily_sales = {}
    customer_totals = {}
    for bill in reversed(list(bills)):
        label = bill.date.strftime("%b %d")
        daily_sales[label] = daily_sales.get(label, Decimal("0.00")) + bill.total_amount
        customer_totals[bill.customer.name] = customer_totals.get(bill.customer.name, Decimal("0.00")) + bill.total_amount

    total_revenue = sum(b.total_amount for b in bills)
    total_due = sum(b.amount_due for b in bills)
    inventory_value = sum(p.quantity * p.sale_rate for p in products)
    top_products = products.order_by("-quantity")[:5]
    top_customers = sorted(customer_totals.items(), key=lambda item: item[1], reverse=True)[:5]
    recent_bills = bills[:5]

    return render(
        request,
        "inventory/dashboard.html",
        {
            "customer_count": Customer.objects.count(),
            "product_count": products.count(),
            "purchase_count": Purchase.objects.count(),
            "bill_count": bills.count(),
            "payment_count": Payment.objects.count(),
            "total_revenue": total_revenue,
            "inventory_value": inventory_value,
            "total_due": total_due,
            "top_products": top_products,
            "top_customers": top_customers,
            "recent_bills": recent_bills,
            "daily_sales_labels": json.dumps(list(daily_sales.keys())),
            "daily_sales_values": json.dumps([float(value) for value in daily_sales.values()]),
            "stock_labels": json.dumps([p.name for p in top_products]),
            "stock_values": json.dumps([p.quantity for p in top_products]),
        },
    )


def customer_list(request):
    return render(request, "inventory/customer_list.html", {"customers": Customer.objects.all()})


def customer_create(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Add Customer"})


def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_form.html", {"form": form, "title": "Edit Customer"})


def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect(reverse("inventory:customer_list"))
    return render(request, "inventory/customer_confirm_delete.html", {"customer": customer})


def product_list(request):
    return render(request, "inventory/product_list.html", {"products": Product.objects.all()})


def product_create(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_form.html", {"form": form, "title": "Add Product"})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_form.html", {"form": form, "title": "Edit Product"})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect(reverse("inventory:product_list"))
    return render(request, "inventory/product_confirm_delete.html", {"product": product})


def purchase_list(request):
    return render(request, "inventory/purchase_list.html", {"purchases": Purchase.objects.all()})


def purchase_create(request):
    form = PurchaseForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("inventory:purchase_list"))
    return render(request, "inventory/purchase_form.html", {"form": form, "title": "Add Purchase"})


def bill_list(request):
    return render(request, "inventory/bill_list.html", {"bills": Bill.objects.select_related("customer", "product").all()})


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
    # prepare simple dicts for the invoice helper
    bill_dict = {
        "Bill_ID": bill.id,
        "Date": bill.date.strftime("%d-%m-%Y") if hasattr(bill, "date") else str(bill.date),
        "Quantity": float(bill.quantity),
        "Rate": float(bill.rate),
    }
    customer_dict = {
        "Name": bill.customer.name,
        "Location": bill.customer.location,
        "Phone_No": bill.customer.phone_no,
        "GST": bill.customer.gst,
    }
    product_dict = {"Name": bill.product.name}

    invoice_text = build_invoice_text(bill_dict, customer_dict, product_dict, float(bill.amount_due))

    return render(
        request,
        "inventory/invoice.html",
        {
            "bill": bill,
            "amount_in_words": number_to_words(float(bill.total_amount)),
            "invoice_text": invoice_text,
        },
    )


def payment_list(request):
    return render(request, "inventory/payment_list.html", {"payments": Payment.objects.select_related("bill").all()})


def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save(commit=False)
        payment.save()
        return redirect(reverse("inventory:payment_list"))
    return render(request, "inventory/payment_form.html", {"form": form, "title": "Record Payment"})
