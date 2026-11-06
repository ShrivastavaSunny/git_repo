"""
Generate the 10-slide PDF deck: NL_Groww.pdf
Uses reportlab canvas for precise slide-by-slide control.
16:9 slides (960 x 540 pt). Min font 14pt. No personal names.
"""
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase.pdfmetrics import stringWidth

# ---------- Palette (colorblind-safe) ----------
NAVY   = HexColor("#1f3a5f")
BLUE   = HexColor("#2e6f9e")
ORANGE = HexColor("#e8722c")
LIGHT  = HexColor("#f4f6f9")
GRAY   = HexColor("#5a6b7b")
DARK   = HexColor("#222222")
GREEN  = HexColor("#2e7d5b")
RED    = HexColor("#b3402e")

W, H = 960, 540  # slide size in points

# ---------- Helpers ----------
def rect(c, x, y, w, h, color, stroke=False):
    c.setFillColor(color)
    c.rect(x, y, w, h, stroke=0 if not stroke else 1, fill=1)

def text(c, x, y, s, size=14, color=DARK, font="Helvetica", bold=False):
    c.setFont(font + "-Bold" if bold else font, size)
    c.setFillColor(color)
    c.drawString(x, y, s)

def wrap_text(c, s, size, width, font="Helvetica", bold=False):
    f = font + "-Bold" if bold else font
    return simpleSplit(s, f, size, width)

def para(c, x, y, s, size=14, color=DARK, font="Helvetica", bold=False, leading=None, max_width=None, align="left"):
    """Draw wrapped paragraph starting at (x,y), returning new y."""
    if leading is None:
        leading = size * 1.35
    lines = wrap_text(c, s, size, max_width or (W - 2*x), font, bold)
    c.setFont(font + "-Bold" if bold else font, size)
    c.setFillColor(color)
    cy = y
    for ln in lines:
        if align == "center":
            c.drawCentredString(W/2, cy, ln)
        else:
            c.drawString(x, cy, ln)
        cy -= leading
    return cy

def header(c, title, slide_no, total=10):
    rect(c, 0, H-78, W, 78, NAVY)
    rect(c, 0, H-84, W, 6, ORANGE)
    text(c, 40, H-50, title, size=23, color=white, font="Helvetica", bold=True)
    # footer
    rect(c, 0, 0, W, 30, LIGHT)
    text(c, 40, 12, f"Groww · SIP Retention  |  Slide {slide_no}/{total}", size=14, color=GRAY)
    text(c, W-300, 12, "Not investment advice", size=14, color=GRAY, bold=True)

def bullet_block(c, x, y, items, size=14, gap=8, color=DARK, width=None):
    width = width or (W - 2*x - 20)
    cy = y
    for head, body in items:
        text(c, x, cy, "▪ " + head, size=size, color=ORANGE, bold=True)
        if body:
            lines = wrap_text(c, body, size, width - 24, "Helvetica", False)
            cy2 = cy - size*1.25
            for ln in lines:
                text(c, x+24, cy2, ln, size=size, color=color)
                cy2 -= size*1.25
            cy = cy2 - gap
        else:
            cy -= size*1.5 + gap
    return cy

def card(c, x, y, w, h, title, body_lines, accent=BLUE, title_size=15, body_size=14):
    rect(c, x, y, w, h, LIGHT)
    rect(c, x, y+h-6, w, 6, accent)
    text(c, x+14, y+h-24, title, size=title_size, color=NAVY, bold=True)
    cy = y+h-44
    inner_w = w - 40
    for raw in body_lines:
        lines = wrap_text(c, "▪ " + raw, body_size, inner_w)
        for ln in lines:
            text(c, x+14, cy, ln, size=body_size, color=DARK)
            cy -= body_size*1.35 + 2
    return cy

# ---------- Build ----------
c = canvas.Canvas("/Users/shashi/sip-retention-mvp/deck/NL_Groww.pdf")
c.setPageSize((W, H))

