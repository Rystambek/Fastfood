document.addEventListener('DOMContentLoaded', function() {
    // Image preview functionality
    const imageInputs = document.querySelectorAll('input[type="file"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                const preview = document.querySelector(`#${this.dataset.previewId}`);
                
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                
                reader.readAsDataURL(file);
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });

    // Price formatting
    const priceInputs = document.querySelectorAll('input[type="number"]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value;
            value = value.replace(/[^0-9.]/g, '');
            const parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            e.target.value = value;
        });
    });

    // Responsive image handling
    const foodImages = document.querySelectorAll('.food-image');
    foodImages.forEach(img => {
        img.addEventListener('error', function() {
            this.src = '/static/images/default-food.jpg';
            this.alt = 'Default food image';
        });
    });

    // Grid layout enhancements
    const container = document.querySelector('.container');
    if (container) {
        // Add animation to cards when they come into view
        const cards = document.querySelectorAll('.card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1
        });

        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });

        // Responsive grid adjustments
        function adjustGrid() {
            const width = window.innerWidth;
            if (width >= 1200) {
                container.style.gridTemplateColumns = 'repeat(3, 1fr)';
            } else if (width >= 768) {
                container.style.gridTemplateColumns = 'repeat(2, 1fr)';
            } else {
                container.style.gridTemplateColumns = '1fr';
            }
        }

        window.addEventListener('resize', adjustGrid);
        adjustGrid();
    }

    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}); 