#!/usr/bin/env python3
"""
Mock JIRA API Simulator
Simulates JIRA REST API responses for TaskFlow testing without requiring actual JIRA access
"""

import json
import datetime
import os
from typing import Dict, List, Optional

class MockJiraAPI:
    def __init__(self):
        """Initialize mock JIRA API with sample data"""
        self.load_mock_data()
    
    def load_mock_data(self):
        """Load mock users and tasks from JSON files"""
        try:
            # Get the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            users_path = os.path.join(script_dir, '../data/mock_jira_users.json')
            tasks_path = os.path.join(script_dir, '../data/mock_jira_tasks.json')
            
            with open(users_path, 'r') as f:
                self.users_data = json.load(f)
            
            with open(tasks_path, 'r') as f:
                self.tasks_data = json.load(f)
                
            print("✅ Mock JIRA data loaded successfully")
        except FileNotFoundError as e:
            print(f"❌ Error loading mock data: {e}")
            self.users_data = {"users": []}
            self.tasks_data = {"tasks": []}
    
    def get_users(self) -> List[Dict]:
        """Get all users (simulates /rest/api/2/users/search)"""
        return self.users_data.get("users", [])
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get specific user by username"""
        users = self.get_users()
        for user in users:
            if user["username"] == username:
                return user
        return None
    
    def get_tasks(self, project_key: str = None, assignee: str = None) -> List[Dict]:
        """Get tasks with optional filtering (simulates /rest/api/2/search)"""
        tasks = self.tasks_data.get("tasks", [])
        
        if project_key:
            tasks = [task for task in tasks if task["project"] == project_key]
        
        if assignee:
            tasks = [task for task in tasks if task.get("assignee") == assignee]
            
        return tasks
    
    def get_unassigned_tasks(self) -> List[Dict]:
        """Get all unassigned tasks"""
        return self.get_tasks(assignee=None)
    
    def assign_task(self, task_key: str, assignee_username: str) -> Dict:
        """Assign a task to a user (simulates PUT /rest/api/2/issue/{issueKey})"""
        tasks = self.tasks_data.get("tasks", [])
        
        for task in tasks:
            if task["key"] == task_key:
                task["assignee"] = assignee_username
                task["status"] = "In Progress"
                task["updated"] = datetime.datetime.now().isoformat()
                
                return {
                    "success": True,
                    "message": f"Task {task_key} assigned to {assignee_username}",
                    "task": task
                }
        
        return {
            "success": False,
            "message": f"Task {task_key} not found"
        }
    
    def get_user_workload(self, username: str) -> Dict:
        """Calculate current workload for a user"""
        user = self.get_user(username)
        if not user:
            return {"error": "User not found"}
        
        assigned_tasks = self.get_tasks(assignee=username)
        total_story_points = sum(task.get("storyPoints", 0) for task in assigned_tasks)
        
        capacity = user.get("capacity", {})
        max_capacity = capacity.get("pointsPerSprint", 40)
        utilization = (total_story_points / max_capacity) * 100 if max_capacity > 0 else 0
        
        return {
            "username": username,
            "assignedTasks": len(assigned_tasks),
            "totalStoryPoints": total_story_points,
            "maxCapacity": max_capacity,
            "utilizationPercent": round(utilization, 1),
            "availableCapacity": max_capacity - total_story_points
        }
    
    def get_team_capacity_overview(self) -> Dict:
        """Get capacity overview for entire team"""
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
        
        if len(users) > 0:
            team_overview["teamTotals"]["averageUtilization"] = round(total_utilization / len(users), 1)
        
        return team_overview

def main():
    """Demo the mock JIRA API functionality"""
    print("🚀 TaskFlow Mock JIRA API Demo")
    print("=" * 50)
    
    # Initialize mock API
    jira = MockJiraAPI()
    
    # Display users
    print("\n👥 USERS:")
    users = jira.get_users()
    for user in users:
        print(f"  • {user['displayName']} ({user['username']}) - {user['timeZone']}")
        skills = ", ".join([f"{skill['name']}({skill['level']})" for skill in user['skills'][:3]])
        print(f"    Skills: {skills}...")
    
    # Display unassigned tasks
    print("\n📋 UNASSIGNED TASKS:")
    unassigned = jira.get_unassigned_tasks()
    for task in unassigned:
        print(f"  • {task['key']}: {task['summary']}")
        print(f"    Priority: {task['priority']} | Points: {task['storyPoints']} | Due: {task['dueDate']}")
        required_skills = ", ".join([f"{skill['name']}({skill['minLevel']}+)" for skill in task['requiredSkills']])
        print(f"    Required: {required_skills}")
    
    # Simulate task assignment
    print("\n🎯 SIMULATING TASK ASSIGNMENTS:")
    assignments = [
        ("TASK-101", "stacey.johnson"),  # UI task to frontend specialist
        ("TASK-102", "maya.patel"),      # API task to backend specialist  
        ("TASK-103", "supraja.reddy")    # Testing task to QA engineer
    ]
    
    for task_key, assignee in assignments:
        result = jira.assign_task(task_key, assignee)
        if result["success"]:
            print(f"  ✅ {result['message']}")
        else:
            print(f"  ❌ {result['message']}")
    
    # Show team capacity after assignments
    print("\n📊 TEAM CAPACITY OVERVIEW:")
    capacity = jira.get_team_capacity_overview()
    
    for member in capacity["members"]:
        workload = member["workload"]
        print(f"  • {member['displayName']}:")
        print(f"    Assigned: {workload['totalStoryPoints']}/{workload['maxCapacity']} points ({workload['utilizationPercent']}%)")
        print(f"    Available: {workload['availableCapacity']} points")
    
    totals = capacity["teamTotals"]
    print(f"\n  Team Total: {totals['totalAssigned']}/{totals['totalCapacity']} points")
    print(f"  Average Utilization: {totals['averageUtilization']}%")

if __name__ == "__main__":
    main()