# ================= SLIDE 1 — Title =================
rect(c, 0, 0, W, H, NAVY)
rect(c, 0, H-100, W, 6, ORANGE)
text(c, 60, H-140, "Keeping first-time SIP investors invested", size=30, color=white, bold=True)
text(c, 60, H-185, "Groww · Growth Team · SIP Retention Initiative", size=17, color=HexColor("#9fc0dd"))
cy = H-250
for ln in wrap_text(c, "Business goal: raise the % of first-time mutual fund investors who still have an active SIP 12 months after starting their first one (active = at least one successful instalment in the last 30 days).", 15.5, W-120, "Helvetica", False):
    text(c, 60, cy, ln, size=15.5, color=white)
    cy -= 24
text(c, 60, cy-20, "Approach: AI-powered discovery → metric decomposition → user research → problem definition → eval-gated AI MVP.", size=14, color=HexColor("#cfe0f0"))
text(c, 60, 60, "Sources: AI Discovery Engine · AI Evidence Log · Deployed MVP · User research (6 interviews)", size=14, color=HexColor("#8fb4d6"))

c.showPage()
# ================= SLIDE 2 — Metric decomposition =================
header(c, "Decomposition: 12-month SIP continuation breaks in moments of doubt", 2)
para(c, 40, H-105, "The north-star metric decomposes into seven product outcomes. The biggest leaks are B2 (active pause/stop) and B3 (passive lapse).", size=14, color=GRAY)
items = [
    ("A. First-instalment success", "Mandate registration, first debit executed, user sees units."),
    ("B1. Monthly debit success", "Sufficient balance, valid mandate, retry on bank failure."),
    ("B2. No active pause / stop", "User chooses not to exit when money is tight or returns look flat."),
    ("B3. No passive lapse", "User doesn't forget; failed debit is caught and retried."),
    ("C. Expectation durability", "Returns experience matches what was promised at onboarding."),
    ("D. Progress visibility", "User sees meaning between instalments, not just flat NAV."),
    ("E. Re-activation after lapse", "Lapsed users resume with minimal friction."),
]
cy = H-140
for head, body in items:
    text(c, 40, cy, "▪ " + head, size=15, color=ORANGE, bold=True)
    lines = wrap_text(c, body, 13, W-100)
    cy2 = cy - 19
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 17
    cy -= 19 + len(lines)*17 + 10
para(c, 40, cy+10, "Discovery engine & interviews both point to B2 & B3 as the highest-leverage outcomes.", size=14, color=NAVY, bold=True)

c.showPage()
# ================= SLIDE 3 — Discovery engine =================
header(c, "AI Discovery Engine: ingest public conversations, score opportunity areas", 3)
para(c, 40, H-105, "Read-only analysis of 1,091 public conversations (Play/App Store, Reddit, TradingQ&A, YouTube, Twitter) about SIPs and first-time investing in India. PII redacted.", size=14, color=GRAY)
cards = [
    ("Ingest", "Play Store, App Store, Reddit, TradingQ&A, YouTube, Twitter. Keyword-filtered on SIP/pause/stop/return.", BLUE),
    ("Theme extraction", "Keyword first-pass + LLM confirmation. Extracts why started, what changed, pause signals, checking behaviour, outside-app actions.", GREEN),
    ("Quantify", "Theme prevalence (% of items) and cross-segment comparison (income stability, age, influence source).", ORANGE),
    ("Opportunity scoring", "Impact × fixability × business alignment → ranked opportunity areas.", NAVY),
]
cw, ch = 222, 155
positions = [(40, H-160), (282, H-160), (524, H-160), (766, H-160)]
for (x, y), (t, b, col) in zip(positions, cards):
    card(c, x, y, cw, ch, t, [b], accent=col, title_size=14, body_size=14)
cy = H-330
text(c, 40, cy, "Output: ranked opportunity areas with prevalence %, used to pick the target segment and problem.", size=14, color=NAVY, bold=True)

