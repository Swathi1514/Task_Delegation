// TaskFlow Integration Script
// Connects mock JIRA data with the UI components

class TaskFlowIntegration {
    constructor() {
        this.mockUsers = [];
        this.mockTasks = [];
        this.recommendations = new Map();
        this.init();
    }

    async init() {
        await this.loadMockData();
        this.setupEventListeners();
        this.renderTasks();
        this.renderCapacityHeatmap();
    }

    async loadMockData() {
        try {
            // Load mock users
            const usersResponse = await fetch('./mock_jira_users.json');
            const usersData = await usersResponse.json();
            this.mockUsers = usersData.users;

            // Load mock tasks
            const tasksResponse = await fetch('./mock_jira_tasks.json');
            const tasksData = await tasksResponse.json();
            this.mockTasks = tasksData.tasks;

            console.log('✅ Mock data loaded successfully');
            console.log(`Loaded ${this.mockUsers.length} users and ${this.mockTasks.length} tasks`);
        } catch (error) {
            console.error('❌ Error loading mock data:', error);
            // Fallback to hardcoded data if files not accessible
            this.loadFallbackData();
        }
    }

    loadFallbackData() {
        // Fallback data in case JSON files can't be loaded
        this.mockUsers = [
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

        this.mockTasks = [
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
        const task = this.mockTasks.find(t => t.key === taskId);
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
        button.textContent = 'Get Recommendation';
        button.disabled = false;
    }

    generateRecommendations(task) {
        const candidates = this.mockUsers.map(user => {
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
            
            chip.innerHTML = `
                <div class="chip-header">
                    <span class="member-name">${rec.user.displayName}</span>
                    <span class="score">${Math.round(rec.score * 100)}%</span>
                </div>
                <div class="chip-details">
                    <small>${rec.explanation.skillMatch}</small>
                    <small>${rec.explanation.currentLoad}</small>
                </div>
                <button class="assign-btn" data-task-id="${taskId}" data-member-id="${rec.user.id}">
                    Assign
                </button>
            `;

            recommendationsDiv.appendChild(chip);
        });
    }

    handleTaskAssignment(taskId, memberId) {
        const user = this.mockUsers.find(u => u.id === memberId);
        const task = this.mockTasks.find(t => t.key === taskId);

        if (user && task) {
            // Update task assignment
            task.assignee = user.username;
            task.status = "In Progress";

            // Update user load
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
        console.log('📋 Current Tasks:', this.mockTasks);
    }

    renderCapacityHeatmap() {
        const heatmapContainer = document.querySelector('.capacity-heatmap');
        if (!heatmapContainer) return;

        heatmapContainer.innerHTML = '<h3>Team Capacity Overview</h3>';

        this.mockUsers.forEach(user => {
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
    window.taskFlowIntegration = new TaskFlowIntegration();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TaskFlowIntegration;
}
