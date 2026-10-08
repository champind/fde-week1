from fastapi import FastAPI
from data_store import invoices

app = FastAPI()

@app.post("/invoices")
def create_invoice(invoice: dict):
    invoice_id = len(invoices) + 1
    invoice["id"] = invoice_id  
    inc