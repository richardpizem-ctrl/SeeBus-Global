// Inicializácia mapy
const map = L.map('map').setView([48.7363, 19.1462], 13); // Banská Bystrica

// Tile layer (podkladová mapa)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

// Načítanie zastávok z backendu
fetch("http://localhost:8000/stops")
    .then(response => response.json())
    .then(stops => {
        stops.forEach(stop => {
            const lat = parseFloat(stop.stop_lat);
            const lon = parseFloat(stop.stop_lon);

            if (!isNaN(lat) && !isNaN(lon)) {
                L.marker([lat, lon])
                    .addTo(map)
                    .bindPopup(`<b>${stop.stop_name || "Bez názvu"}</b><br>ID: ${stop.stop_id}`);
            }
        });
    })
    .catch(err => {
        console.error("Chyba pri načítaní /stops:", err);
    });
