
from fastapi import FastAPI
from routers.payments import router as payments_router

app = FastAPI(
    title="Invoice and Payments API",
    description="CRUD operations for invoice payments",
    version="1.0.0"
)

app.include_router(payments_router)


@app.get("/")
def home():
    return {
        "message": "Invoice and Payments API is running"
    }
