let debounceTimer;

function loadHackathons() {
  clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    const search = document.getElementById("searchInput").value.trim();
    const status = document.getElementById("statusFilter").value;
    const city = document.getElementById("cityFilter").value;
    const skill = document.getElementById("skillFilter").value;
    const skillLevel = document.getElementById("skillLevelFilter").value;

    const params = new URLSearchParams({
      ...(search && { search }),
      ...(status && { status }),
      ...(city && { city }),
      ...(skill && { skill }),
      ...(skillLevel && { skill_level: skillLevel })
    });

    fetch(`/api/hackathons?${params.toString()}`)
      .then(res => res.json())
      .then(renderHackathons)
      .catch(() => {
        document.getElementById("hackathonsContainer").innerHTML =
          `<p class="text-center text-muted">Failed to load hackathons.</p>`;
      });

  }, 300);
}

function renderHackathons(hackathons) {
  const container = document.getElementById("hackathonsContainer");
  container.innerHTML = "";

  if (!hackathons.length) {
    container.innerHTML =
      `<p class="text-center text-muted">No hackathons found.</p>`;
    return;
  }

  hackathons.forEach(h => {


    const card = `

        <div class="hackathon-card">
          <span class="hackathon-tag">HACKATHON</span>

          <h5>${h.title}</h5>
          <p class="hackathon-desc">${h.description}</p>

          <ul class="hackathon-info">
            <li>📅 ${new Date(h.start_date).toDateString()}</li>
            <li>📍 ${h.mode === "online" ? "Online" : (h.city || h.location)}</li>
            <li>🎯 Level: ${h.skill_level.toUpperCase()}</li>
          </ul>

          <a href="event/hackathon/${h.id}">
            <button class="hackathon-btn">Register Now</button>
          </a>
        </div>

    `;
    container.insertAdjacentHTML("beforeend", card);
  });
}

["searchInput", "statusFilter", "cityFilter", "skillFilter", "skillLevelFilter"]
  .forEach(id => {
    document.getElementById(id).addEventListener("input", loadHackathons);
    document.getElementById(id).addEventListener("change", loadHackathons);
  });

loadHackathons();