from fastapi import APIRouter, HTTPException

from storage import load_invoices, save_invoices

router = APIRouter()


@router.delete("/invoices/{invoice_id}")
def delete_invoice(invoice_id: str):
    invoices = load_invoices()

    remaining = [invoice for invoice in invoices if invoice.get("invoice_id") != invoice_id]

    if len(remaining) == len(invoices):
        raise HTTPException(status_code=404, detail="Invoice not found")

    save_invoices(remaining)

    return {"message": "Invoice deleted successfully", "invoice_id": invoice_id}
