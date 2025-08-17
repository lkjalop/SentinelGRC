/**
 * Sentinel GRC Gateway JavaScript
 * Implements the two-door interface pattern with adaptive behavior
 */

// Configuration
const CONFIG = {
    API_BASE_URL: '/api',
    STORAGE_KEY: 'sentinel-preferences',
    UPDATE_INTERVAL: 30000, // 30 seconds
};

// State Management
let state = {
    user: null,
    preferences: {},
    stats: {},
    lastActivity: null,
};

/**
 * Initialize the gateway on page load
 */
function initializeGateway() {
    loadUserPreferences();
    generateGreeting();
    setupThemeToggle();
    setupKeyboardNavigation();
    updateDoorStatuses();
    
    // Auto-update stats
    setInterval(loadPlatformStats, CONFIG.UPDATE_INTERVAL);
    
    console.log('Sentinel Gateway initialized');
}

/**
 * Load user preferences from localStorage
 */
function loadUserPreferences() {
    try {
        const stored = localStorage.getItem(CONFIG.STORAGE_KEY);
        if (stored) {
            state.preferences = JSON.parse(stored);
            
            // Apply theme preference
            if (state.preferences.theme) {
                document.documentElement.setAttribute('data-theme', state.preferences.theme);
            }
            
            // Store user context
            state.user = state.preferences.user || { name: 'User' };
            state.lastActivity = state.preferences.lastActivity;
        }
    } catch (error) {
        console.warn('Failed to load user preferences:', error);
    }
}

/**
 * Save user preferences to localStorage
 */
function saveUserPreferences() {
    try {
        state.preferences.user = state.user;
        state.preferences.lastActivity = state.lastActivity;
        state.preferences.theme = document.documentElement.getAttribute('data-theme') || 'light';
        
        localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(state.preferences));
    } catch (error) {
        console.warn('Failed to save user preferences:', error);
    }
}

/**
 * Generate adaptive greeting based on time and user history
 */
function generateGreeting() {
    const hour = new Date().getHours();
    const userName = state.user?.name || 'User';
    
    let greeting = '';
    if (hour < 12) {
        greeting = 'Good morning';
    } else if (hour < 17) {
        greeting = 'Good afternoon';
    } else {
        greeting = 'Good evening';
    }
    
    greeting += `, ${userName}`;
    
    // Add contextual information based on last activity
    if (state.lastActivity) {
        const daysSince = Math.floor((Date.now() - new Date(state.lastActivity.date).getTime()) / (1000 * 60 * 60 * 24));
        
        if (state.lastActivity.type === 'audit' && daysSince < 7) {
            greeting += '. Your audit preparation is ready for review.';
        } else if (state.lastActivity.type === 'devops' && daysSince < 1) {
            greeting += '. Your pipeline status has been updated.';
        } else {
            greeting += '. Welcome back to Sentinel.';
        }
    } else {
        greeting += '. Welcome to Sentinel.';
    }
    
    const greetingElement = document.getElementById('adaptive-greeting');
    if (greetingElement) {
        greetingElement.textContent = greeting;
    }
}

/**
 * Setup theme toggle functionality
 */
function setupThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;
    
    // Update icons based on current theme
    updateThemeIcons();
    
    themeToggle.addEventListener('click', toggleTheme);
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    updateThemeIcons();
    saveUserPreferences();
}

/**
 * Update theme toggle icons
 */
function updateThemeIcons() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const sunIcon = document.querySelector('.icon-sun');
    const moonIcon = document.querySelector('.icon-moon');
    
    if (sunIcon && moonIcon) {
        if (currentTheme === 'dark') {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        } else {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }
}

/**
 * Setup keyboard navigation for accessibility
 */
function setupKeyboardNavigation() {
    document.addEventListener('keydown', (event) => {
        // Enter key on door cards
        if (event.key === 'Enter' || event.key === ' ') {
            const target = event.target.closest('.door-card');
            if (target) {
                event.preventDefault();
                const doorType = target.getAttribute('data-door');
                enterDoor(doorType);
            }
        }
        
        // Quick navigation shortcuts
        if (event.ctrlKey || event.metaKey) {
            switch (event.key) {
                case 'd':
                    event.preventDefault();
                    enterDoor('devops');
                    break;
                case 'c':
                    event.preventDefault();
                    enterDoor('compliance');
                    break;
                case 'k':
                    event.preventDefault();
                    document.querySelector('.theme-toggle')?.focus();
                    break;
            }
        }
    });
}

/**
 * Update door status indicators
 */
