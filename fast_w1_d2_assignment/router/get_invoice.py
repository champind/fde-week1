from fastapi import APIRouter, HTTPException

from storage import load_invoices

router = APIRouter()


@router.get("/invoices")
def get_invoices():
    return load_invoices()


@router.get("/invoices/{invoice_id}")
def get_invoice(invoice_id: str):
    invoices = load_invoices()
    for invoice in invoices:
        if invoice.get("invoice_id") == invoice_id:
            return invoice
    raise HTTPException(status_code=404, detail="Invoice not found")
