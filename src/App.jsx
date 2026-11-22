import { useMemo, useState } from 'react'
import './App.css'

const services = [
  { id: 'ac', name: 'AC service', icon: '❄', recurring: 'Every 6–12 months', reason: 'Seasonal cooling and filter maintenance' },
  { id: 'clean', name: 'Deep clean', icon: '✦', recurring: 'Every 3–6 months', reason: 'Seasonal or post-event cleaning' },
  { id: 'plumber', name: 'Plumbing', icon: '💧', recurring: 'As symptoms appear', reason: 'Leaks or draining problems' },
  { id: 'salon', name: 'Salon at home', icon: '✂', recurring: 'Every 3–8 weeks', reason: 'Personal care schedule' },
  { id: 'pest', name: 'Pest control', icon: '◉', recurring: 'Every 3–6 months', reason: 'Prevention or a visible issue' },
]

const opportunityRules = [
  { key: 'service_clarity', label: 'Need clarity', pattern: /(leak|ac|cool|clean|dust|pest|appointment|service)/i, weight: 3 },
  { key: 'memory_gap', label: 'Remembering when to act', pattern: /(forgot|remember|remind|don't know|dont know|later|when)/i, weight: 3 },
  { key: 'trust', label: 'Professional trust', pattern: /(trust|professional|technician|partner|quality|safe|damaged)/i, weight: 2 },
  { key: 'control', label: 'Schedule & control', pattern: /(time|late|delay|slot|cancel|reschedule|date)/i, weight: 2 },
  { key: 'price', label: 'Price expectations', pattern: /(price|cost|expensive|cheap|discount|coupon|pay)/i, weight: 2 },
]

function classify(text) {
  const hits = opportunityRules
    .map((rule) => ({ ...rule, score: rule.pattern.test(text) ? rule.weight : 0 }))
    .filter((rule) => rule.score > 0)
  return hits.length ? hits : [{ key: 'other', label: 'Other / mixed', score: 1, weight: 1 }]
}

function App() {
  const [route, setRoute] = useState('mvp')
  return (
    <main>
      <nav>
        <button className={route === 'mvp' ? 'active' : ''} onClick={() => setRoute('mvp')}>Home Care Plan</button>
        <button className={route === 'engine' ? 'active' : ''} onClick={() => setRoute('engine')}>Discovery Engine</button>
        <a href="./evidence.html" target="_blank" rel="noreferrer">Evidence Log</a>
        <a href="./deck.html" target="_blank" rel="noreferrer">Deck</a>
      </nav>
      {route === 'mvp' ? <Mvp /> : <Engine />}
    </main>
  )
}

function Mvp() {
  const [selected, setSelected] = useState([])
  const [household, setHousehold] = useState('1–2 residents')
  const [completed, setCompleted] = useState([])
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10))

  function toggle(id) {
    setSelected((current) => current.includes(id) ? current.filter((x) => x !== id) : [...current, id])
  }

  const plan = useMemo(() => {
    if (!selected.length) return []
    return selected.map((id) => {
      const service = services.find((item) => item.id === id)
      const base = id === 'ac' ? 180 : id === 'clean' ? 120 : id === 'salon' ? 28 : id === 'pest' ? 120 : 30
      const due = new Date(`${date}T12:00:00`)
      due.setDate(due.getDate() + base)
      return { ...service, due: due.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) }
    })
  }, [selected, date])

  function markDone(id) {
    setCompleted((current) => [...current, id])
  }

  return (
    <div className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">HOME CARE PLAN · PRIVATE TO THIS DEVICE</p>
          <h1>Turn “we should get that done” into one clear next step.</h1>
          <p className="lede">A customer-side planner for the next 90 days. It never books, contacts, or changes anything in Urban Company.</p>
        </div>
        <div className="household">
          <label>Household
            <select value={household} onChange={(e) => setHousehold(e.target.value)}>
              <option>1–2 residents</option><option>Family with children</option><option>Shared home / flatmates</option><option>Senior residents</option>
            </select>
          </label>
        </div>
      </header>

      <section className="grid">
        <div className="card">
          <h2>1. What matters in your home?</h2>
          <p className="muted">Choose only things you already know need attention.</p>
          <div className="choices">
            {services.map((service) => (
              <button key={service.id} className={selected.includes(service.id) ? 'choice chosen' : 'choice'} onClick={() => toggle(service.id)}>
                <span className="icon">{service.icon}</span>
                <span><strong>{service.name}</strong><small>{service.reason}</small></span>
                <span className="check">{selected.includes(service.id) ? '✓' : '+'}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>2. Anchor the plan</h2>
          <p className="muted">When was the latest home-service problem or visit?</p>
          <label className="date-label">Date
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
          <div className="principle"><strong>Need check</strong><span>Only recurring or symptom-based tasks are suggested. The plan pauses when no need is chosen.</span></div>
        </div>
      </section>

      {plan.length > 0 && (
        <section className="card plan">
          <div className="plan-title"><div><p className="eyebrow">YOUR 90-DAY VIEW</p><h2>One calm view, no noise</h2></div><span>{household}</span></div>
          <div className="timeline">
            {plan.map((item) => (
              <div className={completed.includes(item.id) ? 'task done' : 'task'} key={item.id}>
                <span className="icon">{item.icon}</span>
                <div><strong>{item.name}</strong><small>Suggested window: {item.due}</small></div>
                <button onClick={() => markDone(item.id)}>{completed.includes(item.id) ? 'Added to my list ✓' : 'Mark handled'}</button>
              </div>
            ))}
          </div>
          <p className="disclaimer">General planning prompt only. This is not a diagnosis or a recommendation to purchase a service. Customer data stays in this browser session.</p>
        </section>
      )}
    </div>
  )
}

function Engine() {
  const [text, setText] = useState('')
  const [rows, setRows] = useState([])
  const [source, setSource] = useState('Customer transcript')

  async function loadPublicSample() {
    const response = await fetch('./data/apple_reviews.json')
    const reviews = response.ok ? await response.json() : []
    setRows(reviews.map((item) => ({ source: item.source, text: `${item.title} ${item.text}`, rating: item.rating, date: item.date, url: item.url })))
  }

  function analyze() {
    const items = text.split('\n').map((x) => x.trim()).filter(Boolean)
    setRows((current) => [
      ...items.map((x) => ({ source, text: x, rating: null, date: 'User supplied', url: null })),
      ...current,
    ])
  }

  const opportunities = useMemo(() => {
    const totals = {}
    rows.forEach((row) => classify(row.text).forEach((hit) => { totals[hit.label] = (totals[hit.label] || 0) + hit.score }))
    return Object.entries(totals).sort((a, b) => b[1] - a[1]).slice(0, 6)
  }, [rows])

  return (
    <div className="shell engine">
      <header className="engine-head"><p className="eyebrow">AI DISCOVERY ENGINE · PUBLIC + CUSTOMER-SUPPLIED</p><h1>From noise to comparable customer opportunities</h1></header>
      <section className="grid">
        <div className="card">
          <h2>Gather</h2>
          <select value={source} onChange={(e) => setSource(e.target.value)}>
            <option>Customer transcript</option><option>App review</option><option>Community post</option><option>Complaint forum</option><option>YouTube comment</option>
          </select>
          <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder={'Paste one customer statement per line…'} />
          <div className="actions"><button className="primary" onClick={analyze}>Analyze text</button><button onClick={loadPublicSample}>Load 50 public Apple reviews</button></div>
        </div>
        <div className="card">
          <h2>Opportunity comparison</h2>
          {opportunities.length ? opportunities.map(([label, score]) => (
            <div className="bar-row" key={label}><span>{label}</span><div><i style={{ width: `${Math.min(100, score / Math.max(...opportunities.map((x) => x[1]), 1) * 100)}%` }} /></div><b>{score}</b></div>
          )) : <p className="muted">Load or paste evidence to begin.</p>}
          <p className="method">Transparent rules identify stated needs, trust, control, price, and memory gaps. Negative public selection is disclosed; silent non-returners require first-party follow-up.</p>
        </div>
      </section>
      <section className="card evidence-table">
        <h2>Evidence ({rows.length})</h2>
        {rows.slice(0, 30).map((row, index) => (
          <article key={index}>
            <span className={`source ${row.source === 'Apple App Store' ? 'apple' : ''}`}>{row.source}{row.rating ? ` · ${row.rating}★` : ''}</span>
            <p>{row.text}</p>
            <div>{classify(row.text).map((hit) => <mark key={hit.key}>{hit.label}</mark>)}</div>
          </article>
        ))}
      </section>
    </div>
  )
}

export default App
