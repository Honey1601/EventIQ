let currentIndex = 0;

function slideCarousel(direction) {
    const track = document.getElementById("carouselTrack");
    const cards = document.querySelectorAll(".carousel-card");
    const visibleCards = window.innerWidth <= 768 ? 1 : 2;

    const maxIndex = cards.length - visibleCards;
    currentIndex += direction;

    if (currentIndex < 0) currentIndex = 0;
    if (currentIndex > maxIndex) currentIndex = maxIndex;

    const cardWidth = cards[0].offsetWidth + 20;
    track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
}

document.addEventListener("DOMContentLoaded", loadLatestHackathons);

function loadLatestHackathons() {
    fetch("/api/hackathons/latest")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("upcomingHackathons");
            container.innerHTML = "";

            if (!data.length) {
                container.innerHTML = "<p>No upcoming hackathons found.</p>";
                return;
            }

            data.forEach(h => {

                // 💰 REGISTRATION FEE LOGIC (FIXED)
                const priceText =
                    h.registration_fee && Number(h.registration_fee) > 0
                        ? `₹${h.registration_fee}`
                        : "FREE";

                container.innerHTML += `
                <div class="col-md-4">
                    <div class="hackathon-card">
                        <span class="hackathon-tag">HACKATHON</span>
                        <span class="hackathon-prize">${priceText}</span>

                        <h5>${h.title}</h5>
                        <p class="hackathon-desc">${h.description || ""}</p>

                        <ul class="hackathon-info">
                            <li>📅 ${formatDate(h.start_date)} – ${formatDate(h.end_date)}</li>
                            <li>🌐 ${h.mode === "online" ? "Online" : (h.city || h.location)}</li>
                            <li>🎯 ${h.skill_level ? h.skill_level.toUpperCase() : "ANY"}</li>
                        </ul>

                        <a href="event/hackathon/${h.id}">
                            <button class="hackathon-btn">Register Now</button>
                        </a>
                    </div>
                </div>
                `;
            });
        })
        .catch(err => {
            console.error("Error loading latest hackathons:", err);
        });
}

function formatDate(dateStr) {
    if (!dateStr) return "TBA";
    return new Date(dateStr).toLocaleDateString();
}

document.addEventListener("DOMContentLoaded", loadLatestWorkshops);

function loadLatestWorkshops() {
    fetch("/api/workshops/latest")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("workshopsContainer");
            if (!container) return;   // safety

            container.innerHTML = "";

            if (!data.length) {
                container.innerHTML = "<p>No workshops available.</p>";
                return;
            }

            data.forEach(w => {
                const priceText =
                    w.registration_fee && Number(w.registration_fee) > 0
                        ? `₹${w.registration_fee}`
                        : "Free";

                const duration = getDuration(w.start_time, w.end_time);

                container.innerHTML += `
                <div class="col-md-4">
                    <div class="workshop-card">
                        <span class="workshop-tag">WORKSHOP</span>
                        <span class="workshop-price">${priceText}</span>

                        <h5>${w.title}</h5>
                        <p class="workshop-desc">${w.description}</p>

                        <ul class="workshop-info">
                            <li>⏱ ${duration}</li>
                            <li>🎯 ${w.skill_level.toUpperCase()}</li>
                            <li>👤 ${w.host_name}</li>
                        </ul>

                         <a href="/event/workshop/${w.id}">
                            <button class="workshop-btn">Enroll Now</button>
                         </a>
                    </div>
                </div>
                `;
            });
        })
        .catch(err => {
            console.error("Workshop fetch failed:", err);
        });
}

function getDuration(start, end) {
    if (!start || !end) return "Flexible";

    const startTime = new Date(`1970-01-01T${start}`);
    const endTime = new Date(`1970-01-01T${end}`);
    const diffMs = endTime - startTime;

    const hours = Math.round(diffMs / (1000 * 60 * 60));
    return `${hours} hours`;
}

document.addEventListener("DOMContentLoaded", loadLatestMeetups);

function loadLatestMeetups() {
    fetch("/api/meetups/latest")
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById("meetupsContainer");
            if (!container) return;

            container.innerHTML = "";

            if (!data.length) {
                container.innerHTML = "<p>No meetups available.</p>";
                return;
            }

            data.forEach(m => {
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

                container.innerHTML += `
                <div class="col-md-6">
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
                </div>
                `;
            });
        })
        .catch(err => {
            console.error("Meetup fetch failed:", err);
        });
}

/* -----------------------------
   TIME FORMATTER
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

document.addEventListener("DOMContentLoaded", loadLatestBootcamps);

function loadLatestBootcamps() {
  fetch("/api/bootcamps/latest")
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("bootcampContainer");
      container.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p>No bootcamps available.</p>";
        return;
      }

      data.forEach(b => {
        if (!b || !b.id) return;

        // 💰 Price
        const priceText =
          Number(b.registration_fee) > 0
            ? `₹${b.registration_fee}`
            : "Free";

        // ⏱ Duration
        const durationText =
          b.duration_days
            ? `${b.duration_days} days`
            : "Flexible";

        container.insertAdjacentHTML("beforeend", `
          <div class="col-md-4">
            <div class="workshop-card">
              <span class="workshop-tag">BOOTCAMP</span>
              <span class="workshop-price">${priceText}</span>

              <h5>${b.title}</h5>
              <p class="workshop-desc">${b.description || ""}</p>

              <ul class="workshop-info">
                <li>⏱ ${durationText}</li>
                <li>👤 ${b.instructor}</li>
              </ul>

              <a href="/event/bootcamp/${b.id}">
                <button class="workshop-btn">View Details</button>
              </a>
            </div>
          </div>
        `);
      });
    })
    .catch(err => {
      console.error("Failed to load latest bootcamps:", err);
    });
}

