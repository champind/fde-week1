import repository
from models import Invoice

def get_invoice_by_id(invoice_id: str) -> Invoice:
    invoice_data = repository.find_invoice_by_id(invoice_id)
    if invoice_data is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")
    return Invoice(**invoice_data)

def create_invoice(invoice: Invoice) -> Invoice:
    new_invoice = Invoice(invoice_data=invoice.dict())
    repository.add_invoice(new_invoice.dict())
    return new_invoice

def update_invoice(invoice_id: str, updated_invoice: Invoice) -> Invoice:
    existing_invoice = repository.get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")

def update_invoice(invoice_id: str, updated_data: dict) -> Invoice:
    existing_invoice = repository.get_invoice_by_id(invoice_id)
    if existing_invoice is None:
        raise ValueError(f"Invoice with ID {invoice_id} not found.")

    updated_invoice = {**existing_invoice, **updated_data}
    repository.update_invoice(invoice_id, updated_invoice.dict ())
    return Invoice(updated_invoice)
