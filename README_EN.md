# Travel Roadbook

An actionable travel-roadbook skill built on the original structured validation, route estimation, and multi-format export pipeline. It adds optional local preference adaptation, dedicated city/hiking/road-trip modes, share sanitization, and a redesigned offline TravelOS HTML experience.

## Highlights

- City mode: area clustering, off-peak choices, rest windows, rain alternatives, and a single lodging base by default
- Hiking mode: ascent/descent, supplies, retreat points, latest-pass times, and observable stop conditions
- Road-trip mode: net driving time, driver breaks, fuel/charging, parking, fallback roads, and stop conditions
- Optional local profile: reads only an explicitly supplied directory and emits derived signals, never raw notes
- Personal/share scopes: share data is recursively sanitized before any format is rendered
- One offline HTML file with responsive/print layouts, checklists, time shifting, and editable budgets
- Markdown, ICS, GeoJSON, normalized JSON, and quality report exports

## Build

```bash
python3 scripts/build_roadbook.py examples/hangzhou-city-3d.json \
  --output generated/hangzhou-roadbook \
  --scope share
```

Optional local context:

```bash
python3 scripts/build_roadbook.py trip.json \
  --output generated/my-trip \
  --knowledge-root /path/to/travel-framework \
  --scope personal
```

Outputs: `.html`, `.md`, `.ics`, `.geojson`, `.normalized.json`, and `.quality.json`.

## Privacy and compatibility

Never commit real knowledge files, personal profiles, names, private events, booking data, or API keys. Use `--scope share` for publication and review every output format; exact tracks can also be sensitive.

Legacy schema `1.0` and `scripts/build_guide.py` remain supported. New roadbooks use schema `2.0` and `scripts/build_roadbook.py`. Amap is optional; without a key, the build uses clearly labeled offline estimates.

## Test

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
npm install
npm run test:browser
```
