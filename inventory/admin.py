from django.contrib import admin

from .models import Bill, Customer, Payment, Product, Purchase


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "phone_no", "gst")
    search_fields = ("name", "gst", "phone_no")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sale_rate", "quantity", "date_of_purchase")
    search_fields = ("name",)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "phone_no", "date")
    search_fields = ("name", "location")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "customer", "product", "quantity", "rate")
    list_filter = ("date",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "bill", "amount", "balance", "date")
    list_filter = ("date",)
