// TaskFlow JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupTabSwitching();
    setupRecommendationButtons();
    setupRecommendationChips();
    setupDrawer();
    setupFilters();
    setupAssignmentButtons();
}

// Tab Switching Functionality
function setupTabSwitching() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            button.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

// Recommendation Button Functionality
function setupRecommendationButtons() {
    const recommendationButtons = document.querySelectorAll('.get-recommendation-btn');
    
    recommendationButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const taskId = button.getAttribute('data-task-id');
            const recommendationsDiv = document.getElementById(`rec-${taskId}`);
            
            if (recommendationsDiv.classList.contains('hidden')) {
                // Show loading state
                button.textContent = '⏳ Loading...';
                button.disabled = true;
                
                // Simulate API call delay
                setTimeout(() => {
                    recommendationsDiv.classList.remove('hidden');
                    button.textContent = '🔄 Refresh Recommendations';
                    button.disabled = false;
                }, 1000);
            } else {
                // Refresh recommendations
                button.textContent = '⏳ Loading...';
                button.disabled = true;
                
                setTimeout(() => {
                    button.textContent = '🔄 Refresh Recommendations';
                    button.disabled = false;
                    showNotification('Recommendations refreshed!');
                }, 800);
            }
        });
    });
}

// Recommendation Chip Functionality
function setupRecommendationChips() {
    const recommendationChips = document.querySelectorAll('.rec-chip');
    
    recommendationChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const memberId = chip.getAttribute('data-member-id');
            const memberName = chip.querySelector('.member-name').textContent;
            const score = chip.querySelector('.score').textContent;
            
            // Remove selected class from all chips in the same group
            const parentChips = chip.parentElement.querySelectorAll('.rec-chip');
            parentChips.forEach(c => c.classList.remove('selected'));
            
            // Add selected class to clicked chip
            chip.classList.add('selected');
            
            // Show explainability drawer
            showExplainabilityDrawer(memberId, memberName, score);
        });
    });
}

// Explainability Drawer Functionality
function setupDrawer() {
    const drawer = document.getElementById('explainability-drawer');
    const overlay = document.getElementById('overlay');
    const closeButton = document.querySelector('.close-drawer');
    
    closeButton.addEventListener('click', hideExplainabilityDrawer);
    overlay.addEventListener('click', hideExplainabilityDrawer);
    
    // Close drawer on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !drawer.classList.contains('hidden')) {
            hideExplainabilityDrawer();
        }
    });
}

function showExplainabilityDrawer(memberId, memberName, score) {
    const drawer = document.getElementById('explainability-drawer');
    const overlay = document.getElementById('overlay');
    
    // Update drawer content based on selected member
    updateDrawerContent(memberId, memberName, score);
    
    // Show drawer and overlay
    drawer.classList.remove('hidden');
    overlay.classList.remove('hidden');
    
    // Add animation delay
    setTimeout(() => {
        drawer.style.transform = 'translateX(0)';
    }, 10);
}

function hideExplainabilityDrawer() {
    const drawer = document.getElementById('explainability-drawer');
    const overlay = document.getElementById('overlay');
    
    drawer.style.transform = 'translateX(100%)';
    
    setTimeout(() => {
        drawer.classList.add('hidden');
        overlay.classList.add('hidden');
    }, 300);
}

function updateDrawerContent(memberId, memberName, score) {
    // Mock data for different members
    const memberData = {
        'john-doe': {
            skillMatch: '90%',
            skillDetails: 'Strong match for React (Expert), Node.js (Advanced), JWT (Intermediate)',
            loadFactor: '78%',
            loadDetails: 'Currently at 31h/40h capacity (78% utilized). Has 9 hours available this week.',
            calendarFactor: '100%',
            calendarDetails: 'No conflicts with deadline. Available throughout the task timeline.',
            historyFactor: '85%',
            historyDetails: 'Successfully completed 3 similar authentication tasks. Average completion time: 2.5 days.'
        },
        'jane-smith': {
            skillMatch: '85%',
            skillDetails: 'Good match for React (Advanced), Node.js (Intermediate), JWT (Beginner)',
            loadFactor: '75%',
            loadDetails: 'Currently at 30h/40h capacity (75% utilized). Has 10 hours available this week.',
            calendarFactor: '90%',
            calendarDetails: 'One meeting conflict on Wednesday, but can work around it.',
            historyFactor: '90%',
            historyDetails: 'Successfully completed 5 similar tasks. Excellent track record with authentication features.'
        },
        'mike-wilson': {
            skillMatch: '80%',
            skillDetails: 'Moderate match for React (Intermediate), Node.js (Expert), JWT (Advanced)',
            loadFactor: '98%',
            loadDetails: 'Currently at 39h/40h capacity (98% utilized). Very limited availability.',
            calendarFactor: '70%',
            calendarDetails: 'Several meetings scheduled. Limited focused work time available.',
            historyFactor: '75%',
            historyDetails: 'Completed 2 similar tasks. Good performance but slower completion times.'
        },
        'sarah-jones': {
            skillMatch: '95%',
            skillDetails: 'Excellent match for PostgreSQL (Expert), Python (Expert), DevOps (Advanced)',
            loadFactor: '50%',
            loadDetails: 'Currently at 20h/40h capacity (50% utilized). Plenty of availability.',
            calendarFactor: '100%',
            calendarDetails: 'No scheduling conflicts. Fully available for the task timeline.',
            historyFactor: '95%',
            historyDetails: 'Database migration specialist. Completed 8 similar tasks with perfect success rate.'
        },
        'emma-davis': {
            skillMatch: '92%',
            skillDetails: 'Excellent match for React Native (Expert), UI/UX (Expert), Mobile Design (Advanced)',
            loadFactor: '80%',
            loadDetails: 'Currently at 32h/40h capacity (80% utilized). Some availability for new tasks.',
            calendarFactor: '85%',
            calendarDetails: 'Few minor scheduling conflicts, but manageable within deadline.',
            historyFactor: '88%',
            historyDetails: 'Mobile UI specialist. Completed 6 similar redesign projects successfully.'
        }
    };
    
    const data = memberData[memberId] || memberData['john-doe'];
    
    // Update drawer elements
    document.getElementById('selected-member-name').textContent = memberName;
    document.getElementById('overall-score').textContent = score;
    document.getElementById('skill-match').textContent = data.skillMatch;
    document.getElementById('skill-details').textContent = data.skillDetails;
    document.getElementById('load-factor').textContent = data.loadFactor;
    document.getElementById('load-details').textContent = data.loadDetails;
    document.getElementById('calendar-factor').textContent = data.calendarFactor;
    document.getElementById('calendar-details').textContent = data.calendarDetails;
    document.getElementById('history-factor').textContent = data.historyFactor;
    document.getElementById('history-details').textContent = data.historyDetails;
}

