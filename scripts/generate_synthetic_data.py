from __future__ import annotations

import json
import random
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.schemas.data_models import Expense, Invoice, Vendor


KB_DIR = ROOT / "data" / "kb"
STRUCTURED_DIR = ROOT / "data" / "structured"
RANDOM_SEED = 42
COMPANY = "NovaLedger Inc."


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")


def build_expense_policy() -> str:
    return f"""
# {COMPANY} Expense Policy

This policy explains how employees of {COMPANY}, a fictional cloud-finance software
company, should spend company funds and request reimbursement. The policy is designed for
training and demo purposes only, but the numbers are intentionally specific so the Finance
Copilot can answer questions with citations.

## Core principles

Every expense must have a clear business purpose, a dated receipt, and a cost center. The
employee who makes the purchase owns the first review: before submitting an expense, confirm
that the amount is reasonable, the category is correct, and the description tells Finance why
the cost helped NovaLedger. Expenses must be submitted in LedgerLoop within 10 calendar days
of the purchase date. Finance closes the monthly reimbursement batch at 5:00 p.m. Pacific on
the third business day of the following month.

## Approval limits

Individual contributor expenses up to 250 USD may be approved by the employee's direct
manager. Expenses from 250.01 USD to 1,000 USD require director approval. Expenses from
1,000.01 USD to 5,000 USD require the department vice president and Finance Operations.
Anything above 5,000 USD requires the CFO, Priya Raman, before the purchase is made. Splitting
one purchase into multiple claims to avoid an approval limit is prohibited. Emergency spending
is allowed only when delaying the purchase would interrupt a customer launch, payroll,
security response, or legally required filing; the employee must add "emergency spend" in the
description and attach written manager approval.

## Reimbursement rules

Approved employee reimbursements are paid on the 7th and 22nd of each month. If either date
falls on a weekend or NovaLedger holiday, payment moves to the next business day. Claims
approved by 12:00 p.m. Pacific two business days before a reimbursement run are included in
that run. Claims approved after the cutoff roll forward. A missing receipt delays payment
unless the amount is under 25 USD and the employee signs the missing receipt declaration.
Currency conversion uses the corporate card processor rate on the transaction date.

## SaaS and software

All software subscriptions must be requested through the SaaS intake form before purchase.
Managers may approve team SaaS trials up to 90 USD per user per month for a maximum of three
months. Annual subscriptions require Procurement review because NovaLedger tracks renewal
risk centrally. Security tools, data tools, and finance systems also require review from the
Security Operations lead, Mateo Chen. Employees may not expense duplicate tools when an
approved company tool already exists. Examples of approved tools include CloudBoard for
project management, SynapseSheets for spreadsheet collaboration, and AuthTower for identity
testing. Personal productivity apps, personal AI subscriptions, consumer storage accounts,
and unapproved browser extensions are not reimbursable.

## Travel

Business travel must be booked through TripHarbor unless Finance grants an exception. Economy
airfare is standard for flights under six hours. Premium economy may be used for flights of
six hours or more with director approval. Hotels are reimbursable up to 260 USD per night in
standard cities and 340 USD per night in high-cost cities such as San Francisco, New York,
London, Singapore, and Zurich. Ground transport should use shared rides, rail, or standard
rideshare. Daily meal reimbursement is capped at 75 USD, split as 18 USD for breakfast, 22 USD
for lunch, and 35 USD for dinner. Alcohol is reimbursable only at approved customer events and
must be itemized separately. Laundry is reimbursable after five consecutive nights of company
travel, capped at 40 USD per trip.

## Customer events and team meals

Customer meals require the customer name, company, attendee list, and business topic. The
standard customer meal cap is 95 USD per person including tax and tip. Internal team meals are
allowed for quarterly planning, all-day onsite workshops, or incident retrospectives lasting
more than four hours. Internal meals are capped at 35 USD per person. Celebratory meals for
birthdays, farewells, or morale events are paid from department engagement budgets and must
not be submitted as ordinary travel expenses.

## Prohibited expenses

NovaLedger does not reimburse personal gym memberships, home furniture without an approved
remote-work accommodation, commuting costs, traffic fines, minibar charges, movies, personal
streaming services, gift cards over 50 USD, political donations, charitable donations made in
an employee's name, pet care, childcare, clothing that is not branded event apparel, or
upgrades chosen for personal preference. The company also does not reimburse expenses that are
illegal, unsafe, discriminatory, or inconsistent with the Code of Conduct. Personal wellness
items, including yoga classes and meditation app subscriptions, are not reimbursable unless
they are part of a pre-approved People Operations program.

## Corporate cards

Corporate cards are issued to employees who travel at least twice per quarter or manage
approved recurring vendor spend. Cardholders must upload receipts within five business days.
A card transaction over 1,500 USD without a receipt triggers an automatic card hold after
seven days. Repeated late documentation may result in card suspension. Corporate cards may
not be used for cash advances, personal purchases, or peer-to-peer transfers.

## Exceptions

Exceptions are rare and must be requested before spending. The request must name the policy
section, amount, vendor, date, business reason, and approving executive. Finance Operations
keeps exception records for seven years. When a policy question is unclear, employees should
ask finance-ops@novaledger.example before buying. Finance may reject an expense even if a
manager approved it when the claim lacks documentation or violates this policy.
"""


