// Simulated sponsored slots (frontend-only)
let maxSlots = 6;
let usedSlots = 3; // mock value

const slotCount = document.getElementById("slotCount");
const imageUpload = document.getElementById("imageUpload");
const imagePreview = document.getElementById("imagePreview");

slotCount.textContent = `${maxSlots - usedSlots} / ${maxSlots}`;

// Image preview
imageUpload.addEventListener("change", () => {
  const file = imageUpload.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    imagePreview.innerHTML = `<img src="${reader.result}" style="max-height:120px;border-radius:12px;">`;
  };
  reader.readAsDataURL(file);
});

// Timeline validation
document.querySelector(".sponsor-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const start = new Date(document.getElementById("startDate").value);
  const end = new Date(document.getElementById("endDate").value);

  if (start >= end) {
    alert("End date must be after start date.");
    return;
  }

  if (usedSlots >= maxSlots) {
    alert("No sponsored slots available.");
    return;
  }

  alert("Sponsorship request submitted (frontend demo).");
});
