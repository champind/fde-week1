from fastapi import APIRouter, HTTPException

from models import Invoice
from storage import load_invoices, save_invoices

router = APIRouter()


@router.put("/invoices/{invoice_id}")
def update_invoice(invoice_id: str, updated_invoice: Invoice):
    invoices = load_invoices()

    for index, invoice in enumerate(invoices):
        if invoice.get("invoice_id") == invoice_id:
            invoice_data = updated_invoice.model_dump()
            invoice_data["invoice_id"] = invoice_id
            invoices[index] = invoice_data

            save_invoices(invoices)

            return {
                "message": "Invoice updated successfully",
                "invoice": invoice_data,
            }

    raise HTTPException(status_code=404, detail="Invoice not found")