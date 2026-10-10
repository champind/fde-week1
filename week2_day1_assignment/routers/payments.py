
from fastapi import APIRouter, HTTPException
from models import Payment, PaymentCreate, PaymentUpdate
from data_store import load_payments, save_payments, load_invoices

router = APIRouter(prefix="/payments", tags=["Payments"])


def get_payment_index(payments, payment_id):
    for index, payment in enumerate(payments):
        if payment["payment_id"] == payment_id:
            return index

    return None


def next_payment_id(payments):
    return max(
        (payment["payment_id"] for payment in payments),
        default=0
    ) + 1


def check_invoice_exists(invoice_id):
    invoices = load_invoices()

    if not any(
        invoice.get("invoice_id") == invoice_id
        for invoice in invoices
    ):
        raise HTTPException(
            status_code=404,
            detail=f"Invoice {invoice_id} not found"
        )


# GET: return all payments
@router.get("/")
def get_payments():
    try:
        return load_payments()
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to read payments: {exc}"
        ) from exc


# GET: return one payment
@router.get("/{payment_id}")
def get_payment(payment_id: int):
    payments = load_payments()
    index = get_payment_index(payments, payment_id)

    if index is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payments[index]


# POST: create a payment
@router.post("/", status_code=201)
def create_payment(payment_data: PaymentCreate):
    try:
        check_invoice_exists(payment_data.invoice_id)

        payments = load_payments()

        new_payment = Payment(
            payment_id=next_payment_id(payments),
            invoice_id=payment_data.invoice_id,
            paid=payment_data.paid
        )

        payments.append(new_payment.model_dump())
        save_payments(payments)

        return {
            "message": "Payment created successfully",
            "payment": new_payment
        }

    except HTTPException:
        raise
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create payment: {exc}"
        ) from exc


# PUT: update a payment
@router.put("/{payment_id}")
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate
):
    try:
        payments = load_payments()
        index = get_payment_index(payments, payment_id)

        if index is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        changes = payment_data.model_dump(exclude_unset=True)

        if not changes:
            raise HTTPException(
                status_code=400,
                detail="Provide at least one field to update"
            )

        if "invoice_id" in changes:
            check_invoice_exists(changes["invoice_id"])

        updated = payments[index].copy()
        updated.update(changes)

        # Validate the complete updated record.
        validated = Payment(**updated)
        payments[index] = validated.model_dump()

        save_payments(payments)

        return {
            "message": "Payment updated successfully",
            "payment": validated
        }

    except HTTPException:
        raise
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to update payment: {exc}"
        ) from exc


# DELETE: remove a payment
@router.delete("/{payment_id}")
def delete_payment(payment_id: int):
    try:
        payments = load_payments()
        index = get_payment_index(payments, payment_id)

        if index is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found"
            )

        deleted = payments.pop(index)
        save_payments(payments)

        return {
            "message": "Payment deleted successfully",
            "payment": deleted
        }

    except HTTPException:
        raise
    except (ValueError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to delete payment: {exc}"
        ) from exc
