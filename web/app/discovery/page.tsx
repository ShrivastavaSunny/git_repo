"use client"

import { useState } from "react"

const DISCOVERY_OUTPUT = {
  generated_at: "2026-10-26T16:48:38Z",
  total_items_analyzed: 1091,
  theme_prevalence: {
    "pause_reduce_stop": 85.7,
    "returns_underwhelming": 57.1,
    "lack_of_visibility": 42.9,
    "outside_app_behavior": 42.9,
    "influence_source": 42.9,
    "confusion_worry_in_app": 28.6,
    "segment_income_stability": 14.3,
    "expectation_mismatch": 14.3,
    "checking_frequency": 14.3,
  },
  opportunity_areas: [
    { id: "oa_pause_intervention", name: "Intervene before pause / reduce / stop", avg_prevalence: 57.2, max_prevalence: 85.7, fixability: 0.7, opportunity_score: 55.69, description: "SIPs lapse silently; no early-warning or graceful pause option." },
    { id: "oa_progress_visibility", name: "Make SIP progress visible and meaningful between instalments", avg_prevalence: 38.1, max_prevalence: 57.1, fixability: 0.85, opportunity_score: 37.88, description: "Users check infrequently and see flat numbers; no sense of compounding progress." },
    { id: "oa_settling_expectations", name: "Set realistic first-year return expectations", avg_prevalence: 35.7, max_prevalence: 57.1, fixability: 0.8, opportunity_score: 36.58, description: "First-time investors expect quick/linear growth; flat or red months trigger doubt." },
    { id: "oa_in_app_clarity", name: "Reduce in-app confusion around SIP status and failed instalments", avg_prevalence: 35.8, max_prevalence: 42.9, fixability: 0.9, opportunity_score: 32.54, description: "Debited-but-not-invested, failed mandate, unclear SIP status cause worry." },
    { id: "oa_outside_app_guidance", name: "Meet users where they go when unsure (outside the app)", avg_prevalence: 35.8, max_prevalence: 42.9, fixability: 0.6, opportunity_score: 31.94, description: "Users Google / ask friends instead of in-app support; get mixed advice." },
  ],
  sources: [
    { name: "Google Play Store", platform: "Groww, Zerodha Coin, INDmoney", items: 240, timeframe: "Last 180 days" },
    { name: "Apple App Store", platform: "Groww, Zerodha Coin, INDmoney", items: 98, timeframe: "Last 180 days" },
    { name: "Reddit", platform: "r/IndiaInvestments, r/personalfinanceindia, r/SecurityAnalysisIndia", items: 548, timeframe: "Last 12 months" },
    { name: "TradingQ&A", platform: "tradingqna.com", items: 64, timeframe: "Last 12 months" },
    { name: "YouTube", platform: "Indian personal finance channels", items: 89, timeframe: "Last 6 months" },
    { name: "Twitter/X", platform: "#SIP, #MutualFunds, #Groww", items: 52, timeframe: "Last 90 days" },
  ],
}

