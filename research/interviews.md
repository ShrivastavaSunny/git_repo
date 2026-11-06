# User Research — 6 Interviews (First-time SIP Investors)

**Product:** Groww
**Segment:** First-time mutual fund investors, age 22–30, early-career / irregular income, SIP ≤ ₹1,000/month, influenced by friends or YouTube, months 3–8 of first SIP.
**Method:** 6 semi-structured remote video interviews, 45 minutes each.
**Recruitment:** Reddit r/IndiaInvestments + personal network, with a screener confirming first-time SIP status.
**Ethics:** No account numbers, PAN, phone numbers, or portfolio screenshots collected. Informed consent obtained; transcripts de-identified. Interviewer gave no investment advice.

| # | Pseudonym | Age | Income | SIP | Month | Status at interview |
|---|-----------|-----|--------|-----|-------|---------------------|
| P1 | Ravi | 24 | Salaried junior (₹28k/mo) | ₹500 | 5 | Active, considering pause |
| P2 | Meena | 26 | Freelance designer | ₹1,000 | 7 | Paused month 5, then stopped |
| P3 | Arjun | 23 | Gig worker (delivery) | ₹500 | 6 | Lapsed (no debit 60 days) |
| P4 | Sana | 27 | Salaried (₹42k/mo) | ₹1,000 | 8 | Active, daily checker |
| P5 | Karthik | 25 | Freelance dev | ₹1,500 | 4 | Active, considering stop |
| P6 | Divya | 24 | Salaried junior | ₹500 | 9 | Active |

---

## P1 — Ravi, 24, salaried junior, ₹500 SIP, month 5
**Why started:** A friend said "start early, compounding works." Chose ₹500 because it felt small enough not to miss.
**Expectations:** Expected to see "some growth" by month 3; after 4 months portfolio is +1.5%. "I don't know if that's good or bad — no one told me the first year could be flat."
**Checking:** Weekly. Watches the SIP screen.
**Pause/stop consideration:** Has considered pausing because the return looks flat and he isn't sure it's working.
**Outside app:** Asked a colleague who said "equity takes time." Trusts the colleague more than the app.
**What would help:** "If the app told me what to expect in year 1, I wouldn't worry so much."

## P2 — Meena, 26, freelance designer, ₹1,000 SIP, month 7
**Why started:** Friend influence; started with ₹1,000.
**Expectations:** Hoped for steady growth.
**Experience:** Income comes in bursts. Missed 2 monthly debits (months 4 and 5). When she tried to resume, the app only offered "stop," not "skip this month" or "pause." She stopped entirely.
**Quote:** "I wanted a break, not a breakup."
**Outside app:** Asked a WhatsApp group; got mixed advice (some said stop, some said continue).
**What would help:** A "pause this one month" option so a tight month doesn't become a permanent stop.

## P3 — Arjun, 23, gig worker, ₹500 SIP, month 6
**Why started:** Saw a YouTube ad; started ₹500.
**Experience:** Forgot the SIP existed. No reminder before the debit date. On the debit date his bank balance was low, the debit failed silently, and nothing prompted him. Never restarted.
**Status:** Lapsed — no successful instalment in 60 days.
**Outside app:** Didn't ask anyone; just let it go.
**What would help:** A reminder before the debit and a retry nudge when a debit fails.

## P4 — Sana, 27, salaried, ₹1,000 SIP, month 8
**Why started:** Brother (an investor) suggested it.
**Experience:** Checks daily. Anxious on red days. Her brother told her "don't check daily," but the app sends daily NAV push notifications.
**Quote:** "I don't know what I'm looking at. Every red day I wonder if I should stop."
**Outside app:** Asks her brother; trusts him.
**What would help:** Context on what a normal month looks like; fewer panic-inducing notifications.

## P5 — Karthik, 25, freelance dev, ₹1,500 SIP, month 4
**Why started:** YouTube video promising "12% returns."
**Expectations:** Expected ~12% quickly.
**Experience:** Month 4 shows −3%. Asked a WhatsApp group — got mixed advice. Considering stopping.
**Quote:** "The app never said returns could be negative in year 1."
**Outside app:** WhatsApp group (mixed, often wrong).
**What would help:** The app setting realistic expectations at onboarding ("year 1 can be negative").

## P6 — Divya, 24, salaried junior, ₹500 SIP, month 9
**Why started:** Friend suggested SIP; started ₹500.
**Experience:** Never increased the SIP. Feels it's "set and forget" but wonders if she's missing something. Doesn't know how to increase or review.
**Status:** Active but passive.
**Outside app:** Hasn't asked anyone.
**What would help:** A simple review/nudge to increase the SIP as income grows.

---

## Synthesis

**What the interviews validated from the discovery engine:**
- Pause vs. stop gap confirmed (P2: "wanted a break, not a breakup") — engine flagged this at high prevalence.
- Irregular income makes fixed monthly debit hard (P2, P5) — engine flagged segment_income_stability.
- Outside-app advice when unsure (P5 WhatsApp group; P1 colleague; P4 brother) — engine flagged outside_app_behavior.
- Expectation mismatch from YouTube (P5) — engine flagged expectation_mismatch.

**What the interviews added to the discovery engine:**
- **Silent lapse from insufficient funds** (P3): a failed debit ends the SIP with no reminder or retry nudge — not a choice to stop.
- **Daily-check anxiety driven by push notifications** (P4): the app itself encourages harmful checking frequency.
- **"Set and forget" without review guidance** (P6): users don't know they can or should review/increase.

**Continuation breaks down not because markets fall, but because:**
(a) the product offers no middle ground between "pay every month" and "stop forever,"
(b) irregular income causes silent debit failures no one flags,
(c) users see flat/negative short-term returns with no explanation that year 1 is volatile.

**Moment to solve:** months 3–6, when the first flat/negative statement arrives and the user considers pausing.
