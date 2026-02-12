let meetups = [];

/* -----------------------------
   LOAD MEETUPS FROM API
------------------------------ */
document.addEventListener("DOMContentLoaded", loadMeetups);

function loadMeetups() {
  fetch("/api/meetups")
    .then(res => res.json())
    .then(data => {
      meetups = data;
      renderMeetups(meetups);
    })
    .catch(err => {
      console.error("Failed to load meetups:", err);
    });
}

/* -----------------------------
   RENDER MEETUPS
------------------------------ */
function renderMeetups(filtered = meetups) {
  const container = document.getElementById("meetupsContainer");
  container.innerHTML = "";

  if (!filtered.length) {
    container.innerHTML = "<p class='text-muted'>No meetups found.</p>";
    return;
  }

  filtered.forEach(m => {
    const dateObj = new Date(m.start_date);
    const meetupDate = dateObj.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric"
    });

    const timeText = getMeetupTime(m.start_time, m.end_time);

    const locationText =
      m.mode === "online"
        ? "Online"
        : (m.city || m.location || "TBA");

    const card = `
      <div class="col-12 meetup-card-wrapper">
        <a href="/meetup/${m.id}" class="card-link">
          <div class="meetup-card">
            <span class="meetup-tag">MEETUP</span>
            <span class="meetup-date">${meetupDate}</span>

            <h5>${m.title}</h5>
            <p class="meetup-desc">${m.description}</p>

            <ul class="meetup-info">
              <li>📍 ${locationText}</li>
              <li>👥 ${m.attending} attending</li>
              <li>⏰ ${timeText}</li>
            </ul>

            <a href="/event/meetup/${m.id}">
                <button class="meetup-btn">Join Meetup</button>
            </a>
          </div>
        </a>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", card);
  });
}

/* -----------------------------
   FILTER MEETUPS
------------------------------ */
function filterMeetups() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const city = document.getElementById("cityFilter").value;
  const topic = document.getElementById("topicFilter").value;

  const filtered = meetups.filter(m => {
    const matchesSearch =
      m.title.toLowerCase().includes(search) ||
      m.description.toLowerCase().includes(search);

    const matchesCity =
      !city || m.city === city || m.location === city;

    const matchesTopic =
      !topic ||
      (m.skills && m.skills.toLowerCase().includes(topic.toLowerCase()));

    return matchesSearch && matchesCity && matchesTopic;
  });

  renderMeetups(filtered);
}

/* -----------------------------
   EVENT LISTENERS
------------------------------ */
document.getElementById("searchInput").addEventListener("input", filterMeetups);
document.getElementById("cityFilter").addEventListener("change", filterMeetups);
document.getElementById("topicFilter").addEventListener("change", filterMeetups);

/* -----------------------------
   HELPERS
------------------------------ */
function getMeetupTime(start, end) {
  if (!start || !end) return "Flexible";

  const startTime = new Date(`1970-01-01T${start}`);
  const endTime = new Date(`1970-01-01T${end}`);

  return `${formatTime(startTime)} – ${formatTime(endTime)}`;
}

function formatTime(date) {
  return date.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });
}