function updateDoorStatuses() {
    // DevOps status
    const devopsStatus = document.getElementById('devops-status');
    if (devopsStatus) {
        // This would typically come from the backend
        // For now, we'll simulate with some dynamic content
        const statuses = [
            { icon: '⚡', text: 'Pipeline Running' },
            { icon: '🔒', text: `${Math.floor(Math.random() * 10) + 1} Security Checks` },
            { icon: '📈', text: `${Math.floor(Math.random() * 50) + 10} Deployments Today` },
        ];
        
        devopsStatus.innerHTML = statuses.map(status => 
            `<div class="status-item">
                <span class="status-icon">${status.icon}</span>
                <span class="status-text">${status.text}</span>
            </div>`
        ).join('');
    }
    
    // Compliance status
    const complianceStatus = document.getElementById('compliance-status');
    if (complianceStatus) {
        const auditDays = Math.floor(Math.random() * 30) + 1;
        const complianceScore = Math.floor(Math.random() * 20) + 80;
        
        const statuses = [
            { icon: '📊', text: `${complianceScore}% Ready` },
            { icon: '🗓️', text: `Audit in ${auditDays} days` },
            { icon: '📋', text: `${Math.floor(Math.random() * 5) + 1} Tasks Pending` },
        ];
        
        complianceStatus.innerHTML = statuses.map(status => 
            `<div class="status-item">
                <span class="status-icon">${status.icon}</span>
                <span class="status-text">${status.text}</span>
            </div>`
        ).join('');
    }
}

/**
 * Load platform statistics from backend
 */
async function loadPlatformStats() {
    try {
        // Simulate API call - replace with actual backend integration
        const mockStats = {
            complianceScore: Math.floor(Math.random() * 20) + 80,
            deploymentsToday: Math.floor(Math.random() * 100) + 10,
            controlsPassing: {
                passing: Math.floor(Math.random() * 100) + 1200,
                total: Math.floor(Math.random() * 200) + 1300
            },
            nextAudit: Math.floor(Math.random() * 30) + 1
        };
        
        // For real implementation, use:
        // const response = await fetch(`${CONFIG.API_BASE_URL}/stats`);
        // const stats = await response.json();
        
        updateStatsDisplay(mockStats);
        state.stats = mockStats;
        
    } catch (error) {
        console.error('Failed to load platform stats:', error);
        
        // Fallback to cached stats if available
        if (state.stats && Object.keys(state.stats).length > 0) {
            updateStatsDisplay(state.stats);
        }
    }
}

/**
 * Update statistics display in the UI
 */
function updateStatsDisplay(stats) {
    // Compliance Score
    const complianceScoreEl = document.getElementById('compliance-score');
    if (complianceScoreEl) {
        complianceScoreEl.textContent = `${stats.complianceScore}%`;
    }
    
    // Deployments Today
    const deploymentsTodayEl = document.getElementById('deployments-today');
    if (deploymentsTodayEl) {
        deploymentsTodayEl.textContent = stats.deploymentsToday.toString();
    }
    
    // Controls Passing
    const controlsPassingEl = document.getElementById('controls-passing');
    if (controlsPassingEl) {
        controlsPassingEl.textContent = `${stats.controlsPassing.passing}/${stats.controlsPassing.total}`;
    }
    
    // Next Audit
    const nextAuditEl = document.getElementById('next-audit');
    if (nextAuditEl) {
        const days = stats.nextAudit;
        nextAuditEl.textContent = days === 1 ? '1 day' : `${days} days`;
    }
}

/**
 * Enter a specific mode (DevOps or Compliance)
 */
function enterDoor(doorType) {
    // Record the activity
    state.lastActivity = {
        type: doorType,
        date: new Date().toISOString()
    };
    saveUserPreferences();
    
    // Show loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        
        const loadingText = loadingOverlay.querySelector('.loading-text');
        if (loadingText) {
            loadingText.textContent = `Loading ${doorType === 'devops' ? 'DevOps' : 'Compliance'} Mode...`;
        }
    }
    
    // Simulate loading time and redirect
    setTimeout(() => {
        if (doorType === 'devops') {
            // Redirect to DevOps interface
            window.location.href = '/devops-dashboard.html';
        } else if (doorType === 'compliance') {
            // Redirect to Compliance interface
            window.location.href = '/compliance-dashboard.html';
        }
    }, 1500);
    
    console.log(`Entering ${doorType} mode`);
}

/**
 * Utility function to get user information
 */
function getUserName() {
    return state.user?.name || 'User';
}

/**
 * Utility function to get last activity
 */
function getLastActivity() {
    return state.lastActivity;
}

/**
 * Calculate days since a given date
 */
function daysSince(date) {
    const now = new Date();
    const then = new Date(date);
    const diffTime = Math.abs(now - then);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Handle window resize for responsive behavior
 */
window.addEventListener('resize', () => {
    // Update any responsive behavior if needed
    updateDoorStatuses();
});

/**
 * Handle visibility change to update stats when tab becomes visible
 */
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        loadPlatformStats();
        generateGreeting();
    }
});

// Export functions for global access
window.sentinelGateway = {
    enterDoor,
    toggleTheme,
    loadPlatformStats,
    updateDoorStatuses,
    initializeGateway,
};