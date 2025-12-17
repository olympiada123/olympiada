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

    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach(function(element) {
        observer.observe(element);
    });

    const featureItems = document.querySelectorAll('.feature-item');
    featureItems.forEach(function(item, index) {
        item.style.transitionDelay = (index * 0.1) + 's';
        observer.observe(item);
    });

    const techCards = document.querySelectorAll('.tech-card');
    techCards.forEach(function(card, index) {
        card.style.transitionDelay = (index * 0.1) + 's';
        observer.observe(card);
    });

    const audienceCards = document.querySelectorAll('.audience-card');
    audienceCards.forEach(function(card, index) {
        card.style.transitionDelay = (index * 0.15) + 's';
        observer.observe(card);
    });

    const contactItems = document.querySelectorAll('.contact-item');
    contactItems.forEach(function(item, index) {
        item.style.opacity = '0';
        item.style.transform = 'translateY(10px)';
        item.style.transition = 'all 0.4s ease-out';
        
        setTimeout(function() {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 300 + (index * 100));
    });

    const sectionHeadings = document.querySelectorAll('.section-heading');
    sectionHeadings.forEach(function(heading) {
        heading.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        heading.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    const featureIcons = document.querySelectorAll('.feature-icon');
    featureIcons.forEach(function(icon) {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'rotate(10deg) scale(1.1)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'rotate(0) scale(1)';
        });
    });

    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.page-header');
        
        parallaxElements.forEach(function(element) {
            const speed = 0.5;
            element.style.transform = 'translateY(' + (scrolled * speed) + 'px)';
        });
    });
});

