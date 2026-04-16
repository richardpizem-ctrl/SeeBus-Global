<!DOCTYPE html>
<html lang="sk">
<head>
  <meta charset="UTF-8" />
  <title>SeeBus Global – mapa</title>

  <!-- Leaflet CSS -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""
  />

  <style>
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
    }
    #map {
      width: 100%;
      height: 100%;
    }
  </style>
</head>
<body>
  <div id="map" aria-label="Mapa zastávok" role="region"></div>

  <!-- Leaflet JS -->
  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""
  ></script>

  <script src="script.js"></script>
</body>
</html>
