"""
invoice_generator.py
=====================
Generates "Bill of Supply" invoice PDFs that follow the layout of the
Vinoth Traders template: double outer border, centered letterhead with
GSTIN, a buyer/invoice-meta strip, an itemised goods table, totals,
amount-in-words, and a signatory block.

Usage (as a library):

    from invoice_generator import InvoiceGenerator

    gen = InvoiceGenerator(seller_config="seller_config.json")
    gen.generate(invoice_data, "output/invoice_63.pdf")

See generate_invoice.py for the command-line interface.
"""

import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

try:
    from .words import amount_to_words
except ImportError:  # pragma: no cover - fallback for CLI execution
    from words import amount_to_words

PAGE_W, PAGE_H = A4


class InvoiceGenerator:
    def __init__(self, seller_config):
        """
        seller_config: path to a JSON file, or an already-loaded dict,
        describing the seller (see seller_config.json for the shape).
        """
        if isinstance(seller_config, str):
            with open(seller_config, "r", encoding="utf-8") as f:
                self.seller = json.load(f)
        else:
            self.seller = seller_config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(self, invoice, output_path):
        """
        invoice: dict matching the shape in sample_data/invoice_63.json
        output_path: where to write the .pdf
        """
        items = invoice["items"]
        for it in items:
            it["amount"] = round(float(it["qty"]) * float(it["rate"]), 2)
        total_qty = sum(float(it["qty"]) for it in items)
        total_amount = round(sum(it["amount"] for it in items), 2)

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        c = canvas.Canvas(output_path, pagesize=A4)

        self._draw_outer_border(c)
        y = self._draw_letterhead(c)
        y = self._draw_party_and_meta_strip(c, invoice, y)
        y = self._draw_items_table(c, items, total_qty, total_amount, y)
        self._draw_totals_and_footer(c, invoice, total_amount, y)

        c.save()
        return output_path

    # ------------------------------------------------------------------
    # Layout building blocks
    # ------------------------------------------------------------------
    MARGIN = 12 * mm
    INNER_GAP = 2.2 * mm

    def _outer_rect(self):
        m = self.MARGIN
        return m, m, PAGE_W - m, PAGE_H - m  # x0, y0, x1, y1

    def _draw_outer_border(self, c):
        x0, y0, x1, y1 = self._outer_rect()
        c.setLineWidth(1.1)
        c.rect(x0, y0, x1 - x0, y1 - y0)
        g = self.INNER_GAP
        c.setLineWidth(0.5)
        c.rect(x0 + g, y0 + g, (x1 - x0) - 2 * g, (y1 - y0) - 2 * g)

    def _draw_letterhead(self, c):
        seller = self.seller
        x0, y0, x1, y1 = self._outer_rect()
        pad = self.INNER_GAP + 3 * mm
        top = y1 - pad
        cx = (x0 + x1) / 2

        # start the company name a bit further from the inner border so its
        # cap-height doesn't touch the border line
        top -= 6

        # phone / cell, top-right
        c.setFont("Helvetica-Bold", 9)
        c.drawRightString(x1 - pad, top - 10, f"Ph : {seller.get('phone', '')}")
        c.drawRightString(x1 - pad, top - 22, f"Cell: {seller.get('cell', '')}")

        # optional logo, top-left
        logo_path = seller.get("logo_path")
        if logo_path and os.path.exists(logo_path):
            try:
                c.drawImage(
                    logo_path, x0 + pad, top - 70, width=60, height=60,
                    preserveAspectRatio=True, mask="auto",
                )
            except Exception:
                pass

        # optional symbol (e.g. swastik/om), top-right above phone block
        symbol_path = seller.get("symbol_path")
        if symbol_path and os.path.exists(symbol_path):
            try:
                c.drawImage(
                    symbol_path, x1 - pad - 45, top - 78, width=45, height=45,
                    preserveAspectRatio=True, mask="auto",
                )
            except Exception:
                pass

        y = top
        c.setFont("Helvetica-Bold", 17)
        c.drawCentredString(cx, y, seller.get("name", ""))
        y -= 20

        c.setFont("Helvetica", 11)
        for line in seller.get("address_lines", []):
            c.drawCentredString(cx, y, line)
            y -= 14

        y -= 2
        c.setFont("Helvetica", 10.5)
        c.drawCentredString(cx, y, f"GSTIN/UIN: {seller.get('gstin', '')}")
        y -= 14
        c.drawCentredString(
            cx, y,
            f"State Name : {seller.get('state_name', '')}, Code : {seller.get('state_code', '')}",
        )
        y -= 14
        if seller.get("email"):
            c.drawCentredString(cx, y, f"E-Mail : {seller['email']}")
            y -= 14

        y -= 6
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(cx, y, "BILL OF SUPPLY")
        y -= 10

        c.setLineWidth(0.8)
        c.line(x0 + self.INNER_GAP, y, x1 - self.INNER_GAP, y)
        return y

    def _wrap_text(self, c, text, font, size, max_width):
        """Greedy word-wrap; returns a list of lines that each fit max_width."""
        if not text:
            return [""]
        words = text.split()
        lines, current = [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if stringWidth(trial, font, size) <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _draw_party_and_meta_strip(self, c, invoice, y_top):
        x0, y0, x1, y1 = self._outer_rect()
        g = self.INNER_GAP
        pad = 3 * mm
        buyer = invoice["buyer"]
        mid_x = x0 + (x1 - x0) * 0.62
        buyer_col_width = (mid_x - pad) - (x0 + g + pad)

        # --- build wrapped buyer lines up front so we can size the strip ---
        buyer_lines = []  # list of (text, font, size)
        for line in self._wrap_text(c, buyer.get("name", ""), "Helvetica-Bold", 11, buyer_col_width):
            buyer_lines.append((line, "Helvetica-Bold", 11))
        for addr_line in buyer.get("address_lines", []):
            for line in self._wrap_text(c, addr_line, "Helvetica", 10, buyer_col_width):
                buyer_lines.append((line, "Helvetica", 10))
        if buyer.get("phone"):
            buyer_lines.append((buyer["phone"], "Helvetica", 10))
        if buyer.get("state_name"):
            for line in self._wrap_text(
                c, f"State Name & Code: {buyer['state_name']}-{buyer.get('state_code', '')}",
                "Helvetica", 10, buyer_col_width,
            ):
                buyer_lines.append((line, "Helvetica", 10))
        if buyer.get("gstin"):
            for line in self._wrap_text(c, f"GSTIN: {buyer['gstin']}", "Helvetica", 10, buyer_col_width):
                buyer_lines.append((line, "Helvetica", 10))

        meta_rows = [
            ("Invoice No", f": {invoice.get('invoice_no', '')}"),
            ("Date", f": {invoice.get('date', '')}"),
            ("Vehicle No", f": {invoice.get('vehicle_no', '')}"),
            ("Palce of Supply", f": {invoice.get('place_of_supply', '')}"),
            ("Bill Type", f": {invoice.get('bill_type', '')}"),
        ]

        line_h = 13
        content_h = max(len(buyer_lines) * line_h, len(meta_rows) * 15)
        strip_h = max(92, content_h + 20)  # 20 = top+bottom breathing room
        strip_bottom = y_top - strip_h

        # vertical divider between buyer box and meta box
        c.setLineWidth(0.6)
        c.line(mid_x, y_top, mid_x, strip_bottom)
        c.line(x0 + g, strip_bottom, x1 - g, strip_bottom)

        # --- left: buyer (Bill To) ---
        ty = y_top - 14
        tx = x0 + g + pad
        for text, font, size in buyer_lines:
            c.setFont(font, size)
            c.drawString(tx, ty, text)
            ty -= line_h

        # --- right: invoice meta ---
        my = y_top - 14
        label_x = mid_x + pad
        value_x = mid_x + 100
        c.setFont("Helvetica-Bold", 10.5)
        for label, value in meta_rows:
            c.drawString(label_x, my, label)
            c.drawString(value_x, my, value)
            my -= 15

        return strip_bottom

    def _draw_items_table(self, c, items, total_qty, total_amount, y_top):
        x0, y0, x1, y1 = self._outer_rect()
        g = self.INNER_GAP

        col_edges = self._col_edges(x0 + g, x1 - g)
        header_h = 18
        row_h = 16
        min_body_h = 170  # keeps the table roomy even with few items, like the source doc

        body_h = max(min_body_h, row_h * (len(items) + 1))
        table_top = y_top
        header_bottom = table_top - header_h
        body_bottom = header_bottom - body_h

        # outer table border
        c.setLineWidth(0.7)
        c.rect(x0 + g, body_bottom, (x1 - g) - (x0 + g), table_top - body_bottom)
        c.line(x0 + g, header_bottom, x1 - g, header_bottom)

        # column separators
        c.setLineWidth(0.5)
        for edge in col_edges[1:-1]:
            c.line(edge, body_bottom, edge, table_top)

        # header labels
        headers = ["S.No", "Description of Goods", "HSN Code", "Qty", "Rate", "Amount"]
        c.setFont("Helvetica-Bold", 9.5)
        for i, h in enumerate(headers):
            cx = (col_edges[i] + col_edges[i + 1]) / 2
            c.drawCentredString(cx, header_bottom + 5, h)

        # item rows
        c.setFont("Helvetica", 9.5)
        ry = header_bottom - 13
        for idx, it in enumerate(items, start=1):
            c.drawCentredString((col_edges[0] + col_edges[1]) / 2, ry, str(idx))
            c.drawString(col_edges[1] + 4, ry, it["description"])
            c.drawCentredString((col_edges[2] + col_edges[3]) / 2, ry, str(it.get("hsn_code", "") or ""))
            c.drawRightString(col_edges[4] - 4, ry, f"{float(it['qty']):.2f} {it.get('unit', '')}".strip())
            c.drawRightString(col_edges[5] - 4, ry, f"{float(it['rate']):.2f}")
            c.drawRightString(col_edges[6] - 4, ry, f"{it['amount']:,.2f}")
            ry -= row_h

        # end-of-list marker, centred in the description column near the bottom
        c.setFont("Helvetica-Oblique", 9)
        c.drawCentredString(
            (col_edges[1] + col_edges[2]) / 2, body_bottom + 6, "\u2666 End of List",
        )

        # totals row directly under the table
        totals_top = body_bottom
        totals_bottom = totals_top - row_h - 4
        c.setLineWidth(0.7)
        c.rect(x0 + g, totals_bottom, (x1 - g) - (x0 + g), totals_top - totals_bottom)
        for edge in (col_edges[1], col_edges[3], col_edges[4]):
            c.line(edge, totals_bottom, edge, totals_top)

        c.setFont("Helvetica-Bold", 10)
        c.drawString(col_edges[1] + 4, totals_bottom + 6, "Total")
        c.drawRightString(col_edges[4] - 4, totals_bottom + 6, f"{total_qty:,.2f} KG")
        c.drawRightString(col_edges[6] - 4, totals_bottom + 6, f"{total_amount:,.2f}")

        return totals_bottom

    def _col_edges(self, left, right):
        """Column boundaries for: S.No | Description | HSN | Qty | Rate | Amount"""
        width = right - left
        fractions = [0.06, 0.42, 0.14, 0.13, 0.12, 0.13]
        edges = [left]
        acc = left
        for f in fractions:
            acc += width * f
            edges.append(acc)
        edges[-1] = right
        return edges

    def _draw_totals_and_footer(self, c, invoice, total_amount, y_top):
        seller = self.seller
        x0, y0, x1, y1 = self._outer_rect()
        g = self.INNER_GAP
        pad = 3 * mm

        y = y_top - 16
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x0 + g + pad, y, "Amount Chargeable")
        c.drawRightString(x1 - g - pad, y, "E & OE")
        y -= 14

        c.setFont("Helvetica-Bold", 10.5)
        words = amount_to_words(total_amount, currency=invoice.get("currency", "INR"))
        c.drawString(x0 + g + pad, y, words)
        y -= 18

        c.line(x0 + g, y, x1 - g, y)
        y -= 16

        # left: bank details ; right: "For <Seller>" + signatory
        bank = seller.get("bank", {})
        c.setFont("Helvetica", 10)
        c.drawString(x0 + g + pad, y, f"Acc No: {bank.get('acc_no', '')}")
        c.setFont("Helvetica-Bold", 10.5)
        c.drawRightString(x1 - g - pad, y, f"For {seller.get('name', '')}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(x0 + g + pad, y, f"IFSC No: {bank.get('ifsc', '')}")

        y -= 34
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(x1 - g - pad, y, "Authorised Signatory")
