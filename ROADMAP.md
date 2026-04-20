# 📘 SeeBus‑Global – Roadmap (2026)

Aktuálny plán vývoja projektu podľa reálneho stavu backendu, frontendu a vydania verzie **v1.0.0**.

Roadmapa sa priebežne aktualizuje podľa vývoja projektu.

---

## ✅ 1. Backend – Stabilizácia (HOTOVÉ)

- Event Engine (IN_TRANSIT / ARRIVING / AT_STOP / DEPARTING)
- Event Dispatcher
- Logging + Debug mód
- `/api/events/process`
- `/api/events/stream`
- GTFS loader
- GTFS‑RT loader
- Shapes loader
- Stops loader
- TrackManager (16‑track routing)
- Testy stabilizované
- Celý backend v stave **Phase 4 – stabilizované**

**Stav:** ✔ kompletne hotové

---

## 🟢 2. Frontend – Real‑Time UI (HOTOVÉ)

### 2.1 Mapové jadro
- Leaflet mapa
- Real‑time pozície vozidiel
- Smooth movement (requestAnimationFrame)
- Smooth camera (flyTo)
- Farebné trasy podľa linky
- Zastávky na trase (highlight prvej)
- Klikateľné vozidlá

### 2.2 UI komponenty
- Info panel (vyleštený)
- Message panel (farebné stavy + animácie)
- Log panel (fade‑in + ikonky)
- Jazykový prepínač (SK/EN)
- CSS polishing (animácie, tieňovanie, hover efekty)

**Stav:** ✔ hotové (v1.0.0)

---

## 🟡 3. Jazyková vrstva (PREBIEHA)

### 3.1 Backend
- parameter `lang` v API  
- načítavanie jazykových súborov  
- prepojenie s EventDispatcher  

### 3.2 Jazykové súbory
- `backend/locales/`  
- SK + EN hotové  
- ďalšie jazyky: DE, PL, HU, CZ, AT, RO, HR, SI, IT, FR, ES, PT, NL, DK, FI, SE, NO, BG, GR, LT, LV, EE, MT  

### 3.3 Hlásenia
- textové hlásenia  
- príprava na voice hlásenia  

**Stav:** 🟡 prebieha

---

## 🔵 4. Datasety dopravy (ČAKÁ)

### 4.1 MHD
- Banská Bystrica (hotové)
- Bratislava
- Košice

### 4.2 Prímestské
- BBSK
- ŽSK
- TTSK

### 4.3 Diaľkové
- Slovak Lines
- FlixBus
- RegioJet

### 4.4 Medzinárodné
- EÚ → EÚ
- EÚ → mimo EÚ

**Stav:** 🔵 čaká na jazykovú vrstvu

---

## 🔵 5. Simulátor vozidiel (ČAKÁ)

- generovanie polohy  
- testovanie eventov  
- testovanie SSE streamu  

**Stav:** 🔵 čaká na datasety

---

## 🔵 6. Dokumentácia (ČAKÁ)

- INDEX.md  
- RELEASE PLAN  
- STYLEGUIDE  
- TESTING GUIDE  
- PERFORMANCE GUIDE  
- ARCHITECTURE.md  
- MODULE MAP  

**Stav:** 🔵 čaká na stabilizáciu jazykovej vrstvy

---

## 🟢 7. Release v1.0.0 (HOTOVÉ)

- GitHub test  
- finálne úpravy  
- polished frontend  
- polished backend  
- prvý verejný release  

**Stav:** ✔ hotové

---

## 🔵 8. Release v1.1.0 (PRIPRAVUJE SA)

- rozšírená jazyková vrstva  
- nové datasety  
- UI prepínač typov dopravy  
- optimalizácie výkonu  
- príprava na mobilnú verziu  

**Stav:** 🔵 čaká na body 3–4

---

# ⭐ Vízia projektu

SeeBus‑Global smeruje k tomu, aby sa stal:

### 🚍 **Najrýchlejším open‑source real‑time dopravným systémom v EÚ**
- okamžité eventy  
- nízka latencia  
- čistá architektúra  

### 🌍 **Multijazyčná platforma pre všetky krajiny EÚ**
- 24 jazykov  
- jednotné hlásenia  
- pripravené na voice engine  

### 📡 **Univerzálny dopravný engine**
- MHD  
- prímestské  
- diaľkové  
- medzinárodné  

### 📱 **Budúca mobilná verzia**
- vibrácie  
- navigácia  
- offline režim  

### 🧩 **Modulárny systém**
- backend moduly  
- frontend moduly  
- dataset moduly  

---

# ⭐ Záver

Aktuálny fokus: **jazyková vrstva + datasety**  
Projekt je po vydaní **v1.0.0** v stave pripravenom na rýchlu expanziu.

