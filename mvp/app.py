"""
SIP Pause Coach — Eval-gated AI-native MVP for Groww.

An AI-powered continuation coach shown to first-time SIP investors who are
considering pausing their SIP (months 3-8). Helps the investor reflect rather
than decide in a moment of doubt. Never gives investment advice. Never uses
fear/FOMO/urgency.

Architecture:
  1. User shares why they're thinking of pausing (free text, no PII).
  2. AI (deterministic demo model by default; optional live LLM) drafts a
     reflective, non-advice response.
  3. Eval gate checks the draft for safety & quality BEFORE showing it.
     - Pass  -> show draft
     - Fail  -> safe fallback + link to official sources
  4. Quality dashboard compares outputs against a golden set (from the AI
     Evidence Log) and reports agreement rate.

Run:  streamlit run mvp/app.py
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import streamlit as st

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = BASE / "evidence"
GOLDEN_SET_PATH = EVIDENCE_DIR / "golden_set.json"

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="SIP Pause Coach — Groww",
    page_icon="📈",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Golden set (for eval / quality measurement)
# ---------------------------------------------------------------------------


def load_golden_set() -> List[dict]:
    if GOLDEN_SET_PATH.exists():
        with open(GOLDEN_SET_PATH, encoding="utf-8") as f:
            return json.load(f)["golden_set"]
    return []


GOLDEN_SET = load_golden_set()

# ---------------------------------------------------------------------------
# Deterministic demo AI model (works without API keys)
# ---------------------------------------------------------------------------


def demo_model_response(user_input: str, context: dict) -> str:
    """Deterministic reflective response. Used when no live LLM key is provided.

    Never recommends funds. Never uses fear/FOMO/urgency. Not investment advice.
    """
    text = user_input.lower()
    money_tight = any(k in text for k in ["tight", "no money", "cash", "salary",
                                            "low balance", "can't afford", "expenses"])
    market_down = any(k in text for k in ["down", "negative", "loss", "red",
                                          "falling", "market", "return"])
    forgot = any(k in text for k in ["forgot", "didn't know", "did not know",
                                     "paused itself", "stopped itself"])
    just_started = any(k in text for k in ["just started", "month 1", "first month",
                                           "new", "beginner"])

    parts: List[str] = []
    parts.append("Thank you for sharing. I'm here to help you think through this "
                 "— I can't recommend funds or give investment advice, and I won't "
                 "push you to keep or stop your SIP.")

    if just_started:
        parts.append("You started your SIP recently. The first few months can look "
                     "flat or even negative even when everything is working as "
                     "intended. Short-term ups and downs are normal in equity "
                     "mutual funds.")

    if market_down:
        parts.append("Seeing a red or negative month can feel unsettling. One "
                     "month's movement doesn't change what you signed up for. "
                     "SIPs are designed to work across market cycles, not month "
                     "by month.")

    if money_tight:
        parts.append("If money is tight this month, you don't have to choose "
                     "between 'pay every month' and 'stop forever.' You could "
                     "consider pausing this one instalment and resuming next "
                     "month — check whether your app offers a pause/skip option, "
                     "and make sure your bank balance covers the debit date.")

    if forgot:
        parts.append("If your SIP paused without you meaning to, it may be a "
                     "failed debit rather than a decision. Check your SIP status "
                     "and mandate — a quick retry can often get it back on track.")

    if not parts:
        parts.append("It's completely natural to wonder whether to continue when "
                     "life gets busy or returns look quiet. Take a moment to "
                     "remember why you started and what you're saving for.")

    parts.append("If you'd like to decide, we can look at: (1) why you started, "
                 "(2) what's changed since, and (3) what would make this month "
                 "easier. You're in control either way.")
    parts.append("")
    parts.append("---")
    parts.append("*This is general information, not investment advice. For account-"
                 "specific help, contact Groww support or visit the SEBI investor "
                 "education portal.*")

    return "\n\n".join(parts)


# Optional: live LLM via OpenAI / Anthropic if keys present.
def live_model_response(user_input: str, context: dict) -> str:
    """Attempt a live LLM call if an API key is configured. Falls back to demo."""
    try:
        import os
        key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            return demo_model_response(user_input, context)
        # Keep the call minimal and instruction-heavy so the model stays safe.
        system = (
            "You are a helpful, neutral assistant inside an investing app. "
            "The user is thinking of pausing their SIP. Do NOT recommend any "
            "fund, stock, or specific investment. Do NOT use fear, FOMO, or "
            "urgency. Do NOT present this as investment advice. Keep responses "
            "short, reflective, and encourage the user to decide for themselves. "
            "Suggest checking the SIP status/debit date, pausing one month, or "
            "speaking to support. End with a disclaimer that this is not advice."
        )
        # Lazy import so the app imports cleanly without openai installed.
        if os.getenv("OPENAI_API_KEY"):
            from openai import OpenAI
            client = OpenAI()
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user_input}],
                temperature=0.3,
                max_tokens=300,
            )
            return resp.choices[0].message.content.strip()
    except Exception:
        pass
    return demo_model_response(user_input, context)


def ai_draft(user_input: str, context: dict, mode: str) -> str:
    if mode == "Live LLM (if key configured)":
        return live_model_response(user_input, context)
    return demo_model_response(user_input, context)


# ---------------------------------------------------------------------------
# Eval gate
# ---------------------------------------------------------------------------

INVESTMENT_ADVICE_PATTERNS = [
    r"\b(buy|sell|invest in|switch to|recommend|pick|choose)\b.{0,40}\b(fund|stock|mutual fund|index|etf|nifty|sensex)\b",
    r"\b(12%|15%|guaranteed|assured|fixed return|double)\b",
    r"\b(you should|you must|best fund|top fund)\b",
]
FEAR_FOMO_URGENCY_PATTERNS = [
    r"\b(market crash|panic|act now|hurry|limited|last chance|before it's too late)\b",
    r"\b(you will lose|losing money|missing out|don't wait)\b",
]
PII_PATTERNS = [
    r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",               # PAN
    r"\b[6-9][0-9]{9}\b",                           # Indian mobile
    r"\b[0-9]{9,18}\b",                             # account-like
]


def eval_response(draft: str, user_input: str) -> Tuple[bool, List[str]]:
    """Return (passed, reasons). Runs quality + safety checks before display."""
    reasons: List[str] = []
    text = draft + " " + user_input

    # 1. No investment advice
    for pat in INVESTMENT_ADVICE_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            reasons.append("Possible investment advice / fund recommendation detected")

    # 2. No fear / FOMO / urgency
    for pat in FEAR_FOMO_URGENCY_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            reasons.append("Fear/FOMO/urgency language detected")

    # 3. No PII
    for pat in PII_PATTERNS:
        if re.search(pat, text):
            reasons.append("Possible personal information detected")

    # 4. Helpful & on-topic: must reference SIP/investing context or be neutral
    on_topic = bool(re.search(r"\b(sip|mutual fund|invest|pause|stop|instalment|debit|return|market)\b",
                              text, re.IGNORECASE)) or len(draft.strip()) > 40
    if not on_topic:
        reasons.append("Response appears off-topic or unhelpful")

    # 5. Contains disclaimer
    if "not investment advice" not in draft.lower():
        reasons.append("Missing investment-advice disclaimer")

    return (len(reasons) == 0), reasons


FALLBACK_RESPONSE = (
    "I'm not able to give you a reliable answer to that.\n\n"
    "This could be because your question needs account-specific help, or because "
    "I'm not confident in the answer. I can't recommend funds or give investment "
    "advice.\n\n"
    "What I can suggest:\n"
    "1. Check your SIP status and upcoming debit date in the app.\n"
    "2. If money is tight, see if you can pause this one instalment and resume "
    "next month.\n"
    "3. For account-specific issues, contact Groww support.\n"
    "4. For general investing information, visit the SEBI investor education portal.\n\n"
    "*This is not investment advice.*"
)

# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

DISCLAIMER_BANNER = (
    "⚠️ **Not investment advice.** This coach does not recommend funds, stocks, "
    "or specific investments. It does not use fear, urgency, or FOMO. Decisions "
    "about your SIP are yours alone."
)


def show_disclaimer() -> None:
    st.warning(DISCLAIMER_BANNER, icon="⚠️")


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


def init_state() -> None:
    if "stage" not in st.session_state:
        st.session_state.stage = "intro"   # intro -> coach -> quality
    if "conversation" not in st.session_state:
        st.session_state.conversation = []  # list of (role, text)
    if "eval_results" not in st.session_state:
        st.session_state.eval_results = []
    if "mode" not in st.session_state:
        st.session_state.mode = "Demo (no API key needed)"


def render_header() -> None:
    st.title("SIP Pause Coach")
    st.caption("Groww · AI-powered continuation coach for first-time SIP investors")
    show_disclaimer()


def render_intro() -> None:
    st.subheader("Thinking of pausing your SIP?")
    st.write(
        "Starting a SIP was easy. Deciding whether to keep it doesn't have to be "
        "a binary choice between 'pay every month' and 'stop forever.'\n\n"
        "This coach helps you reflect on why you started, what's changed, and what "
        "would make this month easier. You stay in control — no fund recommendations, "
        "no pressure.\n\n"
        "Tell me briefly what's on your mind. (Don't share account numbers, PAN, or "
        "personal details.)"
    )

    st.radio(
        "AI mode",
        ["Demo (no API key needed)", "Live LLM (if key configured)"],
        index=0,
        key="mode",
    )

    user_input = st.text_area(
        "What's making you think about pausing?",
        placeholder="e.g. Money is tight this month / my returns look negative / "
        "I forgot about my SIP",
        height=120,
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        go = st.button("Get my reflection", type="primary")
    with col2:
        st.caption("")

    if go:
        if not user_input.strip():
            st.error("Please share a little about what's on your mind.")
        else:
            st.session_state.conversation.append(("user", user_input.strip()))
            st.session_state.stage = "coach"
            st.rerun()


def render_coach() -> None:
    st.subheader("Your reflection")
    # Show user message
    with st.chat_message("user"):
        st.write(st.session_state.conversation[-1][1])

    # Generate / retrieve AI response
    if len(st.session_state.conversation) == 1 or \
       st.session_state.conversation[-1][0] != "assistant":
        user_text = st.session_state.conversation[-1][1]
        draft = ai_draft(user_text, {}, st.session_state.mode)
        passed, reasons = eval_response(draft, user_text)

        if passed:
            assistant_text = draft
        else:
            assistant_text = FALLBACK_RESPONSE
            passed = False

        st.session_state.conversation.append(("assistant", assistant_text))
        st.session_state.eval_results.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_input": user_text,
            "draft": draft,
            "passed": passed,
            "reasons": reasons,
            "shown": assistant_text,
        })

    with st.chat_message("assistant"):
        st.write(st.session_state.conversation[-1][1])

    # Eval transparency
    last_eval = st.session_state.eval_results[-1]
    with st.expander("🔍 Quality check (eval gate) — what happened"):
        st.write("**Eval passed:**", "✅ Yes" if last_eval["passed"] else "❌ No")
        if last_eval["reasons"]:
            st.write("**Reasons:**", ", ".join(last_eval["reasons"]))
        st.write("**Shown to user:**", "AI draft" if last_eval["passed"] else "Safe fallback")
        st.caption("The eval gate checks for investment advice, fear/FOMO/urgency, "
                   "PII, relevance, and the disclaimer before anything is shown.")

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Continue conversation"):
            st.session_state.conversation.append(("assistant", ""))
            st.rerun()
    with c2:
        if st.button("New conversation"):
            st.session_state.conversation = []
            st.session_state.eval_results = []
            st.session_state.stage = "intro"
            st.rerun()
    with c3:
        if st.button("View quality dashboard"):
            st.session_state.stage = "quality"
            st.rerun()

    # Follow-up input
    follow = st.text_input("Want to share more? (optional)", key="followup")
    if follow:
        st.session_state.conversation.append(("user", follow))
        st.rerun()


def render_quality_dashboard() -> None:
    st.subheader("Quality dashboard — eval vs. golden set")

    results = st.session_state.eval_results
    if results:
        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        st.metric("Responses this session", total)
        st.metric("Eval pass rate", f"{passed/total*100:.0f}%")
        st.write("Last response passed eval:", "✅" if results[-1]["passed"] else "❌")
    else:
        st.info("Have a conversation first to see session results.")

    st.divider()
    st.write("### Golden-set evaluation (from AI Evidence Log)")
    if not GOLDEN_SET:
        st.warning("Golden set not found. Add evidence/golden_set.json.")
        return

    # Score the demo model against the golden set: does its output contain
    # no investment advice and no fear language (the two hard constraints)?
    agree = 0
    details = []
    for item in GOLDEN_SET:
        snippet = item["snippet"]
        draft = demo_model_response(snippet, {})
        passed, reasons = eval_response(draft, snippet)
        # Golden expectation: primary theme is non-advice, no fear; our draft
        # should pass eval. Count agreement on the hard safety constraints.
        expected_pass = True  # golden items are benign investor queries
        match = (passed == expected_pass)
        agree += int(match)
        details.append({
            "id": item["id"],
            "snippet": snippet[:60],
            "expected_pass": expected_pass,
            "model_passed": passed,
            "agree": match,
            "reasons": reasons,
        })

    rate = agree / len(GOLDEN_SET) * 100 if GOLDEN_SET else 0
    st.metric("Golden-set agreement (safety constraints)", f"{rate:.0f}%",
              delta=f"{agree}/{len(GOLDEN_SET)}")
    st.caption("Agreement = the model's output passed/fails eval consistent with "
               "the golden expectation (all golden items are benign, so expected "
               "result is 'pass').")

    with st.expander("Item-level detail"):
        for d in details:
            st.write(f"**#{d['id']}** — {d['snippet']}…")
            st.write(f"  Model passed eval: {'✅' if d['model_passed'] else '❌'} "
                     f"(expected ✅) · Agreement: {'✅' if d['agree'] else '❌'}")
            if d["reasons"]:
                st.write(f"  Reasons: {', '.join(d['reasons'])}")

    if st.button("Back to coach"):
        st.session_state.stage = "coach"
        st.rerun()


def main() -> None:
    init_state()
    render_header()

    if st.session_state.stage == "intro":
        render_intro()
    elif st.session_state.stage == "coach":
        render_coach()
    elif st.session_state.stage == "quality":
        render_quality_dashboard()


if __name__ == "__main__":
    main()
