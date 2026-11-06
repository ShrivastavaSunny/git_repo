# Business Metric Decomposition — Groww

## North-star metric
**% of first-time mutual fund investors who still have an active SIP 12 months after starting their first SIP**
- Active SIP = at least one successful instalment in the last 30 days
- Cohort: investors whose *first-ever* SIP was started on Groww

## Decomposition tree

```
12-month SIP continuation (first-time investors)
│
├─ A. First-instalment success (Month 0→1)
│   ├─ Mandate registration success (NACH/eMandate)
│   ├─ First debit executed without failure
│   └─ User confirms SIP is "active" after first debit
│
├─ B. Instalment continuity (Months 1–11)
│   ├─ B1. Each monthly debit succeeds (technical)
│   │   ├─ Sufficient balance on debit date
│   │   ├─ Mandate remains valid (not expired/revoked)
│   │   └─ Bank/npi downtime handled with retry
│   ├─ B2. User does not actively pause/stop (behavioural)
│   │   ├─ No pause action taken
│   │   ├─ No stop/redeem action taken
│   │   └─ No "skip month" requested (where offered)
│   └─ B3. User does not passively lapse (forgotten/insufficient funds silent fail)
│
├─ C. Perception & expectation durability (Months 1–12)
│   ├─ C1. Returns experience matches expectations set at onboarding
│   ├─ C2. User understands short-term volatility is normal
│   └─ C3. User sees progress/meaning between instalments
│
└─ D. Re-activation after a lapse (Months 1–12)
    ├─ Lapsed SIP detected (>=30 days since last instalment)
    ├─ Re-activation prompt delivered
    └─ New mandate/debit executed
```

## Product outcomes that influence continuation

| Outcome | What it means | Levers in product | Evidence signal (from discovery engine) |
|---------|---------------|-------------------|--------------------------------------|
| O1. Mandate & first-debit reliability | First SIP debit succeeds and user sees units | eMandate flow, retry on failed debit, instant confirmation | "SIP instalment failed, no retry option" (confusion_worry_in_app) |
| O2. Monthly debit success rate | Every instalment debits & invests | Balance-aware debit date, grace-period retry, insufficient-funds alert | Freelancer irregular income; pause because can't pay some months |
| O3. No active pause/stop | User doesn't choose to exit | Graceful pause (skip 1 month), market-dip framing, easy restart | "Wanted to pause but only stop available"; "SIP paused itself" |
| O4. No passive lapse | User doesn't forget / silently drop | Reminders before debit, in-app SIP health dashboard, 30-day lapse alert | "Forgot about SIP, realised it paused 2 months ago" |
| O5. Expectation durability | Returns experience matches what user was told | Onboarding expectation-setting, volatility bands, first-year range | "YouTuber said 12% guaranteed, now down 4%"; "Expected quick returns" |
| O6. Progress visibility | User sees meaning between instalments | SIP progress tracker, compounding illustration, milestone badges | "Portfolio shows 2% return"; "Platform flat after 4 months" |
| O7. Re-activation after lapse | Lapsed users resume | Win-back flow, simplified re-mandate, "resume in 2 taps" | "SIP stopped, how to restart?" |

## Where the highest-potential opportunities lie

Discovery engine ranked opportunity areas:

1. **Intervene before pause / reduce / stop** — 55.69 score (57.2% max prevalence)
   - Root: users want to *pause* (temporary) but app only offers *stop* (permanent); irregular income makes monthly commitment hard
2. **Make SIP progress visible and meaningful between instalments** — 37.88 (38.1%)
   - Root: users check and see flat/negative short-term returns; no sense of compounding progress
3. **Set realistic first-year return expectations** — 36.58 (35.7%)
   - Root: influencers promise 12% "guaranteed"; first red month triggers doubt

**Selected opportunity:** O3 (no active pause/stop) + O6 (progress visibility), focused on **first-time investors with irregular or early-career income** who started a small SIP and hit a flat/negative first few months. This is where continuation breaks down despite good intent — not because markets fell, but because the product offers no middle ground between "pay every month" and "stop forever," and shows no progress to sustain motivation.

## Chosen target segment
First-time mutual fund investors, age 22–30, early-career / irregular income (salaried juniors, freelancers, gig workers), started SIP ≤ ₹1,000/month, influenced by friends/YouTube, within months 3–8 of their first SIP.
