// TaskFlow Login Authentication System

document.addEventListener('DOMContentLoaded', function() {
    initializeLogin();
});

function initializeLogin() {
    setupFormValidation();
    setupPasswordToggle();
    setupDemoCredentials();
    setupSSOButtons();
    setupFormSubmission();
    checkExistingSession();
}

// Mock user database
const MOCK_USERS = {
    'admin@taskflow.com': {
        password: 'admin123',
        role: 'admin',
        name: 'Admin User',
        permissions: ['view_all', 'assign_tasks', 'manage_users', 'view_analytics']
    },
    'manager@taskflow.com': {
        password: 'manager123',
        role: 'manager',
        name: 'Project Manager',
        permissions: ['view_team', 'assign_tasks', 'view_analytics']
    },
    'user@taskflow.com': {
        password: 'user123',
        role: 'user',
        name: 'Team Member',
        permissions: ['view_assigned', 'update_status']
    }
};

// Form validation setup
function setupFormValidation() {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    emailInput.addEventListener('blur', validateEmail);
    emailInput.addEventListener('input', clearError);
    passwordInput.addEventListener('blur', validatePassword);
    passwordInput.addEventListener('input', clearError);
}

function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    const email = emailInput.value.trim();
    
    if (!email) {
        showFieldError(emailInput, emailError, 'Email is required');
        return false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showFieldError(emailInput, emailError, 'Please enter a valid email address');
        return false;
    }
    
    clearFieldError(emailInput, emailError);
    return true;
}

function validatePassword() {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('password-error');
    const password = passwordInput.value;
    
    if (!password) {
        showFieldError(passwordInput, passwordError, 'Password is required');
        return false;
    }
    
    if (password.length < 6) {
        showFieldError(passwordInput, passwordError, 'Password must be at least 6 characters');
        return false;
    }
    
    clearFieldError(passwordInput, passwordError);
    return true;
}

function showFieldError(input, errorElement, message) {
    input.classList.add('error');
    errorElement.textContent = message;
}

function clearFieldError(input, errorElement) {
    input.classList.remove('error');
    errorElement.textContent = '';
}

function clearError(event) {
    const input = event.target;
    const errorElement = document.getElementById(input.name + '-error');
    if (errorElement) {
        clearFieldError(input, errorElement);
    }
}

// Password toggle functionality
function setupPasswordToggle() {
    const passwordToggle = document.getElementById('passwordToggle');
    const passwordInput = document.getElementById('password');
    
    passwordToggle.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const eyeIcon = passwordToggle.querySelector('.eye-icon');
        eyeIcon.textContent = type === 'password' ? '👁️' : '🙈';
    });
}

// Demo credentials functionality
function setupDemoCredentials() {
    const demoUsers = document.querySelectorAll('.demo-user');
    
    demoUsers.forEach(user => {
        user.addEventListener('click', () => {
            const email = user.getAttribute('data-email');
            const password = user.getAttribute('data-password');
            
            document.getElementById('email').value = email;
            document.getElementById('password').value = password;
            
            // Clear any existing errors
            clearFieldError(document.getElementById('email'), document.getElementById('email-error'));
            clearFieldError(document.getElementById('password'), document.getElementById('password-error'));
            
            showNotification('Demo credentials filled in!', 'info');
        });
    });
}

// SSO button functionality
function setupSSOButtons() {
    const googleSSO = document.getElementById('googleSSO');
    const microsoftSSO = document.getElementById('microsoftSSO');
    const samlSSO = document.getElementById('samlSSO');
    
    googleSSO.addEventListener('click', () => handleSSOLogin('google'));
    microsoftSSO.addEventListener('click', () => handleSSOLogin('microsoft'));
    samlSSO.addEventListener('click', () => handleSSOLogin('saml'));
}

function handleSSOLogin(provider) {
    showLoadingOverlay();
    
    // Simulate SSO authentication delay
    setTimeout(() => {
        hideLoadingOverlay();
        
        // Mock successful SSO login
        const mockSSOUser = {
            email: `sso.user@${provider}.com`,
            name: `${provider.charAt(0).toUpperCase() + provider.slice(1)} User`,
            role: 'user',
            permissions: ['view_assigned', 'update_status'],
            authMethod: 'sso',
            provider: provider
        };
        
        authenticateUser(mockSSOUser);
    }, 2000);
}

