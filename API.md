# Changelog – SeeBus‑Global

Všetky významné zmeny v projekte SeeBus‑Global sú zaznamenané v tomto súbore.
Projekt používa semantické verzovanie: MAJOR.MINOR.PATCH.

## [Unreleased]
- Plánované zlepšenia robustnosti GTFS‑RT a fallback spracovania.
- Rozšírené prístupové funkcie v oznámeniach a UI.
- Rozšírené API odpovede pre pokročilé klientské integrácie.
- Interné refaktoringy pre lepšiu udržiavateľnosť a výkon.

## [1.0.0] – 2026‑04‑20
### Pridané
- Prvá stabilná verzia SeeBus‑Global.
- Spracovanie GTFS‑RT v reálnom čase a normalizácia dát.
- Načítanie a cache statických GTFS dát (linky, trasy, zastávky, kalendáre).
- Engine na párovanie trás a zastávok (TripMatcher, StopMatcher).
- Výpočet ETA kombinujúci statické a real‑time dáta.
- Engine detekcie udalostí:
  - ARRIVAL_IMMINENT
  - AT_STOP
  - DEPARTING
  - MISSED_TRIP
  - APPROACHING_DESTINATION
  - TRANSFER_SOON
- Vrstva oznámení:
  - formátovanie textových hlásení
  - integrácia TTS cez adaptér
- Webový klient:
  - základné prístupné UI pre výber cesty a zobrazenie stavu
  - vysokokontrastné štýly a veľké ovládacie prvky
- Používateľské profily a prístupové nastavenia (jazyk, verbóznosť, typ výstupu)
- Základná konfigurácia pre nasadenie backendu

### Opravené
- N/A (prvá stabilná verzia)

### Odstránené
- N/A (prvá stabilná verzia)
