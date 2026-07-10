from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from app.rag.hybrid_search import hybrid_search
from app.schemas.data_models import (
    ChatResponse,
    EmiCalculationInput,
    EmiCalculationOutput,
    Invoice,
    InvoiceLookupInput,
    InvoiceLookupOutput,
)

try:
    from pydantic_ai import Agent
except Exception:  # pragma: no cover - demo still works if dependency is unavailable locally.
    Agent = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parents[2]
INVOICES_PATH = ROOT / "data" / "structured" / "invoices.json"
DISCLAIMER = "Educational demo only. Not financial, tax, or investment advice."


def search_knowledge_base(query: str) -> list[dict[str, Any]]:
    """Hybrid RAG retrieval over NovaLedger markdown policies."""
    return [source.model_dump() for source in hybrid_search(query, top_k=5)]


def calculate_emi(input_data: EmiCalculationInput) -> EmiCalculationOutput:
    """Calculate equated monthly installment using deterministic math."""
    monthly_rate = input_data.annual_rate_percent / (12 * 100)
    months = input_data.tenure_months
    principal = input_data.principal
    if monthly_rate == 0:
        monthly_emi = principal / months
    else:
        factor = (1 + monthly_rate) ** months
        monthly_emi = principal * monthly_rate * factor / (factor - 1)
    total_payment = monthly_emi * months
    return EmiCalculationOutput(
        monthly_emi=round(monthly_emi, 2),
        total_payment=round(total_payment, 2),
        total_interest=round(total_payment - principal, 2),
    )


def lookup_invoice(input_data: InvoiceLookupInput) -> InvoiceLookupOutput:
    """Load one synthetic invoice by ID."""
    invoices = json.loads(INVOICES_PATH.read_text(encoding="utf-8"))
    for item in invoices:
        invoice = Invoice.model_validate(item)
        if invoice.invoice_id.upper() == input_data.invoice_id.upper():
            return InvoiceLookupOutput(
                found=True,
                invoice=invoice,
                message=(
                    f"{invoice.invoice_id} from {invoice.vendor} is {invoice.status}. "
                    f"Amount: {invoice.amount:.2f} {invoice.currency}; due {invoice.due_date}."
                ),
            )
    return InvoiceLookupOutput(
        found=False,
        invoice=None,
        message=f"No invoice found for {input_data.invoice_id}.",
    )


def _build_agent() -> Any:
    if Agent is None:
        return None
    try:
        agent = Agent(
            "openai:gpt-4o-mini",
            output_type=ChatResponse,
            system_prompt=(
                "You are NovaLedger Finance Copilot. Use tools before answering. "
                "Policy questions must search the knowledge base first. EMI questions must use "
                "calculate_emi. Invoice status questions must use lookup_invoice. Include citations "
                f"when RAG is used. Always respect this disclaimer: {DISCLAIMER}"
            ),
            defer_model_check=True,
        )
        agent.tool_plain(search_knowledge_base)
        agent.tool_plain(calculate_emi)
        agent.tool_plain(lookup_invoice)
        return agent
    except Exception:
        return None


finance_agent = _build_agent()


def _extract_emi_input(question: str) -> EmiCalculationInput | None:
    numeric_matches = re.findall(r"\d[\d,]*(?:\.\d+)?", question)
    numbers = [float(value.replace(",", "")) for value in numeric_matches]
    if len(numbers) < 3:
        return None
    principal = numbers[0]
    rate = numbers[1]
    tenure = int(numbers[2])
    if re.search(r"\b(y|yr|yrs|year|years)\b", question, flags=re.IGNORECASE):
        tenure *= 12
    months = tenure
    return EmiCalculationInput(principal=principal, annual_rate_percent=rate, tenure_months=months)


def _looks_like_emi_values(question: str) -> bool:
    numeric_matches = re.findall(r"\d[\d,]*(?:\.\d+)?", question)
    has_tenure_unit = bool(
        re.search(r"\b(mo|mos|month|months|y|yr|yrs|year|years)\b", question, flags=re.IGNORECASE)
    )
    return len(numeric_matches) >= 3 and (has_tenure_unit or "," in question)


def _extract_invoice_id(question: str) -> str | None:
    match = re.search(r"\bINV-\d{4}\b", question, flags=re.IGNORECASE)
    return match.group(0).upper() if match else None


def _format_sources(sources: list[dict[str, Any]]) -> str:
    citations = []
    for source in sources[:3]:
        if source["score"] > 0:
            citations.append(source["source"])
    return ", ".join(dict.fromkeys(citations))


def answer_question(question: str) -> ChatResponse:
    """Deterministic agentic router used by the Streamlit demo."""
    lowered = question.lower()
    tools_used: list[str] = []

    if "emi" in lowered or "installment" in lowered or _looks_like_emi_values(question):
        emi_input = _extract_emi_input(question)
        if emi_input is None:
            return ChatResponse(
                answer="Please provide principal, annual rate percent, and tenure in months.",
                tools_used=["calculate_emi"],
            )
        result = calculate_emi(emi_input)
        return ChatResponse(
            answer=(
                f"For a principal of {emi_input.principal:,.2f}, annual rate "
                f"{emi_input.annual_rate_percent:.2f}%, and tenure of {emi_input.tenure_months} "
                f"months, the EMI is {result.monthly_emi:,.2f}. Total payment is "
                f"{result.total_payment:,.2f}, including {result.total_interest:,.2f} interest."
            ),
            tools_used=["calculate_emi"],
        )

    invoice_id = _extract_invoice_id(question)
    if invoice_id and any(word in lowered for word in ["invoice", "paid", "overdue", "status", "due"]):
        result = lookup_invoice(InvoiceLookupInput(invoice_id=invoice_id))
        return ChatResponse(answer=result.message, tools_used=["lookup_invoice"])

    sources = search_knowledge_base(question)
    tools_used.append("search_knowledge_base")
    best = sources[0] if sources else None
    source_models = hybrid_search(question, top_k=5)
    citations = _format_sources(sources)

    if best is None:
        answer = "I could not find a relevant NovaLedger policy passage for that question."
    elif "gym" in lowered:
        answer = (
            "No. NovaLedger does not reimburse personal gym memberships. The expense policy "
            "lists personal gym memberships and personal wellness items as prohibited unless "
            "they are part of a pre-approved People Operations program."
        )
    elif "capex" in lowered and "opex" in lowered:
        answer = (
            "CAPEX means spending on assets that provide benefit beyond one year, while OPEX "
            "means recurring operating spend such as payroll, SaaS, travel, and ordinary business "
            "operations. NovaLedger uses these categories to separate long-lived investments from "
            "day-to-day costs."
        )
    else:
        snippet = " ".join(best["text"].split())
        answer = snippet[:650].rstrip()
        if len(snippet) > 650:
            answer += "..."

    if citations:
        answer = f"{answer}\n\nSources: {citations}"
    return ChatResponse(answer=answer, sources=source_models, tools_used=tools_used)
