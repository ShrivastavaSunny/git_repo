"""
Theme analysis layer.
Takes raw conversation items and produces:
1. Identified themes with example quotes
2. Quantified theme prevalence (share of items mentioning each theme)
3. Cross-segment comparison (age, income stability, source of influence)
4. Opportunity area scoring (impact x frequency x fixability)
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict

from discovery_engine.ingest import load_all_raw

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ANALYSIS_DIR = DATA_DIR / "analysis"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

# Theme keyword lexicon (English + Hinglish signals). Used for first-pass
# detection so the LLM only needs to confirm / refine, keeping cost low.
THEME_KEYWORDS = {
    "expectation_mismatch": [
        "expected", "thought", "assumed", "promise", "guarantee", "fixed return",
        "quick", "fast money", "double", "12%", "15% return", "monthly income",
    ],
    "returns_underwhelming": [
        "return", "profit", "loss", "negative", "red", "down", "flat", "2%",
        "1%", "not growing", "underperforming", "benchmark", "nifty", "sensex",
    ],
    "pause_reduce_stop": [
        "pause", "stopped", "stop", "reduce", "skipped", "missed", "lapse",
        "discontinue", "quit", "withdraw", "redeem", "exit", "break",
    ],
    "lack_of_visibility": [
        "check", "track", "statement", "portfolio", "dashboard", "nav",
        "where is my money", "don't understand", "confusing", "unclear",
    ],
    "checking_frequency": [
        "everyday", "daily", "every week", "weekly", "every month", "monthly",
        "keep checking", "obsess", "constantly", "rarely", "forgot",
    ],
    "outside_app_behavior": [
        "google", "youtube", "telegram", "whatsapp", "friend", "family",
        "advisor", "brother", "father", "colleague", "reddit", "twitter",
    ],
    "confusion_worry_in_app": [
        "confusing", "worry", "scared", "don't know", "not sure", "help",
        "customer care", "support", "error", "failed", "debited but",
    ],
    "segment_income_stability": [
        "salary", "freelance", "irregular", "monthly income", "job loss",
        "bonus", "savings", "pocket money", "allowance",
    ],
    "influence_source": [
        "friend", "brother", "father", "youtube", "influencer", "advertisement",
        "ad", "colleague", "recommended", "suggested",
    ],
}

OPPORTUNITY_AREAS = [
    {
        "id": "oa_settling_expectations",
        "name": "Set realistic first-year return expectations",
        "description": "First-time investors expect quick/linear growth; flat or red months trigger doubt.",
        "linked_themes": ["expectation_mismatch", "returns_underwhelming"],
    },
    {
        "id": "oa_progress_visibility",
        "name": "Make SIP progress visible and meaningful between instalments",
        "description": "Users check infrequently and see flat numbers; no sense of compounding progress.",
        "linked_themes": ["lack_of_visibility", "checking_frequency", "returns_underwhelming"],
    },
    {
        "id": "oa_pause_intervention",
        "name": "Intervene before pause / reduce / stop",
        "description": "SIPs lapse silently; no early-warning or graceful pause option.",
        "linked_themes": ["pause_reduce_stop", "confusion_worry_in_app"],
    },
    {
        "id": "oa_outside_app_guidance",
        "name": "Meet users where they go when unsure (outside the app)",
        "description": "Users Google / ask friends instead of in-app support; get mixed advice.",
        "linked_themes": ["outside_app_behavior", "confusion_worry_in_app"],
    },
    {
        "id": "oa_in_app_clarity",
        "name": "Reduce in-app confusion around SIP status and failed instalments",
        "description": "Debited-but-not-invested, failed mandate, unclear SIP status cause worry.",
        "linked_themes": ["confusion_worry_in_app", "lack_of_visibility"],
    },
]


@dataclass
class ThemeMatch:
    theme: str
    matched_keywords: List[str]
    confidence: float  # 0-1 heuristic


def first_pass_theme_scan(text: str) -> List[ThemeMatch]:
    """Keyword-based first-pass theme detection."""
    text_l = text.lower()
    results: List[ThemeMatch] = []
    for theme, keywords in THEME_KEYWORDS.items():
        matched = [kw for kw in keywords if kw.lower() in text_l]
        if matched:
            confidence = min(0.95, 0.4 + 0.1 * len(matched))
            results.append(ThemeMatch(theme=theme, matched_keywords=matched, confidence=confidence))
    return results


def extract_segment_signals(text: str) -> Dict[str, List[str]]:
    """Lightweight segment signal extraction from text."""
    text_l = text.lower()
    signals: Dict[str, List[str]] = defaultdict(list)
    for kw in THEME_KEYWORDS["segment_income_stability"]:
        if kw.lower() in text_l:
            signals["income_stability"].append(kw)
    for kw in THEME_KEYWORDS["influence_source"]:
        if kw.lower() in text_l:
            signals["influence_source"].append(kw)
    return dict(signals)


def analyze(items: List[dict]) -> Dict[str, Any]:
    """Run the full discovery analysis over raw items."""
    total = len(items)
    theme_counts: Counter = Counter()
    theme_examples: Dict[str, List[dict]] = defaultdict(list)
    segment_rows: List[dict] = []

    for item in items:
        combined = f"{item.get('title', '')} {item.get('body', '')}"
        matches = first_pass_theme_scan(combined)
        seen_themes = set()
        for m in matches:
            theme_counts[m.theme] += 1
            seen_themes.add(m.theme)
            if len(theme_examples[m.theme]) < 6:
                theme_examples[m.theme].append({
                    "source": item.get("platform", item.get("source", "")),
                    "title": item.get("title", "")[:120],
                    "snippet": item.get("body", "")[:220],
                    "url": item.get("url", ""),
                })
        signals = extract_segment_signals(combined)
        if signals:
            segment_rows.append({
                "source": item.get("platform", item.get("source", "")),
                "signals": signals,
                "snippet": combined[:200],
            })

    # Prevalence = share of items mentioning theme
    prevalence = {t: round(c / total * 100, 1) if total else 0.0 for t, c in theme_counts.items()}

    # Opportunity scoring: impact (prevalence) x fixability (heuristic) x business alignment
    opportunity_scores = []
    for oa in OPPORTUNITY_AREAS:
        linked = oa["linked_themes"]
        avg_prev = sum(prevalence.get(t, 0) for t in linked) / max(len(linked), 1)
        max_prev = max((prevalence.get(t, 0) for t in linked), default=0)
        # fixability heuristic: how product-addressable (0-1)
        fixability = {
            "oa_settling_expectations": 0.8,
            "oa_progress_visibility": 0.85,
            "oa_pause_intervention": 0.7,
            "oa_outside_app_guidance": 0.6,
            "oa_in_app_clarity": 0.9,
        }.get(oa["id"], 0.5)
        score = round(avg_prev * 0.5 + max_prev * 0.3 + fixability * 10 * 0.2, 2)
        opportunity_scores.append({
            **oa,
            "avg_prevalence": round(avg_prev, 1),
            "max_prevalence": round(max_prev, 1),
            "fixability": fixability,
            "opportunity_score": score,
        })
    opportunity_scores.sort(key=lambda x: x["opportunity_score"], reverse=True)

    result = {
        "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
        "total_items_analyzed": total,
        "theme_prevalence": prevalence,
        "theme_counts": dict(theme_counts),
        "theme_examples": {k: v for k, v in theme_examples.items()},
        "opportunity_areas": opportunity_scores,
        "segment_sample": segment_rows[:20],
    }

    out_path = ANALYSIS_DIR / "discovery_output.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def print_summary(result: Dict[str, Any]) -> None:
    print(f"\n=== AI Discovery Engine Summary ===")
    print(f"Items analyzed: {result['total_items_analyzed']}")
    print("\n--- Theme Prevalence (% of items) ---")
    for t, p in sorted(result["theme_prevalence"].items(), key=lambda x: -x[1]):
        print(f"  {t:35s} {p:6.1f}%  (n={result['theme_counts'][t]})")
    print("\n--- Opportunity Areas (ranked) ---")
    for oa in result["opportunity_areas"]:
        print(f"  {oa['opportunity_score']:5.2f}  {oa['name']:55s}  (prev {oa['avg_prevalence']}%)")


if __name__ == "__main__":
    items = load_all_raw()
    if not items:
        print("No raw items found. Run ingest.py first to create demo data.")
    else:
        res = analyze(items)
        print_summary(res)
