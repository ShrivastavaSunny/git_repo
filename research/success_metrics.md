# Success Metrics — SIP Pause Coach

## North-star (business) metric
**% of first-time mutual fund investors who still have an active SIP 12 months after starting their first SIP.**
Active SIP = at least one successful instalment in the last 30 days. Cohort = investors whose first-ever SIP was started on Groww.

## Leading indicators (what the solution should move)
| Metric | Definition | Rationale |
|--------|------------|-----------|
| Coach engagements per 1,000 first-time SIPs | # of times a first-time investor opens the Pause Coach ÷ first-time SIPs started × 1,000 | Measures reach into the moment of doubt. |
| % of coach users who choose "pause this month" vs. "stop" | Among coach users who later act on their SIP, share who pause (not stop/redeem) | Directly measures the binary→pause shift the product enables. |
| 30-day re-activation rate after a coached pause | Share of coached-pause users with a successful instalment within 30 days | Shows pauses are temporary, not stops. |

## Guardrail metrics (must not worsen)
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Unsubstantiated fund/stock recommendations by the AI | 0 | Hard product constraint: no investment advice. |
| Fear / FOMO / urgency language in AI output | 0 | Hard product constraint: no manipulative nudges. |
| Eval pass rate | ≥ 95% | The quality gate must reliably block unsafe output. |
| Fallback rate | monitored | High fallback = the AI isn't handling real inputs; tune the model. |

## AI output quality (measured against the golden set)
- **Golden-set agreement rate:** share of the 20 hand-labelled golden-set items for which the coach's output passes/fails eval consistent with expectation (target: all benign items pass → agreement = pass rate).
- **Primary-theme agreement (discovery engine):** 85% (17/20) — from AI Evidence Log.
- **Pause-signal agreement (discovery engine):** 100% (20/20).

## How AI quality is measured
Every AI draft is run through the eval gate before display (investment advice, fear/FOMO/urgency, PII, relevance, disclaimer checks). Results are logged and compared against the 20-item golden set from the AI Evidence Log. Agreement rate is shown in the in-app quality dashboard.
