from typing import Callable, TypeVar

from fastapi import APIRouter, HTTPException

from models import PaymentCreate, PaymentUpdate
from service import (
    EmptyPaymentUpdateError,
    InvoiceNotFoundError,
    PaymentNotFoundError,
    create_payment as create_payment_service,
    delete_payment as delete_payment_service,
    get_payment as get_payment_service,
    get_payments as get_payments_service,
    update_payment as update_payment_service,
)

router = APIRouter(prefix="/payments", tags=["Payments"])
Result = TypeVar("Result")


def call_service(
    operation: Callable[[], Result],
    error_message: str,
) -> Result:
    try:
        return operation()
    except PaymentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        ) from exc
    except InvoiceNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except EmptyPaymentUpdateError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except (OSError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail=f"{error_message}: {exc}",
        ) from exc


@router.get("/")
def get_payments():
    return call_service(
        get_payments_service,
        "Unable to read payments",
    )


@router.get("/{payment_id}")
def get_payment(payment_id: int):
    return call_service(
        lambda: get_payment_service(payment_id),
        "Unable to read payment",
    )


@router.post("/", status_code=201)
def create_payment(payment_data: PaymentCreate):
    payment = call_service(
        lambda: create_payment_service(payment_data),
        "Unable to create payment",
    )
    return {
        "message": "Payment created successfully",
        "payment": payment,
    }


@router.put("/{payment_id}")
def update_payment(payment_id: int, payment_data: PaymentUpdate):
    payment = call_service(
        lambda: update_payment_service(payment_id, payment_data),
        "Unable to update payment",
    )
    return {
        "message": "Payment updated successfully",
        "payment": payment,
    }


@router.delete("/{payment_id}")
def delete_payment(payment_id: int):
    payment = call_service(
        lambda: delete_payment_service(payment_id),
        "Unable to delete payment",
    )
    return {
        "message": "Payment deleted successfully",
        "payment": payment,
    }
