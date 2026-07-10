from __future__ import annotations

import html
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent.finance_agent import DISCLAIMER, answer_question  # noqa: E402


SUGGESTIONS = [
    "Can I expense a personal gym membership?",
    "Explain CAPEX vs OPEX according to our policy.",
    "Calculate EMI for principal 800000, rate 10.5%, tenure 60 months.",
    "Is invoice INV-1002 paid or overdue?",
]

WELCOME_MESSAGE = (
    "Hi, I can answer NovaLedger finance policy questions, calculate EMI, "
    "and look up synthetic invoice statuses."
)


st.set_page_config(page_title="NovaLedger Finance Copilot", page_icon="💰", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #f5f7fb;
        --ink: #18202f;
        --muted: #667085;
        --line: #e6e9ef;
        --blue: #2563eb;
        --blue-soft: #eaf1ff;
        --gold: #b7791f;
        --gold-soft: #fff7df;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 30rem),
            linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    .block-container {
        max-width: 960px;
        padding-top: 1.4rem;
        padding-bottom: 6.5rem;
    }

    h1 {
        font-size: 1.85rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.35rem !important;
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #111318;
        border-right: 1px solid #262a33;
    }

    [data-testid="stSidebar"] * {
        color: #f3f4f6;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #d1d5db;
        font-size: 0.91rem;
        line-height: 1.45;
    }

    [data-testid="stSidebar"] h3 {
        color: #ffffff;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 1.15rem;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: #24262d;
        border: 1px solid #363a44;
        border-radius: 10px;
        color: #f9fafb;
        min-height: 2.75rem;
        text-align: left;
        justify-content: flex-start;
        font-size: 0.92rem;
        transition: all 0.15s ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #2f3340;
        border-color: #4b5563;
        color: #ffffff;
    }

    .brand-card {
        display: flex;
        gap: 0.75rem;
        align-items: center;
        padding: 0.9rem 0.2rem 1rem;
        border-bottom: 1px solid #2a2e37;
        margin-bottom: 1rem;
    }

    .brand-icon {
        display: grid;
        place-items: center;
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1d4ed8, #0f766e);
        font-size: 1.45rem;
    }

    .brand-title {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #aeb4c0;
        font-size: 0.84rem;
        margin-top: 0.15rem;
    }

    .hero {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 0.96rem;
        margin: 0.15rem 0 0.8rem;
    }

    .disclaimer {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: var(--gold-soft);
        color: #805b10;
        border: 1px solid #f3d58b;
        border-radius: 999px;
        padding: 0.46rem 0.72rem;
        font-size: 0.86rem;
        line-height: 1.2;
    }

    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.9rem 0 1.1rem;
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid var(--line);
        background: #ffffff;
        color: var(--ink);
        min-height: 2.7rem;
        font-size: 0.9rem;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    .stButton > button:hover {
        border-color: #bfdbfe;
        background: var(--blue-soft);
        color: #1d4ed8;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.045);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] div {
        font-size: 0.95rem;
        line-height: 1.5;
    }

    [data-testid="stCaptionContainer"] p,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] div {
        font-size: 0.86rem;
        line-height: 1.45;
    }

    [data-testid="stExpander"] h1,
    [data-testid="stExpander"] h2,
    [data-testid="stExpander"] h3 {
        font-size: 0.95rem !important;
        line-height: 1.35 !important;
        margin: 0.55rem 0 0.35rem !important;
        font-weight: 650 !important;
    }

    .source-text {
        white-space: pre-wrap;
        font-size: 0.84rem;
        line-height: 1.45;
        color: #3f4652;
        background: #f8fafc;
        border: 1px solid #edf0f5;
        border-radius: 10px;
        padding: 0.65rem 0.75rem;
        margin-bottom: 0.65rem;
    }

    .tool-chip {
        display: inline-block;
        background: #eef2ff;
        color: #3730a3;
        border: 1px solid #c7d2fe;
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        margin: 0.15rem 0.2rem 0.15rem 0;
        font-size: 0.78rem;
        font-weight: 650;
    }

    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.96);
        border-top: 1px solid var(--line);
    }

    textarea[aria-label="Ask about expenses, budgets, EMI, or invoices..."] {
        font-size: 0.95rem;
    }

    @media (max-width: 720px) {
        .suggestion-grid {
            grid-template-columns: 1fr;
        }

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def reset_chat() -> None:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
            "sources": [],
            "tools_used": [],
        }
    ]


def queue_prompt(prompt_text: str) -> None:
    st.session_state.pending_prompt = prompt_text


def render_sources(sources: list) -> None:
    if not sources:
        return
    with st.expander("Sources", expanded=False):
        for source in sources:
            st.markdown(f"**{source.source}** - score `{source.score:.4f}`")
            st.markdown(
                f"<div class='source-text'>{html.escape(source.text)}</div>",
                unsafe_allow_html=True,
            )


def render_tools(tools_used: list[str]) -> None:
    if not tools_used:
        return
    chips = "".join(
        f"<span class='tool-chip'>{html.escape(tool)}</span>" for tool in tools_used
    )
    st.markdown(chips, unsafe_allow_html=True)


if "messages" not in st.session_state:
    reset_chat()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

with st.sidebar:
    st.markdown(
        """
        <div class="brand-card">
            <div class="brand-icon">💰</div>
            <div>
                <div class="brand-title">NovaLedger</div>
                <div class="brand-subtitle">Finance Copilot</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("+ New chat", use_container_width=True):
        reset_chat()
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown("### Suggested")
    for index, question in enumerate(SUGGESTIONS):
        if st.button(question, key=f"sidebar_suggestion_{index}", use_container_width=True):
            queue_prompt(question)
            st.rerun()

    st.markdown("---")
    st.markdown("### Tools")
    st.markdown(
        """
        - Policy search (hybrid RAG)
        - EMI calculator
        - Invoice lookup
        """
    )
    st.markdown("### Documents")
    st.markdown(
        """
        - Budget guidelines
        - Expense policy
        - Employee finance FAQ
        - Finance glossary
        """
    )
    st.caption("Educational demo only. Not financial advice.")

st.markdown(
    f"""
    <div class="hero">
        <h1>NovaLedger Finance Copilot</h1>
        <div class="hero-subtitle">
            Ask finance policy questions, calculate EMI, or check synthetic invoice status.
        </div>
        <div class="disclaimer">⚠️ {html.escape(DISCLAIMER)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='suggestion-grid'>", unsafe_allow_html=True)
suggestion_cols = st.columns(2)
for index, question in enumerate(SUGGESTIONS):
    with suggestion_cols[index % 2]:
        if st.button(question, key=f"main_suggestion_{index}", use_container_width=True):
            queue_prompt(question)
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_tools(message.get("tools_used", []))
        render_sources(message.get("sources", []))

typed_prompt = st.chat_input("Ask about expenses, budgets, EMI, or invoices...")
prompt = st.session_state.pending_prompt or typed_prompt
st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt, "sources": [], "tools_used": []}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking NovaLedger finance knowledge..."):
            response = answer_question(prompt)
        st.markdown(response.answer)
        render_tools(response.tools_used)
        render_sources(response.sources)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
            "tools_used": response.tools_used,
        }
    )
