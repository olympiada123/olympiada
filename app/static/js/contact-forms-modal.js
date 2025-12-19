document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('contactFormModal');
    const viewButtons = document.querySelectorAll('.view-contact-form-btn');
    const closeButtons = document.querySelectorAll('.modal-close, .modal-close-btn');
    const statusForm = document.getElementById('contactFormStatusForm');
    const statusFilter = document.getElementById('contactFormStatusFilter');
    const formsList = document.getElementById('contactFormsList');
    
    if (!modal) return;
    
    if (statusFilter && formsList) {
        statusFilter.addEventListener('change', function() {
            const selectedStatus = this.value;
            const formItems = formsList.querySelectorAll('.contact-form-item');
            let visibleCount = 0;
            
            formItems.forEach(function(item) {
                if (selectedStatus === '' || item.getAttribute('data-status') === selectedStatus) {
                    item.style.display = '';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });
            
            const existingEmptyState = formsList.querySelector('.empty-state-filtered');
            if (visibleCount === 0 && formItems.length > 0) {
                if (!existingEmptyState) {
                    const emptyDiv = document.createElement('div');
                    emptyDiv.className = 'empty-state empty-state-filtered';
                    emptyDiv.innerHTML = '<p class="empty-state-text">Формы обратной связи с выбранным статусом не найдены.</p>';
                    formsList.appendChild(emptyDiv);
                }
            } else if (existingEmptyState) {
                existingEmptyState.remove();
            }
            
            const url = new URL(window.location);
            if (selectedStatus) {
                url.searchParams.set('status_filter', selectedStatus);
            } else {
                url.searchParams.delete('status_filter');
            }
            window.history.pushState({}, '', url);
        });
    }
    
    function openModal(formData) {
        document.getElementById('modal-form-id').value = formData.formId;
        document.getElementById('modal-form-name').textContent = formData.name;
        document.getElementById('modal-form-email').textContent = formData.email;
        document.getElementById('modal-form-subject').textContent = formData.subject;
        document.getElementById('modal-form-message').textContent = formData.message;
        document.getElementById('modal-form-created').textContent = formData.created;
        document.getElementById('modal-form-updated').textContent = formData.updated;
        document.getElementById('modal-status-select').value = formData.status;
        
        const completedItem = document.getElementById('modal-form-completed');
        const completedDate = document.getElementById('modal-form-completed-date');
        if (formData.status === 'reviewed') {
            completedItem.style.display = 'block';
            completedDate.textContent = formData.updated;
        } else {
            completedItem.style.display = 'none';
        }
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
    
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    viewButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const formData = {
                formId: this.getAttribute('data-form-id'),
                name: this.getAttribute('data-form-name'),
                email: this.getAttribute('data-form-email'),
                subject: this.getAttribute('data-form-subject'),
                message: this.getAttribute('data-form-message'),
                status: this.getAttribute('data-form-status'),
                created: this.getAttribute('data-form-created'),
                updated: this.getAttribute('data-form-updated'),
            };
            openModal(formData);
        });
    });
    
    closeButtons.forEach(function(button) {
        button.addEventListener('click', closeModal);
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    
    
});

