# Road-trip roadbook mode

Separate net driving time from sightseeing. The default maximum is six net driving hours per day. Add planned driver rests, food/toilet stops, fuel or charging, parking, road-surface and altitude notes, vehicle constraints, alternative roads, and observable stop conditions. Flag night driving and non-paved sections explicitly.

Required day fields: `driving_segments`, `fuel_or_charge`, `parking`, and `stop_conditions`.

```json
{"trip":{"primary_mode":"road_trip"},"days":[{"driving_segments":[{"duration_min":180}],"fuel_or_charge":["county station"],"parking":["hotel lot"],"stop_conditions":[{"trigger":"road closure","action":"use signed detour"}]}]}
```
