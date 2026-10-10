from fastapi import FastAPI, HTTPException
from models import Invoice
from service import get_invoice_by_id, create_invoice, update_invoice

app = FastAPI()

@app.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: str):
    try:
        invoice = get_invoice_by_id(invoice_id)
        return invoice
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 

@app.post("/invoices", response_model=Invoice)
def create_new_invoice(invoice: Invoice):   
    new_invoice = create_invoice(invoice)
    return new_invoice              

@app.put("/invoices/{invoice_id}", response_model=Invoice)
def update_existing_invoice(invoice_id: str, updated_invoice: Invoice):
    try:
        updated_invoice = update_invoice(invoice_id, updated_invoice)
        return updated_invoice
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
