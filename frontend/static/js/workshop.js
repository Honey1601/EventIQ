let workshops = [];

// -----------------------------
// LOAD WORKSHOPS FROM API
// -----------------------------
document.addEventListener("DOMContentLoaded", loadWorkshops);

function loadWorkshops() {
  fetch("/api/workshops")
    .then(res => res.json())
    .then(data => {
      workshops = data;
      renderWorkshops(workshops);
    })
    .catch(err => {
      console.error("Failed to load workshops:", err);
    });
}

// -----------------------------
// RENDER WORKSHOPS
// -----------------------------
function renderWorkshops(filtered = workshops) {
  const container = document.getElementById("workshopsContainer");
  container.innerHTML = "";

  if (!filtered.length) {
    container.innerHTML = "<p class='text-muted'>No workshops found.</p>";
    return;
  }

  filtered.forEach(w => {
    const priceText =
      w.registration_fee && Number(w.registration_fee) > 0
        ? `₹${w.registration_fee}`
        : "Free";

    const duration = getDuration(w.start_time, w.end_time);

    const instructor = "Host"; // placeholder (host not sent in API yet)

    const card = `
      <div class="col-12 workshop-card-wrapper">
        <a href="/workshop/${w.id}" class="card-link">
          <div class="workshop-card">
            <span class="workshop-tag">WORKSHOP</span>
            <span class="workshop-price">${priceText}</span>

            <h5>${w.title}</h5>
            <p class="workshop-desc">${w.description}</p>

            <ul class="workshop-info">
              <li>⏱ ${duration}</li>
              <li>🎯 ${w.skill_level.toUpperCase()}</li>
              <li>👤 ${instructor}</li>
            </ul>

            <a href="/event/workshop/${w.id}">
                <button class="workshop-btn">Enroll Now</button>
            </a>
          </div>
        </a>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", card);
  });
}

// -----------------------------
// FILTER WORKSHOPS (CLIENT SIDE)
// -----------------------------
function filterWorkshops() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const skill = document.getElementById("skillFilter").value;
  const skillLevel = document.getElementById("skillLevelFilter")?.value || "";

  const filtered = workshops.filter(w => {
    const matchesSearch =
      w.title.toLowerCase().includes(search) ||
      w.description.toLowerCase().includes(search);

    const matchesSkill =
      !skill ||
      w.skills.toLowerCase().includes(skill.toLowerCase());

    const matchesLevel =
      !skillLevel || w.skill_level === skillLevel;

    return matchesSearch && matchesSkill && matchesLevel;
  });

  renderWorkshops(filtered);
}

// -----------------------------
// EVENT LISTENERS
// -----------------------------
document.getElementById("searchInput").addEventListener("input", filterWorkshops);
document.getElementById("skillFilter").addEventListener("change", filterWorkshops);
document.getElementById("skillLevelFilter")?.addEventListener("change", filterWorkshops);

// -----------------------------
// HELPERS
// -----------------------------
function getDuration(start, end) {
  if (!start || !end) return "Flexible";

  const startTime = new Date(`1970-01-01T${start}`);
  const endTime = new Date(`1970-01-01T${end}`);
  const diffMs = endTime - startTime;

  const hours = Math.round(diffMs / (1000 * 60 * 60));
  return `${hours} hours`;
}
