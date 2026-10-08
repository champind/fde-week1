from fastapi import APIRouter

from models import Invoice
from storage import load_invoices, save_invoices

router = APIRouter()


@router.post("/invoices")
def create_invoice(invoice: Invoice):

    invoices = load_invoices()

    invoices.append(invoice.model_dump())

    save_invoices(invoices)

    return {
        "message": "Invoice created successfully",
        "invoice": invoice,
    }
