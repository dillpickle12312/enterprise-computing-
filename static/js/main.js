// Main JavaScript file for Mentorship System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });    // Auto-hide alerts after 7 seconds (increased from 5)
    setTimeout(function() {
        var alerts = document.querySelectorAll('#flash-messages .alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 7000);

    // Enhanced loading state for forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn && !submitBtn.dataset.skipLoading) {
                var originalText = submitBtn.innerHTML || submitBtn.value;
                var loadingText = submitBtn.dataset.loadingText || 'Processing...';
                
                if (submitBtn.tagName === 'BUTTON') {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + loadingText;
                } else {
                    submitBtn.value = loadingText;
                }
                submitBtn.disabled = true;
                
                // Re-enable after 10 seconds as fallback
                setTimeout(function() {
                    if (submitBtn.tagName === 'BUTTON') {
                        submitBtn.innerHTML = originalText;
                    } else {
                        submitBtn.value = originalText;
                    }
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });

    // Enhanced confirmation dialogs for destructive actions
    var dangerButtons = document.querySelectorAll('.btn-danger, .btn-outline-danger, [data-confirm]');
    dangerButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            var confirmText = btn.dataset.confirm;
            var isDestructive = btn.classList.contains('btn-danger') || 
                              btn.classList.contains('btn-outline-danger') ||
                              btn.textContent.toLowerCase().includes('delete') || 
                              btn.textContent.toLowerCase().includes('remove') ||
                              btn.textContent.toLowerCase().includes('clear');
            
            if (confirmText || isDestructive) {
                var message = confirmText || 'Are you sure you want to perform this action? This cannot be undone.';
                if (!confirm(message)) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    });

    // Search and Filter Functionality
    initializeSearch();
});

// Search and Filter Functions
function initializeSearch() {
    // Mentor search functionality
    const mentorSearch = document.getElementById('mentorSearch');
    const subjectFilter = document.getElementById('subjectFilter');
    const capacityFilter = document.getElementById('capacityFilter');
    
    if (mentorSearch || subjectFilter || capacityFilter) {
        const searchHandler = () => filterMentors();
        
        if (mentorSearch) mentorSearch.addEventListener('input', searchHandler);
        if (subjectFilter) subjectFilter.addEventListener('change', searchHandler);
        if (capacityFilter) capacityFilter.addEventListener('change', searchHandler);
    }

    // Mentee search functionality
    const menteeSearch = document.getElementById('menteeSearch');
    const menteeSubjectFilter = document.getElementById('menteeSubjectFilter');
    const assignmentFilter = document.getElementById('assignmentFilter');
    
    if (menteeSearch || menteeSubjectFilter || assignmentFilter) {
        const searchHandler = () => filterMentees();
        
        if (menteeSearch) menteeSearch.addEventListener('input', searchHandler);
        if (menteeSubjectFilter) menteeSubjectFilter.addEventListener('change', searchHandler);
        if (assignmentFilter) assignmentFilter.addEventListener('change', searchHandler);
    }
}

function filterMentors() {
    const searchTerm = document.getElementById('mentorSearch')?.value.toLowerCase() || '';
    const subjectFilter = document.getElementById('subjectFilter')?.value || '';
    const capacityFilter = document.getElementById('capacityFilter')?.value || '';
    
    const mentorCards = document.querySelectorAll('.col-md-6 .card');
    let visibleCount = 0;
    
    mentorCards.forEach(card => {
        const nameEl = card.querySelector('h5');
        const rollCallEl = card.querySelector('.badge.bg-light');
        const subjectsEl = card.querySelector('.badge.bg-secondary');
        const capacityEl = card.querySelector('small');
        
        if (!nameEl) return; // Skip if not a mentor card
        
        const name = nameEl.textContent.toLowerCase();
        const rollCall = rollCallEl?.textContent.toLowerCase() || '';
        const subjects = subjectsEl?.textContent || '';
        const capacity = capacityEl?.textContent || '';
        
        let visible = true;
        
        // Text search
        if (searchTerm && !name.includes(searchTerm) && !rollCall.includes(searchTerm)) {
            visible = false;
        }
        
        // Subject filter
        if (subjectFilter && !subjects.includes(subjectFilter)) {
            visible = false;
        }
        
        // Capacity filter - look for capacity info in the card
        if (capacityFilter === 'available' && capacity.includes('5 / 5')) {
            visible = false;
        } else if (capacityFilter === 'full' && !capacity.includes('5 / 5')) {
            visible = false;
        }
        
        const cardContainer = card.closest('.col-md-6');
        if (cardContainer) {
            cardContainer.style.display = visible ? '' : 'none';
            if (visible) visibleCount++;
        }
    });
    
    updateResultsCount('mentorResults', visibleCount, mentorCards.length);
}

