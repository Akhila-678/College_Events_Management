// Load events
fetch("http://127.0.0.1:8000/events")
  .then(res => res.json())
  .then(events => {
    const select = document.getElementById("eventSelect");
    const list = document.getElementById("events");

    events.forEach(e => {
      let option = document.createElement("option");
      option.value = e.id;
      option.innerText = `${e.title} @ ${e.venue}`;
      select.appendChild(option);

      let div = document.createElement("div");
      div.innerHTML = `<b>${e.title}</b><br>${e.description}<br>${e.date} at ${e.time} @ ${e.venue}<br><br>`;
      list.appendChild(div);
    });
  });

document.getElementById('registerForm').addEventListener('submit', function (e) {
  e.preventDefault(); // prevent default GET submit

  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const event_id = document.getElementById('eventSelect').value; // ✅ FIXED ID!

  fetch('http://127.0.0.1:8000/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: name,
      email: email,
      event_id: event_id
    }),
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    alert('Registration successful!');
  })
  .catch(error => console.error('Error:', error));
});



