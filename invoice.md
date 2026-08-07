# invoice.py

`invoice.py` contains helper functions that build a human-readable invoice preview from bill, customer, and product data.

## Overview

This module defines functions to format currency, convert numbers to words, and assemble the final invoice text.
It separates presentation logic from the database and user interface code.

## Syntax explained

- `from typing import Dict`: imports the dictionary type alias for type annotations.
- `def format_currency(value: float) -> str:`: defines a helper that formats a number as Indian rupees using an f-string.
- `def _three_digit_to_words(value: int) -> str:`: internal helper that converts numbers from 0 to 999 into English words.
- `ones = [...]` and `tens = [...]`: lists of word mappings for single-digit and tens-digit values.
- `if value < 20: return ones[value]`: handles the special cases for numbers below 20.
- `return ones[value // 100] + " Hundred" + ...`: assembles the wording for hundreds.
- `def number_to_words(amount: float) -> str:`: converts a numeric amount into a full Rupees-and-Paise phrase.
- `integer_part = int(amount)`: extracts the whole rupee amount.
- `fraction_part = int(round((amount - integer_part) * 100))`: computes paise as two decimal digits.
- `while temp > 0: ...`: loops to split the integer part into thousands, lakhs, and crores.
- `def build_invoice_text(bill: Dict, customer: Dict, product: Dict, balance: float) -> str:`: builds the multiline invoice string.
- `if not bill or not customer or not product: return ...`: returns a placeholder if required data is missing.
- `lines = [...]`: assembles the invoice header, customer details, item description, totals, and balance.
- `return "\n".join(lines)`: joins the lines into a final text block.

## Teaching notes

This module is helpful for teaching:

- how to keep formatting logic separate from storage and UI,
- how to work with Python string formatting and f-strings,
- how to translate numeric values into words,
- and how helper functions can make invoice generation easier to test and maintain.
