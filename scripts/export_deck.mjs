import { chromium } from 'playwright'

const browser = await chromium.launch({ headless: true })
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } })
await page.goto('http://127.0.0.1:4173/deck.html', { waitUntil: 'networkidle' })
await page.pdf({
  path: 'public/NL_UrbanCompany_RepeatBooking.pdf',
  printBackground: true,
  preferCSSPageSize: true,
  width: '1280px',
  height: '720px',
  margin: { top: '0', right: '0', bottom: '0', left: '0' },
})
await browser.close()
console.log('Exported public/NL_UrbanCompany_RepeatBooking.pdf')
