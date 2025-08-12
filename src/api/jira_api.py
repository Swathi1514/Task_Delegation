#!/usr/bin/env python3
"""
Real JIRA API Service for TaskFlow
Provides actual JIRA integration for production use
"""

import json
import datetime
import os
from typing import Dict, List, Optional
from jira import JIRA

class JiraAPIService:
    def __init__(self, config_file=None):
        """Initialize JIRA API service with configuration"""
        self.config = self.load_config(config_file)
        self.jira_client = None
        self.connect()
    
    def load_config(self, config_file=None):
        """Load JIRA configuration from file or environment variables"""
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        
        # Default configuration - can be overridden by environment variables
        return {
            "server": os.getenv('JIRA_SERVER', 'https://swathi1514.atlassian.net'),
            "email": os.getenv('JIRA_EMAIL', 'swathi1514@gmail.com'),
            "api_token": os.getenv('JIRA_API_TOKEN', 'ATATT3xFfGF0kf81vZuO6E7oB3wit6Dx0t2042lPdGi1-injn_dOw-AE_txDe7_uKSP6RaOK02-6feF-s1a2_542EIAB8oSoRLDRPVy6B8y4AN5Jlh2qAnOVL9E3VkVYYCMFh9poxrnHHGySGePc9NgBHkMx3tgrwEIoP0AxXnvo7FldWwz7QrA=60675AEB'),
            "project_key": os.getenv('JIRA_PROJECT_KEY', 'SCRUM')
        }
    
    def connect(self):
        """Connect to JIRA using credentials"""
        try:
            self.jira_client = JIRA(
                server=self.config['server'],
                basic_auth=(self.config['email'], self.config['api_token'])
            )
            print(f"✅ Connected to JIRA: {self.config['server']}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to JIRA: {e}")
            return False
    
    def is_connected(self):
        """Check if JIRA connection is active"""
        return self.jira_client is not None
    
    def get_users(self) -> List[Dict]:
        """Get all users from JIRA project"""
        if not self.is_connected():
            return []
        
        try:
            # Get project users
            project = self.jira_client.project(self.config['project_key'])
            users = []
            
            # Get assignable users for the project
            assignable_users = self.jira_client.search_assignable_users_for_projects('', [project.key])
            
            for user in assignable_users:
                user_data = {
                    "id": user.key,
                    "username": user.name,
                    "displayName": user.displayName,
                    "emailAddress": getattr(user, 'emailAddress', ''),
                    "timeZone": getattr(user, 'timeZone', 'UTC'),
                    "active": user.active,
                    # Default skills - in real implementation, this would come from custom fields or external system
                    "skills": self.get_user_skills(user.name),
                    "capacity": self.get_user_capacity(user.name)
                }
                users.append(user_data)
            
            return users
        except Exception as e:
            print(f"❌ Error fetching users: {e}")
            return []
    
    def get_user_skills(self, username: str) -> List[Dict]:
        """Get user skills - placeholder for custom implementation"""
        # In a real implementation, this would fetch from:
        # - JIRA custom fields
        # - External HR system
        # - Skills database
        # For now, return default skills based on username patterns
        default_skills = [
            {"name": "Python", "level": 3},
            {"name": "JavaScript", "level": 3},
            {"name": "Testing", "level": 3}
        ]
        return default_skills
    
    def get_user_capacity(self, username: str) -> Dict:
        """Get user capacity information"""
        # In real implementation, this would come from:
        # - JIRA Tempo or similar capacity planning tools
        # - Custom fields
        # - External systems
        return {
            "pointsPerSprint": 40,
            "currentLoad": 0,  # Will be calculated from assigned tasks
            "availability": 1.0  # 100% available
        }
    
    def get_tasks(self, project_key: str = None, assignee: str = None, status: str = None) -> List[Dict]:
        """Get tasks from JIRA with optional filtering"""
        if not self.is_connected():
            return []
        
        try:
            # Build JQL query
            jql_parts = []
            
            if project_key:
                jql_parts.append(f'project = "{project_key}"')
            else:
                jql_parts.append(f'project = "{self.config["project_key"]}"')
            
            if assignee:
                if assignee.lower() == 'unassigned':
                    jql_parts.append('assignee is EMPTY')
                else:
                    jql_parts.append(f'assignee = "{assignee}"')
            
            if status:
                jql_parts.append(f'status = "{status}"')
            
            jql = ' AND '.join(jql_parts)
            
            # Execute search
            issues = self.jira_client.search_issues(jql, maxResults=100)
            
            tasks = []
            for issue in issues:
                task_data = {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": getattr(issue.fields, 'description', ''),
                    "status": issue.fields.status.name,
                    "priority": issue.fields.priority.name if issue.fields.priority else 'Medium',
                    "assignee": issue.fields.assignee.name if issue.fields.assignee else None,
                    "assigneeDisplayName": issue.fields.assignee.displayName if issue.fields.assignee else None,
                    "reporter": issue.fields.reporter.name if issue.fields.reporter else None,
                    "created": issue.fields.created,
                    "updated": issue.fields.updated,
                    "dueDate": getattr(issue.fields, 'duedate', None),
                    "storyPoints": self.get_story_points(issue),
                    "labels": issue.fields.labels,
                    "project": issue.fields.project.key,
                    "issueType": issue.fields.issuetype.name,
                    "requiredSkills": self.extract_required_skills(issue)
                }
                tasks.append(task_data)
            
            return tasks
        except Exception as e:
            print(f"❌ Error fetching tasks: {e}")
            return []
    
    def get_story_points(self, issue):
        """Extract story points from issue (field ID may vary)"""
        try:
            # Common story points field IDs
            story_point_fields = ['customfield_10016', 'customfield_10002', 'customfield_10004']
            
            for field_id in story_point_fields:
                if hasattr(issue.fields, field_id):
                    value = getattr(issue.fields, field_id)
                    if value is not None:
                        return float(value)
            
            return 0
        except:
            return 0
    
    def extract_required_skills(self, issue) -> List[Dict]:
        """Extract required skills from issue description or custom fields"""
        # In real implementation, this would parse:
        # - Custom fields for skills
        # - Description text for skill requirements
        # - Labels for technology tags
        
        # For now, extract from labels and description
        skills = []
        
        # Extract from labels
        for label in issue.fields.labels:
            if any(tech in label.lower() for tech in ['python', 'javascript', 'react', 'java', 'api']):
                skills.append({
                    "name": label.title(),
                    "minLevel": 3  # Default minimum level
                })
        
        # If no skills found, add default based on issue type
        if not skills:
            if 'ui' in issue.fields.summary.lower() or 'frontend' in issue.fields.summary.lower():
                skills.append({"name": "JavaScript", "minLevel": 3})
                skills.append({"name": "React", "minLevel": 3})
            elif 'api' in issue.fields.summary.lower() or 'backend' in issue.fields.summary.lower():
                skills.append({"name": "Python", "minLevel": 3})
                skills.append({"name": "API Design", "minLevel": 3})
            elif 'test' in issue.fields.summary.lower():
                skills.append({"name": "Testing", "minLevel": 3})
        
        return skills
    
    def get_unassigned_tasks(self) -> List[Dict]:
        """Get all unassigned tasks"""
        return self.get_tasks(assignee='unassigned')
    
    def assign_task(self, task_key: str, assignee_username: str) -> Dict:
        """Assign a task to a user"""
        if not self.is_connected():
            return {"success": False, "message": "Not connected to JIRA"}
        
        try:
            issue = self.jira_client.issue(task_key)
            
            # Find user by username
            users = self.jira_client.search_users(assignee_username)
            if not users:
                return {"success": False, "message": f"User {assignee_username} not found"}
            
            user = users[0]
            
            # Assign the task
            issue.update(assignee={'name': user.name})
            
            return {
                "success": True,
                "message": f"Task {task_key} assigned to {user.displayName}",
                "task": {
                    "key": task_key,
                    "assignee": user.name,
                    "assigneeDisplayName": user.displayName
                }
            }
        except Exception as e:
            return {"success": False, "message": f"Error assigning task: {str(e)}"}
    
    def get_user_workload(self, username: str) -> Dict:
        """Calculate current workload for a user"""
        try:
            assigned_tasks = self.get_tasks(assignee=username)
            total_story_points = sum(task.get("storyPoints", 0) for task in assigned_tasks)
            
            # Get user capacity (would come from external system in real implementation)
            capacity_info = self.get_user_capacity(username)
            max_capacity = capacity_info.get("pointsPerSprint", 40)
            utilization = (total_story_points / max_capacity) * 100 if max_capacity > 0 else 0
            
            return {
                "username": username,
                "assignedTasks": len(assigned_tasks),
                "totalStoryPoints": total_story_points,
                "maxCapacity": max_capacity,
                "utilizationPercent": round(utilization, 1),
                "availableCapacity": max_capacity - total_story_points
            }
        except Exception as e:
            print(f"❌ Error calculating workload for {username}: {e}")
            return {"error": str(e)}
    
    def get_team_capacity_overview(self) -> Dict:
        """Get capacity overview for entire team"""
        try:
            users = self.get_users()
            team_overview = {
                "members": [],
                "teamTotals": {
                    "totalCapacity": 0,
                    "totalAssigned": 0,
                    "averageUtilization": 0
                }
            }
            
            total_utilization = 0
            
            for user in users:
                workload = self.get_user_workload(user["username"])
                if "error" not in workload:
                    member_info = {
                        "username": user["username"],
                        "displayName": user["displayName"],
                        "timeZone": user["timeZone"],
                        "workload": workload
                    }
                    team_overview["members"].append(member_info)
                    
                    team_overview["teamTotals"]["totalCapacity"] += workload.get("maxCapacity", 0)
                    team_overview["teamTotals"]["totalAssigned"] += workload.get("totalStoryPoints", 0)
                    total_utilization += workload.get("utilizationPercent", 0)
            
            if len(team_overview["members"]) > 0:
                team_overview["teamTotals"]["averageUtilization"] = round(
                    total_utilization / len(team_overview["members"]), 1
                )
            
            return team_overview
        except Exception as e:
            print(f"❌ Error getting team capacity: {e}")
            return {"error": str(e)}

