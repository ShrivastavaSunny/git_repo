export const metadata = {
  title: "SIP Pause Coach — Groww",
  description: "Eval-gated AI continuation coach for first-time SIP investors. Not investment advice.",
}
export const viewport = {
  width: "device-width",
  initialScale: 1,
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