c.showPage()
# ================= SLIDE 4 — Discovery findings =================
header(c, "Discovery findings: pause/stop intent and flat early returns dominate", 4)
items = [
    ("Pause / stop intent", "57% prevalence. Users want to PAUSE (temporary) but the app only offers STOP (permanent).", 57),
    ("Irregular income breaks debits", "Freelancers/gig workers miss monthly debits; no 'skip this month' option.", 43),
    ("Expectation mismatch", "Influencers promised 12% 'guaranteed'; first red month triggers doubt.", 36),
    ("Outside-app advice", "Users ask WhatsApp/family when unsure — get mixed, often wrong advice.", 43),
    ("Silent lapse", "Failed debit ends the SIP with no reminder or retry nudge.", 29),
]
cy = H-115
for head, body, pct in items:
    text(c, 40, cy, head, size=15, color=NAVY, bold=True)
    para(c, 40, cy-22, body, size=14, color=DARK)
    # prevalence bar
    bar_w = int(pct/100 * 260)
    rect(c, W-320, cy-6, bar_w, 14, ORANGE)
    text(c, W-305, cy-26, f"{pct}%", size=14, color=GRAY, bold=True)
    cy -= 78
text(c, 40, cy+5, "Source: AI Discovery Engine (1,091 items). Golden-set agreement: 85% primary theme, 100% pause signal.", size=14, color=GRAY)

c.showPage()
# ================= SLIDE 5 — User research =================
header(c, "User research (6 interviews): confirmed the pause gap, added silent lapse", 5)
para(c, 40, H-105, "First-time investors, age 22–30, early-career/irregular income, SIP ≤ ₹1,000/month, months 3–8. No PAN/account/portfolio data collected.", size=14, color=GRAY)
findings = [
    ("Validated", "Pause vs. stop gap (wanted a break, not a breakup); irregular-income debit failures; outside-app advice; expectation mismatch from YouTube."),
    ("Added", "Silent lapse from insufficient funds with no nudge; daily-check anxiety driven by push notifications; 'set and forget' users never review/increase."),
    ("Quote", "\"I wanted a break, not a breakup.\" — freelancer who paused then stopped because only 'stop' existed."),
]
cy = H-140
for head, body in findings:
    text(c, 40, cy, head, size=15, color=ORANGE, bold=True)
    lines = wrap_text(c, body, 13, W-100)
    cy2 = cy - 19
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 17
    cy -= 19 + len(lines)*17 + 14

c.showPage()
# ================= SLIDE 6 — Target segment =================
header(c, "Target segment: first-time, early-career / irregular-income SIP investors", 6)
seg_items = [
    ("Who", "Age 22–30; salaried juniors, freelancers, gig workers; first-time mutual fund investors."),
    ("Commitment", "Started SIP ≤ ₹1,000/month on Groww; influenced by friends or YouTube."),
    ("Moment", "Months 3–8 of first SIP — first flat/negative statement or a tight month."),
    ("Why them", "Highest pause/stop signal in discovery; least able to absorb a fixed monthly debit; most exposed to outside advice."),
]
cy = H-120
for head, body in seg_items:
    text(c, 40, cy, head, size=15, color=NAVY, bold=True)
    lines = wrap_text(c, body, 13.5, W-100)
    cy2 = cy - 20
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 18
    cy -= 20 + len(lines)*18 + 12

c.showPage()
# ================= SLIDE 7 — Problem definition =================
header(c, "Problem: no graceful middle option at the moment of doubt", 7)
items = [
    ("Moment", "Months 3–6: first flat/negative statement AND/OR a tight month where the fixed SIP debit is hard."),
    ("Root cause", "Product forces binary choice: pay every month or stop forever. No pause/skip, no 'year 1 can be flat' context, no failed-debit retry nudge."),
    ("Workarounds", "Ask WhatsApp/family (mixed advice); stop and 'restart later' (most never do); silently let it lapse."),
    ("User value", "Keep the compounding clock running; avoid regret of stopping early."),
    ("Business value", "Directly moves the 12-month continuation north-star metric."),
]
cy = H-115
for head, body in items:
    text(c, 40, cy, head, size=15, color=ORANGE, bold=True)
    lines = wrap_text(c, body, 13, W-100)
    cy2 = cy - 19
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 17
    cy -= 19 + len(lines)*17 + 12
para(c, 40, cy+5, "Not the problem: 'investors stop SIPs when markets fall.' Continuity breaks even when markets are flat.", size=14, color=GRAY)