def main():
    """Demo the real JIRA API functionality"""
    print("🚀 TaskFlow Real JIRA API Demo")
    print("=" * 50)
    
    # Initialize JIRA API
    jira_api = JiraAPIService()
    
    if not jira_api.is_connected():
        print("❌ Cannot connect to JIRA. Please check your credentials.")
        return
    
    # Display users
    print("\n👥 JIRA USERS:")
    users = jira_api.get_users()
    for user in users[:5]:  # Show first 5 users
        print(f"  • {user['displayName']} ({user['username']}) - {user['timeZone']}")
        skills = ", ".join([f"{skill['name']}({skill['level']})" for skill in user['skills'][:3]])
        print(f"    Skills: {skills}")
    
    # Display unassigned tasks
    print("\n📋 UNASSIGNED TASKS:")
    unassigned = jira_api.get_unassigned_tasks()
    for task in unassigned[:5]:  # Show first 5 tasks
        print(f"  • {task['key']}: {task['summary']}")
        print(f"    Priority: {task['priority']} | Points: {task['storyPoints']} | Type: {task['issueType']}")
        if task['requiredSkills']:
            required_skills = ", ".join([f"{skill['name']}({skill['minLevel']}+)" for skill in task['requiredSkills']])
            print(f"    Required: {required_skills}")
    
    # Show team capacity
    print("\n📊 TEAM CAPACITY OVERVIEW:")
    capacity = jira_api.get_team_capacity_overview()
    
    if "error" not in capacity:
        for member in capacity["members"][:5]:  # Show first 5 members
            workload = member["workload"]
            print(f"  • {member['displayName']}:")
            print(f"    Assigned: {workload['totalStoryPoints']}/{workload['maxCapacity']} points ({workload['utilizationPercent']}%)")
            print(f"    Available: {workload['availableCapacity']} points")
        
        totals = capacity["teamTotals"]
        print(f"\n  Team Total: {totals['totalAssigned']}/{totals['totalCapacity']} points")
        print(f"  Average Utilization: {totals['averageUtilization']}%")
    else:
        print(f"  ❌ Error: {capacity['error']}")

if __name__ == "__main__":
    main()
