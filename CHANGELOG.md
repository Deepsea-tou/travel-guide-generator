# Changelog

All notable changes to this project are documented in this file.

## [0.1.0.0] - 2026-09-14

### Added

- Generate modern offline TravelOS roadbooks for city breaks, hiking trips, and road trips.
- Build six coordinated outputs: normalized JSON, quality report, HTML, Markdown, ICS, and GeoJSON.
- Derive reusable travel preferences from allowlisted local notes without copying raw private content or local paths.
- Apply mode-specific planning rules for relaxed city pacing, hiking safety, and driving limits.
- Ship three sanitized examples and an accessible interactive HTML experience with checklists, time shifting, budget editing, print support, responsive layouts, and themed visual systems.

### Changed

- Reframed the original travel guide generator as a concise, reusable `travel-roadbook` skill while preserving the legacy build workflow.
- Updated Chinese and English documentation around the v2 data model, source freshness, privacy boundaries, and output workflow.

### Fixed

- Block invalid mode data and unchecked share artifacts before any files are exported.
- Prevent direct export callers from bypassing validation or publishing unsanitized data.
- Detect local paths, nested private fields, image metadata gaps, and sensitive values copied into unrelated fields.
- Improved mobile touch targets and interaction states without changing the editorial visual direction.
