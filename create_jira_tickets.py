#!/usr/bin/env python3
"""
Script to create Jira tickets from the TaskFlow backend tasks
Requires: pip install jira

Setup Instructions:
1. Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens
2. Update JIRA_EMAIL and JIRA_API_TOKEN below with your credentials
3. Run: python3 create_jira_tickets.py
"""

from jira import JIRA
import json

# Jira configuration
JIRA_SERVER = 'https://swathi1514.atlassian.net'
PROJECT_KEY = 'SCRUM'

# You'll need to set these - get API token from Jira settings
JIRA_EMAIL = 'your-email@example.com'  # Replace with your email
JIRA_API_TOKEN = 'your-api-token'      # Replace with your API token

def connect_to_jira():
    """Connect to Jira using email and API token"""
    try:
        jira = JIRA(
            server=JIRA_SERVER,
            basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
        )
        print(f"Connected to Jira: {JIRA_SERVER}")
        return jira
    except Exception as e:
        print(f"Failed to connect to Jira: {e}")
        return None

def create_epic(jira):
    """Create the main epic for TaskFlow"""
    epic_data = {
        'project': {'key': PROJECT_KEY},
        'summary': 'TaskFlow MVP Backend Development',
        'description': 'Epic for all TaskFlow backend development tasks including Jira integration, recommendation engine, and API development.',
        'issuetype': {'name': 'Epic'},
        'priority': {'name': 'High'},
        'customfield_10011': 'TaskFlow MVP Backend Development'  # Epic Name field (may vary)
    }
    
    try:
        epic = jira.create_issue(fields=epic_data)
        print(f"Created Epic: {epic.key}")
        return epic.key
    except Exception as e:
        print(f"Failed to create epic: {e}")
        return None

def create_tasks(jira, epic_key):
    """Create all backend tasks"""
    
    tasks = [
        {
            'summary': 'Set up Jira OAuth integration for reading task data',
            'description': '''Implement OAuth 2.0 integration with Jira API to read task details from the current sprint. This includes authentication, token management, and basic API connectivity.

Acceptance Criteria:
- OAuth flow implemented for Jira authentication
- Ability to read tasks from current sprint
- Error handling for authentication failures
- Unit tests for authentication module

Required Skills: Node.js/Python: 4, OAuth 2.0: 3, REST APIs: 4''',
            'issuetype': 'Story',
            'priority': 'High',
            'story_points': 8,
            'labels': ['backend', 'integration', 'jira', 'oauth']
        },
        {
            'summary': 'Create database schema and models for task management',
            'description': '''Design and implement database schema for storing task information, team member profiles, and recommendation logs as defined in the TaskFlow data model.

Acceptance Criteria:
- Database schema created for Task, Member, and RecommendationLog entities
- ORM models implemented
- Database migrations created
- Seed data for testing

Required Skills: Database Design: 4, SQL/NoSQL: 3, ORM (Sequelize/Mongoose): 3''',
            'issuetype': 'Story',
            'priority': 'High',
            'story_points': 5,
            'labels': ['backend', 'database', 'models']
        },
        {
            'summary': 'Implement CRUD operations for team member profiles',
            'description': '''Create REST API endpoints for managing team member profiles including skills, capacity, availability, and workload tracking.

Acceptance Criteria:
- GET /api/members - list all team members
- POST /api/members - create new member profile
- PUT /api/members/:id - update member profile
- DELETE /api/members/:id - remove member
- Input validation and error handling

Required Skills: REST API Development: 4, Node.js/Express: 4, Input Validation: 3''',
            'issuetype': 'Story',
            'priority': 'Medium',
            'story_points': 5,
            'labels': ['backend', 'api', 'profiles']
        },
        {
            'summary': 'Implement service to fetch current sprint tasks from Jira',
            'description': '''Create a service that fetches task details from Jira for the current sprint only, including title, description, story points, priority, due date, labels, and status.

Acceptance Criteria:
- Service fetches tasks from current sprint only
- Extracts all required task fields
- Handles Jira API rate limits
- Caches task data appropriately
- Error handling for API failures

Required Skills: Jira API: 4, Node.js/Python: 4, Caching (Redis): 3, Error Handling: 4''',
            'issuetype': 'Story',
            'priority': 'High',
            'story_points': 8,
            'labels': ['backend', 'jira', 'service', 'sprint']
        },
        {
            'summary': 'Implement core recommendation algorithm for task assignment',
            'description': '''Develop the core recommendation engine that scores team members for task assignment based on skill fit, load factor, deadline pressure, and availability.

Acceptance Criteria:
- Skill matching algorithm implemented
- Load factor calculation
- Deadline pressure scoring
- Top-3 candidate ranking
- Configurable scoring weights
- Unit tests for all scoring functions

Required Skills: Algorithm Development: 5, Mathematics/Statistics: 4, Node.js/Python: 4, Unit Testing: 4''',
            'issuetype': 'Story',
            'priority': 'High',
            'story_points': 13,
            'labels': ['backend', 'algorithm', 'recommendation', 'ml']
        }
        # Add more tasks as needed...
    ]
    
    created_issues = []
    
    for task in tasks:
        issue_data = {
            'project': {'key': PROJECT_KEY},
            'summary': task['summary'],
            'description': task['description'],
            'issuetype': {'name': task['issuetype']},
            'priority': {'name': task['priority']},
            'labels': task['labels']
        }
        
        # Add story points if available (field ID may vary)
        if 'story_points' in task:
            issue_data['customfield_10016'] = task['story_points']  # Story Points field
        
        # Link to epic
        if epic_key:
            issue_data['customfield_10014'] = epic_key  # Epic Link field (may vary)
        
        try:
            issue = jira.create_issue(fields=issue_data)
            created_issues.append(issue.key)
            print(f"Created {task['issuetype']}: {issue.key} - {task['summary']}")
        except Exception as e:
            print(f"Failed to create task '{task['summary']}': {e}")
    
    return created_issues

def main():
    """Main function to create all Jira tickets"""
    print("TaskFlow Jira Ticket Creator")
    print("=" * 40)
    
    # Check if credentials are set
    if JIRA_EMAIL == 'your-email@example.com' or JIRA_API_TOKEN == 'your-api-token':
        print("❌ Please update JIRA_EMAIL and JIRA_API_TOKEN in the script")
        print("\nTo get your API token:")
        print("1. Go to https://id.atlassian.com/manage-profile/security/api-tokens")
        print("2. Click 'Create API token'")
        print("3. Copy the token and update this script")
        return
    
    # Connect to Jira
    jira = connect_to_jira()
    if not jira:
        return
    
    # Create epic
    print("\n📋 Creating Epic...")
    epic_key = create_epic(jira)
    
    if epic_key:
        # Create tasks
        print(f"\n🎯 Creating tasks linked to Epic {epic_key}...")
        created_issues = create_tasks(jira, epic_key)
        
        print(f"\n✅ Successfully created {len(created_issues)} issues!")
        print(f"Epic: {epic_key}")
        print("Tasks:", ", ".join(created_issues))
        print(f"\nView in Jira: {JIRA_SERVER}/jira/software/projects/{PROJECT_KEY}/boards/1/backlog")
    else:
        print("❌ Failed to create epic. Cannot proceed with tasks.")

if __name__ == "__main__":
    main()
