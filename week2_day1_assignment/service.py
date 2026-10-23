from data_store import load_invoices, load_payments, save_payments
from models import Payment, PaymentCreate, PaymentUpdate


class PaymentNotFoundError(Exception):
    pass


class InvoiceNotFoundError(Exception):
    pass


class EmptyPaymentUpdateError(Exception):
    pass


def get_payment_index(payments: list[dict], payment_id: int) -> int | None:
    for index, payment in enumerate(payments):
        if payment["payment_id"] == payment_id:
            return index
    return None


def next_payment_id(payments: list[dict]) -> int:
    return max(
        (payment["payment_id"] for payment in payments),
        default=0,
    ) + 1


def check_invoice_exists(invoice_id: str) -> None:
    invoices = load_invoices()

    if not any(
        invoice.get("invoice_id") == invoice_id
        for invoice in invoices
    ):
        raise InvoiceNotFoundError(f"Invoice {invoice_id} not found")


def get_payments() -> list[dict]:
    return load_payments()


def get_payment(payment_id: int) -> dict:
    payments = load_payments()
    index = get_payment_index(payments, payment_id)

    if index is None:
        raise PaymentNotFoundError
    return payments[index]


def create_payment(payment_data: PaymentCreate) -> Payment:
    check_invoice_exists(payment_data.invoice_id)
    payments = load_payments()

    new_payment = Payment(
        payment_id=next_payment_id(payments),
        invoice_id=payment_data.invoice_id,
        paid=payment_data.paid,
    )
    payments.append(new_payment.model_dump())
    save_payments(payments)
    return new_payment


def update_payment(payment_id: int, payment_data: PaymentUpdate) -> Payment:
    payments = load_payments()
    index = get_payment_index(payments, payment_id)

    if index is None:
        raise PaymentNotFoundError

    changes = payment_data.model_dump(exclude_unset=True)
    if not changes:
        raise EmptyPaymentUpdateError(
            "Provide at least one field to update"
        )

    if "invoice_id" in changes:
        check_invoice_exists(changes["invoice_id"])

    updated = payments[index].copy()
    updated.update(changes)
    validated = Payment(**updated)
    payments[index] = validated.model_dump()
    save_payments(payments)
    return validated


def delete_payment(payment_id: int) -> dict:
    payments = load_payments()
    index = get_payment_index(payments, payment_id)

    if index is None:
        raise PaymentNotFoundError

    deleted = payments.pop(index)
    save_payments(payments)
    return deleted
