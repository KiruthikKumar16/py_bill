import json
from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import SimpleTestCase

from invoice_generator.invoice_generator import InvoiceGenerator


class InvoiceGeneratorTests(SimpleTestCase):
    def test_generates_pdf_from_sample_invoice(self):
        base_dir = Path(__file__).resolve().parent.parent
        seller_config_path = base_dir / 'invoice_generator' / 'seller_config.json'
        invoice_data_path = base_dir / 'invoice_generator' / 'sample_data' / 'invoice_63.json'

        with TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / 'invoice.pdf'
            generator = InvoiceGenerator(str(seller_config_path))
            generator.generate(json.loads(invoice_data_path.read_text(encoding='utf-8')), str(output_path))

            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)
