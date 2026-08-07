from typing import Dict


def format_currency(value: float) -> str:
    return f"INR {value:,.2f}"


def _three_digit_to_words(value: int) -> str:
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    if value == 0:
        return ""
    if value < 20:
        return ones[value]
    if value < 100:
        return tens[value // 10] + (" " + ones[value % 10] if value % 10 else "")
    return ones[value // 100] + " Hundred" + (" " + _three_digit_to_words(value % 100) if value % 100 else "")


def number_to_words(amount: float) -> str:
    integer_part = int(amount)
    fraction_part = int(round((amount - integer_part) * 100))
    if integer_part == 0:
        words = "Zero"
    else:
        units = ["", "Thousand", "Lakh", "Crore"]
        parts = []
        divisor = 1000
        temp = integer_part
        unit_index = 0

        while temp > 0:
            part = temp % divisor
            if part:
                parts.append((_three_digit_to_words(part) + (" " + units[unit_index] if units[unit_index] else "")).strip())
            temp //= divisor
            if unit_index == 0:
                divisor = 100
            else:
                divisor = 1000
            unit_index += 1

        words = " ".join(reversed(parts)).strip()

    rupees = f"{words} Rupees"
    paise = f" and {fraction_part:02d}/100 Paise" if fraction_part else ""
    return (rupees + paise + " Only").strip()


def build_invoice_text(bill: Dict, customer: Dict, product: Dict, balance: float) -> str:
    if not bill or not customer or not product:
        return "Select a bill, customer, and product to view the invoice."

    total_amount = bill["Quantity"] * bill["Rate"]
    amount_in_words = number_to_words(total_amount)

    lines = [
        "VINOTH TRADERS",
        "5D, Bolden Puram, 2nd Street, Tuticorin",
        "GSTIN/UIN: BZSPS5243K1ZQ",
        "State Name: Tamil Nadu, Code: 33",
        "",
        f"Invoice No: {bill['Bill_ID']}",
        f"Date: {bill['Date']}",
        f"Customer: {customer['Name']}",
        f"Customer Location: {customer['Location']}",
        f"Customer Phone: {customer['Phone_No']}",
        f"Customer GST: {customer['GST']}",
        "",
        "Description of Goods:",
        f"  {product['Name']}",
        "",
        f"Quantity: {bill['Quantity']}",
        f"Rate: {format_currency(bill['Rate'])}",
        f"Amount: {format_currency(total_amount)}",
        "",
        f"Amount Chargeable (in words): {amount_in_words}",
        f"Balance Due: {format_currency(balance)}",
    ]
    return "\n".join(lines)
