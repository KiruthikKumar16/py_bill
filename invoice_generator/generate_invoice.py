#!/usr/bin/env python3
"""
generate_invoice.py
====================
Command-line interface for the invoice generator.

Single invoice (from a JSON file):
    python3 generate_invoice.py --data sample_data/invoice_63.json

Batch mode (many invoices from one CSV, one row per line-item,
grouped by the "invoice_no" column -- see sample_data/batch_invoices.csv):
    python3 generate_invoice.py --batch sample_data/batch_invoices.csv

Custom seller letterhead / output folder:
    python3 generate_invoice.py --data invoice.json \
        --seller my_seller_config.json --out-dir output
"""

import argparse
import csv
import json
import os
import sys
from collections import OrderedDict

from invoice_generator import InvoiceGenerator


def load_json_invoice(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_batch_csv(path):
    """
    Groups CSV rows into invoices by the 'invoice_no' column.
    Buyer / invoice-meta fields are read from the first row seen for
    each invoice_no; every row contributes one line item.
    """
    invoices = OrderedDict()

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inv_no = row["invoice_no"].strip()
            if inv_no not in invoices:
                invoices[inv_no] = {
                    "invoice_no": inv_no,
                    "date": row.get("date", "").strip(),
                    "vehicle_no": row.get("vehicle_no", "").strip(),
                    "place_of_supply": row.get("place_of_supply", "").strip(),
                    "bill_type": row.get("bill_type", "").strip() or "CASH",
                    "buyer": {
                        "name": row.get("buyer_name", "").strip(),
                        "address_lines": [
                            l.strip() for l in row.get("buyer_address", "").split("|") if l.strip()
                        ],
                        "phone": row.get("buyer_phone", "").strip(),
                        "state_name": row.get("buyer_state_name", "").strip(),
                        "state_code": row.get("buyer_state_code", "").strip(),
                        "gstin": row.get("buyer_gstin", "").strip(),
                    },
                    "items": [],
                }

            invoices[inv_no]["items"].append({
                "description": row.get("description", "").strip(),
                "hsn_code": row.get("hsn_code", "").strip(),
                "qty": float(row.get("qty", 0) or 0),
                "unit": row.get("unit", "").strip(),
                "rate": float(row.get("rate", 0) or 0),
            })

    return list(invoices.values())


def main():
    parser = argparse.ArgumentParser(description="Generate Bill-of-Supply invoice PDFs.")
    parser.add_argument("--data", help="Path to a single invoice JSON file.")
    parser.add_argument("--batch", help="Path to a CSV of line items grouped by invoice_no.")
    parser.add_argument(
        "--seller", default="seller_config.json",
        help="Path to the seller/letterhead config JSON (default: seller_config.json).",
    )
    parser.add_argument(
        "--out-dir", default="output",
        help="Directory to write generated PDFs into (default: output).",
    )
    args = parser.parse_args()

    if not args.data and not args.batch:
        parser.error("Provide either --data <invoice.json> or --batch <invoices.csv>")

    gen = InvoiceGenerator(args.seller)
    os.makedirs(args.out_dir, exist_ok=True)

    if args.data:
        invoice = load_json_invoice(args.data)
        out_path = os.path.join(args.out_dir, f"invoice_{invoice.get('invoice_no', 'output')}.pdf")
        gen.generate(invoice, out_path)
        print(f"Generated: {out_path}")

    if args.batch:
        invoices = load_batch_csv(args.batch)
        if not invoices:
            print("No invoices found in CSV.", file=sys.stderr)
            sys.exit(1)
        for invoice in invoices:
            out_path = os.path.join(args.out_dir, f"invoice_{invoice['invoice_no']}.pdf")
            gen.generate(invoice, out_path)
            print(f"Generated: {out_path}")


if __name__ == "__main__":
    main()
