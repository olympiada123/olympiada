document.addEventListener('DOMContentLoaded', function() {
    /**
     * Инициализирует dropdown меню пользователя в навигации.
     */
    function initUserDropdown() {
        const dropdownToggle = document.getElementById('userDropdownToggle');
        const dropdownMenu = document.getElementById('userDropdownMenu');
        const dropdown = dropdownToggle ? dropdownToggle.closest('.user-dropdown') : null;
        
        if (!dropdownToggle || !dropdownMenu || !dropdown) {
            return;
        }
        
        dropdownToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            dropdown.classList.toggle('active');
        });
        
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
        
        dropdownMenu.addEventListener('click', function(e) {
            if (e.target.closest('.dropdown-item')) {
                dropdown.classList.remove('active');
            }
        });
    }
    
    initUserDropdown();
});

