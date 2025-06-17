document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const passwordInput = this.previousElementSibling;
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
            this.querySelector('i').classList.toggle('fa-eye');
            this.querySelector('i').classList.toggle('fa-eye-slash');
        });
    });

    // Password strength checker & validation
    const passwordInput = document.getElementById('password');
    const progressBar = document.querySelector('.password-strength .progress-bar');
    const passwordFeedback = document.querySelector('.password-feedback');

    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            let errors = [];

            if (password.length < 8) {
                errors.push("Password must be at least 8 characters.");
            } else {
                strength += 20;
            }
            
            if (!/(?=.*[A-Z])(?=.*[a-z])/.test(password)) {
                errors.push("Password must contain at least one uppercase and one lowercase letter.");
            } else {
                strength += 40;
            }
            
            if (!/\d/.test(password)) {
                errors.push("Password must contain at least one number.");
            } else {
                strength += 20;
            }
            
            if (!/[^a-zA-Z0-9]/.test(password)) {
                errors.push("Password must contain at least one special character.");
            } else {
                strength += 20;
            }

            // Mise à jour de la barre de progression
            progressBar.style.width = `${Math.min(strength, 100)}%`;
            progressBar.className = 'progress-bar';
            progressBar.classList.add(strength < 50 ? 'weak' : strength < 75 ? 'medium' : 'strong');

            // Affichage des erreurs
            passwordFeedback.innerHTML = errors.length ? errors.join('<br>') : "Strong password!";
        });
    }

    // Validate email
    function validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});
