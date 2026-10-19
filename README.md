# Save the Date

A single static page: names, date, place, countdown, add-to-calendar, three photos. No backend.
Shares the look (and the EN / 한국어 toggle) of the main wedding site in `../rsvp-bot`.

Preview locally:

```bash
python3 -m http.server 8080
```

then open http://localhost:8080.

Edit the words in `script.js` (both languages are at the top), the photos in `photos/`, and the
calendar event in `save-the-date.ics`. To host it, upload the folder as-is to Netlify, GitHub
Pages, Cloudflare Pages or any static host.
