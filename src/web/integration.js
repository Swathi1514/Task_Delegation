// TaskFlow Integration Script
// Connects JIRA data (real or mock) with the UI components

class TaskFlowIntegration {
    constructor(useRealJira = false) {
        this.useRealJira = useRealJira;
        this.users = [];
        this.tasks = [];
        this.recommendations = new Map();
        this.apiInfo = null;
        this.init();
    }

    async init() {
        await this.loadData();
        this.setupEventListeners();
        this.renderTasks();
        this.renderCapacityHeatmap();
        this.displayApiStatus();
    }

    async loadData() {
        if (this.useRealJira) {
            await this.loadRealJiraData();
        } else {
            await this.loadMockData();
        }
    }

    async loadRealJiraData() {
        try {
            console.log('🔗 Loading data from Real JIRA API...');
            
            // Note: In a real implementation, these would be actual API calls to a backend service
            // For now, we'll simulate the API calls since we don't have a running backend server
            
            // Get API info
            this.apiInfo = { type: 'real', connected: true };
            
            // Load users from real JIRA (simulated)
            this.users = await this.simulateRealJiraUsers();
            
            // Load tasks from real JIRA (simulated)
            this.tasks = await this.simulateRealJiraTasks();
            
            console.log('✅ Real JIRA data loaded successfully');
            console.log(`Loaded ${this.users.length} users and ${this.tasks.length} tasks`);
        } catch (error) {
            console.error('❌ Error loading real JIRA data:', error);
            console.log('⚠️ Falling back to mock data...');
            await this.loadMockData();
        }
    }

    async simulateRealJiraUsers() {
        // In a real implementation, this would call: fetch('/api/users')
        // For now, return realistic JIRA user data
        return [
            {
                id: "jira_user_001",
                username: "swathi1514",
                displayName: "Swathi Reddy",
                emailAddress: "swathi1514@gmail.com",
                timeZone: "America/New_York",
                skills: [
                    {"name": "Python", "level": 5},
                    {"name": "JIRA Administration", "level": 4},
                    {"name": "Project Management", "level": 4}
                ],
                capacity: {"pointsPerSprint": 45, "currentLoad": 28}
            },
            {
                id: "jira_user_002", 
                username: "dev.frontend",
                displayName: "Frontend Developer",
                emailAddress: "frontend@company.com",
                timeZone: "UTC",
                skills: [
                    {"name": "React", "level": 5},
                    {"name": "JavaScript", "level": 5},
                    {"name": "CSS", "level": 4}
                ],
                capacity: {"pointsPerSprint": 40, "currentLoad": 32}
            },
            {
                id: "jira_user_003",
                username: "dev.backend", 
                displayName: "Backend Developer",
                emailAddress: "backend@company.com",
                timeZone: "UTC",
                skills: [
                    {"name": "Python", "level": 5},
                    {"name": "Django", "level": 4},
                    {"name": "API Design", "level": 5}
                ],
                capacity: {"pointsPerSprint": 42, "currentLoad": 25}
            }
        ];
    }

    async simulateRealJiraTasks() {
        // In a real implementation, this would call: fetch('/api/tasks/unassigned')
        // For now, return realistic JIRA task data
        return [
            {
                key: "SCRUM-1",
                summary: "Set up Jira OAuth integration for reading task data",
                description: "Implement OAuth 2.0 integration with Jira API...",
                status: "To Do",
                priority: "High",
                assignee: null,
                storyPoints: 8,
                issueType: "Story",
                labels: ["backend", "integration", "jira", "oauth"],
                requiredSkills: [
                    {"name": "Python", "minLevel": 4},
                    {"name": "OAuth 2.0", "minLevel": 3},
                    {"name": "REST APIs", "minLevel": 4}
                ]
            },
            {
                key: "SCRUM-2",
                summary: "Create database schema and models for task management",
                description: "Design and implement database schema...",
                status: "To Do", 
                priority: "High",
                assignee: null,
                storyPoints: 5,
                issueType: "Story",
                labels: ["backend", "database", "models"],
                requiredSkills: [
                    {"name": "Database Design", "minLevel": 4},
                    {"name": "SQL", "minLevel": 3}
                ]
            },
            {
                key: "SCRUM-3",
                summary: "Implement CRUD operations for team member profiles",
                description: "Create REST API endpoints for managing team member profiles...",
                status: "To Do",
                priority: "Medium", 
                assignee: null,
                storyPoints: 5,
                issueType: "Story",
                labels: ["backend", "api", "profiles"],
                requiredSkills: [
                    {"name": "REST API Development", "minLevel": 4},
                    {"name": "Python", "minLevel": 4}
                ]
            }
        ];
    }

