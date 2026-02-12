document.addEventListener("DOMContentLoaded", () => {

    /* =========================
       FORMAT (ONLINE / OFFLINE)
    ========================== */
    const formatOptions = document.querySelectorAll('input[name="format"]');
    const locationDetails = document.getElementById('locationDetails');
    const onlineDetails = document.getElementById('onlineDetails');

    if (formatOptions.length && locationDetails && onlineDetails) {
        formatOptions.forEach(option => {
            option.addEventListener('change', function () {
                if (this.value === 'online') {
                    locationDetails.style.display = 'none';
                    onlineDetails.style.display = 'block';
                }
                else if (this.value === 'offline') {
                    locationDetails.style.display = 'block';
                    onlineDetails.style.display = 'none';
                }
                else if (this.value === 'hybrid') {
                    locationDetails.style.display = 'block';
                    onlineDetails.style.display = 'block';
                }
            });
        });
    }

    /* =========================
       PRIZES (HACKATHON ONLY)
    ========================== */
    const prizesToggle = document.getElementById('hasPrizes');
    const prizesDetails = document.getElementById('prizesDetails');

    if (prizesToggle && prizesDetails) {
        prizesToggle.addEventListener('change', function () {
            prizesDetails.style.display = this.checked ? 'block' : 'none';

            if (!this.checked) {
                prizesDetails.querySelectorAll("input, textarea")
                    .forEach(el => el.value = "");
            }
        });
    }

    /* =========================
       EVENT TYPE → SHOW PRIZES
    ========================== */
    const eventTypeSelect = document.querySelector('select[name="event_type"]');
    const prizesSection = document.getElementById("prizesSection");
    const hackathonTimeline = document.getElementById("hackathonTimeline");

    function toggleHackathonSections() {
        if (!eventTypeSelect) return;

        const isHackathon = eventTypeSelect.value === "hackathon";

        if (prizesSection) {
            prizesSection.style.display = isHackathon ? "block" : "none";
            if (!isHackathon) {
                prizesSection.querySelectorAll("input, textarea")
                    .forEach(el => el.value = "");
            }
        }

        if (hackathonTimeline) {
            hackathonTimeline.style.display = isHackathon ? "block" : "none";
            if (!isHackathon) {
                hackathonTimeline.querySelectorAll("input")
                    .forEach(el => el.value = "");
            }
        }
    }

    if (eventTypeSelect) {
        eventTypeSelect.addEventListener("change", toggleHackathonSections);
        toggleHackathonSections(); // run once on load
    }

});