def build_glossary() -> str:
    terms = {
        "APR": "Annual percentage rate, the yearly cost of borrowing expressed as a percentage.",
        "EMI": "Equated monthly installment, the fixed payment made each month on a loan.",
        "COGS": "Cost of goods sold, direct costs required to deliver NovaLedger subscriptions.",
        "OPEX": "Operating expenditure used for recurring business operations such as payroll and SaaS.",
        "CAPEX": "Capital expenditure for assets that provide benefit beyond one year.",
        "Gross margin": "Revenue minus COGS, divided by revenue.",
        "Net margin": "Net income divided by revenue after all costs and taxes.",
        "Runway": "Months the company can operate at the current burn rate.",
        "Burn rate": "Net cash outflow per month.",
        "Accounts payable": "Amounts NovaLedger owes vendors for approved invoices.",
        "Accounts receivable": "Amounts customers owe NovaLedger for issued bills.",
        "Accrual": "Expense recorded before cash payment when the obligation is known.",
        "Amortization": "Gradual expensing of intangible assets over useful life.",
        "Depreciation": "Gradual expensing of tangible assets over useful life.",
        "Budget variance": "Difference between planned and actual spending.",
        "Forecast": "Updated estimate of future revenue, expenses, and cash.",
        "Purchase order": "Approved buying document issued before vendor work begins.",
        "Payment terms": "Vendor agreement defining when payment is due, such as Net 30.",
        "Working capital": "Current assets minus current liabilities.",
        "EBITDA": "Earnings before interest, taxes, depreciation, and amortization.",
        "ARR": "Annual recurring revenue from active subscriptions.",
        "MRR": "Monthly recurring revenue from active subscriptions.",
        "Churn": "Revenue or customers lost during a period.",
        "Deferred revenue": "Cash collected before the service is delivered.",
        "Cash basis": "Accounting method that records activity when cash moves.",
        "Accrual basis": "Accounting method that records activity when earned or incurred.",
        "Reconciliation": "Matching internal records to bank, card, or vendor statements.",
        "Ledger": "System of record for financial transactions.",
        "Cost center": "Department or project bucket used to track spending.",
        "Procurement": "Process for selecting vendors and approving purchases.",
        "Invoice aging": "Grouping invoices by days outstanding or overdue.",
        "FX": "Foreign exchange conversion between currencies.",
        "Tax withholding": "Amount retained and remitted to tax authorities.",
        "T&E": "Travel and expense spending by employees.",
        "Contingency": "Reserved budget for uncertain but plausible costs.",
    }
    body = [f"# {COMPANY} Finance Glossary", ""]
    for term, definition in terms.items():
        body.append(f"## {term}\n{definition}\n")
    return "\n".join(body)