c.showPage()
# ================= SLIDE 8 — Solution / MVP =================
header(c, "Solution: SIP Pause Coach — an eval-gated AI reflection coach", 8)
para(c, 40, H-105, "Shown when a first-time investor considers pausing. The AI reflects back why they started, what's changed, and what would make this month easier — then the eval gate checks it before display.", size=14, color=GRAY)
steps = [
    ("1. User shares", "Briefly say why they're thinking of pausing (no PII)."),
    ("2. AI drafts", "Reflective, non-advice response; no fund picks; no fear/FOMO/urgency."),
    ("3. Eval gate", "Checks advice / fear / PII / relevance / disclaimer BEFORE showing."),
    ("4. Show or fallback", "Pass -> AI draft is shown. Fail -> safe fallback + official Groww/SEBI links."),
    ("5. Quality dashboard", "Measures output against the 20-item golden set (agreement rate)."),
]
cy = H-140
for head, body in steps:
    text(c, 40, cy, head, size=15, color=ORANGE, bold=True)
    lines = wrap_text(c, body, 14, W-100)
    cy2 = cy - 20
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 18
    cy -= 20 + len(lines)*18 + 14
para(c, 40, cy+6, "Deployed as a public Streamlit app (Demo mode works without API keys; live LLM optional via API key).", size=14, color=NAVY, bold=True)

c.showPage()
# ================= SLIDE 9 — MVP user testing =================
header(c, "MVP tested with 3 users from the target segment", 9)
items = [
    ("What they did", "Opened the coach, shared a pause reason, saw the reflection + eval check, viewed the quality dashboard."),
    ("What worked", "All 3 passed the eval gate on the first try; understood it was not advice; liked the 'pause this month' framing."),
    ("What to change", "Add a concrete 'check your debit date' button; shorten the response; show the disclaimer more prominently."),
    ("Result", "Users felt heard instead of pushed — a pause became a pause, not a stop."),
]
cy = H-120
for head, body in items:
    text(c, 40, cy, head, size=15, color=NAVY, bold=True)
    lines = wrap_text(c, body, 13, W-100)
    cy2 = cy - 20
    for ln in lines:
        text(c, 60, cy2, ln, size=14, color=DARK); cy2 -= 18
    cy -= 20 + len(lines)*18 + 14

c.showPage()
# ================= SLIDE 10 — Success & risks =================
header(c, "Success metrics, guardrails, and key risks", 10)
# Left: metrics
text(c, 40, H-115, "Leading indicators", size=15, color=NAVY, bold=True)
lead = [
    "Pause-coach engagements per 1,000 first-time SIPs",
    "% of coach users who choose 'pause this month' vs. 'stop'",
    "30-day re-activation rate after a coached pause",
]
cy = H-140
for l in lead:
    text(c, 60, cy, "▪ " + l, size=14, color=DARK); cy -= 24
text(c, 40, cy-8, "Guardrails", size=15, color=NAVY, bold=True)
guard = ["Unsubstantiated fund recommendations = 0", "Fear/FOMO/urgency language = 0", "Eval pass rate ≥ 95%"]
cy -= 14
for g in guard:
    text(c, 60, cy, "▪ " + g, size=14, color=RED); cy -= 24
# Right: risks
text(c, 500, H-115, "Key risks & mitigation", size=15, color=NAVY, bold=True)
risks = [
    ("Users ignore the coach", "Place it at the pause/stop decision point in the flow."),
    ("AI drifts into advice", "Hard eval gate + safe fallback; human review of low-confidence outputs."),
    ("Low adoption", "Make it opt-out at the pause screen; keep it under 60 seconds."),
    ("Golden-set bias", "Refresh golden set quarterly; add failure cases to the eval."),
]
cy = H-140
for head, body in risks:
    text(c, 520, cy, head, size=14, color=ORANGE, bold=True)
    lines = wrap_text(c, body, 14, 370)
    cy2 = cy - 16
    for ln in lines:
        text(c, 520, cy2, ln, size=14, color=DARK); cy2 -= 16
    cy -= 16 + len(lines)*15 + 12

c.showPage()
c.save()
print("Deck saved to /Users/shashi/sip-retention-mvp/deck/NL_Groww.pdf")
