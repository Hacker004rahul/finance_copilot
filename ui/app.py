from __future__ import annotations

import html
import sys
import time
from pathlib import Path
from uuid import uuid4

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


st.set_page_config(page_title="NovaLedger Finance Copilot", page_icon="NL", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --ink: #101828;
        --muted: #667085;
        --line: rgba(148, 163, 184, 0.24);
        --panel: rgba(255, 255, 255, 0.78);
        --blue: #2563eb;
        --cyan: #0891b2;
        --violet: #6d28d9;
        --gold: #b7791f;
        --shadow: 0 24px 70px rgba(15, 23, 42, 0.12);
    }

    @keyframes floatGlow {
        0% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.55; }
        50% { transform: translate3d(28px, -18px, 0) scale(1.08); opacity: 0.78; }
        100% { transform: translate3d(0, 0, 0) scale(1); opacity: 0.55; }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes sheen {
        from { background-position: 200% center; }
        to { background-position: -200% center; }
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 12% 12%, rgba(37, 99, 235, 0.18), transparent 24rem),
            radial-gradient(circle at 88% 18%, rgba(8, 145, 178, 0.14), transparent 24rem),
            linear-gradient(135deg, #f8fbff 0%, #eef3f9 48%, #f7f9fc 100%);
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0 auto auto 47%;
        width: 36rem;
        height: 36rem;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(37, 99, 235, 0.14), transparent 68%);
        pointer-events: none;
        animation: floatGlow 8s ease-in-out infinite;
        z-index: 0;
    }

    .block-container {
        max-width: 1000px;
        padding-top: 1.25rem;
        padding-bottom: 7rem;
        position: relative;
        z-index: 1;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(16, 18, 24, 0.98), rgba(14, 17, 23, 0.98)),
            radial-gradient(circle at top, rgba(37, 99, 235, 0.24), transparent 16rem);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    [data-testid="stSidebar"] h3 {
        color: #f8fafc;
        font-size: 0.74rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 1rem 0 0.45rem;
    }

    .brand-card {
        display: flex;
        gap: 0.78rem;
        align-items: center;
        padding: 0.85rem 0 1.05rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 0.9rem;
    }

    .brand-icon {
        display: grid;
        place-items: center;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        color: #ffffff;
        background: linear-gradient(135deg, #2563eb, #0891b2 60%, #14b8a6);
        box-shadow: 0 14px 34px rgba(37, 99, 235, 0.35);
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .brand-title {
        font-size: 1.08rem;
        font-weight: 780;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #a8b3c7;
        font-size: 0.84rem;
        margin-top: 0.18rem;
    }

    .sidebar-note {
        color: #a8b3c7;
        font-size: 0.8rem;
        font-style: italic;
        margin-top: 1rem;
    }

    .stButton > button {
        border-radius: 14px;
        min-height: 2.75rem;
        border: 1px solid rgba(148, 163, 184, 0.28);
        background: rgba(255, 255, 255, 0.78);
        color: var(--ink);
        font-size: 0.9rem;
        font-weight: 580;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06);
        transition: transform 0.16s ease, box-shadow 0.16s ease, border-color 0.16s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(37, 99, 235, 0.35);
        box-shadow: 0 18px 38px rgba(37, 99, 235, 0.14);
        color: #1d4ed8;
        background: #ffffff;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.08);
        color: #f8fafc;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: none;
        justify-content: flex-start;
        text-align: left;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.14);
        border-color: rgba(255, 255, 255, 0.22);
        color: #ffffff;
    }

    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.88);
        border-radius: 26px;
        padding: 1.35rem 1.45rem;
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.88), rgba(255, 255, 255, 0.62)),
            radial-gradient(circle at top right, rgba(37, 99, 235, 0.14), transparent 18rem);
        box-shadow: var(--shadow);
        backdrop-filter: blur(18px);
        margin-bottom: 1rem;
        animation: slideIn 0.45s ease both;
    }

    .hero::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(110deg, transparent 30%, rgba(255, 255, 255, 0.45), transparent 70%);
        background-size: 220% 100%;
        animation: sheen 7s linear infinite;
        pointer-events: none;
    }

    .hero-kicker {
        color: #1d4ed8;
        font-size: 0.76rem;
        font-weight: 760;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .hero h1 {
        font-size: 2rem !important;
        line-height: 1.14 !important;
        letter-spacing: 0 !important;
        margin: 0 0 0.35rem !important;
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 0.97rem;
        max-width: 42rem;
        margin-bottom: 0.8rem;
    }

    .disclaimer {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background: #fff8e7;
        color: #7a5412;
        border: 1px solid #f2d38b;
        border-radius: 999px;
        padding: 0.48rem 0.75rem;
        font-size: 0.84rem;
        line-height: 1.25;
    }

    .suggestion-title {
        color: #334155;
        font-size: 0.76rem;
        font-weight: 760;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin: 0.95rem 0 0.45rem;
    }

    .suggestion-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.62rem;
        margin-bottom: 1.05rem;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 22px;
        padding: 0.92rem 1rem;
        margin-bottom: 0.78rem;
        background: rgba(255, 255, 255, 0.78);
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.07);
        backdrop-filter: blur(14px);
        animation: slideIn 0.28s ease both;
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(239, 246, 255, 0.9), rgba(255, 255, 255, 0.75));
        border-color: rgba(191, 219, 254, 0.9);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] div {
        font-size: 0.94rem;
        line-height: 1.55;
    }

    [data-testid="stExpander"] {
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        overflow: hidden;
        background: rgba(248, 250, 252, 0.8);
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] div {
        font-size: 0.84rem;
        line-height: 1.45;
    }

    [data-testid="stExpander"] h1,
    [data-testid="stExpander"] h2,
    [data-testid="stExpander"] h3 {
        font-size: 0.95rem !important;
        line-height: 1.35 !important;
        margin: 0.55rem 0 0.35rem !important;
        font-weight: 680 !important;
    }

    .source-text {
        white-space: pre-wrap;
        font-size: 0.83rem;
        line-height: 1.46;
        color: #3f4652;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 12px;
        padding: 0.68rem 0.76rem;
        margin-bottom: 0.65rem;
    }

    .tool-chip {
        display: inline-block;
        background: linear-gradient(135deg, #eef2ff, #e0f2fe);
        color: #3730a3;
        border: 1px solid #c7d2fe;
        border-radius: 999px;
        padding: 0.2rem 0.58rem;
        margin: 0.18rem 0.22rem 0.18rem 0;
        font-size: 0.76rem;
        font-weight: 720;
    }

    [data-testid="stChatInput"] {
        background: rgba(248, 250, 252, 0.82);
        border-top: 1px solid rgba(148, 163, 184, 0.22);
        backdrop-filter: blur(18px);
    }

    textarea[aria-label="Ask about expenses, budgets, EMI, or invoices..."] {
        font-size: 0.95rem;
    }

    @media (max-width: 760px) {
        .suggestion-grid {
            grid-template-columns: 1fr;
        }

        .block-container {
            padding-left: 0.78rem;
            padding-right: 0.78rem;
        }

        .hero h1 {
            font-size: 1.55rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def make_welcome_message() -> dict:
    return {
        "role": "assistant",
        "content": WELCOME_MESSAGE,
        "sources": [],
        "tools_used": [],
    }


def make_conversation(title: str = "New chat") -> dict:
    return {
        "id": uuid4().hex,
        "title": title,
        "created_at": time.time(),
        "messages": [make_welcome_message()],
    }


def current_conversation() -> dict:
    for conversation in st.session_state.conversations:
        if conversation["id"] == st.session_state.active_conversation_id:
            return conversation
    conversation = make_conversation()
    st.session_state.conversations.insert(0, conversation)
    st.session_state.active_conversation_id = conversation["id"]
    return conversation


def set_current_messages(messages: list[dict]) -> None:
    conversation = current_conversation()
    conversation["messages"] = messages


def reset_chat() -> None:
    conversation = make_conversation()
    st.session_state.conversations.insert(0, conversation)
    st.session_state.conversations = st.session_state.conversations[:8]
    st.session_state.active_conversation_id = conversation["id"]


def switch_chat(conversation_id: str) -> None:
    st.session_state.active_conversation_id = conversation_id


def queue_prompt(prompt_text: str) -> None:
    st.session_state.pending_prompt = prompt_text


def update_conversation_title(prompt_text: str) -> None:
    conversation = current_conversation()
    if conversation["title"] == "New chat":
        title = prompt_text.strip().replace("\n", " ")
        conversation["title"] = title[:48] + ("..." if len(title) > 48 else "")


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


if "conversations" not in st.session_state:
    first_conversation = make_conversation()
    st.session_state.conversations = [first_conversation]
    st.session_state.active_conversation_id = first_conversation["id"]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

conversation = current_conversation()
messages = conversation["messages"]

with st.sidebar:
    st.markdown(
        """
        <div class="brand-card">
            <div class="brand-icon">NL</div>
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
        st.rerun()

    st.markdown("### Recent chats")
    for index, item in enumerate(st.session_state.conversations[:6]):
        label = item["title"]
        if item["id"] == st.session_state.active_conversation_id:
            label = "Active - " + label
        if st.button(label, key=f"recent_chat_{item['id']}_{index}", use_container_width=True):
            switch_chat(item["id"])
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
    st.markdown(
        "<div class='sidebar-note'>Educational demo only. Not financial advice.</div>",
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">Agentic RAG finance assistant</div>
        <h1>NovaLedger Finance Copilot</h1>
        <div class="hero-subtitle">
            Ask policy questions, inspect sources, calculate EMI, and look up synthetic invoices
            from one focused finance workspace.
        </div>
        <div class="disclaimer">Notice: {html.escape(DISCLAIMER)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='suggestion-title'>Try asking</div>", unsafe_allow_html=True)
st.markdown("<div class='suggestion-grid'>", unsafe_allow_html=True)
suggestion_cols = st.columns(2)
for index, question in enumerate(SUGGESTIONS):
    with suggestion_cols[index % 2]:
        if st.button(question, key=f"main_suggestion_{index}", use_container_width=True):
            queue_prompt(question)
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        render_tools(message.get("tools_used", []))
        render_sources(message.get("sources", []))

typed_prompt = st.chat_input("Ask about expenses, budgets, EMI, or invoices...")
prompt = st.session_state.pending_prompt or typed_prompt
st.session_state.pending_prompt = None

if prompt:
    user_message = {"role": "user", "content": prompt, "sources": [], "tools_used": []}
    messages.append(user_message)
    update_conversation_title(prompt)
    set_current_messages(messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Checking NovaLedger finance knowledge..."):
            response = answer_question(prompt)
        st.markdown(response.answer)
        render_tools(response.tools_used)
        render_sources(response.sources)

    messages.append(
        {
            "role": "assistant",
            "content": response.answer,
            "sources": response.sources,
            "tools_used": response.tools_used,
        }
    )
    set_current_messages(messages)
