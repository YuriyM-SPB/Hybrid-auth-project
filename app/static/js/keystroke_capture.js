let events = [];
let lastKeyUpTime = null;

document.addEventListener("DOMContentLoaded", function () {
    const typingBox = document.getElementById("typingBox");

    typingBox.addEventListener("keydown", function (e) {
        const event = {
            key: e.key,
            down_time: performance.now()
        };
        e._customEvent = event;
        events.push(event);
    });

    typingBox.addEventListener("keyup", function (e) {
        const upTime = performance.now();
        const matchingEvent = events.find(ev => ev.key === e.key && !ev.up_time);
        if (matchingEvent) {
            matchingEvent.up_time = upTime;
            matchingEvent.hold_time = upTime - matchingEvent.down_time;
        }

        if (lastKeyUpTime !== null && matchingEvent) {
            matchingEvent.flight_time = matchingEvent.down_time - lastKeyUpTime;
        }
        lastKeyUpTime = upTime;

        if (events.length >= 10) { 
            sendKeystrokeData();
        }
    });
});

function sendKeystrokeData() {
    const payload = { events: events };
    fetch("/api/keystroke", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Keystroke score:", data.keystroke_score);
        console.log("Combined risk:", data.combined_risk);
    })
    .catch(error => {
        console.error("Error sending keystroke data:", error);
    });

    events = [];
}