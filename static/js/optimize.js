const progressBar = document.getElementById('progressBar');
const progressStatus = document.getElementById('progressStatus');
const optimizeBtn = document.getElementById('optimizeBtn');

optimizeBtn.addEventListener('click', () => {
    if (!optimizeBtn.disabled) {
        progressStatus.textContent = 'Optimizing...';
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                progressStatus.textContent = 'Optimization Complete';
            }
        }, 500); // Simulate progress
    }
});