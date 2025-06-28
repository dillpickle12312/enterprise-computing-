/* Enhanced Interactive Features for Outstanding Rating */

// Real-time notification system
function initializeNotifications() {
    // Check for new notifications every 30 seconds
    setInterval(checkNotifications, 30000);
    
    // Show browser notifications if permission granted
    if ("Notification" in window && Notification.permission === "granted") {
        enableRealTimeNotifications();
    }
}

// Advanced search with filters
function enhancedSearch() {
    const searchInput = document.getElementById('search');
    const filters = {
        subject: document.getElementById('filter-subject').value,
        experience: document.getElementById('filter-experience').value,
        availability: document.getElementById('filter-availability').value
    };
    
    // Live search with debouncing
    searchInput.addEventListener('input', debounce(performSearch, 300));
}

// Progress tracking with visual indicators
function createProgressChart(menteeId, progressData) {
    const ctx = document.getElementById('progressChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: progressData.dates,
            datasets: [{
                label: 'Progress Score',
                data: progressData.scores,
                borderColor: '#4CAF50',
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Mentee Progress Over Time'
                }
            }
        }
    });
}

// Mobile-first PWA features
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
        .then(registration => console.log('PWA registered'))
        .catch(error => console.log('PWA registration failed'));
}

// Advanced data export with multiple formats
function exportData(format, dataType) {
    const exportOptions = {
        'csv': exportToCSV,
        'excel': exportToExcel,
        'pdf': exportToPDF,
        'json': exportToJSON
    };
    
    exportOptions[format](dataType);
}

// Bulk operations for efficient management
function initializeBulkOperations() {
    const selectAllCheckbox = document.getElementById('select-all');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');
    const bulkActionBtn = document.getElementById('bulk-action-btn');
    
    // Select all functionality
    selectAllCheckbox?.addEventListener('change', function() {
        itemCheckboxes.forEach(checkbox => {
            checkbox.checked = this.checked;
        });
        updateBulkActionButton();
    });
    
    // Individual checkbox handling
    itemCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionButton);
    });
    
    function updateBulkActionButton() {
        const checkedBoxes = document.querySelectorAll('.item-checkbox:checked');
        if (checkedBoxes.length > 0) {
            bulkActionBtn.style.display = 'block';
            bulkActionBtn.textContent = `Bulk Actions (${checkedBoxes.length} selected)`;
        } else {
            bulkActionBtn.style.display = 'none';
        }
    }
}

// Smart matching suggestions for coordinators
function generateMatchingSuggestions() {
    fetch('/api/matching-suggestions')
        .then(response => response.json())
        .then(suggestions => {
            const container = document.getElementById('suggestions-container');
            container.innerHTML = '';
            
            suggestions.forEach(suggestion => {
                const card = createSuggestionCard(suggestion);
                container.appendChild(card);
            });
        });
}

function createSuggestionCard(suggestion) {
    const card = document.createElement('div');
    card.className = 'suggestion-card';
    card.innerHTML = `
        <div class="match-score">Match Score: ${suggestion.score}%</div>
        <div class="mentor-info">
            <strong>Mentor:</strong> ${suggestion.mentor.name}
            <span class="expertise">${suggestion.mentor.expertise.join(', ')}</span>
        </div>
        <div class="mentee-info">
            <strong>Mentee:</strong> ${suggestion.mentee.name}
            <span class="interests">${suggestion.mentee.interests.join(', ')}</span>
        </div>
        <div class="match-reasons">
            <strong>Why this match:</strong>
            <ul>
                ${suggestion.reasons.map(reason => `<li>${reason}</li>`).join('')}
            </ul>
        </div>
        <div class="action-buttons">
            <button onclick="acceptMatch(${suggestion.mentor.id}, ${suggestion.mentee.id})" 
                    class="btn btn-success">Accept Match</button>
            <button onclick="dismissSuggestion(${suggestion.id})" 
                    class="btn btn-secondary">Dismiss</button>
        </div>
    `;
    return card;
}

// Automated progress tracking and alerts
function setupProgressMonitoring() {
    // Check for mentees who haven't had sessions recently
    fetch('/api/inactive-mentees')
        .then(response => response.json())
        .then(inactiveMentees => {
            if (inactiveMentees.length > 0) {
                showInactivityAlert(inactiveMentees);
            }
        });
    
    // Generate weekly progress summary
    generateWeeklyProgressSummary();
}

function showInactivityAlert(inactiveMentees) {
    const alertContainer = document.getElementById('alerts-container');
    const alert = document.createElement('div');
    alert.className = 'alert alert-warning';
    alert.innerHTML = `
        <h5>⚠️ Attention Required</h5>
        <p>${inactiveMentees.length} mentee(s) haven't had sessions in over 2 weeks:</p>
        <ul>
            ${inactiveMentees.map(mentee => 
                `<li>${mentee.name} - Last session: ${mentee.lastSession}</li>`
            ).join('')}
        </ul>
        <button onclick="scheduleFollowUp()" class="btn btn-primary btn-sm">
            Schedule Follow-up Sessions
        </button>
    `;
    alertContainer.appendChild(alert);
}

