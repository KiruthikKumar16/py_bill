# Invoice Generator (Bill of Supply)

Generates PDF invoices that reproduce the layout of the **Vinoth Traders**
"Bill of Supply" template: double outer border, centered GSTIN letterhead,
buyer/invoice-meta strip, itemised goods table, totals, amount-in-words,
and a signatory block.

```
invoice_generator/
├── invoice_generator.py     # InvoiceGenerator class — draws the PDF
├── words.py                 # Number → Indian-style words (Lakh/Crore) for "Amount Chargeable"
├── generate_invoice.py      # Command-line interface (single + batch)
├── seller_config.json       # Your letterhead: name, address, GSTIN, bank details, logo
├── sample_data/
│   ├── invoice_63.json      # Recreates the original sample invoice exactly
│   └── batch_invoices.csv   # Example for generating several invoices at once
└── output/                  # Generated PDFs land here
```

## Install

```bash
pip install -r requirements.txt
```

## 1. Set up your letterhead once

Edit `seller_config.json` with your business details:

```json
{
  "name": "VINOTH TRADERS",
  "address_lines": ["5D, Bolden Puram,", "2nd Street,", "Tuticorin."],
  "phone": "04612320926",
  "cell": "9842130011",
  "gstin": "BZSPS5243K1ZQ",
  "state_name": "Tamil Nadu",
  "state_code": "33",
  "email": "vinothtraders@gmail.com",
  "bank": { "acc_no": "", "ifsc": "" },
  "logo_path": null,
  "symbol_path": null
}
```

> The original invoice's email was printed as `vinothetradersgmail.com` (missing
> the `@`), and this project assumes that was a scan/print typo — double check
> and correct it here.

`logo_path` / `symbol_path` are optional paths to PNG/JPG files (e.g. your
Ganesha logo and swastik/om mark). Leave them as `null` to omit — nothing is
drawn in their place, so the letterhead still looks clean without them.

## 2. Generate a single invoice

Create a JSON file describing the buyer, invoice details, and line items
(see `sample_data/invoice_63.json`), then run:

```bash
python3 generate_invoice.py --data sample_data/invoice_63.json
```

This writes `output/invoice_63.pdf`. Amount, total, and the "Amount
Chargeable ... Only" line are all calculated automatically from `qty × rate`.

### Invoice JSON shape

```json
{
  "invoice_no": "63",
  "date": "25-5-2022",
  "vehicle_no": "",
  "place_of_supply": "",
  "bill_type": "CREDIT",
  "buyer": {
    "name": "S.K.A.PRASANNA TRADING COMPANY",
    "address_lines": ["THENI"],
    "phone": "9443052770",
    "state_name": "Tamil Nadu",
    "state_code": "33",
    "gstin": "33ADTFS0016J1Z1"
  },
  "items": [
    { "description": "THUVARAM PARUPPU", "hsn_code": "", "qty": 250.00, "unit": "KG", "rate": 102.26 }
  ]
}
```

Add as many objects to `items` as you need — the table and "End of List"
marker resize automatically.

## 3. Generate many invoices at once (batch mode)

Put one row per line item in a CSV, using the same `invoice_no` for rows
that belong to the same invoice (see `sample_data/batch_invoices.csv`).
Use `|` inside `buyer_address` to separate multiple address lines.

```bash
python3 generate_invoice.py --batch sample_data/batch_invoices.csv
```

This produces one PDF per distinct `invoice_no`, e.g. `output/invoice_64.pdf`,
`output/invoice_65.pdf`, ...

## Other options

```bash
python3 generate_invoice.py --data invoice.json \
    --seller my_seller_config.json \
    --out-dir output
```

- `--seller` — use a different letterhead config
- `--out-dir` — change where PDFs are written

## Using it from your own code

```python
import json
from invoice_generator import InvoiceGenerator

gen = InvoiceGenerator("seller_config.json")
invoice = json.load(open("sample_data/invoice_63.json"))
gen.generate(invoice, "output/invoice_63.pdf")
```

## Notes

- This reproduces a **Bill of Supply** (no tax columns), matching the
  source document. If you need a GST **Tax Invoice** with CGST/SGST/IGST
  columns instead, the table-drawing code in `_draw_items_table` is the
  place to add those columns.
- Amounts are converted to words using the Indian numbering system
  (Thousand / Lakh / Crore) in `words.py`, with no external dependencies.
