// The Stones TaskFlow Authentication Middleware

// Authentication state
let currentUser = null;
let sessionData = null;

// Initialize authentication on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
});

function initializeAuth() {
    // Check if user is authenticated
    if (!checkAuthentication()) {
        redirectToLogin();
        return;
    }
    
    // Setup authenticated UI
    setupAuthenticatedUI();
    setupLogoutFunctionality();
    setupSessionMonitoring();
}

function checkAuthentication() {
    sessionData = getStoredSession();
    
    if (!sessionData || !isSessionValid(sessionData)) {
        clearInvalidSession();
        return false;
    }
    
    currentUser = sessionData.user;
    return true;
}

function getStoredSession() {
    // Check both localStorage and sessionStorage
    let sessionData = localStorage.getItem('thestones_taskflow_session');
    if (!sessionData) {
        sessionData = sessionStorage.getItem('thestones_taskflow_session');
    }
    
    if (sessionData) {
        try {
            return JSON.parse(sessionData);
        } catch (e) {
            // Invalid session data, remove it
            clearInvalidSession();
        }
    }
    
    return null;
}

function isSessionValid(sessionData) {
    if (!sessionData || !sessionData.expiresAt) {
        return false;
    }
    
    return new Date(sessionData.expiresAt) > new Date();
}

function clearInvalidSession() {
    localStorage.removeItem('thestones_taskflow_session');
    sessionStorage.removeItem('thestones_taskflow_session');
}

function redirectToLogin() {
    // Show a brief message before redirecting
    document.body.innerHTML = `
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            text-align: center;
        ">
            <div>
                <h2>Authentication Required</h2>
                <p>Redirecting to login...</p>
                <div style="
                    width: 40px;
                    height: 40px;
                    border: 4px solid rgba(255, 255, 255, 0.3);
                    border-top: 4px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 20px auto;
                "></div>
            </div>
        </div>
        <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    `;
    
    setTimeout(() => {
        window.location.href = '../../login.html';
    }, 2000);
}

function setupAuthenticatedUI() {
    // Add user info to header
    addUserInfoToHeader();
    
    // Apply role-based permissions
    applyRoleBasedPermissions();
    
    // Add logout button
    addLogoutButton();
}

function addUserInfoToHeader() {
    const header = document.querySelector('.header');
    if (!header) return;
    
    // Create user info section
    const userInfo = document.createElement('div');
    userInfo.className = 'user-info';
    userInfo.innerHTML = `
        <div class="user-details">
            <span class="user-name">Welcome, ${currentUser.name}</span>
            <span class="user-role">${formatRole(currentUser.role)}</span>
        </div>
        <div class="user-actions">
            <button class="profile-btn" id="profileBtn">Profile</button>
            <button class="logout-btn" id="logoutBtn">Logout</button>
        </div>
    `;
    
    header.appendChild(userInfo);
    
    // Add styles for user info
    addUserInfoStyles();
}

function addUserInfoStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 20px;
            color: white;
        }
        
        .user-details {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            text-align: right;
        }
        
        .user-name {
            font-weight: 600;
            font-size: 1.1rem;
        }
        
        .user-role {
            font-size: 0.9rem;
            opacity: 0.8;
            text-transform: capitalize;
        }
        
        .user-actions {
            display: flex;
            gap: 10px;
        }
        
        .profile-btn,
        .logout-btn {
            padding: 8px 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .profile-btn:hover,
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        .logout-btn:hover {
            background: rgba(220, 38, 38, 0.2);
            border-color: rgba(220, 38, 38, 0.5);
        }
        
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                text-align: center;
            }
            
            .user-info {
                flex-direction: column;
                gap: 12px;
            }
            
            .user-details {
                align-items: center;
                text-align: center;
            }
        }
    `;
    
    document.head.appendChild(style);
}

function formatRole(role) {
    const roleMap = {
        'admin': 'Administrator',
        'manager': 'Project Manager',
        'user': 'Team Member'
    };
    
    return roleMap[role] || role;
}

function applyRoleBasedPermissions() {
    const permissions = currentUser.permissions || [];
    
    // Hide/show elements based on permissions
    if (!permissions.includes('assign_tasks')) {
        // Hide assignment buttons for users without assign permission
        const assignButtons = document.querySelectorAll('.assign-btn');
        assignButtons.forEach(btn => {
            btn.style.display = 'none';
        });
        
        // Hide get recommendation buttons
        const recButtons = document.querySelectorAll('.get-recommendation-btn');
        recButtons.forEach(btn => {
            btn.style.display = 'none';
        });
    }
    
    if (!permissions.includes('view_all')) {
        // Filter tasks to only show assigned ones for regular users
        filterTasksForUser();
    }
    
    if (!permissions.includes('view_analytics')) {
        // Hide capacity heatmap tab for users without analytics permission
        const capacityTab = document.querySelector('[data-tab="capacity"]');
        if (capacityTab) {
            capacityTab.style.display = 'none';
        }
    }
    
    // Add role indicator
    addRoleIndicator();
}

function filterTasksForUser() {
    // This would typically filter tasks based on user assignment
    // For demo purposes, we'll just add a notice
    const taskListSection = document.querySelector('.task-list-section');
    if (taskListSection) {
        const notice = document.createElement('div');
        notice.className = 'user-notice';
        notice.innerHTML = `
            <div style="
                background: #ebf4ff;
                border: 1px solid #bee3f8;
                border-radius: 8px;
                padding: 12px 16px;
                margin-bottom: 16px;
                color: #2b6cb0;
                font-size: 0.9rem;
            ">
                <strong>Note:</strong> You are viewing tasks in read-only mode. Contact your manager for task assignments.
            </div>
        `;
        
        taskListSection.insertBefore(notice, taskListSection.firstChild.nextSibling);
    }
}

function addRoleIndicator() {
    const roleColors = {
        'admin': '#e53e3e',
        'manager': '#ed8936',
        'user': '#48bb78'
    };
    
    const color = roleColors[currentUser.role] || '#667eea';
    
    const style = document.createElement('style');
    style.textContent = `
        .user-role::before {
            content: '●';
            color: ${color};
            margin-right: 4px;
        }
    `;
    
    document.head.appendChild(style);
}

function setupLogoutFunctionality() {
    // Setup logout button click handler
    document.addEventListener('click', (e) => {
        if (e.target.id === 'logoutBtn') {
            handleLogout();
        }
        
        if (e.target.id === 'profileBtn') {
            showUserProfile();
        }
    });
}

function handleLogout() {
    // Show confirmation dialog
    const confirmed = confirm('Are you sure you want to logout?');
    if (!confirmed) return;
    
    // Clear session data
    localStorage.removeItem('thestones_taskflow_session');
    sessionStorage.removeItem('thestones_taskflow_session');
    
    // Show logout message
    showNotification('Logged out successfully', 'info');
    
    // Redirect to login after short delay
    setTimeout(() => {
        window.location.href = '../../login.html';
    }, 1500);
}

function showUserProfile() {
    // Create and show user profile modal
    const modal = document.createElement('div');
    modal.className = 'profile-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h3>User Profile</h3>
                    <button class="close-modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="profile-info">
                        <div class="info-row">
                            <label>Name:</label>
                            <span>${currentUser.name}</span>
                        </div>
                        <div class="info-row">
                            <label>Email:</label>
                            <span>${currentUser.email}</span>
                        </div>
                        <div class="info-row">
                            <label>Role:</label>
                            <span>${formatRole(currentUser.role)}</span>
                        </div>
                        <div class="info-row">
                            <label>Login Method:</label>
                            <span>${currentUser.authMethod === 'sso' ? 'SSO (' + currentUser.provider + ')' : 'Email/Password'}</span>
                        </div>
                        <div class="info-row">
                            <label>Session Expires:</label>
                            <span>${new Date(sessionData.expiresAt).toLocaleString()}</span>
                        </div>
                        <div class="info-row">
                            <label>Permissions:</label>
                            <div class="permissions-list">
                                ${currentUser.permissions.map(perm => `<span class="permission-tag">${formatPermission(perm)}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    addProfileModalStyles();
    
    // Setup close functionality
    modal.querySelector('.close-modal').addEventListener('click', () => {
        modal.remove();
    });
    
    modal.querySelector('.modal-overlay').addEventListener('click', (e) => {
        if (e.target === modal.querySelector('.modal-overlay')) {
            modal.remove();
        }
    });
}

function addProfileModalStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .profile-modal .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
        }
        
        .profile-modal .modal-content {
            background: white;
            border-radius: 12px;
            width: 90%;
            max-width: 500px;
            max-height: 80vh;
            overflow-y: auto;
        }
        
        .profile-modal .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .profile-modal .modal-header h3 {
            margin: 0;
            color: #2d3748;
        }
        
        .profile-modal .close-modal {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #718096;
            padding: 4px;
            border-radius: 4px;
        }
        
        .profile-modal .close-modal:hover {
            background: #f0f2f5;
            color: #2d3748;
        }
        
        .profile-modal .modal-body {
            padding: 20px;
        }
        
        .profile-modal .info-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid #f7fafc;
        }
        
        .profile-modal .info-row:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }
        
        .profile-modal .info-row label {
            font-weight: 600;
            color: #4a5568;
            min-width: 120px;
        }
        
        .profile-modal .info-row span {
            color: #2d3748;
            text-align: right;
            flex: 1;
        }
        
        .profile-modal .permissions-list {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            justify-content: flex-end;
        }
        
        .profile-modal .permission-tag {
            background: #edf2f7;
            color: #4a5568;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
    `;
    
    document.head.appendChild(style);
}

function formatPermission(permission) {
    const permissionMap = {
        'view_all': 'View All Tasks',
        'assign_tasks': 'Assign Tasks',
        'manage_users': 'Manage Users',
        'view_analytics': 'View Analytics',
        'view_team': 'View Team Tasks',
        'view_assigned': 'View Assigned Tasks',
        'update_status': 'Update Task Status'
    };
    
    return permissionMap[permission] || permission;
}

function setupSessionMonitoring() {
    // Check session validity every 5 minutes
    setInterval(() => {
        if (!isSessionValid(sessionData)) {
            showNotification('Your session has expired. Please login again.', 'warning');
            setTimeout(() => {
                handleLogout();
            }, 3000);
        }
    }, 5 * 60 * 1000);
    
    // Warn user 5 minutes before session expires
    const expirationTime = new Date(sessionData.expiresAt).getTime();
    const warningTime = expirationTime - (5 * 60 * 1000);
    const currentTime = Date.now();
    
    if (warningTime > currentTime) {
        setTimeout(() => {
            showNotification('Your session will expire in 5 minutes. Please save your work.', 'warning');
        }, warningTime - currentTime);
    }
}

// Notification system (reuse from login.js)
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.auth-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `auth-notification notification-${type}`;
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
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 4000);
}

// Export authentication functions
window.TheStonesTaskFlowAuth = {
    getCurrentUser: () => currentUser,
    getSessionData: () => sessionData,
    hasPermission: (permission) => currentUser?.permissions?.includes(permission) || false,
    logout: handleLogout,
    showUserProfile,
    isAuthenticated: () => currentUser !== null
};
