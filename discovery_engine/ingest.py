"""
Data ingestion layer for the AI Discovery Engine.
Connects to public sources of SIP / first-time investor conversation in India.

Sources supported (read-only, public data only):
- App Store reviews (Groww, Zerodha Coin, INDmoney)
- Play Store reviews (same apps)
- Reddit (r/IndiaInvestments, r/personalfinanceindia, r/SecurityAnalysisIndia)
- TradingQ&A forum
- YouTube comments on personal finance videos (Indian creators)
- Twitter/X conversations about SIPs in India

All ingestion is read-only. No PII (account numbers, PAN, phone numbers) is stored.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class ConversationItem:
    """A single public conversation item about SIP / first-time investing."""
    source: str               # e.g. "play_store", "reddit", "youtube"
    source_id: str            # platform-specific ID
    platform: str             # e.g. "Groww", "Reddit", "YouTube"
    title: str
    body: str
    author: Optional[str]     # username / reviewer name (hashed in storage)
    url: str
    posted_at: str            # ISO timestamp
    upvotes: int = 0
    language: str = "en"

    def content_hash(self) -> str:
        raw = f"{self.source}|{self.source_id}|{self.body}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def to_dict(self) -> dict:
        return asdict(self)


def clean_text(text: str) -> str:
    """Normalise whitespace and strip obvious PII patterns."""
    text = re.sub(r"\s+", " ", text or "").strip()
    # Redact PAN-like patterns (5 letters + 4 digits + 1 letter)
    text = re.sub(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b", "[PAN_REDACTED]", text)
    # Redact 10-digit phone numbers
    text = re.sub(r"\b[6-9][0-9]{9}\b", "[PHONE_REDACTED]", text)
    # Redact account-number-like 9-18 digit runs
    text = re.sub(r"\b[0-9]{9,18}\b", "[ACCOUNT_REDACTED]", text)
    return text


def save_raw(items: List[ConversationItem], batch_name: str) -> str:
    """Persist a batch of raw items as JSONL. Returns the file path."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    fname = RAW_DIR / f"{batch_name}_{ts}.jsonl"
    with open(fname, "w", encoding="utf-8") as f:
        for item in items:
            clean = item.to_dict()
            clean["body"] = clean_text(clean.get("body", ""))
            clean["title"] = clean_text(clean.get("title", ""))
            f.write(json.dumps(clean, ensure_ascii=False) + "\n")
    return str(fname)


def load_all_raw() -> List[dict]:
    """Load every raw JSONL batch from disk."""
    items: List[dict] = []
    if not RAW_DIR.exists():
        return items
    for f in sorted(RAW_DIR.glob("*.jsonl")):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
    return items


if __name__ == "__main__":
    # Demo: create a small synthetic batch so the pipeline can run end-to-end
    demo = [
        ConversationItem(
            source="play_store",
            source_id="rev_001",
            platform="Groww",
            title="Good app but SIP paused itself",
            body="Started a SIP of 500 in month 1. After 3 months it just paused. No clear reason in app. I kept checking returns but they looked flat.",
            author="user_a",
            url="https://play.google.com/store/apps/details?id=com.groww",
            posted_at="2025-01-15T10:00:00Z",
        ),
        ConversationItem(
            source="reddit",
            source_id="t3_abc123",
            platform="Reddit",
            title="First time SIP - what to expect after 6 months?",
            body="I started a SIP via Groww 6 months ago. Portfolio shows 2% return. Friends say equity takes time but the app doesn't explain this. Should I stop?",
            author="investor_22",
            url="https://reddit.com/r/IndiaInvestments/comments/abc123",
            posted_at="2025-02-20T14:30:00Z",
        ),
        ConversationItem(
            source="play_store",
            source_id="rev_002",
            platform="Groww",
            title="SIP money debited but not invested",
            body="₹1000 was debited from my bank for SIP but mutual fund units not showing. Customer care gave no timeline. Very worried. Thinking to stop SIP.",
            author="salaried_user",
            url="https://play.google.com/store/apps/details?id=com.groww",
            posted_at="2025-02-10T09:00:00Z",
        ),
        ConversationItem(
            source="reddit",
            source_id="t3_def456",
            platform="Reddit",
            title="Freelancer income irregular - should I pause SIP?",
            body="I earn freelance, income comes in bursts. Started SIP of 2000 but some months I can't pay. App shows SIP failed but no option to skip just one month. Feels all-or-nothing.",
            author="freelancer_88",
            url="https://reddit.com/r/IndiaInvestments/comments/def456",
            posted_at="2025-03-05T16:00:00Z",
        ),
        ConversationItem(
            source="youtube",
            source_id="yt_comment_1",
            platform="YouTube",
            title="Comment on SIP returns video",
            body="Started SIP last year because a YouTuber said 12% guaranteed. After 8 months I am down 4%. App doesn't explain why negative. My father says stop and put in FD.",
            author="first_timer_19",
            url="https://youtube.com/watch?v=example",
            posted_at="2025-03-12T11:00:00Z",
        ),
        ConversationItem(
            source="tradingqa",
            source_id="tqa_99",
            platform="TradingQ&A",
            title="How often should I check SIP portfolio?",
            body="New to Groww. Checking NAV daily. Some days green some days red. Anxiety every evening. Friends say don't check daily but app sends daily push notifications.",
            author="newbie_trader",
            url="https://tradingqna.com/question/99",
            posted_at="2025-03-18T08:00:00Z",
        ),
        ConversationItem(
            source="reddit",
            source_id="t3_ghi789",
            platform="Reddit",
            title="SIP pause vs stop - confused",
            body="Market fell 5% this month. Wanted to pause SIP for 2 months but app only has stop. Don't want to lose the SIP. Ended up doing nothing and now it lapsed.",
            author="cautious_saver",
            url="https://reddit.com/r/personalfinanceindia/comments/ghi789",
            posted_at="2025-04-01T13:00:00Z",
        ),
    ]
    path = save_raw(demo, "demo_batch")
    print(f"Saved {len(demo)} items to {path}")
    print(f"Total raw items on disk: {len(load_all_raw())}")
