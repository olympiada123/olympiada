document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('olympiad-search');
    const statusFilter = document.getElementById('status-filter');
    const subjectFilter = document.getElementById('subject-filter');
    const sortFilter = document.getElementById('sort-filter');
    const resetBtn = document.getElementById('reset-filters');
    const container = document.getElementById('olympiads-container');
    const resultsCount = document.getElementById('results-count');
    const paginationContainer = document.getElementById('pagination-container');
    
    let currentPage = 1;
    const itemsPerPage = 6;
    let allCards = Array.from(container.querySelectorAll('.olympiad-card'));
    let filteredCards = [...allCards];
    
    /**
     * Определяет статус олимпиады на основе CSS классов карточки.
     * @param {HTMLElement} card - Элемент карточки олимпиады.
     * @returns {string} Статус олимпиады: 'active', 'upcoming', 'finished' или пустая строка.
     */
    function getCardStatus(card) {
        const statusAttr = card.getAttribute('data-status');
        if (statusAttr) {
            return statusAttr;
        }
        const statusElement = card.querySelector('.olympiad-status');
        if (!statusElement) return '';
        
        if (statusElement.classList.contains('olympiad-status-active')) {
            return 'active';
        } else if (statusElement.classList.contains('olympiad-status-upcoming')) {
            return 'upcoming';
        } else if (statusElement.classList.contains('olympiad-status-finished')) {
            return 'finished';
        }
        return '';
    }
    
    /**
     * Извлекает текст из карточки для поиска (название + описание).
     * @param {HTMLElement} card - Элемент карточки олимпиады.
     * @returns {string} Объединенный текст в нижнем регистре.
     */
    function getCardText(card) {
        const title = card.querySelector('.olympiad-title')?.textContent || '';
        const description = card.querySelector('.olympiad-description')?.textContent || '';
        return (title + ' ' + description).toLowerCase();
    }
    
    /**
     * Получает список предметов олимпиады из data-атрибута.
     * @param {HTMLElement} card - Элемент карточки олимпиады.
     * @returns {Array<string>} Массив названий предметов в нижнем регистре.
     */
    function getCardSubjects(card) {
        const subjectsAttr = card.getAttribute('data-subjects') || '';
        return subjectsAttr.toLowerCase().split(',').map(function(s) {
            return s.trim();
        });
    }
    
    /**
     * Фильтрует карточки олимпиад по поисковому запросу, статусу и предмету.
     * После фильтрации применяет сортировку и обновляет отображение.
     */
    function filterCards() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const statusValue = statusFilter.value;
        const subjectValue = subjectFilter.value;
        
        filteredCards = allCards.filter(function(card) {
            // Фильтр по поиску
            if (searchTerm && !getCardText(card).includes(searchTerm)) {
                return false;
            }
            
            // Фильтр по статусу
            if (statusValue !== 'all') {
                const cardStatus = getCardStatus(card);
                if (cardStatus !== statusValue) {
                    return false;
                }
            }
            
            // Фильтр по предмету
            if (subjectValue !== 'all') {
                const cardSubjects = getCardSubjects(card);
                if (!cardSubjects.includes(subjectValue.toLowerCase())) {
                    return false;
                }
            }
            
            return true;
        });
        
        // Сортировка
        sortCards();
        
        // Обновление отображения
        updateDisplay();
    }
    
    /**
     * Сортирует отфильтрованные карточки олимпиад.
     * Поддерживает сортировку по названию и дате начала.
     */
    function sortCards() {
        const sortValue = sortFilter.value;
        
        filteredCards.sort(function(a, b) {
            if (sortValue === 'name-asc' || sortValue === 'name-desc') {
                const titleA = a.querySelector('.olympiad-title')?.textContent || '';
                const titleB = b.querySelector('.olympiad-title')?.textContent || '';
                return sortValue === 'name-asc' 
                    ? titleA.localeCompare(titleB, 'ru')
                    : titleB.localeCompare(titleA, 'ru');
            } else if (sortValue === 'date-desc' || sortValue === 'date-asc') {
                const dateA = new Date(a.getAttribute('data-start-date') || 0);
                const dateB = new Date(b.getAttribute('data-start-date') || 0);
                return sortValue === 'date-desc' ? dateB - dateA : dateA - dateB;
            }
            return 0;
        });
    }
    
    /**
     * Обновляет отображение отфильтрованных карточек с учетом пагинации.
     * Обновляет счетчик результатов и создает элементы пагинации.
     */
    function updateDisplay() {
        // Обновление счетчика
        const count = filteredCards.length;
        resultsCount.innerHTML = 'Найдено: <strong>' + count + '</strong> олимпиад';
        
        // Очистка контейнера
        container.innerHTML = '';
        
        // Вычисление пагинации
        const totalPages = Math.ceil(filteredCards.length / itemsPerPage);
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const cardsToShow = filteredCards.slice(startIndex, endIndex);
        
        // Отображение карточек
        cardsToShow.forEach(function(card) {
            container.appendChild(card);
        });
        
        // Обновление пагинации
        updatePagination(totalPages);
    }
    
    /**
     * Создает и обновляет элементы пагинации.
     * @param {number} totalPages - Общее количество страниц.
     */
    function updatePagination(totalPages) {
        if (totalPages <= 1) {
            paginationContainer.style.display = 'none';
            return;
        }
        
        paginationContainer.style.display = 'flex';
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';
        
        // Кнопка "Предыдущая"
        const prevBtn = document.createElement('button');
        prevBtn.className = 'pagination-btn' + (currentPage === 1 ? ' disabled' : '');
        prevBtn.textContent = '← Предыдущая';
        prevBtn.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                updateDisplay();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
        pagination.appendChild(prevBtn);
        
        // Номера страниц
        const maxVisible = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
        let endPage = Math.min(totalPages, startPage + maxVisible - 1);
        
        if (endPage - startPage < maxVisible - 1) {
            startPage = Math.max(1, endPage - maxVisible + 1);
        }
        
        if (startPage > 1) {
            const firstBtn = document.createElement('button');
            firstBtn.className = 'pagination-btn';
            firstBtn.textContent = '1';
            firstBtn.addEventListener('click', function() {
                currentPage = 1;
                updateDisplay();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            pagination.appendChild(firstBtn);
            
            if (startPage > 2) {
                const dots = document.createElement('span');
                dots.className = 'pagination-info';
                dots.textContent = '...';
                pagination.appendChild(dots);
            }
        }
        
        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.className = 'pagination-btn' + (i === currentPage ? ' active' : '');
            pageBtn.textContent = i;
            pageBtn.addEventListener('click', function() {
                currentPage = i;
                updateDisplay();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            pagination.appendChild(pageBtn);
        }
        
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                const dots = document.createElement('span');
                dots.className = 'pagination-info';
                dots.textContent = '...';
                pagination.appendChild(dots);
            }
            
            const lastBtn = document.createElement('button');
            lastBtn.className = 'pagination-btn';
            lastBtn.textContent = totalPages;
            lastBtn.addEventListener('click', function() {
                currentPage = totalPages;
                updateDisplay();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            pagination.appendChild(lastBtn);
        }
        
        // Кнопка "Следующая"
        const nextBtn = document.createElement('button');
        nextBtn.className = 'pagination-btn' + (currentPage === totalPages ? ' disabled' : '');
        nextBtn.textContent = 'Следующая →';
        nextBtn.addEventListener('click', function() {
            if (currentPage < totalPages) {
                currentPage++;
                updateDisplay();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
        pagination.appendChild(nextBtn);
    }
    
    // Обработчики событий
    searchInput.addEventListener('input', function() {
        currentPage = 1;
        filterCards();
    });
    
    statusFilter.addEventListener('change', function() {
        currentPage = 1;
        filterCards();
    });
    
    subjectFilter.addEventListener('change', function() {
        currentPage = 1;
        filterCards();
    });
    
    sortFilter.addEventListener('change', function() {
        currentPage = 1;
        filterCards();
    });
    
    resetBtn.addEventListener('click', function() {
        searchInput.value = '';
        statusFilter.value = 'all';
        subjectFilter.value = 'all';
        sortFilter.value = 'date-desc';
        currentPage = 1;
        filterCards();
    });
    
    // Инициализация
    updateDisplay();
});

