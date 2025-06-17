// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Animation des statistiques
    const statNumbers = document.querySelectorAll('.stat-number');
    
    function animateStats() {
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-count'));
            const duration = 2000; // 2 secondes
            const step = target / (duration / 16); // 16ms par frame (environ 60fps)
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    clearInterval(timer);
                    stat.textContent = target;
                } else {
                    stat.textContent = Math.floor(current);
                }
            }, 16);
        });
    }

    // Observer pour déclencher l'animation des statistiques lorsqu'elles sont visibles
    const statsSection = document.querySelector('.stats-section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateStats();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    if (statsSection) {
        observer.observe(statsSection);
    }

    // Gestion des onglets de la démo
    const demoTabs = document.querySelectorAll('.demo-tab');
    const demoPanes = document.querySelectorAll('.demo-pane');
    
    demoTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Retirer la classe active de tous les onglets
            demoTabs.forEach(t => t.classList.remove('active'));
            // Ajouter la classe active à l'onglet cliqué
            tab.classList.add('active');
            
            // Masquer tous les panneaux
            demoPanes.forEach(pane => pane.classList.remove('active'));
            // Afficher le panneau correspondant
            const targetPane = document.getElementById(`${tab.getAttribute('data-tab')}-pane`);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // Boutons "Suivant" dans la démo
    const nextButtons = document.querySelectorAll('.demo-next-btn');
    nextButtons.forEach(button => {
        button.addEventListener('click', () => {
            const nextTab = button.getAttribute('data-next');
            const tabToClick = document.querySelector(`.demo-tab[data-tab="${nextTab}"]`);
            if (tabToClick) {
                tabToClick.click();
            }
        });
    });

    // Animation de l'analyse
    function startAnalysisAnimation() {
        const analysisPane = document.getElementById('analysis-pane');
        if (!analysisPane) return;
        
        const progressBar = analysisPane.querySelector('.progress-bar');
        const percentageText = document.getElementById('analysis-percentage');
        const steps = analysisPane.querySelectorAll('.analysis-step');
        
        let progress = 0;
        const interval = setInterval(() => {
            progress += 1;
            if (progress <= 100) {
                progressBar.style.width = `${progress}%`;
                progressBar.setAttribute('aria-valuenow', progress);
                percentageText.textContent = progress;
                
                // Mettre à jour les étapes
                if (progress >= 25 && progress < 50) {
                    steps[0].classList.add('completed');
                    steps[0].querySelector('i').className = 'fas fa-check-circle';
                } else if (progress >= 50 && progress < 75) {
                    steps[1].classList.add('completed');
                    steps[1].querySelector('i').className = 'fas fa-check-circle';
                    
                    steps[2].classList.add('active');
                    steps[2].querySelector('i').className = 'fas fa-spinner fa-spin';
                } else if (progress >= 75 && progress < 100) {
                    steps[2].classList.add('completed');
                    steps[2].classList.remove('active');
                    steps[2].querySelector('i').className = 'fas fa-check-circle';
                    
                    steps[3].classList.add('active');
                    steps[3].querySelector('i').className = 'fas fa-spinner fa-spin';
                } else if (progress >= 100) {
                    steps[3].classList.add('completed');
                    steps[3].classList.remove('active');
                    steps[3].querySelector('i').className = 'fas fa-check-circle';
                    
                    clearInterval(interval);
                    
                    // Passer automatiquement à l'onglet des résultats après un court délai
                    setTimeout(() => {
                        const resultsTab = document.querySelector('.demo-tab[data-tab="results"]');
                        if (resultsTab) {
                            resultsTab.click();
                        }
                    }, 1000);
                }
            } else {
                clearInterval(interval);
            }
        }, 50);
    }

    // Déclencher l'animation d'analyse lorsque l'onglet d'analyse est affiché
    const analysisTab = document.querySelector('.demo-tab[data-tab="analysis"]');
    if (analysisTab) {
        analysisTab.addEventListener('click', startAnalysisAnimation);
    }

    // Gestion des onglets de résultats
    const resultsTabs = document.querySelectorAll('.results-tab');
    const resultsPanes = document.querySelectorAll('.results-pane');
    
    resultsTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Retirer la classe active de tous les onglets
            resultsTabs.forEach(t => t.classList.remove('active'));
            // Ajouter la classe active à l'onglet cliqué
            tab.classList.add('active');
            
            // Masquer tous les panneaux
            resultsPanes.forEach(pane => pane.classList.remove('active'));
            // Afficher le panneau correspondant
            const targetPane = document.getElementById(`${tab.getAttribute('data-results-tab')}-pane`);
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // Slider de témoignages
    const testimonialItems = document.querySelectorAll('.testimonial-item');
    const testimonialDots = document.querySelectorAll('.testimonial-dots .dot');
    const prevButton = document.querySelector('.testimonial-prev');
    const nextButton = document.querySelector('.testimonial-next');
    let currentTestimonial = 0;
    
    function showTestimonial(index) {
        // Masquer tous les témoignages
        testimonialItems.forEach(item => item.classList.remove('active'));
        // Désactiver tous les points
        testimonialDots.forEach(dot => dot.classList.remove('active'));
        
        // Afficher le témoignage actif
        testimonialItems[index].classList.add('active');
        // Activer le point correspondant
        testimonialDots[index].classList.add('active');
        
        currentTestimonial = index;
    }
    
    // Événements pour les boutons précédent/suivant
    if (prevButton) {
        prevButton.addEventListener('click', () => {
            let newIndex = currentTestimonial - 1;
            if (newIndex < 0) {
                newIndex = testimonialItems.length - 1;
            }
            showTestimonial(newIndex);
        });
    }
    
    if (nextButton) {
        nextButton.addEventListener('click', () => {
            let newIndex = currentTestimonial + 1;
            if (newIndex >= testimonialItems.length) {
                newIndex = 0;
            }
            showTestimonial(newIndex);
        });
    }
    
    // Événements pour les points
    testimonialDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showTestimonial(index);
        });
    });
    
    // Rotation automatique des témoignages
    setInterval(() => {
        let newIndex = currentTestimonial + 1;
        if (newIndex >= testimonialItems.length) {
            newIndex = 0;
        }
        showTestimonial(newIndex);
    }, 5000);

    // Smooth scroll pour les liens d'ancrage
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Fermer le menu mobile si ouvert
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                    document.querySelector('.navbar-toggler').click();
                }
            }
        });
    });

    // Gestion des modals
    const loginLinks = document.querySelectorAll('a[href="#connexion"]');
    const registerLinks = document.querySelectorAll('a[href="#inscription"]');
    
    loginLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
            loginModal.show();
        });
    });
    
    registerLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
            registerModal.show();
        });
    });

    // Gestion des formulaires
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simuler l'envoi du formulaire
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Envoi en cours...';
            
            setTimeout(() => {
                // Réinitialiser le formulaire
                this.reset();
                
                // Restaurer le bouton
                submitButton.disabled = false;
                submitButton.textContent = originalText;
                
                // Afficher un message de succès
                const formContainer = this.closest('.contact-form');
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success mt-3';
                successMessage.textContent = 'Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.';
                formContainer.appendChild(successMessage);
                
                // Supprimer le message après quelques secondes
                setTimeout(() => {
                    successMessage.remove();
                }, 5000);
            }, 1500);
        });
    }

    // Animation de la zone de téléchargement
    const uploadArea = document.querySelector('.demo-upload-area');
    if (uploadArea) {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('border-primary');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('border-primary');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('border-primary');
            
            // Simuler le téléchargement d'un fichier
            const uploadIcon = uploadArea.querySelector('.upload-icon i');
            const originalClass = uploadIcon.className;
            
            uploadIcon.className = 'fas fa-spinner fa-spin';
            
            setTimeout(() => {
                uploadIcon.className = 'fas fa-check-circle';
                uploadArea.querySelector('h3').textContent = 'Fichier téléchargé';
                uploadArea.querySelector('p').textContent = 'CV_exemple.pdf (143 KB)';
                
                // Activer le bouton Continuer
                const nextButton = document.querySelector('.demo-next-btn[data-next="analysis"]');
                if (nextButton) {
                    nextButton.disabled = false;
                }
            }, 1500);
        });
        
        // Clic sur le bouton Parcourir
        const browseButton = uploadArea.querySelector('.btn');
        if (browseButton) {
            browseButton.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Simuler le téléchargement d'un fichier
                const uploadIcon = uploadArea.querySelector('.upload-icon i');
                const originalClass = uploadIcon.className;
                
                uploadIcon.className = 'fas fa-spinner fa-spin';
                
                setTimeout(() => {
                    uploadIcon.className = 'fas fa-check-circle';
                    uploadArea.querySelector('h3').textContent = 'Fichier téléchargé';
                    uploadArea.querySelector('p').textContent = 'CV_exemple.pdf (143 KB)';
                    
                    // Activer le bouton Continuer
                    const nextButton = document.querySelector('.demo-next-btn[data-next="analysis"]');
                    if (nextButton) {
                        nextButton.disabled = false;
                    }
                }, 1500);
            });
        }
    }

    // Animation du bouton d'optimisation automatique
    const optimizeButton = document.querySelector('.optimization-actions .btn-success');
    if (optimizeButton) {
        optimizeButton.addEventListener('click', function() {
            const originalText = this.innerHTML;
            
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Optimisation en cours...';
            
            setTimeout(() => {
                // Mettre à jour le score
                const scoreCircle = document.querySelector('.circle');
                const scoreText = document.querySelector('.percentage');
                
                scoreCircle.setAttribute('stroke-dasharray', '92, 100');
                scoreText.textContent = '92%';
                
                // Restaurer le bouton
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-check-circle me-2"></i>CV optimisé';
                
                // Mettre à jour le compteur d'optimisations
                const counter = document.querySelector('.optimization-counter');
                counter.textContent = '8 optimisations gratuites restantes';
                
                // Ajouter un message de succès
                const resultsHeader = document.querySelector('.results-header');
                const successMessage = document.createElement('div');
                successMessage.className = 'alert alert-success w-100 mt-3';
                successMessage.innerHTML = '<i class="fas fa-check-circle me-2"></i>Votre CV a été optimisé avec succès! Le score d\'adéquation est passé de 65% à 92%.';
                resultsHeader.appendChild(successMessage);
            }, 2000);
        });
    }

    // Initialisation des tooltips Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialisation des popovers Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

