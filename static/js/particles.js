// Animation des particules
function animateParticles() {
    const particles = document.querySelectorAll('.particle');
    
    particles.forEach((particle, index) => {
        // Position initiale aléatoire
        const posX = Math.random() * 50;
        const posY = Math.random() * 50;
        const size = Math.random() * 5 + 2;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 5;
        
        // Appliquer les styles initiaux
        particle.style.left = `${posX}%`;
        particle.style.top = `${posY}%`;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        particle.style.animation = `float ${duration}s ease-in-out ${delay}s infinite`;
    });
}

// Ajouter l'animation CSS pour les particules
function addParticleAnimation() {
    // Vérifier si l'animation existe déjà
    if (!document.getElementById('particle-animation')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'particle-animation';
        styleSheet.textContent = `
            @keyframes float {
                0% {
                    transform: translateY(0) translateX(0);
                }
                25% {
                    transform: translateY(-20px) translateX(10px);
                }
                50% {
                    transform: translateY(-35px) translateX(-10px);
                }
                75% {
                    transform: translateY(-20px) translateX(8px);
                }
                100% {
                    transform: translateY(0) translateX(0);
                }
            }
        `;
        document.head.appendChild(styleSheet);
    }
}

// Initialiser les particules
function initParticles() {
    const heroSection = document.querySelector('.hero-section');
    const particlesContainer = document.querySelector('.particles');
    
    // Si le conteneur de particules n'existe pas, le créer
    if (!particlesContainer) {
        const newParticlesContainer = document.createElement('div');
        newParticlesContainer.className = 'particles';
        heroSection.prepend(newParticlesContainer);
        
        // Créer 20 particules
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            newParticlesContainer.appendChild(particle);
        }
    }
    
    // Ajouter l'animation CSS
    addParticleAnimation();
    
    // Animer les particules
    animateParticles();
}

// Appeler la fonction d'initialisation des particules au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Code existant...
    
    // Initialiser les particules
    initParticles();
});
