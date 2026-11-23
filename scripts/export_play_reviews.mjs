import gplay from 'google-play-scraper'
import fs from 'node:fs/promises'

const reviews = await gplay.reviews({
  appId: 'com.urbanclap.urbanclap',
  lang: 'en',
  country: 'in',
  sort: gplay.sort.NEWEST,
  num: 150,
  throttle: 10,
})
const rows = reviews.data.map((item) => ({
  source: 'Google Play Store', rating: item.score, title: item.title || '', text: item.text || '', date: item.date?.toISOString?.() || '', url: 'https://play.google.com/store/apps/details?id=com.urbanclap.urbanclap',
}))
await fs.mkdir('public/data', { recursive: true })
await fs.writeFile('public/data/play_reviews.json', JSON.stringify(rows, null, 2))
console.log(`Exported ${rows.length} Google Play reviews`)
