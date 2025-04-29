// hybrid_auth_project/app/static/js/keystroke_capture.js

// Capture key timing events and send batches to the server
(function () {
    let events = [];
    let lastKeyUpTime = null;

    document.addEventListener('keydown', (e) => {
        const now = performance.now();
        const existingEvent = events.find(ev => ev.key === e.code && !ev.up_time);
        if (!existingEvent) {
            events.push({
                key: e.code,
                down_time: now,
                hold_time: null,
                up_time: null
            });
        }
    });

    document.addEventListener('keyup', (e) => {
        const now = performance.now();
        const existingEvent = events.find(ev => ev.key === e.code && ev.hold_time === null);
        if (existingEvent) {
            existingEvent.up_time = now;
            existingEvent.hold_time = now - existingEvent.down_time;
        }
    });

    // Periodically send collected keystroke data
    setInterval(() => {
        if (events.length > 0) {
            const payload = {
                events: events.map(ev => ({
                    down_time: ev.down_time,
                    up_time: ev.up_time,
                    hold_time: ev.hold_time
                }))
            };

            fetch('/api/keystroke', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload),
                credentials: 'include' // Important to send cookies for session auth
            }).then(response => response.json())
              .then(data => {
                  if (data.status === 'ok') {
                      // Clear events buffer after successful send
                      events = [];
                  }
              }).catch((err) => {
                  console.error('Error sending keystroke data:', err);
              });
        }
    }, 5000); // Send batch every 5 seconds
})();