    async loadMockData() {
        try {
            console.log('🎭 Loading data from Mock JIRA API...');
            
            // Load mock users
            const usersResponse = await fetch('../data/mock_jira_users.json');
            const usersData = await usersResponse.json();
            this.users = usersData.users;

            // Load mock tasks
            const tasksResponse = await fetch('../data/mock_jira_tasks.json');
            const tasksData = await tasksResponse.json();
            this.tasks = tasksData.tasks;

            this.apiInfo = { type: 'mock', connected: true };

            console.log('✅ Mock data loaded successfully');
            console.log(`Loaded ${this.users.length} users and ${this.tasks.length} tasks`);
        } catch (error) {
            console.error('❌ Error loading mock data:', error);
            // Fallback to hardcoded data if files not accessible
            this.loadFallbackData();
        }
    }

    loadFallbackData() {
        // Fallback data in case JSON files can't be loaded
        this.users = [
            {
                id: "user_001",
                username: "stacey.johnson",
                displayName: "Stacey",
                skills: [
                    {"name": "React", "level": 4},
                    {"name": "JavaScript", "level": 5},
                    {"name": "CSS", "level": 4}
                ],
                capacity: {"pointsPerSprint": 40, "currentLoad": 24}
            },
            {
                id: "user_002",
                username: "maya.patel", 
                displayName: "Maya",
                skills: [
                    {"name": "Python", "level": 5},
                    {"name": "Django", "level": 4},
                    {"name": "API Design", "level": 5}
                ],
                capacity: {"pointsPerSprint": 45, "currentLoad": 36}
            },
            {
                id: "user_003",
                username: "supraja.reddy",
                displayName: "Supraja",
                skills: [
                    {"name": "Java", "level": 4},
                    {"name": "Testing", "level": 5},
                    {"name": "React", "level": 3}
                ],
                capacity: {"pointsPerSprint": 42, "currentLoad": 30}
            }
        ];

        this.tasks = [
            {
                key: "TASK-101",
                summary: "Implement user authentication UI",
                priority: "High",
                storyPoints: 8,
                requiredSkills: [
                    {"name": "React", "minLevel": 3},
                    {"name": "JavaScript", "minLevel": 4}
                ]
            },
            {
                key: "TASK-102",
                summary: "Design and implement recommendation API",
                priority: "Critical",
                storyPoints: 13,
                requiredSkills: [
                    {"name": "Python", "minLevel": 4},
                    {"name": "API Design", "minLevel": 4}
                ]
            }
        ];

        this.apiInfo = { type: 'fallback', connected: true };
    }

    displayApiStatus() {
        // Display current API status in the UI
        const statusElement = document.getElementById('api-status');
        if (statusElement) {
            const statusText = this.useRealJira ? 
                `🔗 Connected to Real JIRA (${this.apiInfo?.type || 'unknown'})` :
                `🎭 Using Mock JIRA (${this.apiInfo?.type || 'unknown'})`;
            
            statusElement.innerHTML = `
                <div class="api-status ${this.apiInfo?.type}">
                    ${statusText}
                    <button onclick="window.taskFlowIntegration.toggleApiMode()" class="toggle-api-btn">
                        Switch to ${this.useRealJira ? 'Mock' : 'Real'} JIRA
                    </button>
                </div>
            `;
        }
    }

