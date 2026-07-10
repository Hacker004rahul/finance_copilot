from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, computed_field


Currency = Literal["USD"]
InvoiceStatus = Literal["paid", "pending", "overdue"]
ExpenseStatus = Literal["approved", "pending", "rejected", "reimbursed"]


class Invoice(BaseModel):
    invoice_id: str = Field(..., pattern=r"^INV-\d{4}$")
    vendor: str = Field(..., min_length=2, max_length=80)
    amount: float = Field(..., gt=0, le=1_000_000)
    currency: Currency = "USD"
    category: str = Field(..., min_length=2, max_length=50)
    issue_date: date
    due_date: date
    status: InvoiceStatus


class Expense(BaseModel):
    expense_id: str = Field(..., pattern=r"^EXP-\d{4}$")
    employee: str = Field(..., min_length=2, max_length=80)
    department: str = Field(..., min_length=2, max_length=50)
    amount: float = Field(..., gt=0, le=50_000)
    category: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=8, max_length=240)
    submitted_date: date
    status: ExpenseStatus


class Vendor(BaseModel):
    vendor_id: str = Field(..., pattern=r"^VEN-\d{3}$")
    name: str = Field(..., min_length=2, max_length=80)
    category: str = Field(..., min_length=2, max_length=50)
    payment_terms: str = Field(..., min_length=4, max_length=60)
    contact_email: EmailStr


class EmiCalculationInput(BaseModel):
    principal: float = Field(..., gt=0, le=100_000_000)
    annual_rate_percent: float = Field(..., ge=0, le=100)
    tenure_months: int = Field(..., ge=1, le=480)


class EmiCalculationOutput(BaseModel):
    monthly_emi: float = Field(..., ge=0)
    total_payment: float = Field(..., ge=0)
    total_interest: float = Field(..., ge=0)


class InvoiceLookupInput(BaseModel):
    invoice_id: str = Field(..., pattern=r"^INV-\d{4}$")


class InvoiceLookupOutput(BaseModel):
    found: bool
    invoice: Invoice | None = None
    message: str = Field(..., min_length=1)

    @computed_field
    @property
    def status(self) -> str | None:
        return self.invoice.status if self.invoice else None


class SourceChunk(BaseModel):
    source: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    score: float = Field(..., ge=0)


class ChatResponse(BaseModel):
    answer: str = Field(..., min_length=1)
    sources: list[SourceChunk] = Field(default_factory=list)
    tools_used: list[str] = Field(default_factory=list)
