/**
 * Optional live LLM proxy (Mistral). Used only when MISTRAL_API_KEY is set in
 * environment variables. Otherwise the app runs fully in demo mode client-side.
 * Never returns investment advice; the client-side eval gate re-checks output.
 */
export const runtime = "edge"

export async function POST(req: Request) {
  try {
    const { userInput } = await req.json()
    if (!userInput || typeof userInput !== "string") {
      return new Response(JSON.stringify({ error: "userInput required" }), { status: 400, headers: { "content-type": "application/json" } })
    }

    const apiKey = process.env.MISTRAL_API_KEY
    if (!apiKey) {
      return new Response(JSON.stringify({ error: "no live LLM key configured" }), { status: 501, headers: { "content-type": "application/json" } })
    }

    const system =
      "You are a helpful, neutral assistant inside an investing app. The user is thinking of pausing their SIP. " +
      "Do NOT recommend any fund, stock, or specific investment. Do NOT use fear, FOMO, or urgency. " +
      "Do NOT present this as investment advice. Keep responses short, reflective, and encourage the user to decide " +
      "for themselves. Suggest checking the SIP status/debit date, pausing one month, or speaking to support. " +
      "End with a disclaimer that this is not investment advice."

    const resp = await fetch("https://api.mistral.ai/v1/chat/completions", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: "mistral-tiny",
        messages: [
          { role: "system", content: system },
          { role: "user", content: userInput },
        ],
        temperature: 0.3,
        max_tokens: 300,
      }),
    })

    if (!resp.ok) {
      return new Response(JSON.stringify({ error: "llm request failed" }), { status: 502, headers: { "content-type": "application/json" } })
    }

    const data = await resp.json()
    const text = data.choices?.[0]?.message?.content || ""
    return new Response(JSON.stringify({ text }), { headers: { "content-type": "application/json" } })
  } catch {
    return new Response(JSON.stringify({ error: "unexpected error" }), { status: 500, headers: { "content-type": "application/json" } })
  }
}
