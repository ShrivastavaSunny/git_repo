# Urban Company Repeat-Booking Discovery

A greenfield prototype for the 90-day repeat-booking product challenge.

## Public deliverables

- [Production MVP and Discovery Engine](https://dist-pink-one-67.vercel.app/)
- [AI Evidence Log](https://dist-pink-one-67.vercel.app/evidence.html)
- [10-slide deck PDF](https://dist-pink-one-67.vercel.app/NL_UrbanCompany_RepeatBooking.pdf)
- [Interview recruitment and protocol](https://dist-pink-one-67.vercel.app/research/recruitment.md)

## Public deliverables

- [Production MVP and Discovery Engine](https://dist-pink-one-67.vercel.app/)
- [AI Evidence Log](https://dist-pink-one-67.vercel.app/evidence.html)
- [10-slide deck PDF](https://dist-pink-one-67.vercel.app/NL_UrbanCompany_RepeatBooking.pdf)

## Run

```bash
npm install
npm run export:evidence
npm run dev
```

The app contains:

- **Home Care Plan**: a customer-side 90-day planning MVP that never books, messages, scrapes or changes an account.
- **Discovery Engine**: paste customer statements or load 50 public Apple App Store reviews for transparent opportunity classification.

## Research plan

- Recruit 6 adults who completed a core Urban Company booking in the last 6 months.
- Include 3 people who completed another booking within 90 days and 3 who did not.
- Cover more than one service category across respondents.
- Record household role and total booking count.
- Collect no screenshots, invoices, addresses, phone numbers or account details.

## Evidence

- `public/data/apple_reviews.json`: 50 public Apple App Store India reviews.
- `public/evidence.html`: sources, volume, golden-set and correction log.
- `public/deck.html`: printable 10-slide deck.