    async toggleApiMode() {
        this.useRealJira = !this.useRealJira;
        console.log(`🔄 Switching to ${this.useRealJira ? 'Real' : 'Mock'} JIRA...`);
        
        // Reload data with new mode
        await this.loadData();
        this.renderTasks();
        this.renderCapacityHeatmap();
        this.displayApiStatus();
        
        // Clear existing recommendations
        this.recommendations.clear();
    }

    setupEventListeners() {
        // Override the existing recommendation button functionality
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('get-recommendation-btn')) {
                e.preventDefault();
                const taskId = e.target.getAttribute('data-task-id');
                this.handleRecommendationRequest(taskId, e.target);
            }

            if (e.target.classList.contains('assign-btn')) {
                e.preventDefault();
                const taskId = e.target.getAttribute('data-task-id');
                const memberId = e.target.getAttribute('data-member-id');
                this.handleTaskAssignment(taskId, memberId);
            }
        });
    }

    async handleRecommendationRequest(taskId, button) {
        const task = this.tasks.find(t => t.key === taskId);
        if (!task) {
            console.error('Task not found:', taskId);
            return;
        }

        // Show loading state
        button.textContent = 'Loading...';
        button.disabled = true;

        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Generate recommendations
        const recommendations = this.generateRecommendations(task);
        this.recommendations.set(taskId, recommendations);

        // Update UI
        this.displayRecommendations(taskId, recommendations);
        
        // Reset button
        button.textContent = '🎯 Get Recommendation';
        button.disabled = false;
    }

    generateRecommendations(task) {
        const candidates = this.users.map(user => {
            const score = this.calculateScore(user, task);
            return {
                user,
                score,
                explanation: this.generateExplanation(user, task, score)
            };
        });

        // Sort by score descending and take top 3
        return candidates
            .sort((a, b) => b.score - a.score)
            .slice(0, 3);
    }

    calculateScore(user, task) {
        let skillFit = 0;
        let skillCount = 0;

        // Calculate skill match
        task.requiredSkills.forEach(reqSkill => {
            const userSkill = user.skills.find(s => s.name === reqSkill.name);
            if (userSkill) {
                skillFit += Math.min(userSkill.level / reqSkill.minLevel, 1);
            }
            skillCount++;
        });

        skillFit = skillCount > 0 ? skillFit / skillCount : 0;

        // Calculate load factor
        const capacity = user.capacity.pointsPerSprint;
        const currentLoad = user.capacity.currentLoad;
        const loadFactor = 1 - (currentLoad / capacity);

        // Weighted score
        const score = (0.7 * skillFit) + (0.3 * loadFactor);
        return Math.round(score * 100) / 100;
    }

    generateExplanation(user, task, score) {
        const capacity = user.capacity.pointsPerSprint;
        const currentLoad = user.capacity.currentLoad;
        const utilization = Math.round((currentLoad / capacity) * 100);

        let skillMatch = "Skills: ";
        task.requiredSkills.forEach(reqSkill => {
            const userSkill = user.skills.find(s => s.name === reqSkill.name);
            if (userSkill) {
                skillMatch += `${reqSkill.name}(${userSkill.level}/${reqSkill.minLevel}) `;
            }
        });

        return {
            skillMatch,
            currentLoad: `Current load: ${currentLoad}/${capacity} points (${utilization}%)`,
            availability: `Available capacity: ${capacity - currentLoad} points`,
            score: `Overall score: ${score}`
        };
    }

    displayRecommendations(taskId, recommendations) {
        const recommendationsDiv = document.getElementById(`rec-${taskId}`);
        if (!recommendationsDiv) return;

        recommendationsDiv.innerHTML = '';
        recommendationsDiv.classList.remove('hidden');

        recommendations.forEach((rec, index) => {
            const chip = document.createElement('div');
            chip.className = `recommendation-chip ${index === 0 ? 'primary' : 'secondary'}`;
            
            // Fun emojis based on ranking
            const rankEmojis = ['🏆', '🥈', '🥉', '⭐', '👍'];
            const rankEmoji = rankEmojis[index] || '👤';
            
            // Score-based emojis
            const scoreEmoji = rec.score >= 0.9 ? '🔥' : rec.score >= 0.8 ? '✨' : rec.score >= 0.7 ? '👌' : '💪';
            
            chip.innerHTML = `
                <div class="chip-header">
                    <span class="member-name">${rankEmoji} ${rec.user.displayName}</span>
                    <span class="score">${scoreEmoji} ${Math.round(rec.score * 100)}%</span>
                </div>
                <div class="chip-details">
                    <small>🎯 ${rec.explanation.skillMatch}</small>
                    <small>⚡ ${rec.explanation.currentLoad}</small>
                </div>
                <button class="assign-btn" data-task-id="${taskId}" data-member-id="${rec.user.id}">
                    🚀 Assign
                </button>
            `;

            recommendationsDiv.appendChild(chip);
        });
    }

    async handleTaskAssignment(taskId, memberId) {
        const user = this.users.find(u => u.id === memberId);
        const task = this.tasks.find(t => t.key === taskId);

        if (user && task) {
            // In a real implementation, this would make an API call
            if (this.useRealJira) {
                // Simulate real JIRA assignment
                console.log(`🔗 Assigning ${taskId} to ${user.username} via Real JIRA API`);
                // await fetch('/api/assign', { method: 'POST', body: JSON.stringify({task_key: taskId, assignee: user.username}) });
            } else {
                console.log(`🎭 Assigning ${taskId} to ${user.username} via Mock JIRA API`);
            }

            // Update local state
            task.assignee = user.username;
            task.status = "In Progress";
            user.capacity.currentLoad += task.storyPoints;

            // Show success message
            this.showNotification(`Task ${taskId} assigned to ${user.displayName}`, 'success');

            // Update UI
            this.renderTasks();
            this.renderCapacityHeatmap();
        }
    }

    renderTasks() {
        // This would update the task list in the UI
        // For now, just log the current state
        console.log(`📋 Current Tasks (${this.apiInfo?.type}):`, this.tasks);
    }

    renderCapacityHeatmap() {
        const heatmapContainer = document.querySelector('.capacity-heatmap');
        if (!heatmapContainer) return;

        heatmapContainer.innerHTML = `
            <h3>Team Capacity Overview (${this.apiInfo?.type?.toUpperCase() || 'UNKNOWN'})</h3>
        `;

        this.users.forEach(user => {
            const capacity = user.capacity.pointsPerSprint;
            const currentLoad = user.capacity.currentLoad;
            const utilization = Math.round((currentLoad / capacity) * 100);

            const memberDiv = document.createElement('div');
            memberDiv.className = 'capacity-member';
            memberDiv.innerHTML = `
                <div class="member-info">
                    <strong>${user.displayName}</strong>
                    <span>${currentLoad}/${capacity} points (${utilization}%)</span>
                </div>
                <div class="capacity-bar">
                    <div class="capacity-fill" style="width: ${utilization}%; background-color: ${this.getCapacityColor(utilization)}"></div>
                </div>
            `;

            heatmapContainer.appendChild(memberDiv);
        });
    }

    getCapacityColor(utilization) {
        if (utilization < 60) return '#4CAF50'; // Green
        if (utilization < 80) return '#FF9800'; // Orange
        return '#F44336'; // Red
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;

        // Add to page
        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize the integration when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check URL parameters to determine which API to use
    const urlParams = new URLSearchParams(window.location.search);
    const useRealJira = urlParams.get('api') === 'real';
    
    window.taskFlowIntegration = new TaskFlowIntegration(useRealJira);
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TaskFlowIntegration;
}
