let eventSource = null;

// Load saved language
const langSelect = document.getElementById("language");
langSelect.value = localStorage.getItem("lang") || "sk";

langSelect.addEventListener("change", () => {
    localStorage.setItem("lang", langSelect.value);
});

document.getElementById("start").addEventListener("click", () => {
    const lang = langSelect.value;

    if (eventSource) {
        eventSource.close();
    }

    const url = `http://localhost:8000/stream/events?vehicle_id=1&route=24&lang=${lang}`;
    eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
        document.getElementById("message").textContent = event.data;
    };

    eventSource.onerror = () => {
        document.getElementById("message").textContent = "Stream disconnected.";
    };
});

document.getElementById("stop").addEventListener("click", () => {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
        document.getElementById("message").textContent = "Stream stopped.";
    }
});
