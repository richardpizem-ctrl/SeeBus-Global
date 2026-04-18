# 📘 SeeBus‑Global – Roadmap (2026)

Kompletný plán vývoja projektu, rozdelený do logických etáp.  
Roadmapa sa priebežne aktualizuje podľa stavu projektu.

---

## ✅ 1. Backend – Stabilizácia (HOTOVÉ)

- Event Engine  
- Event Dispatcher  
- Logging  
- `/api/events/process`  
- `/api/events/stream`  
- main.py integrácia  
- testy stabilizované  
- __init__.py doplnené  
- GTFS loader  
- GTFS‑RT loader  
- TrackManager (16‑track routing pre autobusy)  

**Stav:** ✔ kompletne hotové

---

## 🟡 2. Jazyková vrstva (PREBIEHA)

Cieľ: podpora všetkých 24 jazykov EÚ + angličtiny.

### 2.1 Backend
- parameter `lang` v API  
- načítavanie jazykových súborov  
- prepojenie s EventDispatcher  

### 2.2 Jazykové súbory
- vytvoriť `backend/locales/`  
- 24 jazykov EÚ  
- každý jazyk = 1 JSON súbor  

### 2.3 Prepojenie s hláseniami
- textové hlásenia  
- príprava na voice hlásenia  

**Stav:** 🟡 prebieha

---

## 🔵 3. Frontend – Základné UI (ČAKÁ)

### 3.1 Prepínač jazykov
- SK / EN / DE / PL / HU / …  
- uloženie do localStorage  
- posielanie `lang` do API  

### 3.2 Prepínač typu dopravy
- MHD  
- Prímestské  
- Diaľkové  
- Medzinárodné  

### 3.3 SSE listener
- EventSource  
- real‑time eventy  
- zobrazovanie hlásení  

**Stav:** 🔵 čaká na jazykovú vrstvu

---

## 🔵 4. Datasety dopravy (ČAKÁ)

### 4.1 MHD
- Banská Bystrica  
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

**Stav:** 🔵 čaká na UI prepínače

---

## 🔵 5. Simulátor vozidiel (ČAKÁ)

- generovanie polohy  
- testovanie eventov  
- testovanie SSE streamu  

**Stav:** 🔵 čaká na jazykovú vrstvu

---

## 🔵 6. Dokumentácia (ČAKÁ)

- INDEX.md  
- RELEASE PLAN  
- STYLEGUIDE  
- TESTING GUIDE  
- PERFORMANCE GUIDE  
- ARCHITECTURE.md  
- MODULE MAP  

**Stav:** 🔵 čaká na finalizáciu backendu

---

## 🔵 7. Release v1.0.0 (ČAKÁ)

- GitHub test  
- finálne úpravy  
- prvý verejný release  
- čakáme na prvú organickú ⭐  

**Stav:** 🔵 čaká na body 2–6

---

## ⭐ Záver

Táto roadmapa definuje jasný smer projektu a poradie krokov.  
Aktuálny fokus: **jazyková vrstva (24 jazykov EÚ + EN)**.
