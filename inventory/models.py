from datetime import date
from decimal import Decimal

from django.db import models
from django.db.models import Sum


class Customer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    phone_no = models.CharField(max_length=15, blank=True)
    gst = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    date_of_purchase = models.DateField(null=True, blank=True)
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200, blank=True)
    phone_no = models.CharField(max_length=15, blank=True)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name} ({self.date})"


class Bill(models.Model):
    date = models.DateField(default=date.today)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bills")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bills")
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-date", "id"]

    def __str__(self):
        return f"Bill #{self.id} - {self.customer.name}"

    @property
    def total_amount(self):
        return self.quantity * self.rate

    @property
    def amount_paid(self):
        total = self.payments.aggregate(total=Sum("amount"))["total"]
        return total or Decimal("0.00")

    @property
    def amount_due(self):
        return max(Decimal("0.00"), self.total_amount - self.amount_paid)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and self.quantity:
            stored_product = self.product
            if stored_product.quantity < self.quantity:
                raise ValueError("Not enough stock available for this product.")
            stored_product.quantity -= self.quantity
            stored_product.save()
        super().save(*args, **kwargs)


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ["-date", "id"]

    def __str__(self):
        return f"Payment #{self.id} for Bill #{self.bill_id}"

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")
        unpaid = self.bill.amount_due
        if self.amount > unpaid:
            raise ValueError("Payment amount cannot exceed the due balance.")
        self.balance = unpaid - self.amount
        super().save(*args, **kwargs)