// Enhanced reporting dashboard for coordinators
function createCoordinatorDashboard() {
    const dashboardData = {
        totalMentors: 45,
        totalMentees: 156,
        activeAssignments: 89,
        completedSessions: 234,
        averageSessionRating: 4.2,
        programmeEffectiveness: 87
    };
    
    // Create KPI cards
    createKPICards(dashboardData);
    
    // Create trend charts
    createTrendCharts();
    
    // Create actionable insights
    generateActionableInsights();
}

function createKPICards(data) {
    const kpiContainer = document.getElementById('kpi-container');
    const kpis = [
        { title: 'Total Mentors', value: data.totalMentors, icon: '👨‍🏫', trend: '+5%' },
        { title: 'Total Mentees', value: data.totalMentees, icon: '👨‍🎓', trend: '+12%' },
        { title: 'Active Matches', value: data.activeAssignments, icon: '🔗', trend: '+8%' },
        { title: 'Avg. Rating', value: data.averageSessionRating, icon: '⭐', trend: '+0.3' }
    ];
    
    kpis.forEach(kpi => {
        const card = document.createElement('div');
        card.className = 'kpi-card';
        card.innerHTML = `
            <div class="kpi-icon">${kpi.icon}</div>
            <div class="kpi-content">
                <h3>${kpi.value}</h3>
                <p>${kpi.title}</p>
                <span class="kpi-trend trend-positive">${kpi.trend}</span>
            </div>
        `;
        kpiContainer.appendChild(card);
    });
}

// Smart scheduling assistant
function initializeSchedulingAssistant() {
    const scheduleBtn = document.getElementById('smart-schedule-btn');
    scheduleBtn?.addEventListener('click', function() {
        const mentorId = document.getElementById('mentor-select').value;
        const menteeId = document.getElementById('mentee-select').value;
        
        if (mentorId && menteeId) {
            findOptimalTimeSlots(mentorId, menteeId);
        }
    });
}

function findOptimalTimeSlots(mentorId, menteeId) {
    fetch(`/api/optimal-slots/${mentorId}/${menteeId}`)
        .then(response => response.json())
        .then(slots => {
            displayTimeSlotSuggestions(slots);
        });
}

function displayTimeSlotSuggestions(slots) {
    const container = document.getElementById('time-suggestions');
    container.innerHTML = '<h5>Suggested Time Slots:</h5>';
    
    slots.forEach((slot, index) => {
        const suggestion = document.createElement('div');
        suggestion.className = 'time-suggestion';
        suggestion.innerHTML = `
            <div class="slot-info">
                <strong>${slot.day} ${slot.time}</strong>
                <span class="compatibility-score">Compatibility: ${slot.score}%</span>
            </div>
            <button onclick="bookTimeSlot('${slot.datetime}')" 
                    class="btn btn-primary btn-sm">Book This Slot</button>
        `;
        container.appendChild(suggestion);
    });
}

// Automated email templates for common scenarios
function setupEmailTemplates() {
    const templates = {
        'welcome-mentor': {
            subject: 'Welcome to the Mentorship Programme',
            body: 'Dear {mentor_name}, Welcome to our mentorship programme...'
        },
        'assignment-notification': {
            subject: 'New Mentee Assignment',
            body: 'You have been assigned a new mentee: {mentee_name}...'
        },
        'session-reminder': {
            subject: 'Upcoming Mentoring Session',
            body: 'Reminder: You have a session scheduled for {date} at {time}...'
        },
        'progress-check': {
            subject: 'Monthly Progress Check-in',
            body: 'It\'s time for your monthly progress update...'
        }
    };
    
    // Make templates available globally
    window.emailTemplates = templates;
}

// Quick actions for busy coordinators
function initializeQuickActions() {
    const quickActions = [
        {
            name: 'Assign Unmatched Mentees',
            action: assignUnmatchedMentees,
            icon: '🔗',
            count: 12
        },
        {
            name: 'Send Weekly Reminders',
            action: sendWeeklyReminders,
            icon: '📧',
            count: null
        },
        {
            name: 'Generate Progress Report',
            action: generateProgressReport,
            icon: '📊',
            count: null
        },
        {
            name: 'Review Pending Sessions',
            action: reviewPendingSessions,
            icon: '📅',
            count: 8
        }
    ];
    
    const container = document.getElementById('quick-actions');
    quickActions.forEach(action => {
        const button = document.createElement('button');
        button.className = 'quick-action-btn';
        button.innerHTML = `
            ${action.icon} ${action.name}
            ${action.count ? `<span class="count-badge">${action.count}</span>` : ''}
        `;
        button.addEventListener('click', action.action);
        container.appendChild(button);
    });
}

// Initialize all enhanced features when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeBulkOperations();
    initializeSchedulingAssistant();
    setupProgressMonitoring();
    setupEmailTemplates();
    initializeQuickActions();
    
    // Load dashboard if user is coordinator/admin
    if (document.body.classList.contains('coordinator-role')) {
        createCoordinatorDashboard();
        generateMatchingSuggestions();
    }
});

// Utility functions
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