def build_budget_guidelines() -> str:
    return f"""
# {COMPANY} Budget Guidelines

NovaLedger plans budgets quarterly with a rolling twelve-month forecast. Each department
owns a baseline budget, a hiring plan, and a vendor plan. Finance publishes the first draft
for the next quarter by the 15th day of the final month in the current quarter. Department
leaders return changes within five business days, and the CFO publishes the approved version
by the 25th day of the month.

Engineering owns a quarterly budget of 1,250,000 USD. Within that amount, 720,000 USD is
reserved for payroll and contractors, 210,000 USD for cloud infrastructure, 160,000 USD for
developer SaaS, 90,000 USD for security and compliance, and 70,000 USD for team operations.
Sales owns 830,000 USD per quarter, including 390,000 USD for payroll, 170,000 USD for
customer travel, 140,000 USD for events, 80,000 USD for CRM and sales tools, and 50,000 USD
for enablement. Marketing owns 610,000 USD per quarter, including 220,000 USD for campaigns,
120,000 USD for content, 110,000 USD for events, 90,000 USD for agencies, and 70,000 USD for
marketing operations. People Operations owns 340,000 USD, Finance and Legal share 420,000 USD,
and Customer Success owns 540,000 USD.

Quarterly planning separates committed spend, planned spend, and optional spend. Committed
spend includes signed vendor contracts, approved hires, tax obligations, insurance, payroll,
and tools required for security or customer delivery. Planned spend includes travel, campaign
budgets, training, and software renewals that have not yet been signed. Optional spend covers
experiments, new events, pilot tools, and discretionary offsites. Leaders should protect
committed spend first, then planned spend, then optional spend.

Budget owners review actuals every Friday. A cost center forecast must be updated when spend
is expected to land more than 5 percent or 25,000 USD above the approved quarter budget,
whichever is lower. Overspend below 10,000 USD can be corrected within the department by
reducing optional spend. Overspend from 10,000 USD to 50,000 USD requires a written mitigation
plan from the department leader and Finance Business Partner. Overspend above 50,000 USD
requires CFO approval and must be escalated within two business days of discovery.

New vendor requests above 15,000 USD per year require Procurement review and a purchase order.
Requests above 75,000 USD per year require Legal review and a business case showing expected
value, implementation owner, data-security impact, and renewal risk. Teams should not commit
to multi-year agreements unless the annual discount is at least 12 percent and the responsible
vice president confirms usage for the full term.

Budget transfers between departments are allowed only when both budget owners approve and the
Finance Business Partner records the transfer in LedgerLoop. Transfers cannot be used to hide
recurring overspend. If a team repeatedly exceeds budget because the baseline is wrong, the
leader must request a forecast reset during the next quarterly planning cycle.
"""


def build_faq() -> str:
    qas = [
        ("How do I submit an expense?", "Submit it in LedgerLoop with a receipt, category, cost center, and business purpose within 10 calendar days."),
        ("When are reimbursements paid?", "Approved reimbursements are paid on the 7th and 22nd of each month, or the next business day."),
        ("What is the approval limit for my manager?", "A direct manager may approve expenses up to 250 USD."),
        ("Who approves an expense above 5,000 USD?", "CFO Priya Raman must approve any expense above 5,000 USD before purchase."),
        ("Can I expense a personal gym membership?", "No. Personal gym memberships are prohibited expenses."),
        ("Can I buy a SaaS subscription myself?", "Use the SaaS intake form first. Team trials up to 90 USD per user per month may be manager-approved for three months."),
        ("What if I lost a receipt?", "For expenses under 25 USD you may sign a missing receipt declaration; otherwise reimbursement is delayed."),
        ("Can I fly premium economy?", "Premium economy is allowed for flights of six hours or more with director approval."),
        ("What is the hotel cap?", "The cap is 260 USD per night in standard cities and 340 USD in high-cost cities."),
        ("What is the daily meal cap?", "The daily meal cap is 75 USD: 18 USD breakfast, 22 USD lunch, and 35 USD dinner."),
        ("Can I expense alcohol?", "Only at approved customer events, and it must be itemized separately."),
        ("When should overspend be escalated?", "Escalate when expected overspend is more than 5 percent or 25,000 USD above the quarterly budget."),
        ("What needs a purchase order?", "New vendor requests above 15,000 USD per year require Procurement review and a purchase order."),
        ("How long does Finance keep exception records?", "Finance Operations keeps exception records for seven years."),
        ("Can I use a corporate card for cash advances?", "No. Corporate cards may not be used for cash advances."),
        ("What happens if a receipt is late?", "A card transaction over 1,500 USD without a receipt can trigger an automatic card hold after seven days."),
    ]
    body = [f"# {COMPANY} Employee Finance FAQ", ""]
    for idx, (question, answer) in enumerate(qas, 1):
        body.append(f"## Q{idx}. {question}\n{answer}\n")
    return "\n".join(body)