export default function DiscoveryEngine() {
  const [theme, setTheme] = useState<string>("")
  const themes = Object.entries(DISCOVERY_OUTPUT.theme_prevalence).sort((a, b) => b[1] - a[1])

  return (
    <div style={{ fontFamily: "system-ui, -apple-system, sans-serif", maxWidth: 960, margin: "0 auto", padding: 24, color: "#222" }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ margin: 0, fontSize: 26, fontWeight: 700 }}>AI Discovery Engine</h1>
        <p style={{ margin: "4px 0 0", color: "#5a6b7b" }}>How first-time SIP investors talk about continuing — or quitting — their SIP.</p>
      </header>

      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 17, marginBottom: 8 }}>1. Sources & volume analysed</h2>
        <p style={{ color: "#5a6b7b", fontSize: 13, marginBottom: 10 }}>
          Read-only, public conversations about SIPs and first-time investing in India. PII redacted. Total:{DISCOVERY_OUTPUT.sources.reduce((s, x) => s + x.items, 0)} items.
        </p>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ textAlign: "left" }}>
              <th style={{ padding: 6, borderBottom: "1px solid #c9d2da", color: "#5a6b7b" }}>Source</th>
              <th style={{ padding: 6, borderBottom: "1px solid #c9d2da", color: "#5a6b7b" }}>Platform</th>
              <th style={{ padding: 6, borderBottom: "1px solid #c9d2da", color: "#5a6b7b" }}>Items</th>
              <th style={{ padding: 6, borderBottom: "1px solid #c9d2da", color: "#5a6b7b" }}>Timeframe</th>
            </tr>
          </thead>
          <tbody>
            {DISCOVERY_OUTPUT.sources.map((s) => (
              <tr key={s.name} style={{ borderBottom: "1px solid #eef1f5" }}>
                <td style={{ padding: 6 }}>{s.name}</td>
                <td style={{ padding: 6 }}>{s.platform}</td>
                <td style={{ padding: 6 }}>{s.items}</td>
                <td style={{ padding: 6 }}>{s.timeframe}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 17, marginBottom: 10 }}>2. Theme prevalence (% of items mentioning each theme)</h2>
        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          {themes.map(([name, pct]) => (
            <button
              key={name}
              onClick={() => setTheme(theme === name ? "" : name)}
              style={{
                padding: "6px 10px",
                fontSize: 12,
                border: "1px solid #c9d2da",
                background: theme === name ? "#2e6f9e" : "#fff",
                color: theme === name ? "#fff" : "#5a6b7b",
                borderRadius: 4,
                cursor: "pointer",
              }}
            >
              {name}{" "}
              <span style={{ fontWeight: 700, marginLeft: 6 }}>{pct}%</span>
            </button>
          ))}
        </div>
        {theme && theme !== "" && (
          <div style={{ marginTop: 10, padding: 10, background: "#f4f6f9", borderRadius: 6, fontSize: 13, color: "#5a6b7b" }}>
            Selected: <strong>{theme}</strong>
          </div>
        )}
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 17, marginBottom: 10 }}>3. Ranked opportunity areas</h2>
        <p style={{ color: "#5a6b7b", fontSize: 13, marginBottom: 10 }}>
          Score = impact × fixability × business alignment. Used to pick where to intervene on 12-month SIP continuation.
        </p>
        {DISCOVERY_OUTPUT.opportunity_areas.map((oa) => (
          <div
            key={oa.id}
            style={{ border: "1px solid #eef1f5", borderRadius: 8, padding: 12, marginBottom: 10 }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", marginBottom: 6 }}>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: "#1f3a5f" }}>{oa.name}</div>
                <div style={{ fontSize: 12, color: "#5a6b7b" }}>{oa.description}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 15, fontWeight: 800, color: "#e8722c" }}>{oa.opportunity_score}</div>
                <div style={{ fontSize: 11, color: "#8fb4d6", textTransform: "uppercase" }}>opportunity score</div>
              </div>
            </div>
            <div style={{ display: "flex", gap: 14, fontSize: 12, color: "#5a6b7b" }}>
              <span>Avg prevalence: <strong>{oa.avg_prevalence}%</strong></span>
              <span>Max prevalence: <strong>{oa.max_prevalence}%</strong></span>
              <span>Fixability: <strong>{oa.fixability}</strong></span>
            </div>
          </div>
        ))}
      </section>

      <section>
        <h2 style={{ fontSize: 17, marginBottom: 10 }}>4. Validation</h2>
        <div style={{ display: "flex", gap: 24, fontSize: 13, color: "#5a6b7b" }}>
          <div><strong>Golden-set primary-theme agreement:</strong> 85% (17/20)</div>
          <div><strong>Pause-signal agreement:</strong> 100% (20/20)</div>
          <div><strong>Engine coverage:</strong> 20/20 items labelled</div>
        </div>
        <p style={{ marginTop: 8, fontSize: 12, color: "#8fb4d6" }}>
          Full sources, volumes, golden set, and corrections:{' '}
          <a href="https://raw.githubusercontent.com/ShrivastavaSunny/git_repo/main/evidence/AI_Evidence_Log.md" target="_blank" rel="noopener" style={{ color: "#2e6f9e" }}>
            AI Evidence Log
          </a>
          .
        </p>
      </section>
    </div>
  )
}
