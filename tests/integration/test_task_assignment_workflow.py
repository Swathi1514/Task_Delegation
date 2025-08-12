#!/usr/bin/env python3
"""
Integration Tests for Task Assignment Workflow
Tests the complete end-to-end task assignment process
"""

import unittest
import json
import sys
import os
from unittest.mock import patch, mock_open

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/api'))

from mock_jira_api import MockJiraAPI


class TestTaskAssignmentWorkflow(unittest.TestCase):
    """Integration tests for complete task assignment workflow"""
    
    def setUp(self):
        """Set up realistic test data for integration testing"""
        self.users_data = {
            "users": [
                {
                    "id": "user_001",
                    "username": "stacey.johnson",
                    "displayName": "Stacey",
                    "emailAddress": "stacey.johnson@company.com",
                    "timeZone": "America/New_York",
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
                    }
                },
                {
                    "id": "user_002",
                    "username": "maya.patel",
                    "displayName": "Maya",
                    "emailAddress": "maya.patel@company.com",
                    "timeZone": "America/Los_Angeles",
                    "skills": [
                        {"name": "Python", "level": 5},
                        {"name": "Django", "level": 4},
                        {"name": "PostgreSQL", "level": 4},
                        {"name": "AWS", "level": 4},
                        {"name": "API Design", "level": 5}
                    ],
                    "capacity": {
                        "pointsPerSprint": 45,
                        "hoursPerWeek": 40,
                        "currentLoad": 36,
                        "utilizationPercent": 80
                    }
                },
                {
                    "id": "user_003",
                    "username": "supraja.reddy",
                    "displayName": "Supraja",
                    "emailAddress": "supraja.reddy@company.com",
                    "timeZone": "Asia/Kolkata",
                    "skills": [
                        {"name": "Java", "level": 4},
                        {"name": "Spring Boot", "level": 4},
                        {"name": "React", "level": 3},
                        {"name": "Selenium", "level": 4},
                        {"name": "Testing", "level": 5}
                    ],
                    "capacity": {
                        "pointsPerSprint": 42,
                        "hoursPerWeek": 40,
                        "currentLoad": 30,
                        "utilizationPercent": 71
                    }
                }
            ]
        }
        
        self.tasks_data = {
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
                    "project": "TASK",
                    "storyPoints": 8,
                    "dueDate": "2025-08-20",
                    "requiredSkills": [
                        {"name": "React", "minLevel": 3},
                        {"name": "JavaScript", "minLevel": 4},
                        {"name": "CSS", "minLevel": 3}
                    ]
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
                    "project": "TASK",
                    "storyPoints": 13,
                    "dueDate": "2025-08-18",
                    "requiredSkills": [
                        {"name": "Python", "minLevel": 4},
                        {"name": "API Design", "minLevel": 4},
                        {"name": "Django", "minLevel": 3}
                    ]
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
                    "project": "TASK",
                    "storyPoints": 5,
                    "dueDate": "2025-08-25",
                    "requiredSkills": [
                        {"name": "Testing", "minLevel": 4},
                        {"name": "Selenium", "minLevel": 3}
                    ]
                }
            ]
        }
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_complete_task_assignment_workflow(self, mock_json_load, mock_file):
        """Test complete workflow from data loading to task assignment"""
        # Setup mock data loading
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        # Initialize API
        api = MockJiraAPI()
        
        # Verify initial state
        self.assertEqual(len(api.get_users()), 3)
        self.assertEqual(len(api.get_unassigned_tasks()), 3)
        
        # Test task assignment workflow
        unassigned_tasks = api.get_unassigned_tasks()
        
        # Assign React task to Stacey (best match)
        react_task = next(t for t in unassigned_tasks if "authentication UI" in t["summary"])
        result1 = api.assign_task(react_task["key"], "stacey.johnson")
        
        self.assertTrue(result1["success"])
        self.assertEqual(result1["task"]["assignee"], "stacey.johnson")
        self.assertEqual(result1["task"]["status"], "In Progress")
        
        # Assign Python task to Maya (best match)
        python_task = next(t for t in unassigned_tasks if "recommendation API" in t["summary"])
        result2 = api.assign_task(python_task["key"], "maya.patel")
        
        self.assertTrue(result2["success"])
        self.assertEqual(result2["task"]["assignee"], "maya.patel")
        
        # Assign Testing task to Supraja (best match)
        testing_task = next(t for t in unassigned_tasks if "testing framework" in t["summary"])
        result3 = api.assign_task(testing_task["key"], "supraja.reddy")
        
        self.assertTrue(result3["success"])
        self.assertEqual(result3["task"]["assignee"], "supraja.reddy")
        
        # Verify no unassigned tasks remain
        remaining_unassigned = api.get_unassigned_tasks()
        self.assertEqual(len(remaining_unassigned), 0)
        
        # Verify each user has correct assignments
        stacey_tasks = api.get_tasks(assignee="stacey.johnson")
        maya_tasks = api.get_tasks(assignee="maya.patel")
        supraja_tasks = api.get_tasks(assignee="supraja.reddy")
        
        self.assertEqual(len(stacey_tasks), 1)
        self.assertEqual(len(maya_tasks), 1)
        self.assertEqual(len(supraja_tasks), 1)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_capacity_management_workflow(self, mock_json_load, mock_file):
        """Test capacity management throughout assignment workflow"""
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Get initial capacity overview
        initial_overview = api.get_team_capacity_overview()
        initial_totals = initial_overview["teamTotals"]
        
        self.assertEqual(initial_totals["totalCapacity"], 127)  # 40 + 45 + 42
        self.assertEqual(initial_totals["totalAssigned"], 0)    # No assignments yet
        
        # Assign tasks and track capacity changes
        tasks = api.get_unassigned_tasks()
        
        # Assign first task (8 points)
        api.assign_task(tasks[0]["key"], "stacey.johnson")
        
        overview_after_1 = api.get_team_capacity_overview()
        self.assertEqual(overview_after_1["teamTotals"]["totalAssigned"], 8)
        
        # Assign second task (13 points)
        api.assign_task(tasks[1]["key"], "maya.patel")
        
        overview_after_2 = api.get_team_capacity_overview()
        self.assertEqual(overview_after_2["teamTotals"]["totalAssigned"], 21)  # 8 + 13
        
        # Assign third task (5 points)
        api.assign_task(tasks[2]["key"], "supraja.reddy")
        
        final_overview = api.get_team_capacity_overview()
        final_totals = final_overview["teamTotals"]
        
        self.assertEqual(final_totals["totalAssigned"], 26)  # 8 + 13 + 5
        self.assertAlmostEqual(final_totals["averageUtilization"], 20.5, places=1)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_individual_workload_tracking(self, mock_json_load, mock_file):
        """Test individual user workload tracking during assignments"""
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Get initial workloads
        stacey_initial = api.get_user_workload("stacey.johnson")
        maya_initial = api.get_user_workload("maya.patel")
        supraja_initial = api.get_user_workload("supraja.reddy")
        
        self.assertEqual(stacey_initial["totalStoryPoints"], 0)
        self.assertEqual(maya_initial["totalStoryPoints"], 0)
        self.assertEqual(supraja_initial["totalStoryPoints"], 0)
        
        # Assign tasks
        tasks = api.get_unassigned_tasks()
        api.assign_task(tasks[0]["key"], "stacey.johnson")    # 8 points
        api.assign_task(tasks[1]["key"], "maya.patel")        # 13 points
        api.assign_task(tasks[2]["key"], "supraja.reddy")     # 5 points
        
        # Check final workloads
        stacey_final = api.get_user_workload("stacey.johnson")
        maya_final = api.get_user_workload("maya.patel")
        supraja_final = api.get_user_workload("supraja.reddy")
        
        self.assertEqual(stacey_final["totalStoryPoints"], 8)
        self.assertEqual(stacey_final["assignedTasks"], 1)
        self.assertEqual(stacey_final["utilizationPercent"], 20.0)  # 8/40
        self.assertEqual(stacey_final["availableCapacity"], 32)
        
        self.assertEqual(maya_final["totalStoryPoints"], 13)
        self.assertEqual(maya_final["assignedTasks"], 1)
        self.assertAlmostEqual(maya_final["utilizationPercent"], 28.9, places=1)  # 13/45
        
        self.assertEqual(supraja_final["totalStoryPoints"], 5)
        self.assertEqual(supraja_final["assignedTasks"], 1)
        self.assertAlmostEqual(supraja_final["utilizationPercent"], 11.9, places=1)  # 5/42
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_error_handling_workflow(self, mock_json_load, mock_file):
        """Test error handling in assignment workflow"""
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Test assigning non-existent task
        result1 = api.assign_task("NONEXISTENT-001", "stacey.johnson")
        self.assertFalse(result1["success"])
        self.assertIn("not found", result1["message"])
        
        # Test assigning to non-existent user (should still work but with invalid assignee)
        tasks = api.get_unassigned_tasks()
        result2 = api.assign_task(tasks[0]["key"], "nonexistent.user")
        self.assertTrue(result2["success"])  # Assignment succeeds but with invalid user
        
        # Test getting workload for non-existent user
        workload = api.get_user_workload("nonexistent.user")
        self.assertIn("error", workload)
        self.assertEqual(workload["error"], "User not found")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_project_filtering_workflow(self, mock_json_load, mock_file):
        """Test project-based task filtering workflow"""
        # Add project information to tasks
        for task in self.tasks_data["tasks"]:
            task["project"] = "TASK"
        
        # Add task from different project
        self.tasks_data["tasks"].append({
            "key": "OTHER-001",
            "summary": "Other project task",
            "project": "OTHER",
            "assignee": None,
            "storyPoints": 3
        })
        
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Test filtering by project
        task_project_tasks = api.get_tasks(project_key="TASK")
        other_project_tasks = api.get_tasks(project_key="OTHER")
        
        self.assertEqual(len(task_project_tasks), 3)
        self.assertEqual(len(other_project_tasks), 1)
        
        # Assign task from TASK project
        api.assign_task("TASK-101", "stacey.johnson")
        
        # Verify filtering still works after assignment
        task_assigned = api.get_tasks(project_key="TASK", assignee="stacey.johnson")
        self.assertEqual(len(task_assigned), 1)
        self.assertEqual(task_assigned[0]["key"], "TASK-101")
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_concurrent_assignment_workflow(self, mock_json_load, mock_file):
        """Test handling of concurrent task assignments"""
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Simulate concurrent assignment attempts
        tasks = api.get_unassigned_tasks()
        task_key = tasks[0]["key"]
        
        # First assignment should succeed
        result1 = api.assign_task(task_key, "stacey.johnson")
        self.assertTrue(result1["success"])
        
        # Second assignment to same task should still succeed (reassignment)
        result2 = api.assign_task(task_key, "maya.patel")
        self.assertTrue(result2["success"])
        self.assertEqual(result2["task"]["assignee"], "maya.patel")
        
        # Verify task is now assigned to second user
        assigned_task = api.get_tasks(assignee="maya.patel")
        self.assertEqual(len(assigned_task), 1)
        self.assertEqual(assigned_task[0]["key"], task_key)
        
        # Verify first user no longer has the task
        stacey_tasks = api.get_tasks(assignee="stacey.johnson")
        self.assertEqual(len(stacey_tasks), 0)
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_data_consistency_workflow(self, mock_json_load, mock_file):
        """Test data consistency throughout assignment workflow"""
        mock_json_load.side_effect = [self.users_data, self.tasks_data]
        
        api = MockJiraAPI()
        
        # Track initial state
        initial_users = len(api.get_users())
        initial_tasks = len(api.get_tasks())
        initial_unassigned = len(api.get_unassigned_tasks())
        
        # Perform assignments
        tasks = api.get_unassigned_tasks()
        for i, task in enumerate(tasks):
            user = api.get_users()[i % len(api.get_users())]
            api.assign_task(task["key"], user["username"])
        
        # Verify data consistency
        final_users = len(api.get_users())
        final_tasks = len(api.get_tasks())
        final_unassigned = len(api.get_unassigned_tasks())
        
        # User count should remain the same
        self.assertEqual(initial_users, final_users)
        
        # Task count should remain the same
        self.assertEqual(initial_tasks, final_tasks)
        
        # All tasks should now be assigned
        self.assertEqual(final_unassigned, 0)
        self.assertEqual(initial_unassigned, initial_tasks)
        
        # Verify all tasks have assignees
        all_tasks = api.get_tasks()
        for task in all_tasks:
            self.assertIsNotNone(task["assignee"])
            self.assertEqual(task["status"], "In Progress")


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTaskAssignmentWorkflow))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
