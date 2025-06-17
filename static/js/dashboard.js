// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', () => {
    const circles = document.querySelectorAll('.usage-circle');
    circles.forEach(circle => {
        const progress = circle.getAttribute('data-progress');
        const fill = circle.querySelector('.circle-fill');
        fill.style.setProperty('--progress', progress);
    });
});