// Form submission
function setupFormSubmission() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        handleLogin();
    });
}

function handleLogin() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    // Validate form
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();
    
    if (!isEmailValid || !isPasswordValid) {
        showNotification('Please fix the errors above', 'error');
        return;
    }
    
    // Show loading state
    setLoginButtonLoading(true);
    showLoadingOverlay();
    
    // Simulate authentication delay
    setTimeout(() => {
        authenticateCredentials(email, password, rememberMe);
    }, 1500);
}

function authenticateCredentials(email, password, rememberMe) {
    const user = MOCK_USERS[email];
    
    if (!user || user.password !== password) {
        setLoginButtonLoading(false);
        hideLoadingOverlay();
        showNotification('Invalid email or password', 'error');
        return;
    }
    
    // Successful authentication
    const authenticatedUser = {
        email: email,
        name: user.name,
        role: user.role,
        permissions: user.permissions,
        authMethod: 'credentials',
        loginTime: new Date().toISOString()
    };
    
    authenticateUser(authenticatedUser, rememberMe);
}

function authenticateUser(user, rememberMe = false) {
    // Store user session
    const sessionData = {
        user: user,
        sessionId: generateSessionId(),
        expiresAt: new Date(Date.now() + (rememberMe ? 30 * 24 * 60 * 60 * 1000 : 24 * 60 * 60 * 1000)).toISOString()
    };
    
    // Store in localStorage or sessionStorage based on remember me
    const storage = rememberMe ? localStorage : sessionStorage;
    storage.setItem('taskflow_session', JSON.stringify(sessionData));
    
    setLoginButtonLoading(false);
    hideLoadingOverlay();
    
    showNotification(`Welcome back, ${user.name}!`, 'success');
    
    // Redirect to main application after short delay
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 1500);
}

function generateSessionId() {
    return 'sess_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
}

// Check for existing session
function checkExistingSession() {
    const sessionData = getStoredSession();
    
    if (sessionData && isSessionValid(sessionData)) {
        showNotification('You are already logged in. Redirecting...', 'info');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    }
}

function getStoredSession() {
    // Check both localStorage and sessionStorage
    let sessionData = localStorage.getItem('taskflow_session');
    if (!sessionData) {
        sessionData = sessionStorage.getItem('taskflow_session');
    }
    
    if (sessionData) {
        try {
            return JSON.parse(sessionData);
        } catch (e) {
            // Invalid session data, remove it
            localStorage.removeItem('taskflow_session');
            sessionStorage.removeItem('taskflow_session');
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

// UI Helper Functions
function setLoginButtonLoading(loading) {
    const loginBtn = document.getElementById('loginBtn');
    const btnText = loginBtn.querySelector('.btn-text');
    const btnLoader = loginBtn.querySelector('.btn-loader');
    
    if (loading) {
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
        loginBtn.disabled = true;
    } else {
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
        loginBtn.disabled = false;
    }
}

function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('hidden');
}

function hideLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('hidden');
}

// Notification system
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    
    // Remove existing notifications
    const existingNotifications = container.querySelectorAll('.notification');
    existingNotifications.forEach(notification => {
        notification.remove();
    });
    
    // Create new notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    container.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 4000);
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Enter key to submit form
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.altKey) {
        const activeElement = document.activeElement;
        if (activeElement.tagName === 'INPUT' || activeElement.tagName === 'BUTTON') {
            const form = activeElement.closest('form');
            if (form && form.id === 'loginForm') {
                e.preventDefault();
                handleLogin();
            }
        }
    }
});

// Export functions for potential external use
window.TaskFlowAuth = {
    authenticateUser,
    getStoredSession,
    isSessionValid,
    showNotification,
    logout: function() {
        localStorage.removeItem('taskflow_session');
        sessionStorage.removeItem('taskflow_session');
        window.location.href = 'login.html';
    }
};
