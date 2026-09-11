# Travel Roadbook v2 data model

`schema_version` is `2.0`. `meta` describes the trip and output theme. `trip.primary_mode` is `city`, `hiking`, or `road_trip`; `secondary_modes` adds only relevant modules. `days` keeps the compatible timed `items` array and adds mode-specific safety or comfort fields.

`personalization` contains derived signals and named rules, never raw local notes. `privacy.output_scope` is `personal` or `share`; `sensitive_fields` names fields that must be removed from a share build. `quality` stores stable validation codes, warnings, schedule conflicts, and the overall status.

Sources use stable ids. Current facts set `dynamic: true` and provide `verified_at`; estimates set `estimated: true`. Records reference them through `source_ids`.

The v1 migration keeps unknown extension fields, moves `preferences.primary_mode` into `trip`, adds empty privacy/personalization/quality objects, and does not mutate the input. The legacy `build_guide.py` contract remains available.

The v2 build produces `.normalized.json`, `.quality.json`, `.html`, `.md`, `.ics`, and `.geojson`. Share scope sanitizes the structured data before every format is rendered.
