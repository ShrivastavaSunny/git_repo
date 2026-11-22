import fs from 'node:fs/promises'

const url = 'https://itunes.apple.com/in/rss/customerreviews/id=1032480595/sortBy=mostRecent/json'
const response = await fetch(url)
if (!response.ok) throw new Error(`Apple reviews failed: ${response.status}`)

const data = await response.json()
const entries = (data.feed.entry || []).filter((entry) => entry['im:rating'])
const reviews = entries.map((entry) => ({
  source: 'Apple App Store',
  rating: Number(entry['im:rating'].label),
  title: entry.title?.label || '',
  text: entry.content?.label || '',
  date: entry.updated?.label || '',
  url: `https://apps.apple.com/in/app/urban-company-home-services/id1032480595`,
}))

await fs.mkdir('public/data', { recursive: true })
await fs.writeFile('public/data/apple_reviews.json', JSON.stringify(reviews, null, 2))
console.log(`Exported ${reviews.length} Apple App Store reviews`)
