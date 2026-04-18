let eventSource = null;

// Load saved language
const langSelect = document.getElementById("language");
langSelect.value = localStorage.getItem("lang") || "sk";

langSelect.addEventListener("change", () => {
    localStorage.setItem("lang", langSelect.value);
});

// Start stream
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

        // Parse JSON
        let data = null;
        try {
            data = JSON.parse(event.data);
        } catch {
            msgBox.textContent = event.data;
            return;
        }

        // Update main message
        msgBox.textContent = data.text || event.data;

        // Reset classes
        msgBox.className = "";

        // Apply color class
        if (data.state === "ARRIVING") msgBox.classList.add("state-arriving");
        if (data.state === "AT_STOP") msgBox.classList.add("state-at_stop");
        if (data.state === "DEPARTING") msgBox.classList.add("state-departing");
        if (data.state === "MISSED") msgBox.classList.add("state-missed");

        // ⭐ Add to log
        const entry = document.createElement("div");
        entry.className = "log-entry";

        // Apply same color to log entry
        if (data.state === "ARRIVING") entry.classList.add("state-arriving");
        if (data.state === "AT_STOP") entry.classList.add("state-at_stop");
        if (data.state === "DEPARTING") entry.classList.add("state-departing");
        if (data.state === "MISSED") entry.classList.add("state-missed");

        entry.textContent = `${new Date().toLocaleTimeString()} — ${data.text}`;
        logList.prepend(entry); // newest first
    };

    eventSource.onerror = () => {
        document.getElementById("message").textContent = "Stream disconnected.";
    };
});

// Stop stream
document.getElementById("stop").addEventListener("click", () => {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
        document.getElementById("message").textContent = "Stream stopped.";
        document.getElementById("message").className = "";
    }
});
