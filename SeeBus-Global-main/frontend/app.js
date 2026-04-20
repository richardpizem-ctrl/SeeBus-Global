let eventSource = null;

/* ⭐ LANGUAGE — load saved language */
const langSelect = document.getElementById("language");
langSelect.value = localStorage.getItem("lang") || "sk";

langSelect.addEventListener("change", () => {
    localStorage.setItem("lang", langSelect.value);
});

/* ⭐ MAPA — inicializácia */
const map = L.map('map').setView([48.7363, 19.1462], 13); // Banská Bystrica

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

/* ⭐ MARKERS PRE VŠETKY VOZIDLÁ */
const markers = {};  // { vehicle_id: marker }

/* ⭐ SELECTED VEHICLE */
let selectedVehicleId = null;

/* ⭐ POLYLINE PRE TRASU */
let currentShapePolyline = null;

/* ⭐ FAREBNÉ TRASY PODĽA LINKY (KROK 23) */
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
    return routeColors[route] || "#007bff"; // default modrá
}

/* ⭐ CUSTOM ICONS PODĽA EVENTU */
const icons = {
    IN_TRANSIT: L.icon({
        iconUrl: 'bus_blue.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    }),
    ARRIVING: L.icon({
        iconUrl: 'bus_yellow.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    }),
    AT_STOP: L.icon({
        iconUrl: 'bus_green.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    }),
    DEPARTING: L.icon({
        iconUrl: 'bus_orange.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    }),
    UNKNOWN: L.icon({
        iconUrl: 'bus_gray.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    })
};

/* ⭐ KROK 24 — ZVÝRAZNENÁ IKONKA PRE VYBRANÉ VOZIDLO */
const selectedIcon = L.icon({
    iconUrl: 'bus_blue.png',   // môžeš dať vlastnú ikonku
    iconSize: [42, 42],
    iconAnchor: [21, 21]
});

/* ⭐ SMOOTH MOVEMENT */
function smoothMove(marker, newLat, newLon) {
    const duration = 500;
    const frames = 20;
    const delay = duration / frames;

    const start = marker.getLatLng();
    const dLat = (newLat - start.lat) / frames;
    const dLon = (newLon - start.lng) / frames;

    let i = 0;
    const step = () => {
        if (i >= frames) return;
        marker.setLatLng([start.lat + dLat * i, start.lng + dLon * i]);
        i++;
        setTimeout(step, delay);
    };
    step();
}

/* ⭐ AUTO‑ZOOM NA VYBRANÉ VOZIDLO */
function focusOnVehicle(lat, lon) {
    map.setView([lat, lon], 16, { animate: true });
}

/* ⭐ LOAD SHAPE (backend → frontend) */
async function loadShape(shapeId) {
    if (!shapeId) return null;
    try {
        const res = await fetch(`http://localhost:8000/shapes/${shapeId}`);
        return await res.json();
    } catch {
        return null;
    }
}

/* ⭐ DRAW SHAPE (polyline) — farba podľa linky */
function drawShape(points, route) {
    if (!points) return;

    if (currentShapePolyline) {
        map.removeLayer(currentShapePolyline);
    }

    const latlngs = points.map(p => [p.lat, p.lon]);

    currentShapePolyline = L.polyline(latlngs, {
        color: getRouteColor(route),
        weight: 4,
        opacity: 0.85
    }).addTo(map);
}

/* ⭐ STREAM — MULTI VEHICLE */
document.getElementById("start").addEventListener("click", () => {
    const lang = langSelect.value;

    if (eventSource) {
        eventSource.close();
    }

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

        /* ⭐ PRE KAŽDÉ VOZIDLO */
        vehicles.forEach(v => {
            if (!v.lat || !v.lon) return;

            const pos = [v.lat, v.lon];

            /* Ak marker neexistuje → vytvoríme */
            if (!markers[v.vehicle_id]) {
                const marker = L.marker(pos, {
                    icon: icons[v.event] || icons.UNKNOWN
                }).addTo(map);

                /* ⭐ KROK 21 + 22 + 23 + 24 */
                marker.on("click", () => {
                    selectedVehicleId = v.vehicle_id;
                    updateInfoPanel(v);

                    focusOnVehicle(v.lat, v.lon);

                    // ⭐ KROK 24 — zvýraznenie vybraného vozidla
                    Object.values(markers).forEach(m => m.setIcon(icons.IN_TRANSIT));
                    marker.setIcon(selectedIcon);

                    if (v.shape_id) {
                        loadShape(v.shape_id).then(points => {
                            drawShape(points, v.route);
                        });
                    }
                });

                markers[v.vehicle_id] = marker;
            } else {
                /* Existujúci marker → aktualizácia */
                const marker = markers[v.vehicle_id];

                if (selectedVehicleId === v.vehicle_id) {
                    marker.setIcon(selectedIcon);   // ⭐ zvýraznený marker
                } else {
                    marker.setIcon(icons[v.event] || icons.UNKNOWN);
                }

                smoothMove(marker, v.lat, v.lon);
            }

            /* ⭐ Ak je toto vybrané vozidlo → aktualizuj info panel */
            if (selectedVehicleId === v.vehicle_id) {
                updateInfoPanel(v);
            }
        });

        /* ⭐ LOG — posledné hlásenie */
        if (vehicles.length > 0) {
            const last = vehicles[0];
            msgBox.textContent = last.text || "No announcement";
            msgBox.className = "";

            if (last.event === "ARRIVING") msgBox.classList.add("state-arriving");
            if (last.event === "AT_STOP") msgBox.classList.add("state-at_stop");
            if (last.event === "DEPARTING") msgBox.classList.add("state-departing");
            if (last.event === "IN_TRANSIT") msgBox.classList.add("state-transit");

            const entry = document.createElement("div");
            entry.className = "log-entry";
            entry.textContent = `${new Date().toLocaleTimeString()} — ${last.text}`;
            logList.prepend(entry);
        }
    };
});

/* ⭐ INFO PANEL UPDATE FUNKCIA */
function updateInfoPanel(v) {
    const infoBox = document.getElementById("info");
    infoBox.innerHTML = `
        <b>Vozidlo:</b> ${v.vehicle_id}<br>
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
