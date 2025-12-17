document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const featureCards = document.querySelectorAll('.feature-card-compact');
    featureCards.forEach(function(item, index) {
        item.style.transition = 'all 0.5s ease-out';
        item.style.transitionDelay = (index * 0.1) + 's';
        observer.observe(item);
    });

    const stepItems = document.querySelectorAll('.step-item');
    stepItems.forEach(function(item, index) {
        item.style.transition = 'all 0.5s ease-out';
        item.style.transitionDelay = (index * 0.15) + 's';
        observer.observe(item);
    });

    const tipsItems = document.querySelectorAll('.tips-list li');
    tipsItems.forEach(function(item, index) {
        item.style.transition = 'all 0.4s ease-out';
        item.style.transitionDelay = (index * 0.1) + 's';
        observer.observe(item);
    });

    const aboutCards = document.querySelectorAll('.about-card');
    aboutCards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    const featureIcons = document.querySelectorAll('.feature-icon-compact');
    featureIcons.forEach(function(icon) {
        icon.style.transition = 'all 0.3s ease-out';
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2) rotate(5deg)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0)';
        });
    });

    const stepNumbers = document.querySelectorAll('.step-number');
    stepNumbers.forEach(function(number) {
        number.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        number.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0)';
        });
    });
});

