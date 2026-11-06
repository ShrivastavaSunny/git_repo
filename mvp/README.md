# SIP Pause Coach — Deployed AI-Native MVP

## What it is
An eval-gated AI continuation coach shown to first-time Groww SIP investors who are considering pausing their SIP (months 3–8). Helps the investor reflect rather than decide in a moment of doubt.

## Constraints honoured
- ✅ No fund/stock recommendations (no investment advice)
- ✅ No fear, FOMO, or urgency nudges
- ✅ Clear "not investment advice" disclaimer
- ✅ Eval gate runs before anything is shown; safe fallback on failure
- ✅ No PII collected or stored

## How the eval gate works
1. User submits why they're thinking of pausing.
2. AI drafts a reflective response (demo model by default; optional live LLM).
3. Eval gate checks the draft for: investment advice, fear/FOMO/urgency language, PII, relevance, and the disclaimer.
4. **Pass** → AI draft shown. **Fail** → safe fallback response + links to official Groww support / SEBI investor education.
5. Quality dashboard compares outputs against the 20-item golden set from the AI Evidence Log and reports agreement rate.

## Run locally
```
pip install -r requirements.txt
streamlit run mvp/app.py
```
Then open the URL Streamlit prints (typically `http://localhost:8501`).

## Deploy to production (publicly accessible)
Option A — Streamlit Cloud (free, public URL):
1. Push this folder to a public GitHub repo.
2. Go to https://streamlit.io/cloud and connect the repo.
3. Set the entry point to `mvp/app.py`.
4. Deploy. You'll get a public `https://<app>.streamlit.app` link mentors can use.

Option B — Any platform that runs Python (Heroku, Railway, Render, Fly.io):
1. `pip install -r requirements.txt`
2. `streamlit run mvp/app.py --server.port $PORT --server.address 0.0.0.0`

No API key is required (demo mode). To use a live LLM, set `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` in the environment and choose "Live LLM" in the app.

## Test task for mentors
1. Open the app.
2. Enter: "Money is tight this month and my SIP return looks negative, thinking of pausing."
3. Observe: a reflective, non-advice response is shown after passing the eval gate.
4. Open the eval expander: confirm the quality check ran.
5. Click "View quality dashboard": confirm golden-set agreement is displayed.
