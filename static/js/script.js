// Javascript file for Quoty
const year = new Date();

// Set copyright year.
const cpFooter = document.getElementById("curYear");
cpFooter.innerHTML = year.getFullYear();

// Use JavaScript to remove the fade class and data-bs-dismiss attribute
document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
    alert.classList.remove('fade');
    alert.removeAttribute('data-bs-dismiss');
    });
});
