from __future__ import annotations

import html
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent.finance_agent import DISCLAIMER, answer_question  # noqa: E402


st.set_page_config(page_title="NovaLedger Finance Copilot", page_icon="NL", layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 980px;
        padding-top: 2rem;
    }

    h1 {
        font-size: 1.75rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stChatMessage"] {
        padding: 0.65rem 0.85rem;
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
    }

    textarea[aria-label="Ask about expenses, budgets, EMI, or invoices..."] {
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("NovaLedger Finance Copilot")
st.warning(DISCLAIMER)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi, I can answer NovaLedger finance policy questions, calculate EMI, "
                "and look up synthetic invoice statuses."
            ),
            "sources": [],
            "tools_used": [],
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("tools_used"):
            st.caption("Tools used: " + ", ".join(message["tools_used"]))
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    st.markdown(f"**{source.source}** - score `{source.score:.4f}`")
                    st.markdown(
                        f"<div class='source-text'>{html.escape(source.text)}</div>",
                        unsafe_allow_html=True,
                    )

prompt = st.chat_input("Ask about expenses, budgets, EMI, or invoices...")

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
        if response.tools_used:
            st.caption("Tools used: " + ", ".join(response.tools_used))
        if response.sources:
            with st.expander("Sources"):
                for source in response.sources:
                    st.markdown(f"**{source.source}** - score `{source.score:.4f}`")
                    st.markdown(
                        f"<div class='source-text'>{html.escape(source.text)}</div>",
                        unsafe_allow_html=True,
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
            "tools_used": response.tools_used,
        }
    )
