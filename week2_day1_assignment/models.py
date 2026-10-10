
from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    invoice_id: str = Field(min_length=1)
    paid: float = Field(ge=0)


class Payment(PaymentCreate):
    payment_id: int = Field(gt=0)


class PaymentUpdate(BaseModel):
    invoice_id: str | None = Field(default=None, min_length=1)
    paid: float | None = Field(default=None, ge=0)
