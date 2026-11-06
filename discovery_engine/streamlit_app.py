"""
SIP Retention AI Discovery Engine — public web UI.
Lets anyone run the analysis over public conversations about SIPs and
first-time investing in India, view theme prevalence, opportunity scoring,
and golden-set agreement.

No PII is stored or displayed. All sources are public and read-only.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="SIP Retention AI Discovery Engine — Groww",
    page_icon="🔍",
    layout="wide",
)

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data"
RAW_DIR = DATA_DIR / "raw"
ANALYSIS_DIR = DATA_DIR / "analysis"
EVIDENCE_DIR = BASE / "evidence"
DISCOVERY_OUT = ANALYSIS_DIR / "discovery_output.json"
GOLDEN_SET_PATH = EVIDENCE_DIR / "golden_set.json"
EVIDENCE_LOG_PATH = EVIDENCE_DIR / "AI_Evidence_Log.md"


# ---------------------------------------------------------------------------
# Analysis (imported from the engine)
# ---------------------------------------------------------------------------
import sys

sys.path.insert(0, str(BASE / "discovery_engine"))  # noqa: E402
from ingest import load_all_raw  # noqa: E402
from analyze import analyze  # noqa: E402


def load_json(path: Path, default=None):
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("SIP Retention AI Discovery Engine")
st.caption(
    "Groww · Growth Team · AI-powered discovery over public conversations "
    "about SIPs and first-time investing in India. "
    "Read-only, PII-redacted, no investment advice."
)

with st.expander("How the engine works", expanded=False):
    st.markdown(
        """
1. **Ingest** — Pull public conversations from Play Store, App Store, Reddit
   (r/IndiaInvestments, r/personalfinanceindia), TradingQ&A, YouTube comments,
   and Twitter/X. Keyword-filter on SIP / pause / stop / return / NAV.
2. **Deduplicate & store** — Hash-based dedup; PII (PAN, phone, account numbers)
   redacted; raw JSONL batches saved to `/data/raw`.
3. **Theme extraction** — Keyword first-pass lexicon (English + Hinglish signals)
   followed by an LLM confirmation pass. Extracts why investors started, what
   changed, pause/stop signals, checking behaviour, outside-app actions, and
   segment signals (income stability, influence source).
4. **Quantify** — Theme prevalence (% of items) and cross-segment comparison.
5. **Opportunity scoring** — Impact × fixability × business alignment → ranked
   opportunity areas linked to the 12-month SIP continuation metric.
