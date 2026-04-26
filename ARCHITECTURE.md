# SeeBus‑Global Architecture

## 1. High‑level overview

SeeBus‑Global is a real‑time, voice‑guided public transport assistant designed primarily for blind and visually impaired users, seniors, and international tourists. It runs as a cloud‑hosted backend with a web/mobile client and focuses on:

- **Real‑time arrival awareness** (not just static timetables)
- **Stop detection and trip progress tracking**
- **Accessible multimodal output** (voice + text + haptics)
- **Low cognitive load** for the user

At a high level, the system consists of:

- **Data ingestion layer** (GTFS‑RT, static GTFS, optional GPS feeds)
- **Core processing layer** (normalization, matching, ETA logic, event detection)
- **Announcement layer** (TTS, text, optional vibration patterns)
- **Client layer** (web/mobile UI)
- **Accessibility and configuration layer** (user profiles, language, verbosity)

---

## 2. Architectural goals

- **Accessibility‑first:** All logic je navrhnutá primárne pre nevidiacich a slabozrakých používateľov.
- **Real‑time by design:** Systém pracuje s živými dátami (GTFS‑RT, GPS), nie len so statickými cestovnými poriadkami.
- **Robustness:** Bezpečné spracovanie neúplných, oneskorených alebo nekonzistentných dát.
- **Modularita:** Jednotlivé vrstvy (ingestion, processing, events, announcements, UI) sú oddelené a rozšíriteľné.
- **Internationalization:** Podpora viacerých jazykov a lokalizačných profilov.
- **Future‑proof:** Pripravené na rozšírenie o mobilnú appku, offline režim a ďalšie dopravné systémy.

---

## 3. High‑level architecture

### 3.1 Layers

1. **Data Ingestion Layer**
   - GTFS‑RT feeds (vehicle positions, trip updates, service alerts)
   - Static GTFS (routes, trips, stops, calendars)
   - Optional GPS / device location (from client)

2. **Core Processing Layer**
   - GTFS normalizer & cache
   - Trip & stop matcher
   - ETA computation
   - Event detection engine (arrival, at_stop, departing, missed, transfer, etc.)

3. **Announcement Layer**
   - TTS engine (server‑side or client‑side)
   - Text output (screen, notifications)
   - Optional haptic patterns (mobile app / wearables)

4. **Client Layer**
   - Web UI (desktop / mobile browser)
   - Future: native Android app
   - Future: WearOS / companion devices

5. **Accessibility & Profile Layer**
   - User profiles (language, verbosity, preferred modes)
   - Output modes (voice‑only, voice+text, text‑only)
   - Safety & confirmation prompts

---

## 4. Core components

### 4.1 Data ingestion

**Responsibilities:**

- Fetch GTFS‑RT feeds in configurable intervals
- Load and cache static GTFS (routes, trips, stops)
- Normalize provider‑specific formats into internal canonical structures
- Handle network errors, timeouts, and partial data

**Key concepts:**

- `FeedFetcher` – periodic downloader for GTFS‑RT
- `GtfsStaticStore` – in‑memory / on‑disk cache of static GTFS
- `GtfsRtParser` – parser + normalizer pre real‑time dáta

---

### 4.2 Trip & stop matching

**Responsibilities:**

- Map real‑time vehicle positions and trip updates na konkrétne:
  - route
  - trip
  - stop sequence
- Určiť, kde sa používateľ nachádza v rámci svojej cesty:
  - pred nástupom
  - na palube
  - blíži sa k cieľovej zastávke
  - po vystúpení

**Key concepts:**

- `TripMatcher` – spája GTFS‑RT trip_id s GTFS trip definíciou
- `StopMatcher` – určuje najbližšiu relevantnú zastávku pre používateľa
- `UserJourney` – reprezentuje aktuálnu cestu používateľa (origin → destination)

---

### 4.3 ETA & timing engine

**Responsibilities:**

- Vypočítať odhadovaný čas príchodu (ETA) na:
  - najbližšiu zastávku
  - cieľovú zastávku
  - prestupnú zastávku
- Pracovať s:
  - plánovanými časmi (static GTFS)
  - real‑time odchýlkami (GTFS‑RT)
  - oneskoreniami a zrušenými spojmi

**Key concepts:**

- `EtaCalculator` – kombinuje plánované a real‑time dáta
- `DelayModel` – reprezentuje meškanie / odchýlku
- `ServiceStatus` – informuje o zrušených alebo presmerovaných spojoch

---

### 4.4 Event detection engine

**Responsibilities:**

