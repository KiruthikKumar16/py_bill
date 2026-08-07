from django import forms

from .models import Bill, Customer, Payment, Product, Purchase


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (classes + " form-control").strip()


class CustomerForm(BootstrapModelForm):
    class Meta:
        model = Customer
        fields = ["name", "location", "phone_no", "gst"]
        widgets = {
            "location": forms.TextInput(attrs={"placeholder": "City / Address"}),
            "phone_no": forms.TextInput(attrs={"placeholder": "Mobile or landline"}),
            "gst": forms.TextInput(attrs={"placeholder": "GSTIN"}),
        }


class ProductForm(BootstrapModelForm):
    class Meta:
        model = Product
        fields = ["name", "date_of_purchase", "purchase_rate", "sale_rate", "quantity"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product name"}),
            "date_of_purchase": forms.DateInput(attrs={"type": "date"}),
            "purchase_rate": forms.NumberInput(attrs={"placeholder": "Purchase rate"}),
            "sale_rate": forms.NumberInput(attrs={"placeholder": "Sale rate"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "Starting quantity"}),
        }


class PurchaseForm(BootstrapModelForm):
    class Meta:
        model = Purchase
        fields = ["name", "location", "phone_no", "date"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Supplier or retailer name"}),
            "location": forms.TextInput(attrs={"placeholder": "Location"}),
            "phone_no": forms.TextInput(attrs={"placeholder": "Phone number"}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class BillForm(BootstrapModelForm):
    class Meta:
        model = Bill
        fields = ["date", "customer", "product", "quantity", "rate"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "Quantity to bill"}),
            "rate": forms.NumberInput(attrs={"placeholder": "Sale rate"}),
        }


class PaymentForm(BootstrapModelForm):
    class Meta:
        model = Payment
        fields = ["bill", "amount", "date"]
        widgets = {
            "amount": forms.NumberInput(attrs={"placeholder": "Payment amount"}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        bill = self.cleaned_data.get("bill")
        if amount is None or amount <= 0:
            raise forms.ValidationError("Enter a valid payment amount.")
        if bill and amount > bill.amount_due:
            raise forms.ValidationError("Payment amount cannot exceed the current due balance.")
        return amount