6. **Validate** — Compare engine output against a hand-labelled 20-item golden
   set; report agreement rate and log corrections.
        """
    )

# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------
st.subheader("1. Run the analysis")

col_a, col_b = st.columns([1, 3])
with col_a:
    run_btn = st.button("Analyze all raw conversations", type="primary")
with col_b:
    st.caption(
        "Re-runs theme extraction and opportunity scoring over every raw batch "
        "on disk. Writes `/data/analysis/discovery_output.json`."
    )

if run_btn or DISCOVERY_OUT.exists():
    if run_btn:
        raw_items = load_all_raw()
        if not raw_items:
            st.warning(
                "No raw conversation batches found. The engine ships with a "
                "demo batch so it runs end-to-end; add real batches under "
                "`/data/raw/` to analyze live data."
            )
        else:
            result = analyze(raw_items)
            st.success(f"Analyzed {result['total_items_analyzed']} items.")
            st.session_state["discovery_result"] = result

    result = load_json(DISCOVERY_OUT) or st.session_state.get("discovery_result")

if "discovery_result" in st.session_state or DISCOVERY_OUT.exists():
    result = st.session_state.get("discovery_result") or load_json(DISCOVERY_OUT)

    st.divider()

    # ------------------------------------------------------------------
    # Overview metrics
    # ------------------------------------------------------------------
    st.subheader("2. Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric("Items analyzed", result.get("total_items_analyzed", 0))
    n_themes = len(result.get("theme_prevalence", {}))
    m2.metric("Themes detected", n_themes)
    n_oa = len(result.get("opportunity_areas", []))
    m3.metric("Opportunity areas ranked", n_oa)

    # ------------------------------------------------------------------
    # Theme prevalence
    # ------------------------------------------------------------------
    st.subheader("3. Theme prevalence (% of items mentioning each theme)")
    prevalence = result.get("theme_prevalence", {})
    counts = result.get("theme_counts", {})
    if prevalence:
        import pandas as pd

        theme_df = pd.DataFrame(
            [
                {"theme": t, "prevalence_pct": p, "items": counts.get(t, 0)}
                for t, p in prevalence.items()
            ]
        ).sort_values("prevalence_pct", ascending=False)
        st.bar_chart(theme_df.set_index("theme")["prevalence_pct"])
        st.dataframe(theme_df, use_container_width=True, hide_index=True)
    else:
        st.info("Run the analysis to see theme prevalence.")

    # ------------------------------------------------------------------
    # Opportunity areas
    # ------------------------------------------------------------------
    st.subheader("4. Ranked opportunity areas")
    oas = result.get("opportunity_areas", [])
    if oas:
        import pandas as pd

        oa_df = pd.DataFrame(oas)[
            ["name", "avg_prevalence", "max_prevalence", "fixability", "opportunity_score"]
        ]
        oa_df.columns = [
            "Opportunity",
            "Avg prevalence (%)",
            "Max prevalence (%)",
            "Fixability (0-1)",
            "Opportunity score",
        ]
        st.dataframe(
            oa_df.sort_values("Opportunity score", ascending=False),
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Score = 0.5 × avg prevalence + 0.3 × max prevalence + 0.2 × (fixability × 10). "
            "Higher = higher potential impact on 12-month SIP continuation."
        )
    else:
        st.info("Run the analysis to see opportunity areas.")

    # ------------------------------------------------------------------
    # Theme examples
    # ------------------------------------------------------------------
    st.subheader("5. Example quotes by theme")
    examples = result.get("theme_examples", {})
    if examples:
        theme_choice = st.selectbox("Choose a theme", sorted(examples.keys()))
        for ex in examples.get(theme_choice, []):
            st.markdown(
                f"**{ex.get('source','')}** — {ex.get('title','')}\n\n"
                f"> {ex.get('snippet','')}\n"
                f"{ex.get('url','')}"
            )
            st.divider()
    else:
        st.info("Run the analysis to see example quotes.")

    # ------------------------------------------------------------------
    # Segment sample
    # ------------------------------------------------------------------
    st.subheader("6. Segment signals (sample)")
    seg = result.get("segment_sample", [])
    if seg:
        for row in seg[:10]:
            sig = row.get("signals", {})
            st.markdown(
                f"**{row.get('source','')}** · {', '.join(f'{k}: {v}' for k, v in sig.items())}\n"
                f"> {row.get('snippet','')[:200]}…"
            )
            st.divider()
    else:
        st.info("Run the analysis to see segment signals.")

# ---------------------------------------------------------------------------
# Golden set validation
# ---------------------------------------------------------------------------
st.divider()
st.subheader("7. Validation against the golden set (AI Evidence Log)")

golden = load_json(GOLDEN_SET_PATH)
if golden:
    gs = golden.get("golden_set", [])
    agreement = golden.get("agreement", {})
    c1, c2, c3 = st.columns(3)
    c1.metric("Golden-set items", len(gs))
    c2.metric("Primary-theme agreement", agreement.get("primary_theme_match_pct", "—"))
    c3.metric("Pause-signal agreement", agreement.get("pause_signal_match_pct", "—"))

    with st.expander("Golden-set items (hand-labelled)", expanded=False):
        for item in gs:
            st.markdown(
                f"**#{item['id']}** [{item['source']}] {item['snippet']}  \n"
                f"Primary: `{item['primary_theme']}` · Pause signal: `{item['pause_signal']}` · "
                f"Segment: `{item['segment']}` · Engine agree: {'✅' if item.get('engine_agree') else '❌'}"
            )

    st.divider()
    st.subheader("8. AI output corrections (rejected / corrected)")
    for corr in golden.get("ai_corrections", []):
        st.markdown(
            f"**{corr['id']}** — Issue: {corr['issue']}  \n"
            f"AI output: {corr['ai_output']}  \n"
            f"Correction: {corr['correction']}  \n"
            f"Why: {corr['reason']}"
        )
        st.divider()
else:
    st.info("Golden set not found at evidence/golden_set.json.")

# ---------------------------------------------------------------------------
# Evidence log link
# ---------------------------------------------------------------------------
st.divider()
st.subheader("9. AI Evidence Log")
st.markdown(
    "Full sources & volumes, golden set, corrections, and validation method: "
    "[AI_Evidence_Log.md](https://raw.githubusercontent.com/ShrivastavaSunny/git_repo/main/evidence/AI_Evidence_Log.md)"
)

st.caption(
    "Not investment advice. This engine analyses public conversations only and does "
    "not recommend funds or stocks. Deployed from ShrivastavaSunny/git_repo."
)
