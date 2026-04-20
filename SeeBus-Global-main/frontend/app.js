/* ============================================================
   SeeBus-Global – v1.0.0 Polished Frontend
   Kompletný app.js s kozmetickými úpravami
   ============================================================ */

let eventSource = null;

/* ⭐ LANGUAGE — load saved language */
const langSelect = document.getElementById("language");
langSelect.value = localStorage.getItem("lang") || "sk";

langSelect.addEventListener("change", () => {
    localStorage.setItem("lang", langSelect.value);
});

/* ⭐ MAPA — inicializácia */
const map = L.map('map').setView([48.7363, 19.1462], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

/* ⭐ MARKERS PRE VŠETKY VOZIDLÁ */
const markers = {};

/* ⭐ SELECTED VEHICLE */
let selectedVehicleId = null;

/* ⭐ POLYLINE PRE TRASU */
let currentShapePolyline = null;

/* ⭐ ZASTÁVKY NA TRASE */
let currentStopMarkers = [];

/* ⭐ FAREBNÉ TRASY PODĽA LINKY */
const routeColors = {
    "24": "#ff0000",
    "20": "#00aaff",
    "22": "#ffaa00",
    "90": "#00cc44",
    "97": "#cc00ff",
    "21": "#ff6600",
    "25": "#009933"
};

function getRouteColor(route) {
    return routeColors[route] || "#007bff";
}

/* ⭐ CUSTOM ICONS PODĽA EVENTU */
const icons = {
    IN_TRANSIT: L.icon({
        iconUrl: 'bus_blue.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "bus-icon"
    }),
    ARRIVING: L.icon({
        iconUrl: 'bus_yellow.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "bus-icon pulse"
    }),
    AT_STOP: L.icon({
        iconUrl: 'bus_green.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "bus-icon"
    }),
    DEPARTING: L.icon({
        iconUrl: 'bus_orange.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "bus-icon"
    }),
    UNKNOWN: L.icon({
        iconUrl: 'bus_gray.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        className: "bus-icon"
    })
};

/* ⭐ ZVÝRAZNENÁ IKONKA PRE VYBRANÉ VOZIDLO */
const selectedIcon = L.icon({
    iconUrl: 'bus_blue.png',
    iconSize: [42, 42],
    iconAnchor: [21, 21],
    className: "bus-icon selected"
});

/* ⭐ SMOOTH MOVEMENT (requestAnimationFrame) */
function smoothMove(marker, newLat, newLon) {
    const duration = 400;
    const start = marker.getLatLng();
    const startTime = performance.now();

    function animate(time) {
        const t = Math.min((time - startTime) / duration, 1);
        const lat = start.lat + (newLat - start.lat) * t;
        const lon = start.lng + (newLon - start.lng) * t;
        marker.setLatLng([lat, lon]);
        if (t < 1) requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
}

/* ⭐ AUTO‑ZOOM – jemný flyTo */
function focusOnVehicle(lat, lon) {
    map.flyTo([lat, lon], 16, { duration: 0.8 });
}

/* ⭐ LOAD SHAPE */
async function loadShape(shapeId) {
    if (!shapeId) return null;
    try {
        const res = await fetch(`http://localhost:8000/shapes/${shapeId}`);
        return await res.json();
    } catch {
        return null;
    }
}

/* ⭐ DRAW SHAPE – zvýraznená trasa */
function drawShape(points, route) {
    if (!points) return;

    if (currentShapePolyline) {
        map.removeLayer(currentShapePolyline);
    }

    const latlngs = points.map(p => [p.lat, p.lon]);

    currentShapePolyline = L.polyline(latlngs, {
        color: getRouteColor(route),
        weight: 6,
        opacity: 0.95
    }).addTo(map);
}

/* ⭐ CLEAR STOPS */
function clearStops() {
    currentStopMarkers.forEach(m => map.removeLayer(m));
    currentStopMarkers = [];
}

/* ⭐ LOAD STOPS */
async function loadStops(tripId) {
    try {
        const res = await fetch(`http://localhost:8000/stops/${tripId}`);
        return await res.json();
    } catch {
        return [];
    }
}

/* ⭐ DRAW STOPS – zvýraznenie prvej zastávky */
function drawStops(stops) {
    clearStops();

    stops.forEach((s, index) => {
        const marker = L.circleMarker([s.lat, s.lon], {
            radius: index === 0 ? 8 : 6,
            color: index === 0 ? "#ffcc00" : "#333333",
            fillColor: index === 0 ? "#ffcc00" : "#555555",
            fillOpacity: 0.95,
            weight: 2
        }).addTo(map);

        marker.bindPopup(`<b>${s.name}</b><br>Sequence: ${s.sequence}`);
        currentStopMarkers.push(marker);
    });
}

/* ⭐ STREAM — MULTI VEHICLE */
document.getElementById("start").addEventListener("click", () => {
    const lang = langSelect.value;

    if (eventSource) eventSource.close();

    const url = `http://localhost:8000/stream/events/all?lang=${lang}`;
    eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        const msgBox = document.getElementById("message");
        const logList = document.getElementById("log-list");

        let data = null;
        try {
            data = JSON.parse(event.data);
        } catch {
            msgBox.textContent = event.data;
            return;
        }

        const vehicles = data.vehicles || [];

        vehicles.forEach(v => {
            if (v.lat == null || v.lon == null) return;

            const pos = [v.lat, v.lon];

            /* NOVÝ MARKER */
            if (!markers[v.vehicle_id]) {
                const marker = L.marker(pos, {
                    icon: icons[v.event] || icons.UNKNOWN
                }).addTo(map);

                marker.on("click", () => {
                    selectedVehicleId = v.vehicle_id;
                    updateInfoPanel(v);

                    focusOnVehicle(v.lat, v.lon);

                    Object.values(markers).forEach(m => m.setIcon(icons.IN_TRANSIT));
                    marker.setIcon(selectedIcon);

                    if (v.shape_id) loadShape(v.shape_id).then(points => drawShape(points, v.route));
                    loadStops(v.trip_id).then(drawStops);
                });

                markers[v.vehicle_id] = marker;
            } else {
                /* EXISTUJÚCI MARKER */
                const marker = markers[v.vehicle_id];

                if (selectedVehicleId === v.vehicle_id) {
                    marker.setIcon(selectedIcon);
                } else {
                    marker.setIcon(icons[v.event] || icons.UNKNOWN);
                }

                smoothMove(marker, v.lat, v.lon);
            }

            if (selectedVehicleId === v.vehicle_id) updateInfoPanel(v);
        });

        /* ⭐ LOG PANEL */
        if (vehicles.length > 0) {
            const last = vehicles.at(0);

            msgBox.textContent = last.text || "No announcement";
            msgBox.className = "fade";

            msgBox.classList.add(`state-${last.event.toLowerCase()}`);

            const entry = document.createElement("div");
            entry.className = "log-entry";
            entry.innerHTML = `<span class="log-icon">🚌</span> ${new Date().toLocaleTimeString()} — ${last.text}`;
            logList.prepend(entry);
        }
    };
});

/* ⭐ INFO PANEL */
function updateInfoPanel(v) {
    const infoBox = document.getElementById("info");
    infoBox.innerHTML = `
        <div class="info-title">🚌 Vozidlo ${v.vehicle_id}</div>
        <b>Linka:</b> ${v.route || "-"}<br>
        <b>Ďalšia zastávka:</b> ${v.next_stop || "-"}<br>
        <b>ETA:</b> ${v.eta_seconds ? Math.round(v.eta_seconds) + " s" : "-"}<br>
        <b>Meškanie:</b> ${v.delay_seconds ? Math.round(v.delay_seconds) + " s" : "-"}<br>
        <b>Stav:</b> ${v.event}<br>
    `;
}

/* ⭐ STOP STREAM */
document.getElementById("stop").addEventListener("click", () => {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
        document.getElementById("message").textContent = "Stream stopped.";
        document.getElementById("message").className = "";
    }
});
