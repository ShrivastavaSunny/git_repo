"use client"
export default function TestMap() {
  const items = [{ id: 1, text: "a" }, { id: 2, text: "b" }]
  return (
    <div>
      {items.map((d) => (
        <div key={d.id}>{d.text}</div>
      ))}
    </div>
  )
}
