
// Initial fetch
fetchEvents();

async function fetchEvents() {
    const response = await fetch('/events');
    const events = await response.json();

    const eventsList = document.getElementById('events-list');
    eventsList.innerHTML = '';

    events.forEach(event => {
        const li = document.createElement('li');
        li.textContent = `${event.event_type}: ${event.message}`;
        eventsList.appendChild(li);
    });
}

// Fetch events every 15 seconds
setInterval(fetchEvents, 15000);

// Initial fetch
fetchEvents();