function filterMentees() {
    const searchTerm = document.getElementById('menteeSearch')?.value.toLowerCase() || '';
    const subjectFilter = document.getElementById('menteeSubjectFilter')?.value || '';
    const assignmentFilter = document.getElementById('assignmentFilter')?.value || '';
    
    const rows = document.querySelectorAll('#menteeTable tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const name = row.querySelector('td:nth-child(1)')?.textContent.toLowerCase() || '';
        const rollCall = row.querySelector('td:nth-child(2)')?.textContent.toLowerCase() || '';
        const subject = row.querySelector('td:nth-child(3)')?.textContent || '';
        const mentor = row.querySelector('td:nth-child(5)')?.textContent || '';
        
        let visible = true;
        
        // Text search
        if (searchTerm && !name.includes(searchTerm) && !rollCall.includes(searchTerm)) {
            visible = false;
        }
        
        // Subject filter
        if (subjectFilter && !subject.includes(subjectFilter)) {
            visible = false;
        }
        
        // Assignment filter
        if (assignmentFilter === 'assigned' && mentor.includes('Unassigned')) {
            visible = false;
        } else if (assignmentFilter === 'unassigned' && !mentor.includes('Unassigned')) {
            visible = false;
        }
        
        row.style.display = visible ? '' : 'none';
        if (visible) visibleCount++;
    });
    
    updateResultsCount('menteeResults', visibleCount, rows.length);
}

function updateResultsCount(elementId, visible, total) {
    const resultsEl = document.getElementById(elementId);
    if (resultsEl) {
        resultsEl.textContent = visible === total ? 
            `Showing all ${total} results` : 
            `Showing ${visible} of ${total} results`;
    }
}

// Utility Functions

/**
 * Show a toast notification
 * @param {string} message - The message to display
 * @param {string} type - The type of toast (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type === 'error' ? 'danger' : type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
    
    // Remove toast element after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Get or create toast container
 */
function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Format date for display
 * @param {Date|string} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Format time for display
 * @param {Date|string} date - The date/time to format
 * @returns {string} Formatted time string
 */
function formatTime(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Format datetime for display
 * @param {Date|string} date - The datetime to format
 * @returns {string} Formatted datetime string
 */
function formatDateTime(date) {
    return formatDate(date) + ' at ' + formatTime(date);
}

/**
 * Validate form data
 * @param {HTMLFormElement} form - The form to validate
 * @returns {boolean} True if valid, false otherwise
 */
function validateForm(form) {
    var isValid = true;
    var requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

/**
 * Show loading spinner
 * @param {HTMLElement} element - Element to show spinner in
 */
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.setAttribute('data-original-content', originalContent);
    element.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
    element.disabled = true;
}

/**
 * Hide loading spinner
 * @param {HTMLElement} element - Element to hide spinner from
 */
function hideLoading(element) {
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
    }
    element.disabled = false;
}

/**
 * Debounce function to limit rapid function calls
 * @param {Function} func - The function to debounce
 * @param {number} wait - The wait time in milliseconds
 * @returns {Function} Debounced function
 */
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

/**
 * Filter table rows based on search input
 * @param {string} searchValue - The search value
 * @param {HTMLTableElement} table - The table to filter
 */
function filterTable(searchValue, table) {
    const rows = table.querySelectorAll('tbody tr');
    const searchTerm = searchValue.toLowerCase();
    
    rows.forEach(function(row) {
        const text = row.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

/**
 * Copy text to clipboard
 * @param {string} text - Text to copy
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
    } catch (err) {
        console.error('Failed to copy: ', err);
        showToast('Failed to copy to clipboard', 'error');
    }
}

/**
 * Get status badge class based on status
 * @param {string} status - The status
 * @returns {string} Bootstrap class for the status
 */
function getStatusBadgeClass(status) {
    const statusClasses = {
        'scheduled': 'bg-primary',
        'completed': 'bg-success',
        'canceled': 'bg-danger',
        'cancelled': 'bg-danger',
        'rescheduled': 'bg-warning',
        'missed': 'bg-dark',
        'active': 'bg-success',
        'inactive': 'bg-secondary',
        'pending': 'bg-warning'
    };
    
    return statusClasses[status.toLowerCase()] || 'bg-secondary';
}

/**
 * Auto-resize textarea based on content
 * @param {HTMLTextAreaElement} textarea - The textarea element
 */
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Initialize auto-resize for all textareas
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
    });
});

/**
 * Smooth scroll to element
 * @param {string} elementId - ID of the element to scroll to
 */
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Check if user is on mobile device
 * @returns {boolean} True if on mobile
 */
function isMobile() {
    return window.innerWidth <= 768;
}

/**
 * Format file size for display
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
function formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 Bytes';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

// Session management functions
window.sessionFunctions = {
    updateStatus: function(sessionId, status) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/update_session_status';
        
        const sessionInput = document.createElement('input');
        sessionInput.type = 'hidden';
        sessionInput.name = 'session_id';
        sessionInput.value = sessionId;
        
        const statusInput = document.createElement('input');
        statusInput.type = 'hidden';
        statusInput.name = 'status';
        statusInput.value = status;
        
        form.appendChild(sessionInput);
        form.appendChild(statusInput);
        
        document.body.appendChild(form);
        form.submit();
    },
    
    reschedule: function(sessionId) {
        document.getElementById('reschedule-session-id').value = sessionId;
        const modal = new bootstrap.Modal(document.getElementById('rescheduleModal'));
        modal.show();
    }
};

// Export functions for global use
window.mentorshipUtils = {
    showToast,
    formatDate,
    formatTime,
    formatDateTime,
    validateForm,
    showLoading,
    hideLoading,
    debounce,
    filterTable,
    copyToClipboard,
    getStatusBadgeClass,
    autoResizeTextarea,
    smoothScrollTo,
    isMobile,
    formatFileSize
};
