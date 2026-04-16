# SeaBus Global

SeaBus Global is a real-time, voice-guided public transport assistant designed for blind and visually impaired users, seniors, and international tourists.  
It provides precise arrival notifications, stop detection, multilingual support, and both voice and text announcements for maximum accessibility.

## 🎯 Mission
To make public transport fully accessible for everyone — regardless of vision, age, language, or orientation skills.

## 🌍 Key Features
- Real-time bus and tram arrival tracking (GTFS-RT)
- Voice announcements with precise timing (“arriving”, “at stop”, “doors open”, “departing”)
- Text announcements for deaf and hard-of-hearing users
- Automatic stop detection based on GPS
- Multilingual interface and voice output
- High-contrast, simple UI for seniors
- Vibration alerts for critical moments (arrival, boarding, departure)

## 👥 Target Users
- Blind and visually impaired users  
- Seniors  
- Tourists and foreign visitors  
- People with anxiety or orientation difficulties  
- Anyone who wants a hands-free transit assistant  

## 🧠 How It Works
SeaBus Global connects to real-time public transport data (GTFS-RT) and uses:
- GPS tracking  
- ETA prediction algorithms  
- State detection (moving, stopping, door events)  
- Voice synthesis  
- Text rendering  
- Vibration patterns  

to deliver precise, reliable, and accessible transit information.

---

## ⚡ Event Logic (Arrival, Stop, Departure)

SeaBus Global uses a precise event‑detection engine to determine what the vehicle is doing in real time.  
This enables accurate voice, text, and vibration alerts for blind and visually impaired users.

### 1. ARRIVING
Triggered when the vehicle is approaching the stop.

**Conditions:**
- Distance to stop is between 40 m and 120 m  
- Vehicle is moving faster than 3 km/h  
- Distance is decreasing (approaching)

**Action:**
- Voice: “Bus {line} is arriving.”  
- Vibration: short double pulse  

---

### 2. AT_STOP
Triggered when the vehicle reaches the stop and remains stationary.

**Conditions:**
- Distance < 15 m  
- Speed < 1 km/h  
- State lasts at least 2 seconds  

**Action:**
- Voice: “Bus {line} is at the stop.”  
- Vibration: long single pulse  

---

### 3. DEPARTING
Triggered when the vehicle leaves the stop.

**Conditions:**
- Previous state was AT_STOP  
- Speed rises above 3 km/h  
- Distance from stop begins to increase  

**Action:**
- Voice: “Bus {line} is departing.”  
- Vibration: short triple pulse  

---

### 4. MISSED (optional)
Triggered when the user remains at the stop but the bus leaves.

**Conditions:**
- AT_STOP → DEPARTING sequence occurred  
- User’s GPS position remains at the stop  
- No boarding confirmation  

**Action:**
- Voice: “Bus {line} has left.”  

---

## 🛠 Planned Architecture
- **Backend API** (Python / FastAPI)
- **GTFS-RT Processor**
- **Arrival Prediction Engine**
- **Voice & Text Announcement Engine**
- **Mobile App (Android first)**
- **Multilingual Module**
- **Accessibility Layer (Voice, Text, Vibration)**

## 🚀 Roadmap
- [ ] Define core modules  
- [ ] Build GTFS-RT parser  
- [ ] Implement arrival prediction  
- [ ] Create voice announcement engine  
- [ ] Add vibration patterns  
- [ ] Build Android prototype  
- [ ] Add multilingual support  
- [ ] Public beta release  

## 📄 License
To be added (MIT recommended).

---

SeaBus Global — because public transport should be accessible to everyone.
