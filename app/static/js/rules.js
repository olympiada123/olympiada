document.addEventListener('DOMContentLoaded', function() {
    const rulesSections = document.querySelectorAll('.rules-section');
    
    rulesSections.forEach(function(section) {
        const header = section.querySelector('.rules-section-header');
        const toggle = section.querySelector('.rules-section-toggle');
        
        header.addEventListener('click', function() {
            const isActive = section.classList.contains('active');
            
            if (isActive) {
                section.classList.remove('active');
                toggle.textContent = '+';
            } else {
                section.classList.add('active');
                toggle.textContent = '−';
            }
        });
    });
});