// Filter Functionality
function setupFilters() {
    const filters = document.querySelectorAll('.filters-section select');
    
    filters.forEach(filter => {
        filter.addEventListener('change', () => {
            applyFilters();
        });
    });
}

function applyFilters() {
    const projectFilter = document.getElementById('project-filter').value;
    const roleFilter = document.getElementById('role-filter').value;
    const skillFilter = document.getElementById('skill-filter').value;
    const priorityFilter = document.getElementById('priority-filter').value;
    const dueWindowFilter = document.getElementById('due-window-filter').value;
    
    const taskItems = document.querySelectorAll('.task-item');
    
    taskItems.forEach(item => {
        let shouldShow = true;
        
        // Apply project filter
        if (projectFilter) {
            const projectTag = item.querySelector('.project-tag');
            if (!projectTag || !projectTag.textContent.toLowerCase().includes(projectFilter.toLowerCase())) {
                shouldShow = false;
            }
        }
        
        // Apply priority filter
        if (priorityFilter) {
            const priorityTag = item.querySelector('.priority-tag');
            if (!priorityTag || !priorityTag.classList.contains(priorityFilter)) {
                shouldShow = false;
            }
        }
        
        // Apply skill filter
        if (skillFilter) {
            const skillTags = item.querySelectorAll('.skill-tag');
            let hasSkill = false;
            skillTags.forEach(tag => {
                if (tag.textContent.toLowerCase().includes(skillFilter.toLowerCase())) {
                    hasSkill = true;
                }
            });
            if (!hasSkill) {
                shouldShow = false;
            }
        }
        
        // Show/hide item
        if (shouldShow) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
    
    showNotification('Filters applied successfully!');
}

// Assignment Button Functionality
function setupAssignmentButtons() {
    const assignButtons = document.querySelectorAll('.assign-btn');
    
    assignButtons.forEach(button => {
        button.addEventListener('click', () => {
            const taskId = button.getAttribute('data-task-id');
            const selectedChip = button.closest('.recommendations').querySelector('.rec-chip.selected');
            
            if (!selectedChip) {
                showNotification('Please select a team member first!', 'warning');
                return;
            }
            
            const memberName = selectedChip.querySelector('.member-name').textContent;
            const notifyCheckbox = button.parentElement.querySelector('input[type="checkbox"]');
            const shouldNotify = notifyCheckbox.checked;
            
            // Show loading state
            button.textContent = 'Assigning...';
            button.disabled = true;
            
            // Simulate assignment API call
            setTimeout(() => {
                button.textContent = 'Assigned!';
                button.style.background = '#48bb78';
                
                let message = `Task assigned to ${memberName}`;
                if (shouldNotify) {
                    message += ' (notification sent)';
                }
                
                showNotification(message, 'success');
                
                // Reset button after delay
                setTimeout(() => {
                    button.textContent = 'Override & Assign';
                    button.style.background = '';
                    button.disabled = false;
                }, 2000);
            }, 1500);
        });
    });
}

// Notification System
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '12px 20px',
        borderRadius: '6px',
        color: 'white',
        fontWeight: '500',
        zIndex: '10000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease',
        maxWidth: '300px',
        wordWrap: 'break-word'
    });
    
    // Set background color based on type
    switch (type) {
        case 'success':
            notification.style.background = '#48bb78';
            break;
        case 'warning':
            notification.style.background = '#ed8936';
            break;
        case 'error':
            notification.style.background = '#e53e3e';
            break;
        default:
            notification.style.background = '#667eea';
    }
    
    // Add to DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// Capacity Heatmap Functionality
function setupCapacityHeatmap() {
    const sprintSelect = document.getElementById('sprint-select');
    
    if (sprintSelect) {
        sprintSelect.addEventListener('change', () => {
            updateCapacityData();
        });
    }
}

function updateCapacityData() {
    // Simulate loading new capacity data
    showNotification('Updating capacity data...', 'info');
    
    setTimeout(() => {
        showNotification('Capacity data updated!', 'success');
    }, 1000);
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + 1 for Tasks tab
    if ((e.ctrlKey || e.metaKey) && e.key === '1') {
        e.preventDefault();
        document.querySelector('[data-tab="tasks"]').click();
    }
    
    // Ctrl/Cmd + 2 for Capacity tab
    if ((e.ctrlKey || e.metaKey) && e.key === '2') {
        e.preventDefault();
        document.querySelector('[data-tab="capacity"]').click();
    }
});

// Initialize capacity heatmap when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupCapacityHeatmap();
});

// Utility Functions
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

// Export functions for potential external use
window.TaskFlow = {
    showNotification,
    showExplainabilityDrawer,
    hideExplainabilityDrawer,
    applyFilters
};
