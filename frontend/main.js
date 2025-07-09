const apiUrl = "http://127.0.0.1:8000";

document.getElementById("eventForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const id = document.getElementById("eventId").value;
  const event = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    date: document.getElementById("date").value,
    time: document.getElementById("time").value,
    venue: document.getElementById("venue").value
  };
  const method = id ? "PUT" : "POST";
  const url = id ? `${apiUrl}/events/${id}` : `${apiUrl}/events`;

  await fetch(url, {
    method: method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event)
  });

  loadEvents();
  this.reset();
});

async function loadEvents() {
  const res = await fetch(`${apiUrl}/events`);
  const events = await res.json();
  displayEvents(events);
}

function displayEvents(events) {
  const container = document.getElementById("eventsList");
  container.innerHTML = "";
  events.forEach((event) => {
    const div = document.createElement("div");
    div.className = "event";
    div.innerHTML = `
      <h3>${event.title}</h3>
      <p>${event.description}</p>
      <p><strong>Date:</strong> ${event.date} | <strong>Time:</strong> ${event.time}</p>
      <p><strong>Venue:</strong> ${event.venue}</p>
      <button onclick="editEvent(${event.id})">Edit</button>
      <button onclick="deleteEvent(${event.id})">Delete</button>
      <button onclick="viewRegistrations(${event.id})">View Registrations</button>

      <div id="registrations-${event.id}"></div>

      <div class="register-box">
        <h4>Register for this Event</h4>
        <input type="text" id="reg-name-${event.id}" placeholder="Your Name" required>
        <input type="email" id="reg-email-${event.id}" placeholder="Your Email" required>
        <button onclick="registerStudent(${event.id})">Register</button>
      </div>
    `;
    container.appendChild(div);
  });
}

function editEvent(id) {
  fetch(`${apiUrl}/events`)
    .then((res) => res.json())
    .then((events) => {
      const event = events.find((e) => e.id === id);
      document.getElementById("eventId").value = event.id;
      document.getElementById("title").value = event.title;
      document.getElementById("description").value = event.description;
      document.getElementById("date").value = event.date;
      document.getElementById("time").value = event.time;
      document.getElementById("venue").value = event.venue;
    });
}

async function deleteEvent(id) {
  await fetch(`${apiUrl}/events/${id}`, { method: "DELETE" });
  loadEvents();
}

async function searchEvents() {
  const name = document.getElementById("searchInput").value;
  const res = await fetch(`${apiUrl}/events/search?name=${name}`);
  const events = await res.json();
  displayEvents(events);
}

async function viewRegistrations(eventId) {
  const res = await fetch(`${apiUrl}/events/${eventId}/registrations`);
  const registrations = await res.json();
  const container = document.getElementById(`registrations-${eventId}`);
  if (registrations.length === 0) {
    container.innerHTML = "<p>No registrations yet.</p>";
    return;
  }
  container.innerHTML = "<h5>Registrations:</h5><ul>" + registrations.map(r => `<li>${r.name} - ${r.email}</li>`).join("") + "</ul>";
}

async function registerStudent(eventId) {
  const name = document.getElementById(`reg-name-${eventId}`).value;
  const email = document.getElementById(`reg-email-${eventId}`).value;

  if (!name || !email) {
    alert("Please enter your name and email.");
    return;
  }

  const registration = {
    event_id: eventId,
    name: name,
    email: email
  };

  await fetch(`${apiUrl}/registrations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(registration)
  });

  alert("Registration successful!");
  viewRegistrations(eventId);

  document.getElementById(`reg-name-${eventId}`).value = "";
  document.getElementById(`reg-email-${eventId}`).value = "";
}

window.onload = loadEvents;
