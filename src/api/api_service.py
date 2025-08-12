#!/usr/bin/env python3
"""
TaskFlow API Service
Provides a unified interface that can switch between mock and real JIRA implementations
"""

import os
import sys
import json
from typing import Dict, List, Optional

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from jira_api import JiraAPIService
    JIRA_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Real JIRA API not available: {e}")
    JIRA_AVAILABLE = False

from mock_jira_api import MockJiraAPI

class TaskFlowAPIService:
    def __init__(self, use_real_jira=True, config_file=None):
        """
        Initialize API service
        
        Args:
            use_real_jira (bool): If True, use real JIRA API. If False, use mock.
            config_file (str): Path to JIRA configuration file
        """
        self.use_real_jira = use_real_jira and JIRA_AVAILABLE
        self.config_file = config_file
        
        if self.use_real_jira:
            print("🔗 Initializing Real JIRA API Service...")
            self.api = JiraAPIService(config_file)
            if not self.api.is_connected():
                print("⚠️  Failed to connect to real JIRA, falling back to mock...")
                self.use_real_jira = False
                self.api = MockJiraAPI()
        else:
            print("🎭 Initializing Mock JIRA API Service...")
            self.api = MockJiraAPI()
        
        print(f"✅ API Service initialized ({'Real JIRA' if self.use_real_jira else 'Mock JIRA'})")
    
    def get_api_info(self) -> Dict:
        """Get information about the current API configuration"""
        return {
            "type": "real" if self.use_real_jira else "mock",
            "connected": self.api.is_connected() if hasattr(self.api, 'is_connected') else True,
            "jira_available": JIRA_AVAILABLE
        }
    
    def get_users(self) -> List[Dict]:
        """Get all users"""
        return self.api.get_users()
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get specific user by username"""
        return self.api.get_user(username)
    
    def get_tasks(self, project_key: str = None, assignee: str = None, status: str = None) -> List[Dict]:
        """Get tasks with optional filtering"""
        if self.use_real_jira:
            return self.api.get_tasks(project_key, assignee, status)
        else:
            return self.api.get_tasks(project_key, assignee)
    
    def get_unassigned_tasks(self) -> List[Dict]:
        """Get all unassigned tasks"""
        return self.api.get_unassigned_tasks()
    
    def assign_task(self, task_key: str, assignee_username: str) -> Dict:
        """Assign a task to a user"""
        return self.api.assign_task(task_key, assignee_username)
    
    def get_user_workload(self, username: str) -> Dict:
        """Calculate current workload for a user"""
        return self.api.get_user_workload(username)
    
    def get_team_capacity_overview(self) -> Dict:
        """Get capacity overview for entire team"""
        return self.api.get_team_capacity_overview()

class TaskFlowWebAPI:
    """Web API wrapper for TaskFlow that provides HTTP-like responses"""
    
    def __init__(self, use_real_jira=True, config_file=None):
        self.service = TaskFlowAPIService(use_real_jira, config_file)
    
    def handle_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """
        Handle API requests in a REST-like manner
        
        Args:
            endpoint (str): API endpoint (e.g., '/users', '/tasks', '/assign')
            method (str): HTTP method ('GET', 'POST', 'PUT', 'DELETE')
            data (Dict): Request data for POST/PUT requests
        
        Returns:
            Dict: Response with status, data, and message
        """
        try:
            if endpoint == '/api/info':
                return {
                    "status": "success",
                    "data": self.service.get_api_info(),
                    "message": "API info retrieved successfully"
                }
            
            elif endpoint == '/api/users':
                if method == 'GET':
                    users = self.service.get_users()
                    return {
                        "status": "success",
                        "data": users,
                        "message": f"Retrieved {len(users)} users"
                    }
            
            elif endpoint.startswith('/api/users/'):
                username = endpoint.split('/')[-1]
                if method == 'GET':
                    user = self.service.get_user(username)
                    if user:
                        return {
                            "status": "success",
                            "data": user,
                            "message": f"User {username} retrieved successfully"
                        }
                    else:
                        return {
                            "status": "error",
                            "data": None,
                            "message": f"User {username} not found"
                        }
            
            elif endpoint == '/api/tasks':
                if method == 'GET':
                    # Parse query parameters from data
                    project_key = data.get('project_key') if data else None
                    assignee = data.get('assignee') if data else None
                    status = data.get('status') if data else None
                    
                    tasks = self.service.get_tasks(project_key, assignee, status)
                    return {
                        "status": "success",
                        "data": tasks,
                        "message": f"Retrieved {len(tasks)} tasks"
                    }
            
            elif endpoint == '/api/tasks/unassigned':
                if method == 'GET':
                    tasks = self.service.get_unassigned_tasks()
                    return {
                        "status": "success",
                        "data": tasks,
                        "message": f"Retrieved {len(tasks)} unassigned tasks"
                    }
            
            elif endpoint == '/api/assign':
                if method == 'POST' and data:
                    task_key = data.get('task_key')
                    assignee = data.get('assignee')
                    
                    if not task_key or not assignee:
                        return {
                            "status": "error",
                            "data": None,
                            "message": "task_key and assignee are required"
                        }
                    
                    result = self.service.assign_task(task_key, assignee)
                    return {
                        "status": "success" if result.get("success") else "error",
                        "data": result,
                        "message": result.get("message", "Assignment completed")
                    }
            
            elif endpoint == '/api/workload':
                if method == 'GET' and data and data.get('username'):
                    username = data.get('username')
                    workload = self.service.get_user_workload(username)
                    return {
                        "status": "success",
                        "data": workload,
                        "message": f"Workload for {username} retrieved successfully"
                    }
            
            elif endpoint == '/api/capacity':
                if method == 'GET':
                    capacity = self.service.get_team_capacity_overview()
                    return {
                        "status": "success",
                        "data": capacity,
                        "message": "Team capacity overview retrieved successfully"
                    }
            
            else:
                return {
                    "status": "error",
                    "data": None,
                    "message": f"Endpoint {endpoint} not found"
                }
        
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "message": f"Internal server error: {str(e)}"
            }

def main():
    """Demo the unified API service"""
    print("🚀 TaskFlow Unified API Service Demo")
    print("=" * 50)
    
    # Test with real JIRA first
    print("\n🔗 Testing Real JIRA API:")
    real_api = TaskFlowWebAPI(use_real_jira=True)
    
    # Get API info
    info_response = real_api.handle_request('/api/info')
    print(f"API Info: {info_response}")
    
    # Get users
    users_response = real_api.handle_request('/api/users')
    print(f"Users: {users_response['message']}")
    
    # Get unassigned tasks
    tasks_response = real_api.handle_request('/api/tasks/unassigned')
    print(f"Unassigned Tasks: {tasks_response['message']}")
    
    # Get team capacity
    capacity_response = real_api.handle_request('/api/capacity')
    print(f"Team Capacity: {capacity_response['message']}")
    
    print("\n" + "="*50)
    
    # Test with mock API
    print("\n🎭 Testing Mock JIRA API:")
    mock_api = TaskFlowWebAPI(use_real_jira=False)
    
    # Get API info
    info_response = mock_api.handle_request('/api/info')
    print(f"API Info: {info_response}")
    
    # Get users
    users_response = mock_api.handle_request('/api/users')
    print(f"Users: {users_response['message']}")
    
    # Get unassigned tasks
    tasks_response = mock_api.handle_request('/api/tasks/unassigned')
    print(f"Unassigned Tasks: {tasks_response['message']}")
    
    # Test assignment
    assign_response = mock_api.handle_request('/api/assign', 'POST', {
        'task_key': 'TASK-101',
        'assignee': 'stacey.johnson'
    })
    print(f"Assignment: {assign_response['message']}")

if __name__ == "__main__":
    main()
