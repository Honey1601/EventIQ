
function togglePassword() {
  const password = document.getElementById('password');
  const icon = document.querySelector('#togglePassword i');
  if (password.type === 'password') {
    password.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    password.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}

function toggleConfirmPassword() {
  const confirmPassword = document.getElementById('confirmPassword');
  const icon = document.querySelector('#toggleConfirmPassword i');
  if (confirmPassword.type === 'password') {
    confirmPassword.type = 'text';
    icon.classList.remove('fa-eye');
    icon.classList.add('fa-eye-slash');
  } else {
    confirmPassword.type = 'password';
    icon.classList.remove('fa-eye-slash');
    icon.classList.add('fa-eye');
  }
}

document.getElementById('togglePassword').addEventListener('click', togglePassword);
document.getElementById('toggleConfirmPassword').addEventListener('click', toggleConfirmPassword);

// Basic form validation
document.getElementById('signupForm').addEventListener('submit', function(event) {
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  if (password !== confirmPassword) {
    alert('Passwords do not match!');
    event.preventDefault();
  }
  // reCAPTCHA validation would be handled server-side
});


document.getElementById("isHost").addEventListener("change", function () {
  const hostFields = document.getElementById("hostFields");
  hostFields.style.display = this.checked ? "block" : "none";
});

const isHost = document.getElementById("isHost");
const hostFields = document.getElementById("hostFields");
const skillsSection = document.getElementById("skillsSection");
const courseYearSection = document.getElementById("courseYearSection");
const collegeSection = document.getElementById("collegeSection");

hostFields.style.display = "none";

isHost.addEventListener("change", () => {
  if (isHost.checked) {
    hostFields.style.display = "block";
    skillsSection.style.display = "none";
    courseYearSection.style.display = "none";
    collegeSection.style.display = "none";
  } else {
    hostFields.style.display = "none";
    skillsSection.style.display = "block";
    courseYearSection.style.display = "flex";
    collegeSection.style.display = "block";
  }
});

