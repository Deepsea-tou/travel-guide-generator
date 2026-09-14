---
name: travel-roadbook
description: Use when a user asks to plan, generate, revise, or publish a leisure trip, city break, food trip, hiking itinerary, mountain route, or road trip as an actionable travel guide or roadbook.
---

# Travel Roadbook

Create a sourced, executable plan whose route, pace, safety decisions, and fallbacks still work on the road. Produce a modern offline HTML roadbook plus Markdown, ICS, GeoJSON, normalized JSON, and a quality report.

## Start with the request

Use the current request as the highest-priority input. Infer low-risk details when reasonable; ask only when a missing date, traveler constraint, or safety choice would materially change the plan. For long trips over 14 days, suggest logical segments.

Choose one primary mode and load only its reference:

- City, food, architecture, museum, slow travel: [city-roadbook.md](references/city-roadbook.md)
- Trail, mountain, hiking, race: [hiking-roadbook.md](references/hiking-roadbook.md)
- Self-drive, camper, long-distance road trip: [road-trip-roadbook.md](references/road-trip-roadbook.md)

For mixed trips, keep one primary mode and add only the necessary secondary module. Read [data-model.md](references/data-model.md) when creating or migrating structured input.

## Personal context and privacy

Local knowledge is optional and read-only. Use it only when the user supplied or authorized a directory. Read [personal-knowledge.md](references/personal-knowledge.md), then pass that directory with `--knowledge-root`; never copy raw notes into the repository or output.

Priority is: explicit current request → hard safety rules → derived long-term preferences → generic defaults. Turn goals into observable constraints: “少排队” needs off-peak timing and alternatives; “少搬酒店” prefers one base unless a move has a clear, explained benefit.

Default to `personal`. For anything intended to be sent, posted, or published, read [privacy-and-sharing.md](references/privacy-and-sharing.md) and build with `--scope share`. Do not call an output share-safe if the privacy scan fails.

## Research and truthfulness

Research current transport, opening, closure, price, weather, and road/trail conditions. Follow [research-and-freshness.md](references/research-and-freshness.md). Prefer primary sources; record source ids and verification dates. Never turn a search snippet, ordinary map estimate, or memory into a precise current fact. When a critical hiking or driving fact is unknown, mark it unknown and reduce the plan's commitment instead of inventing certainty.

## Build and verify

1. Construct schema v2 data using [roadbook-schema.json](references/roadbook-schema.json).
2. Build: `python3 scripts/build_roadbook.py INPUT.json --output OUTPUT_BASE [--knowledge-root DIR] [--scope personal|share]`.
3. Resolve validation errors. Explain warnings or conflicts that remain.
4. Open the HTML and verify desktop, mobile, interactions, print, and mode-specific safety content. The page must remain readable without JavaScript or network access.

Mode-required fields and share privacy checks are blocking errors, not warnings. Do not deliver the affected artifact until they pass.

An Amap key is optional. Without it, retain clearly labeled offline estimates. Never expose keys or cookies.

## Deliver

Lead with clickable artifact links, then summarize the route, daily rhythm, food/stay logic, budget, important verification actions, and safety/fallback decisions. Keep local delivery paths outside the content of a public share version.

Preserve the legacy `scripts/build_guide.py` path for v1 inputs; use `build_roadbook.py` for all new work.