def build_vendors() -> list[dict]:
    vendors = [
        ("VEN-001", "CloudBoard Labs", "Project Management", "Net 30", "billing@cloudboard.example"),
        ("VEN-002", "SynapseSheets", "Collaboration SaaS", "Net 30", "ar@synapsesheets.example"),
        ("VEN-003", "AuthTower Security", "Security", "Net 45", "finance@authtower.example"),
        ("VEN-004", "TripHarbor Travel", "Travel", "Net 15", "accounts@tripharbor.example"),
        ("VEN-005", "Northstar Events", "Events", "Net 30", "billing@northstarevents.example"),
        ("VEN-006", "LedgerLoop Systems", "Finance Systems", "Net 30", "invoices@ledgerloop.example"),
        ("VEN-007", "Nimbus Cloud", "Cloud Infrastructure", "Net 30", "receivables@nimbuscloud.example"),
        ("VEN-008", "Harbor Legal LLP", "Legal", "Net 45", "billing@harborlegal.example"),
        ("VEN-009", "BrightPath Recruiting", "Recruiting", "Net 30", "ap@brightpath.example"),
        ("VEN-010", "MetricForge Analytics", "Data Tools", "Net 30", "billing@metricforge.example"),
    ]
    return [
        Vendor(
            vendor_id=vendor_id,
            name=name,
            category=category,
            payment_terms=terms,
            contact_email=email,
        ).model_dump(mode="json")
        for vendor_id, name, category, terms, email in vendors
    ]


def build_invoices(vendors: list[dict]) -> list[dict]:
    base = date(2026, 3, 1)
    statuses = ["paid", "pending", "overdue", "paid", "pending", "overdue", "paid", "pending"]
    invoices = []
    for idx in range(15):
        vendor = vendors[idx % len(vendors)]
        issue = base + timedelta(days=idx * 5)
        due = issue + timedelta(days=15 + (idx % 3) * 15)
        status = statuses[idx % len(statuses)]
        if idx in {2, 5, 10, 14}:
            status = "overdue"
            due = date(2026, 4, 15) + timedelta(days=idx)
        invoices.append(
            Invoice(
                invoice_id=f"INV-{1000 + idx}",
                vendor=vendor["name"],
                amount=round(random.uniform(950, 82_000), 2),
                currency="USD",
                category=vendor["category"],
                issue_date=issue,
                due_date=due,
                status=status,
            ).model_dump(mode="json")
        )
    return invoices


def build_expenses() -> list[dict]:
    employees = [
        ("Avery Stone", "Engineering"),
        ("Mina Patel", "Sales"),
        ("Jordan Lee", "Marketing"),
        ("Rosa Kim", "People Operations"),
        ("Elena Torres", "Customer Success"),
        ("Marcus Young", "Finance"),
        ("Nia Brooks", "Engineering"),
        ("Owen Grant", "Legal"),
    ]
    categories = ["Travel", "Meals", "SaaS", "Training", "Events", "Office Supplies"]
    descriptions = [
        "Customer onsite ride and train fare",
        "Quarterly planning team lunch",
        "Approved developer SaaS trial",
        "Compliance webinar registration",
        "Customer advisory board materials",
        "Replacement keyboard for office workstation",
    ]
    statuses = ["approved", "pending", "reimbursed", "rejected", "pending", "approved"]
    expenses = []
    for idx in range(20):
        employee, department = employees[idx % len(employees)]
        status = statuses[idx % len(statuses)]
        if idx in {1, 7, 13, 18}:
            status = "pending"
        expenses.append(
            Expense(
                expense_id=f"EXP-{2000 + idx}",
                employee=employee,
                department=department,
                amount=round(random.uniform(18, 1_950), 2),
                category=categories[idx % len(categories)],
                description=descriptions[idx % len(descriptions)],
                submitted_date=date(2026, 5, 1) + timedelta(days=idx),
                status=status,
            ).model_dump(mode="json")
        )
    return expenses


def main() -> None:
    random.seed(RANDOM_SEED)
    write_text(KB_DIR / "expense-policy.md", build_expense_policy())
    write_text(KB_DIR / "finance-glossary.md", build_glossary())
    write_text(KB_DIR / "budget-guidelines.md", build_budget_guidelines())
    write_text(KB_DIR / "employee-finance-faq.md", build_faq())

    vendors = build_vendors()
    invoices = build_invoices(vendors)
    expenses = build_expenses()
    write_json(STRUCTURED_DIR / "vendors.json", vendors)
    write_json(STRUCTURED_DIR / "invoices.json", invoices)
    write_json(STRUCTURED_DIR / "expenses.json", expenses)

    overdue_count = sum(1 for invoice in invoices if invoice["status"] == "overdue")
    pending_expense_count = sum(1 for expense in expenses if expense["status"] == "pending")
    print(f"Generated corpus for {COMPANY}")
    print(f"Markdown files: 4")
    print(f"Invoices: {len(invoices)} ({overdue_count} overdue)")
    print(f"Expenses: {len(expenses)} ({pending_expense_count} pending)")
    print(f"Vendors: {len(vendors)}")


if __name__ == "__main__":
    main()
