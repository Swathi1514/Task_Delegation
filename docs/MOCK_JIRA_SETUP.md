# Mock JIRA Setup for TaskFlow Testing

Since you don't have access to a JIRA instance, this setup provides a complete mock JIRA environment with 3 users (Stacey, Maya, Supraja) for testing the TaskFlow system.

## Files Created

### 1. `mock_jira_users.json`
Contains detailed user profiles with:
- **Stacey Johnson** - Frontend Specialist (React, JavaScript, UI/UX)
- **Maya Patel** - Senior Backend Developer (Python, Django, AWS)
- **Supraja Reddy** - Full Stack Developer & QA Engineer (Java, Testing, React)

Each user includes:
- Skills with proficiency levels (1-5)
- Capacity and current workload
- Time zones and preferences
- JIRA groups and roles

### 2. `mock_jira_tasks.json`
Contains 5 sample tasks for the TaskFlow project:
- **TASK-101**: User authentication UI (Frontend - suits Stacey)
- **TASK-102**: Recommendation API (Backend - suits Maya)
- **TASK-103**: Testing framework (QA - suits Supraja)
- **TASK-104**: Database schema (Backend - suits Maya)
- **TASK-105**: Capacity dashboard (Frontend - suits Stacey)

### 3. `mock_jira_api.py`
Python simulator that provides:
- User management functions
- Task assignment capabilities
- Workload calculation
- Team capacity overview
- JIRA API-like interface

## User Profiles Summary

| User | Role | Key Skills | Capacity | Current Load | Timezone |
|------|------|------------|----------|--------------|----------|
| **Stacey** | Frontend Specialist | React(4), JavaScript(5), CSS(4) | 40 pts | 24 pts (60%) | EST |
| **Maya** | Senior Backend Dev | Python(5), Django(4), AWS(4) | 45 pts | 36 pts (80%) | PST |
| **Supraja** | Full Stack & QA | Java(4), Testing(5), React(3) | 42 pts | 30 pts (71%) | IST |

## How to Use

### 1. Run the Mock JIRA API Demo
```bash
cd Task_Delegation
python3 mock_jira_api.py
```

This will:
- Load the mock data
- Display all users and their skills
- Show unassigned tasks
- Simulate task assignments
- Display team capacity overview

### 2. Test TaskFlow Recommendations

You can use this data to test your TaskFlow recommendation algorithm:

```python
# Example: Get best assignee for a task
task = {
    "requiredSkills": [{"name": "React", "minLevel": 3}],
    "storyPoints": 8,
    "priority": "High"
}

# Expected recommendation: Stacey (React:4, 60% utilization)
```

### 3. Integration Testing

Use the mock data for:
- **Algorithm Testing**: Test recommendation scoring with known user profiles
- **UI Testing**: Display mock tasks and assignments in your interface
- **API Testing**: Simulate JIRA API calls without actual JIRA access
- **Load Testing**: Scale up the mock data for performance testing

## Sample API Responses

### Get Users
```json
{
  "users": [
    {
      "displayName": "Stacey",
      "username": "stacey.johnson",
      "skills": [{"name": "React", "level": 4}],
      "capacity": {"pointsPerSprint": 40, "currentLoad": 24}
    }
  ]
}
```

### Get Tasks
```json
{
  "tasks": [
    {
      "key": "TASK-101",
      "summary": "Implement user authentication UI",
      "requiredSkills": [{"name": "React", "minLevel": 3}],
      "storyPoints": 8,
      "priority": "High"
    }
  ]
}
```

## Extending the Mock Data

### Add More Users
Edit `mock_jira_users.json` to add additional team members:
```json
{
  "id": "user_004",
  "username": "new.developer",
  "displayName": "New Developer",
  "skills": [{"name": "Python", "level": 3}],
  "capacity": {"pointsPerSprint": 35}
}
```

### Add More Tasks
Edit `mock_jira_tasks.json` to add more test scenarios:
```json
{
  "key": "TASK-106",
  "summary": "New feature implementation",
  "requiredSkills": [{"name": "Java", "minLevel": 4}],
  "storyPoints": 13,
  "priority": "Medium"
}
```

### Customize Skills
Modify the skills database to match your team's technology stack:
- Add new programming languages
- Include domain-specific skills
- Adjust proficiency levels
- Add soft skills (leadership, communication)

## TaskFlow Integration Points

This mock setup supports all TaskFlow features:

1. **Skill Matching**: Users have detailed skill profiles with levels
2. **Capacity Planning**: Each user has defined capacity and current load
3. **Priority Handling**: Tasks have priority levels for urgent assignments
4. **Time Zone Awareness**: Users span multiple time zones (EST, PST, IST)
5. **Historical Data**: Framework for tracking assignment success rates
6. **Feedback Loop**: Structure for capturing assignment feedback

## Next Steps

1. **Run the demo** to see the mock JIRA in action
2. **Integrate with TaskFlow** recommendation engine
3. **Test different scenarios** by modifying user loads and task requirements
4. **Scale up** by adding more users and tasks as needed
5. **Transition to real JIRA** when you get access to an actual instance

This mock setup provides everything you need to develop and test TaskFlow without requiring actual JIRA access!
