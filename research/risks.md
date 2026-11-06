# Risks & Mitigation — SIP Pause Coach

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Users ignore the coach | Medium | Medium | Place the coach at the pause/stop decision point in the flow; keep the interaction under 60 seconds; make it opt-out at the pause screen. |
| AI drifts into investment advice / fear-FOMO-urgency | Low | High | Hard eval gate runs before any output; unsafe drafts are replaced with a safe fallback + official links (Groww support, SEBI investor education); human review of low-confidence outputs. |
| Low adoption | Medium | Medium | Integrate into the existing SIP pause flow (no new destination); keep the copy short and reflective, not promotional. |
| Golden-set bias (eval only covers known cases) | Medium | Low | Refresh the golden set quarterly; add failure cases from real sessions to the eval; route confidence < 0.6 outputs to human review. |
| Users treat the coach as advice anyway | Low | Medium | Prominent "not investment advice" disclaimer at top of every screen; no fund names ever appear; clear copy that the decision is theirs. |
| Silent debit failures still cause lapses | Medium | Medium | Coach addresses paused-forgotten SIPs; pair with a separate product fix for failed-debit retry nudges (out of MVP scope). |
| Regulation / compliance (SEBI) around AI in investing | Low | High | The coach deliberately gives no investment advice and says so; routes account-specific questions to Groww support / SEBI portal; legal review before scale. |

## Most important risk
The coach addresses the **behavioural moment of doubt**, but a large share of lapses come from **technical debit failure** (insufficient funds, invalid mandate) that the user never chooses. Mitigation: pair the coach with a product fix for failed-debit retry and pre-debit reminders; measure B3 (passive lapse) as a guardrail.
