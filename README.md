# NovaLedger Finance Copilot

Educational demo only. Not financial, tax, or investment advice.

NovaLedger Finance Copilot is a Streamlit chat app for a fictional company. It uses synthetic
markdown and JSON data, local hybrid RAG, Pydantic models, and a PydanticAI-compatible agent
tool layer to answer finance questions.

## What is included

- Synthetic knowledge base in `data/kb/`
- Synthetic structured records in `data/structured/`
- Pydantic schemas for invoices, expenses, vendors, tool I/O, and chat responses
- Local ingestion script that chunks markdown and persists a retrieval index to `app/rag/store/`
- Hybrid search combining hashed semantic vectors and token keyword scoring
- Agent tools: `search_knowledge_base`, `calculate_emi`, and `lookup_invoice`
- Streamlit chat UI with disclaimer, history, tools used, and source panel

## Setup

```bash
uv sync
uv run python scripts/generate_synthetic_data.py
uv run python scripts/ingest.py
uv run streamlit run ui/app.py
```

The app opens in your browser from Streamlit, usually at `http://localhost:8501`.

## Data generation

The generator uses fixed random seed `42` for reproducibility. It creates:

- `expense-policy.md` with reimbursement rules, approval limits, SaaS/travel policy, and prohibited expenses
- `finance-glossary.md` with more than 30 finance terms
- `budget-guidelines.md` with quarterly planning, department budgets, and overspend escalation
- `employee-finance-faq.md` with more than 15 Q&A pairs
- `invoices.json` with 15 validated invoices, including at least 3 overdue invoices
- `expenses.json` with 20 validated expenses, including at least 3 pending expenses
- `vendors.json` with 10 validated vendors

No real websites are scraped and no real financial data is used.

## Self-check prompts

```text
Explain the difference between CAPEX and OPEX according to our policy.
Calculate EMI for principal 800000, rate 10.5%, tenure 60 months.
Is invoice INV-1002 paid or overdue?
Can I expense a personal gym membership?
```

## Notes

The PydanticAI `Agent` is defined in `app/agent/finance_agent.py` with the required tools.
The Streamlit demo uses the same tools through a deterministic router so it can run reliably
for the assignment prompts without requiring live financial data.
