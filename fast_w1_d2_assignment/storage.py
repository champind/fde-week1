import json

from data_path_config import INVOICE_FILE


def load_invoices():
    with INVOICE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_invoices(invoices):
    INVOICE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with INVOICE_FILE.open("w", encoding="utf-8") as file:
        json.dump(invoices, file, indent=4)
