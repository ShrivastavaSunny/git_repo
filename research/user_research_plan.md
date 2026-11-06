# User Research Plan — Groww SIP Retention

## Target segment
First-time mutual fund investors, age 22–30, early-career / irregular income (salaried juniors, freelancers, gig workers), started SIP ≤ ₹1,000/month on Groww, influenced by friends or YouTube, currently in months 3–8 of their first SIP (active, paused, or lapsed).

## Methodology
- **5–6 semi-structured interviews**, 45 minutes each, remote video
- **Recruitment:** via Reddit r/IndiaInvestments + personal network; screener to confirm first-time SIP status and income type
- **No PII collected:** no account numbers, PAN, phone numbers, or portfolio screenshots
- **Informed consent:** recorded with permission; transcript de-identified
- **Analysis:** thematic coding against discovery-engine themes; validate/challenge AI findings

## Interview guide

### 1. Origin story (why they started)
- Tell me about when you first started your SIP. What prompted it?
- Who or what influenced you to start? (friend, YouTube, ad, family)
- What amount did you choose, and why that amount?
- What did you expect to happen after 3 months? After 12 months?

### 2. Experience since starting
- Walk me through what happened after your first instalment.
- How often do you check your SIP in the app? What do you look at?
- How do you feel when you open the SIP screen?
- Have you ever received a notification about your SIP? What did it say?

### 3. Pause / reduce / stop consideration
- Have you ever paused, reduced, or considered stopping your SIP? Walk me through that moment.
- What was happening in your life / finances at that time?
- What did the app let you do — and what did it NOT let you do?
- If you paused/stopped, did you try to restart? What was that like?

### 4. Checking behaviour & feelings
- On a typical month, when do you check your investments? What triggers it?
- When you see a red/negative month, what goes through your head?
- What do you do when you're unsure whether to continue?

### 5. Outside-app behavior
- When you're unsure about your SIP, where do you go outside the app? (Google, YouTube, WhatsApp group, family)
- What do you ask? Whose answer do you trust most?
- Has outside advice ever made you want to change your SIP?

### 6. What would help you continue
- What would make it easier to keep your SIP going through a tight month?
- If the app could do one thing differently to help you stay, what would it be?
- (Show MVP prototype) — walk through concept; react.

## Research ethics & guardrails
- No investment advice given by interviewer
- No account/PAN/portfolio data requested
- If user asks "which fund should I pick," redirect to official Groww help / SEBI investor education

---

## Illustrative findings (from 6 simulated interviews)

These findings are illustrative, structured to match the research guide. In a real execution they would be replaced by actual transcripts.

| # | Persona | Income | Started | Status at interview | Key insight |
|---|---------|--------|---------|---------------------|-------------|
| P1 | Ravi, 24 | Salaried junior (₹28k/mo) | SIP ₹500, month 5 | Active but considering pause | Started because friend said "start early." After 4 months portfolio +1.5%. Doesn't know if that's good. Checks weekly. "No one told me the first year could be flat." |
| P2 | Meena, 26 | Freelance designer | SIP ₹1000, month 7 | Paused month 5 | Income comes in bursts. Missed 2 debits. App only offered "stop," not "skip this month." Stopped entirely. "I wanted a break, not a breakup." |
| P3 | Arjun, 23 | Gig worker (delivery) | SIP ₹500, month 6 | Lapsed (no debit 60 days) | Forgot SIP existed. No reminder before debit. Bank balance low on debit date, failed silently. Never restarted. |
| P4 | Sana, 27 | Salaried (₹42k/mo) | SIP ₹1000, month 8 | Active | Checks daily. Anxious on red days. Brother (investor) told her "don't check daily." App sends daily NAV push. "I don't know what I'm looking at." |
| P5 | Karthik, 25 | Freelance dev | SIP ₹1500, month 4 | Active | Started after YouTube video promising 12%. Month 4 shows -3%. Asked WhatsApp group — mixed advice. Considering stop. "The app never said returns could be negative in year 1." |
| P6 | Divya, 24 | Salaried junior | SIP ₹500, month 9 | Active | Started ₹500, never increased. Doesn't know how to increase. Feels SIP is "set and forget" but also wonders if she's missing something. |

### What validated the discovery engine
- Pause vs. stop gap confirmed (P2: "wanted a break, not a breakup") — engine flagged this at 85.7% prevalence
- Irregular income makes fixed monthly debit hard (P2, P5) — engine flagged segment_income_stability
- Outside-app advice when unsure (P5 WhatsApp group) — engine flagged outside_app_behavior
- Expectation mismatch from YouTube (P5) — engine flagged expectation_mismatch

### What challenged / added to the discovery engine
- **Silent lapse from insufficient funds** (P3): engine under-weighted technical debit failure as a continuation breaker; users don't "choose" to stop, the debit just fails and nothing prompts them.
- **Daily-check anxiety from push notifications** (P4): engine's keyword lexicon missed emotional language ("anxious"); push notifications actively drive harmful checking frequency.
- **"Set and forget" without guidance** (P6): users don't know they *can* or *should* review/increase — a gap not captured by pause/stop themes.

## Synthesis
Continuation breaks down not when markets fall, but when (a) the product offers no middle ground between "pay every month" and "stop forever," (b) irregular income causes silent debit failures that no one flags, and (c) users see flat/negative short-term returns with no explanation that year 1 is volatile. The moment to solve: **months 3–6, when the first flat/negative statement arrives and the user considers pausing.**
