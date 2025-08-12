#!/usr/bin/env python3
"""
Test Fixtures for TaskFlow Backend Tests
Provides consistent test data across all test modules
"""

import json
from datetime import datetime, timedelta


class TestDataFixtures:
    """Centralized test data fixtures for TaskFlow testing"""
    
    @staticmethod
    def get_sample_users():
        """Get sample user data for testing"""
        return {
            "users": [
                {
                    "id": "user_001",
                    "username": "stacey.johnson",
                    "displayName": "Stacey",
                    "emailAddress": "stacey.johnson@company.com",
                    "accountType": "atlassian",
                    "active": True,
                    "timeZone": "America/New_York",
                    "groups": ["jira-software-users", "developers"],
                    "roles": ["Developer", "Frontend Specialist"],
                    "skills": [
                        {"name": "React", "level": 4},
                        {"name": "JavaScript", "level": 5},
                        {"name": "CSS", "level": 4},
                        {"name": "TypeScript", "level": 3},
                        {"name": "UI/UX Design", "level": 3}
                    ],
                    "capacity": {
                        "pointsPerSprint": 40,
                        "hoursPerWeek": 40,
                        "currentLoad": 24,
                        "utilizationPercent": 60
                    },
                    "preferences": {
                        "workTypes": ["Frontend Development", "UI Components", "User Experience"],
                        "projectTypes": ["Web Applications", "Mobile Apps"]
                    }
                },
                {
                    "id": "user_002",
                    "username": "maya.patel",
                    "displayName": "Maya",
                    "emailAddress": "maya.patel@company.com",
                    "accountType": "atlassian",
                    "active": True,
                    "timeZone": "America/Los_Angeles",
                    "groups": ["jira-software-users", "developers", "senior-developers"],
                    "roles": ["Senior Developer", "Backend Specialist"],
                    "skills": [
                        {"name": "Python", "level": 5},
                        {"name": "Django", "level": 4},
                        {"name": "PostgreSQL", "level": 4},
                        {"name": "AWS", "level": 4},
                        {"name": "Docker", "level": 3},
                        {"name": "API Design", "level": 5}
                    ],
                    "capacity": {
                        "pointsPerSprint": 45,
                        "hoursPerWeek": 40,
                        "currentLoad": 36,
                        "utilizationPercent": 80
                    },
                    "preferences": {
                        "workTypes": ["Backend Development", "API Development", "Database Design"],
                        "projectTypes": ["Microservices", "Data Processing", "Integration"]
                    }
                },
                {
                    "id": "user_003",
                    "username": "supraja.reddy",
                    "displayName": "Supraja",
                    "emailAddress": "supraja.reddy@company.com",
                    "accountType": "atlassian",
                    "active": True,
                    "timeZone": "Asia/Kolkata",
                    "groups": ["jira-software-users", "developers", "qa-team"],
                    "roles": ["Full Stack Developer", "QA Engineer"],
                    "skills": [
                        {"name": "Java", "level": 4},
                        {"name": "Spring Boot", "level": 4},
                        {"name": "React", "level": 3},
                        {"name": "Selenium", "level": 4},
                        {"name": "Jest", "level": 3},
                        {"name": "MySQL", "level": 3},
                        {"name": "Testing", "level": 5}
                    ],
                    "capacity": {
                        "pointsPerSprint": 42,
                        "hoursPerWeek": 40,
                        "currentLoad": 30,
                        "utilizationPercent": 71
                    },
                    "preferences": {
                        "workTypes": ["Full Stack Development", "Test Automation", "Quality Assurance"],
                        "projectTypes": ["Enterprise Applications", "Testing Frameworks"]
                    }
                }
            ],
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "description": "Test user data for TaskFlow testing",
                "totalUsers": 3
            }
        }
    
    @staticmethod
    def get_sample_tasks():
        """Get sample task data for testing"""
        future_date = datetime.now() + timedelta(days=10)
        
        return {
            "tasks": [
                {
                    "id": "TASK-101",
                    "key": "TASK-101",
                    "summary": "Implement user authentication UI",
                    "description": "Create login and registration forms with validation and error handling",
                    "issueType": "Story",
                    "priority": "High",
                    "status": "To Do",
                    "assignee": None,
                    "reporter": "maya.patel",
                    "project": "TASK",
                    "storyPoints": 8,
                    "dueDate": future_date.strftime("%Y-%m-%d"),
                    "labels": ["frontend", "authentication", "ui"],
                    "requiredSkills": [
                        {"name": "React", "minLevel": 3},
                        {"name": "JavaScript", "minLevel": 4},
                        {"name": "CSS", "minLevel": 3}
                    ],
                    "estimatedHours": 16
                },
                {
                    "id": "TASK-102",
                    "key": "TASK-102",
                    "summary": "Design and implement recommendation API",
                    "description": "Create REST API endpoints for task recommendation engine with scoring algorithm",
                    "issueType": "Story",
                    "priority": "Critical",
                    "status": "To Do",
                    "assignee": None,
                    "reporter": "maya.patel",
                    "project": "TASK",
                    "storyPoints": 13,
                    "dueDate": (future_date - timedelta(days=2)).strftime("%Y-%m-%d"),
                    "labels": ["backend", "api", "algorithm"],
                    "requiredSkills": [
                        {"name": "Python", "minLevel": 4},
                        {"name": "API Design", "minLevel": 4},
                        {"name": "Django", "minLevel": 3}
                    ],
                    "estimatedHours": 26
                },
                {
                    "id": "TASK-103",
                    "key": "TASK-103",
                    "summary": "Set up automated testing framework",
                    "description": "Implement unit tests, integration tests, and end-to-end testing for the application",
                    "issueType": "Task",
                    "priority": "Medium",
                    "status": "To Do",
                    "assignee": None,
                    "reporter": "supraja.reddy",
                    "project": "TASK",
                    "storyPoints": 5,
                    "dueDate": (future_date + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "labels": ["testing", "automation", "qa"],
                    "requiredSkills": [
                        {"name": "Testing", "minLevel": 4},
                        {"name": "Selenium", "minLevel": 3},
                        {"name": "Jest", "minLevel": 3}
                    ],
                    "estimatedHours": 10
                },
                {
                    "id": "TASK-104",
                    "key": "TASK-104",
                    "summary": "Database schema design and migration",
                    "description": "Design database schema for users, tasks, and recommendations with migration scripts",
                    "issueType": "Story",
                    "priority": "High",
                    "status": "To Do",
                    "assignee": None,
                    "reporter": "maya.patel",
                    "project": "TASK",
                    "storyPoints": 8,
                    "dueDate": (future_date + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "labels": ["database", "backend", "migration"],
                    "requiredSkills": [
                        {"name": "PostgreSQL", "minLevel": 3},
                        {"name": "Python", "minLevel": 3},
                        {"name": "Django", "minLevel": 3}
                    ],
                    "estimatedHours": 16
                },
                {
                    "id": "TASK-105",
                    "key": "TASK-105",
                    "summary": "Create capacity dashboard UI",
                    "description": "Build interactive dashboard showing team capacity, workload distribution, and availability",
                    "issueType": "Story",
                    "priority": "Medium",
                    "status": "To Do",
                    "assignee": None,
                    "reporter": "stacey.johnson",
                    "project": "TASK",
                    "storyPoints": 10,
                    "dueDate": (future_date + timedelta(days=8)).strftime("%Y-%m-%d"),
                    "labels": ["frontend", "dashboard", "visualization"],
                    "requiredSkills": [
                        {"name": "React", "minLevel": 4},
                        {"name": "JavaScript", "minLevel": 4},
                        {"name": "UI/UX Design", "minLevel": 3}
                    ],
                    "estimatedHours": 20
                }
            ],
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0",
                "description": "Test task data for TaskFlow testing",
                "totalTasks": 5,
                "totalStoryPoints": 44
            }
        }
    
    @staticmethod
    def get_edge_case_users():
        """Get edge case user data for testing boundary conditions"""
        return {
            "users": [
                {
                    "id": "user_overloaded",
                    "username": "overloaded.user",
                    "displayName": "Overloaded User",
                    "skills": [{"name": "Python", "level": 5}],
                    "capacity": {
                        "pointsPerSprint": 40,
                        "currentLoad": 38  # 95% capacity
                    }
                },
                {
                    "id": "user_novice",
                    "username": "novice.user",
                    "displayName": "Novice User",
                    "skills": [
                        {"name": "Python", "level": 1},
                        {"name": "JavaScript", "level": 2}
                    ],
                    "capacity": {
                        "pointsPerSprint": 30,
                        "currentLoad": 5  # Low capacity usage
                    }
                },
                {
                    "id": "user_specialist",
                    "username": "specialist.user",
                    "displayName": "Specialist User",
                    "skills": [
                        {"name": "MachineLearning", "level": 5},
                        {"name": "DataScience", "level": 5}
                    ],
                    "capacity": {
                        "pointsPerSprint": 35,
                        "currentLoad": 15
                    }
                }
            ]
        }
    
    @staticmethod
    def get_edge_case_tasks():
        """Get edge case task data for testing boundary conditions"""
        return {
            "tasks": [
                {
                    "key": "EDGE-001",
                    "summary": "High complexity task",
                    "priority": "Critical",
                    "storyPoints": 21,  # Very high story points
                    "requiredSkills": [
                        {"name": "Python", "minLevel": 5},
                        {"name": "MachineLearning", "minLevel": 4},
                        {"name": "DataScience", "minLevel": 4}
                    ]
                },
                {
                    "key": "EDGE-002",
                    "summary": "No skill requirements task",
                    "priority": "Low",
                    "storyPoints": 2,
                    "requiredSkills": []  # No required skills
                },
                {
                    "key": "EDGE-003",
                    "summary": "Impossible skill requirements",
                    "priority": "High",
                    "storyPoints": 8,
                    "requiredSkills": [
                        {"name": "NonExistentSkill", "minLevel": 5}
                    ]
                }
            ]
        }
    
    @staticmethod
    def get_performance_test_data(num_users=100, num_tasks=500):
        """Generate large dataset for performance testing"""
        users = []
        tasks = []
        
        skills_pool = [
            "Python", "JavaScript", "Java", "React", "Angular", "Vue",
            "Django", "Flask", "Spring", "Node.js", "PostgreSQL", "MySQL",
            "AWS", "Docker", "Kubernetes", "Testing", "Selenium", "Jest"
        ]
        
        # Generate users
        for i in range(num_users):
            user_skills = []
            # Each user gets 3-6 random skills
            import random
            selected_skills = random.sample(skills_pool, random.randint(3, 6))
            
            for skill in selected_skills:
                user_skills.append({
                    "name": skill,
                    "level": random.randint(2, 5)
                })
            
            users.append({
                "id": f"perf_user_{i:03d}",
                "username": f"user{i:03d}",
                "displayName": f"User {i:03d}",
                "skills": user_skills,
                "capacity": {
                    "pointsPerSprint": random.randint(30, 50),
                    "currentLoad": random.randint(0, 35)
                }
            })
        
        # Generate tasks
        for i in range(num_tasks):
            # Each task requires 1-3 random skills
            import random
            required_skills = []
            selected_skills = random.sample(skills_pool, random.randint(1, 3))
            
            for skill in selected_skills:
                required_skills.append({
                    "name": skill,
                    "minLevel": random.randint(2, 4)
                })
            
            tasks.append({
                "key": f"PERF-{i:03d}",
                "summary": f"Performance test task {i:03d}",
                "priority": random.choice(["Low", "Medium", "High", "Critical"]),
                "storyPoints": random.randint(1, 13),
                "requiredSkills": required_skills,
                "assignee": None,
                "status": "To Do"
            })
        
        return {
            "users": users,
            "tasks": tasks,
            "metadata": {
                "generated": datetime.now().isoformat(),
                "purpose": "Performance testing",
                "userCount": num_users,
                "taskCount": num_tasks
            }
        }
    
    @staticmethod
    def save_test_data_to_files(base_path="tests/fixtures"):
        """Save test data to JSON files for use in tests"""
        import os
        
        # Ensure directory exists
        os.makedirs(base_path, exist_ok=True)
        
        # Save sample data
        with open(f"{base_path}/sample_users.json", "w") as f:
            json.dump(TestDataFixtures.get_sample_users(), f, indent=2)
        
        with open(f"{base_path}/sample_tasks.json", "w") as f:
            json.dump(TestDataFixtures.get_sample_tasks(), f, indent=2)
        
        # Save edge case data
        with open(f"{base_path}/edge_case_users.json", "w") as f:
            json.dump(TestDataFixtures.get_edge_case_users(), f, indent=2)
        
        with open(f"{base_path}/edge_case_tasks.json", "w") as f:
            json.dump(TestDataFixtures.get_edge_case_tasks(), f, indent=2)
        
        # Save performance test data
        perf_data = TestDataFixtures.get_performance_test_data(50, 200)
        with open(f"{base_path}/performance_users.json", "w") as f:
            json.dump({"users": perf_data["users"]}, f, indent=2)
        
        with open(f"{base_path}/performance_tasks.json", "w") as f:
            json.dump({"tasks": perf_data["tasks"]}, f, indent=2)


if __name__ == "__main__":
    # Generate and save test data files
    TestDataFixtures.save_test_data_to_files()
    print("✅ Test fixture files generated successfully!")
    
    # Print summary
    sample_users = TestDataFixtures.get_sample_users()
    sample_tasks = TestDataFixtures.get_sample_tasks()
    
    print(f"📊 Generated test data:")
    print(f"   - Sample users: {len(sample_users['users'])}")
    print(f"   - Sample tasks: {len(sample_tasks['tasks'])}")
    print(f"   - Edge case users: {len(TestDataFixtures.get_edge_case_users()['users'])}")
    print(f"   - Edge case tasks: {len(TestDataFixtures.get_edge_case_tasks()['tasks'])}")
    print(f"   - Performance test data: 50 users, 200 tasks")
