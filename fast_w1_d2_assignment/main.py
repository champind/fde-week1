from fastapi import FastAPI


from router.get_invoice import router as get_invoice_router
from router.create_invoice import router as create_invoice_router
from router.delete_invoice import router as delete_invoice_router
from router.put_invoice import router as put_invoice_router

app = FastAPI()

app.include_router(get_invoice_router)
app.include_router(create_invoice_router)
app.include_router(delete_invoice_router)
app.include_router(put_invoice_router)