# Changelog

All notable changes to **SeeBus‑Global** will be documented in this file.  
This project follows semantic versioning: `MAJOR.MINOR.PATCH`.

---

## [Unreleased]

- Planned improvements to GTFS‑RT robustness and fallback handling
- Additional accessibility refinements in announcements and UI
- Extended API responses for advanced client integrations
- Internal refactors to improve maintainability and performance

---

## [1.0.0] – 2026-04-20

### Added
- Initial stable release of **SeeBus‑Global**
- Real‑time GTFS‑RT ingestion and normalization
- Static GTFS loading and caching (routes, trips, stops, calendars)
- Trip and stop matching engine (`TripMatcher`, `StopMatcher`)
- ETA computation engine combining static and real‑time data
- Event detection engine for:
  - arrival imminent
  - at stop
  - departing
  - missed trip
  - approaching destination
  - transfer soon
- Announcement layer:
  - text announcement formatting
  - TTS integration via pluggable adapter
- Web client:
  - basic accessible UI for journey selection and status display
  - high‑contrast styles and large interactive elements
- User profile and accessibility settings (language, verbosity, output mode)
- Initial deployment configuration for backend runtime

### Fixed
- N/A (first stable release)

### Removed
- N/A (first stable release)
