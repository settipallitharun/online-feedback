// JavaScript for Online Feedback Collector

document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation and submission
    const feedbackForm = document.getElementById('feedbackForm');
    const submitBtn = document.getElementById('submitBtn');
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    const errorMessage = document.getElementById('errorMessage');

    // Form validation
    function validateForm() {
        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const rating = document.querySelector('input[name="rating"]:checked');
        
        let isValid = true;

        // Validate name
        if (!name) {
            document.getElementById('name').classList.add('is-invalid');
            isValid = false;
        } else {
            document.getElementById('name').classList.remove('is-invalid');
            document.getElementById('name').classList.add('is-valid');
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email || !emailRegex.test(email)) {
            document.getElementById('email').classList.add('is-invalid');
            isValid = false;
        } else {
            document.getElementById('email').classList.remove('is-invalid');
            document.getElementById('email').classList.add('is-valid');
        }

        // Validate rating
        if (!rating) {
            isValid = false;
            // Highlight rating buttons
            document.querySelectorAll('.btn-outline-warning').forEach(btn => {
                btn.classList.add('border-danger');
            });
        } else {
            document.querySelectorAll('.btn-outline-warning').forEach(btn => {
                btn.classList.remove('border-danger');
            });
        }

        return isValid;
    }

    // Clear validation states on input
    document.getElementById('name').addEventListener('input', function() {
        this.classList.remove('is-invalid', 'is-valid');
    });

    document.getElementById('email').addEventListener('input', function() {
        this.classList.remove('is-invalid', 'is-valid');
    });

    // Clear rating validation on selection
    document.querySelectorAll('input[name="rating"]').forEach(radio => {
        radio.addEventListener('change', function() {
            document.querySelectorAll('.btn-outline-warning').forEach(btn => {
                btn.classList.remove('border-danger');
            });
        });
    });

    // Form submission
    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function(e) {
            e.preventDefault();

            if (!validateForm()) {
                // Shake the form to indicate validation error
                feedbackForm.classList.add('shake');
                setTimeout(() => {
                    feedbackForm.classList.remove('shake');
                }, 500);
                return;
            }

            // Disable submit button and show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Submitting...';

            // Prepare form data
            const formData = new FormData(feedbackForm);

            // Submit via AJAX
            fetch('/submit-feedback', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success modal
                    successModal.show();
                    
                    // Reset form
                    feedbackForm.reset();
                    document.querySelectorAll('.is-valid').forEach(el => {
                        el.classList.remove('is-valid');
                    });
                    
                    // Reset rating buttons
                    document.querySelectorAll('.btn-check').forEach(btn => {
                        btn.checked = false;
                    });
                    
                } else {
                    // Show error modal with message
                    errorMessage.textContent = data.message || 'An error occurred while submitting your feedback.';
                    errorModal.show();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorMessage.textContent = 'Network error. Please check your connection and try again.';
                errorModal.show();
            })
            .finally(() => {
                // Re-enable submit button
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-paper-plane me-1"></i>Submit Feedback';
            });
        });
    }

    // Add shake animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        .shake {
            animation: shake 0.5s;
        }
    `;
    document.head.appendChild(style);

    // Character counter for comments
    const commentsTextarea = document.getElementById('comments');
    if (commentsTextarea) {
        const charCounter = document.createElement('small');
        charCounter.className = 'form-text text-muted';
        charCounter.textContent = '0 characters';
        commentsTextarea.parentNode.appendChild(charCounter);

        commentsTextarea.addEventListener('input', function() {
            const length = this.value.length;
            charCounter.textContent = `${length} character${length !== 1 ? 's' : ''}`;
            
            // Change color based on length
            if (length > 500) {
                charCounter.classList.remove('text-muted');
                charCounter.classList.add('text-warning');
            } else {
                charCounter.classList.remove('text-warning');
                charCounter.classList.add('text-muted');
            }
        });
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Initialize tooltips if any
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Print functionality for dashboard
    const printBtn = document.getElementById('printBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (feedbackForm && document.activeElement.form === feedbackForm) {
                feedbackForm.dispatchEvent(new Event('submit'));
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });

    // Lazy loading for images (if any are added later)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Performance monitoring
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
    });

    // Service Worker registration (for future PWA functionality)
    if ('serviceWorker' in navigator) {
        // This can be uncommented when a service worker is created
        // navigator.serviceWorker.register('/sw.js')
        //     .then(registration => console.log('SW registered'))
        //     .catch(error => console.log('SW registration failed'));
    }
});

// Utility functions
function showLoadingSpinner(element) {
    element.classList.add('loading');
}

function hideLoadingSpinner(element) {
    element.classList.remove('loading');
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for global use
window.FeedbackCollector = {
    showLoadingSpinner,
    hideLoadingSpinner,
    formatDate,
    debounce
};
