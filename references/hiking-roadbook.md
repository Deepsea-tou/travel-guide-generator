# Hiking roadbook mode

Use for trails, mountains, races, or trips where terrain controls the day. Record distance, ascent, descent, surface, moving-time range, buffer, supplies, water, retreat points, latest-pass times, weather exposure, mandatory gear, and observable stop conditions. Safety conditions override preference scores.

Required day fields: `elevation`, `supplies`, `retreat_points`, and `stop_conditions`.

```json
{"trip":{"primary_mode":"hiking"},"days":[{"elevation":{"ascent_m":900},"retreat_points":["cable station"],"stop_conditions":[{"trigger":"thunder","action":"descend"}]}]}
```
