"""
Convert a rupee amount (with optional paise) into words using the
Indian numbering system (Thousand / Lakh / Crore), e.g.:

    25565.00  -> "Twenty Five Thousand Five Hundred Sixty Five Only"
    150000.50 -> "One Lakh Fifty Thousand Only and Fifty Paise"

No external dependencies -- pure Python.
"""

_ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]
_TENS = [
    "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety",
]


def _two_digits(n: int) -> str:
    if n < 20:
        return _ONES[n]
    tens, ones = divmod(n, 10)
    return (_TENS[tens] + (" " + _ONES[ones] if ones else "")).strip()


def _three_digits(n: int) -> str:
    hundreds, rest = divmod(n, 100)
    parts = []
    if hundreds:
        parts.append(f"{_ONES[hundreds]} Hundred")
    if rest:
        parts.append(_two_digits(rest))
    return " ".join(parts)


def _int_to_indian_words(n: int) -> str:
    if n == 0:
        return "Zero"

    crore, n = divmod(n, 10_000_000)
    lakh, n = divmod(n, 100_000)
    thousand, n = divmod(n, 1_000)
    hundred = n

    parts = []
    if crore:
        parts.append(f"{_int_to_indian_words(crore)} Crore")
    if lakh:
        parts.append(f"{_two_digits(lakh) if lakh < 100 else _int_to_indian_words(lakh)} Lakh")
    if thousand:
        parts.append(f"{_two_digits(thousand) if thousand < 100 else _int_to_indian_words(thousand)} Thousand")
    if hundred:
        parts.append(_three_digits(hundred))

    return " ".join(parts).strip()


def amount_to_words(amount, currency="INR") -> str:
    """
    Render a currency amount as words, Indian-invoice style.
    e.g. amount_to_words(25565.00) -> "INR Twenty Five Thousand Five Hundred Sixty Five Only"
    """
    amount = round(float(amount) + 1e-9, 2)
    rupees = int(amount)
    paise = int(round((amount - rupees) * 100))

    words = _int_to_indian_words(rupees) + " Only"
    if paise:
        words += f" and {_two_digits(paise)} Paise"

    prefix = f"{currency} " if currency else ""
    return prefix + words


if __name__ == "__main__":
    # quick self-test against the sample invoice total
    assert amount_to_words(25565.00) == "INR Twenty Five Thousand Five Hundred Sixty Five Only"
    print(amount_to_words(25565.00))
    print(amount_to_words(1234567.89))
    print(amount_to_words(100))
    print(amount_to_words(0))