- Generovať udalosti, ktoré majú zmysel pre používateľa, napr.:

  - `ARRIVAL_IMMINENT` – „Váš autobus príde o 2 minúty.“
  - `AT_STOP` – „Práve ste na zastávke X.“
  - `DEPARTING` – „Autobus odchádza.“
  - `MISSED_TRIP` – „Spoj ste nestihli.“
  - `APPROACHING_DESTINATION` – „Blížite sa k cieľovej zastávke.“
  - `TRANSFER_SOON` – „O 3 minúty prestup na linku Y.“

- Filtrovať šum a nezahlcovať používateľa zbytočnými hláškami.

**Key concepts:**

- `EventEngine` – hlavný modul, ktorý rozhoduje, kedy a čo oznámiť
- `EventRules` – konfigurovateľné pravidlá (časové prahy, vzdialenosti, priority)
- `UserState` – stav používateľa v rámci cesty (pred nástupom, na palube, po vystúpení)

---

### 4.5 Announcement layer

**Responsibilities:**

- Preklopiť interné udalosti na konkrétne výstupy:

  - hlasové hlásenie
  - text na obrazovke
  - notifikácia
  - vibrácia (v budúcnosti)

- Rešpektovať používateľské nastavenia (jazyk, hlasitosť, úroveň detailu).

**Key concepts:**

- `AnnouncementFormatter` – generuje textové hlášky z eventov
- `TtsAdapter` – integrácia s TTS (lokálna / cloudová)
- `OutputChannel` – abstrakcia pre rôzne výstupné kanály (web, mobil, wearables)

---

### 4.6 Client layer (UI)

**Responsibilities:**

- Poskytnúť jednoduché, prehľadné a prístupné rozhranie:

  - výber linky / cieľa
  - zobrazenie stavu cesty
  - zobrazenie ETA
  - zobrazenie posledných hlásení

- Byť použiteľný aj pre slabozrakých (kontrast, veľké prvky, jednoduché ovládanie).

**Key concepts:**

- `WebUI` – HTML/CSS/JS front‑end
- `ApiClient` – komunikácia s backendom
- `AccessibilityStyles` – špecifické CSS pre vysoký kontrast a veľké prvky

---

### 4.7 Accessibility & profiles

**Responsibilities:**

- Ukladať a používať preferencie používateľa:

  - jazyk
  - typ výstupu (voice/text)
  - úroveň detailu (krátke vs. podrobné hlásenia)
  - preferované dopravné módy

- Umožniť bezpečné defaulty pre nových používateľov.

**Key concepts:**

- `UserProfile` – per‑user nastavenia
- `ProfileManager` – načítanie a aplikovanie profilov
- `AccessibilityPolicy` – pravidlá pre bezpečné a zrozumiteľné hlásenia

---

## 5. Data flow

### 5.1 Typical runtime flow

1. **Data ingestion**
   - GTFS‑RT feed sa periodicky stiahne a spracuje.
   - Static GTFS je načítaný a držaný v cache.

2. **User session**
   - Používateľ zvolí linku / cieľ / smer.
   - Backend vytvorí `UserJourney`.

3. **Matching & ETA**
   - TripMatcher a StopMatcher nájdu relevantný spoj a zastávky.
   - EtaCalculator vypočíta časy príchodu / odchodu.

4. **Event detection**
   - EventEngine sleduje zmeny v ETA, polohách a stave cesty.
   - Pri splnení podmienok generuje udalosti (ARRIVAL_IMMINENT, AT_STOP, atď.).

5. **Announcements**
   - AnnouncementFormatter vytvorí text.
   - TtsAdapter (alebo text output) doručí hlásenie používateľovi.

6. **Feedback loop**
   - Používateľ môže potvrdiť / ignorovať / upraviť cestu.
   - Systém aktualizuje `UserState` a pokračuje v monitorovaní.

---

## 6. Deployment & runtime

- **Backend:** Python (napr. FastAPI / podobný framework)
- **Data:** GTFS + GTFS‑RT (HTTP(S) endpoints)
- **Clients:** Web browser (desktop / mobile), budúca Android app
- **Scaling:** Horizontálne škálovanie podľa počtu používateľov a feedov
- **Monitoring:** Logovanie chýb, latencií a kvality GTFS‑RT dát

---

## 7. Extensibility

SeeBus‑Global je navrhnutý tak, aby sa dal rozširovať bez zásahu do jadra:

- **Noví dopravcovia:** pridaním nových GTFS/GTFS‑RT konektorov.
- **Nové jazyky:** rozšírením lokalizačných súborov a TTS konfigurácie.
- **Nové zariadenia:** implementáciou nových `OutputChannel` (napr. WearOS, Bluetooth beacons).
- **Pokročilé modely ETA:** integráciou ML modelov do `EtaCalculator`.

Architektúra je modulárna a vrstvená, aby bolo možné pridávať nové funkcie bez narušenia existujúcich.

---
