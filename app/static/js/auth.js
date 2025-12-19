document.addEventListener('DOMContentLoaded', function() {
    /**
     * Инициализирует переключатели видимости паролей на страницах входа и регистрации.
     */
    function initPasswordToggles() {
        const passwordToggles = document.querySelectorAll('.password-toggle');
        
        passwordToggles.forEach(function(toggle) {
            toggle.addEventListener('click', function() {
                const wrapper = this.closest('.password-input-wrapper');
                const input = wrapper.querySelector('input[type="password"], input[type="text"]');
                
                if (input.type === 'password') {
                    input.type = 'text';
                    this.setAttribute('aria-label', 'Скрыть пароль');
                    this.classList.add('active');
                } else {
                    input.type = 'password';
                    this.setAttribute('aria-label', 'Показать пароль');
                    this.classList.remove('active');
                }
            });
        });
    }
    
    initPasswordToggles();
});

