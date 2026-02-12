let bootcamps = [];

/* -----------------------------
   LOAD BOOTCAMPS FROM DB
------------------------------ */
document.addEventListener("DOMContentLoaded", loadBootcamps);

function loadBootcamps() {
  fetch("/api/bootcamps")
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch bootcamps");
      return res.json();
    })
    .then(data => {
      bootcamps = data;
      renderBootcamps(bootcamps);
    })
    .catch(err => {
      console.error("Failed to load bootcamps:", err);
    });
}

/* -----------------------------
   RENDER BOOTCAMPS
------------------------------ */
function renderBootcamps(filtered = bootcamps) {
  const container = document.getElementById("bootcampsContainer");
  if (!container) return;

  container.innerHTML = "";

  if (!filtered.length) {
    container.innerHTML = "<p class='text-muted'>No bootcamps found.</p>";
    return;
  }

  filtered.forEach(b => {
    // 💰 Price
    const priceText =
      b.registration_fee && Number(b.registration_fee) > 0
        ? `₹${b.registration_fee}`
        : "Free";

    // ⏱ Duration (days → weeks if large)
    let durationText = "Flexible";
    if (b.duration_days) {
      durationText =
        b.duration_days >= 7
          ? `${Math.round(b.duration_days / 7)} weeks`
          : `${b.duration_days} days`;
    }

    const card = `
      <div class="col-12 bootcamp-card-wrapper">
        <div class="workshop-card">
          <span class="workshop-tag">BOOTCAMP</span>
          <span class="workshop-price">${priceText}</span>

          <h5>${b.title}</h5>
          <p class="workshop-desc">${b.description}</p>

          <ul class="workshop-info">
            <li>⏱ ${durationText}</li>
            <li>👤 ${b.instructor || "TechHub"}</li>
          </ul>

            <a href="/event/bootcamp/${b.id}">
                <button class="workshop-btn">View Details</button>
            </a>

        </div>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", card);
  });
}

/* -----------------------------
   FILTER BOOTCAMPS
------------------------------ */
function filterBootcamps() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const price = document.getElementById("priceFilter").value;
  const skill = document.getElementById("skillFilter").value;
  const duration = document.getElementById("durationFilter").value;

  const filtered = bootcamps.filter(b => {
    const matchesSearch =
      b.title.toLowerCase().includes(search) ||
      b.description.toLowerCase().includes(search);

    const matchesPrice =
      !price ||
      (price === "Free"
        ? !b.registration_fee || b.registration_fee === 0
        : b.registration_fee > 0);

    const matchesSkill =
      !skill ||
      (b.skills && b.skills.toLowerCase().includes(skill.toLowerCase()));

    const matchesDuration =
      !duration ||
      (b.duration_days &&
        (duration.includes("weeks")
          ? Math.round(b.duration_days / 7) + " weeks" === duration
          : b.duration_days + " days" === duration));

    return (
      matchesSearch &&
      matchesPrice &&
      matchesSkill &&
      matchesDuration
    );
  });

  renderBootcamps(filtered);
}

/* -----------------------------
   EVENT LISTENERS
------------------------------ */
["searchInput", "priceFilter", "skillFilter", "durationFilter"]
  .forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener("input", filterBootcamps);
    el.addEventListener("change", filterBootcamps);
  });
