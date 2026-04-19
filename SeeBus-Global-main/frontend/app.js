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

let vehicleMarker = null;

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

/* ⭐ SMOOTH MOVEMENT */
function smoothMove(marker, newLat, newLon) {
    const duration = 500; // ms
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

/* ⭐ STREAM */
document.getElementById("start").addEventListener("click", () => {
    const lang = langSelect.value;
    const route = document.getElementById("route").value;
    const vehicle = document.getElementById("vehicle").value;

    if (eventSource) {
        eventSource.close();
    }

    const url = `http://localhost:8000/stream/events?vehicle_id=${vehicle}&route=${route}&lang=${lang}`;
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

        /* ⭐ TEXT + FARBA */
        msgBox.textContent = data.text || event.data;
        msgBox.className = "";

        if (data.event === "ARRIVING") msgBox.classList.add("state-arriving");
        if (data.event === "AT_STOP") msgBox.classList.add("state-at_stop");
        if (data.event === "DEPARTING") msgBox.classList.add("state-departing");
        if (data.event === "IN_TRANSIT") msgBox.classList.add("state-transit");

        /* ⭐ LOG */
        const entry = document.createElement("div");
        entry.className = "log-entry";

        if (data.event === "ARRIVING") entry.classList.add("state-arriving");
        if (data.event === "AT_STOP") entry.classList.add("state-at_stop");
        if (data.event === "DEPARTING") entry.classList.add("state-departing");
        if (data.event === "IN_TRANSIT") entry.classList.add("state-transit");

        entry.textContent = `${new Date().toLocaleTimeString()} — ${data.text}`;
        logList.prepend(entry);

        /* ⭐ MAPA — aktualizácia polohy vozidla */
        if (data.lat && data.lon) {
            const pos = [data.lat, data.lon];

            if (!vehicleMarker) {
                vehicleMarker = L.marker(pos, {
                    icon: icons[data.event] || icons.UNKNOWN
                }).addTo(map);
            } else {
                vehicleMarker.setIcon(icons[data.event] || icons.UNKNOWN);
                smoothMove(vehicleMarker, data.lat, data.lon);
            }
        }

        /* ⭐ ETA + DELAY + NEXT STOP */
        const infoBox = document.getElementById("info");
        infoBox.innerHTML = `
            <b>Linka:</b> ${data.route}<br>
            <b>Ďalšia zastávka:</b> ${data.next_stop || "-"}<br>
            <b>ETA:</b> ${data.eta_seconds ? Math.round(data.eta_seconds) + " s" : "-"}<br>
            <b>Meškanie:</b> ${data.delay_seconds ? Math.round(data.delay_seconds) + " s" : "-"}<br>
        `;
    };
});

/* STOP */
document.getElementById("stop").addEventListener("click", () => {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
        document.getElementById("message").textContent = "Stream stopped.";
        document.getElementById("message").className = "";
    }
});
