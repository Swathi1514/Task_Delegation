#!/usr/bin/env python3
"""
Unit Tests for Mock JIRA API
Tests the core functionality of the MockJiraAPI class
"""

import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/api'))

from mock_jira_api import MockJiraAPI


class TestMockJiraAPI(unittest.TestCase):
    """Test cases for MockJiraAPI class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.sample_users_data = {
            "users": [
                {
                    "id": "user_001",
                    "username": "test.user",
                    "displayName": "Test User",
                    "skills": [
                        {"name": "Python", "level": 4},
                        {"name": "React", "level": 3}
                    ],
                    "capacity": {
                        "pointsPerSprint": 40,
                        "currentLoad": 20
                    }
                }
            ]
        }
        
        self.sample_tasks_data = {
            "tasks": [
                {
                    "key": "TEST-001",
                    "summary": "Test task",
                    "priority": "High",
                    "storyPoints": 8,
                    "assignee": None,
                    "status": "To Do",
                    "requiredSkills": [
                        {"name": "Python", "minLevel": 3}
                    ]
                }
            ]
        }

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load_mock_data_success(self, mock_json_load, mock_file):
        """Test successful loading of mock data from JSON files"""
        # Setup mock return values
        mock_json_load.side_effect = [self.sample_users_data, self.sample_tasks_data]
        
        # Create API instance
        api = MockJiraAPI()
        
        # Verify data was loaded correctly
        self.assertEqual(len(api.users_data["users"]), 1)
        self.assertEqual(len(api.tasks_data["tasks"]), 1)
        self.assertEqual(api.users_data["users"][0]["username"], "test.user")
        self.assertEqual(api.tasks_data["tasks"][0]["key"], "TEST-001")

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_mock_data_file_not_found(self, mock_file):
        """Test fallback behavior when JSON files are not found"""
        api = MockJiraAPI()
        
        # Should fall back to empty data structures
        self.assertEqual(api.users_data, {"users": []})
        self.assertEqual(api.tasks_data, {"tasks": []})

    def test_get_users(self):
        """Test retrieving all users"""
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        
        users = api.get_users()
        
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["username"], "test.user")
        self.assertEqual(users[0]["displayName"], "Test User")

    def test_get_user_found(self):
        """Test retrieving a specific user by username"""
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        
        user = api.get_user("test.user")
        
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "test.user")
        self.assertEqual(user["displayName"], "Test User")

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        
        user = api.get_user("nonexistent.user")
        
        self.assertIsNone(user)

    def test_get_tasks_all(self):
        """Test retrieving all tasks without filters"""
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        tasks = api.get_tasks()
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["key"], "TEST-001")

    def test_get_tasks_by_project(self):
        """Test retrieving tasks filtered by project"""
        # Add project field to sample data
        self.sample_tasks_data["tasks"][0]["project"] = "TEST"
        
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        tasks = api.get_tasks(project_key="TEST")
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["project"], "TEST")

    def test_get_tasks_by_assignee(self):
        """Test retrieving tasks filtered by assignee"""
        # Set assignee in sample data
        self.sample_tasks_data["tasks"][0]["assignee"] = "test.user"
        
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        tasks = api.get_tasks(assignee="test.user")
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["assignee"], "test.user")

    def test_get_unassigned_tasks(self):
        """Test retrieving only unassigned tasks"""
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        unassigned_tasks = api.get_unassigned_tasks()
        
        self.assertEqual(len(unassigned_tasks), 1)
        self.assertIsNone(unassigned_tasks[0]["assignee"])

    def test_assign_task_success(self):
        """Test successful task assignment"""
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        result = api.assign_task("TEST-001", "test.user")
        
        self.assertTrue(result["success"])
        self.assertIn("assigned to test.user", result["message"])
        self.assertEqual(result["task"]["assignee"], "test.user")
        self.assertEqual(result["task"]["status"], "In Progress")
        self.assertIn("updated", result["task"])

    def test_assign_task_not_found(self):
        """Test assignment of non-existent task"""
        api = MockJiraAPI()
        api.tasks_data = self.sample_tasks_data
        
        result = api.assign_task("NONEXISTENT-001", "test.user")
        
        self.assertFalse(result["success"])
        self.assertIn("not found", result["message"])

    def test_get_user_workload(self):
        """Test calculating user workload"""
        # Setup data with assigned task
        self.sample_tasks_data["tasks"][0]["assignee"] = "test.user"
        
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        api.tasks_data = self.sample_tasks_data
        
        workload = api.get_user_workload("test.user")
        
        self.assertEqual(workload["username"], "test.user")
        self.assertEqual(workload["assignedTasks"], 1)
        self.assertEqual(workload["totalStoryPoints"], 8)
        self.assertEqual(workload["maxCapacity"], 40)
        self.assertEqual(workload["utilizationPercent"], 20.0)
        self.assertEqual(workload["availableCapacity"], 32)

    def test_get_user_workload_user_not_found(self):
        """Test workload calculation for non-existent user"""
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        
        workload = api.get_user_workload("nonexistent.user")
        
        self.assertIn("error", workload)
        self.assertEqual(workload["error"], "User not found")

    def test_get_team_capacity_overview(self):
        """Test team capacity overview calculation"""
        # Add assigned task
        self.sample_tasks_data["tasks"][0]["assignee"] = "test.user"
        
        api = MockJiraAPI()
        api.users_data = self.sample_users_data
        api.tasks_data = self.sample_tasks_data
        
        overview = api.get_team_capacity_overview()
        
        self.assertIn("members", overview)
        self.assertIn("teamTotals", overview)
        
        # Check member data
        self.assertEqual(len(overview["members"]), 1)
        member = overview["members"][0]
        self.assertEqual(member["username"], "test.user")
        self.assertEqual(member["displayName"], "Test User")
        
        # Check team totals
        totals = overview["teamTotals"]
        self.assertEqual(totals["totalCapacity"], 40)
        self.assertEqual(totals["totalAssigned"], 8)
        self.assertEqual(totals["averageUtilization"], 20.0)

    def test_get_team_capacity_overview_empty_team(self):
        """Test team capacity overview with no users"""
        api = MockJiraAPI()
        api.users_data = {"users": []}
        api.tasks_data = {"tasks": []}
        
        overview = api.get_team_capacity_overview()
        
        self.assertEqual(len(overview["members"]), 0)
        self.assertEqual(overview["teamTotals"]["totalCapacity"], 0)
        self.assertEqual(overview["teamTotals"]["totalAssigned"], 0)
        self.assertEqual(overview["teamTotals"]["averageUtilization"], 0)


class TestMockJiraAPIIntegration(unittest.TestCase):
    """Integration tests for MockJiraAPI with realistic data"""

    def setUp(self):
        """Set up realistic test data"""
        self.realistic_users = {
            "users": [
                {
                    "id": "user_001",
                    "username": "stacey.johnson",
                    "displayName": "Stacey",
                    "skills": [
                        {"name": "React", "level": 4},
                        {"name": "JavaScript", "level": 5},
                        {"name": "CSS", "level": 4}
                    ],
                    "capacity": {"pointsPerSprint": 40, "currentLoad": 24}
                },
                {
                    "id": "user_002",
                    "username": "maya.patel",
                    "displayName": "Maya",
                    "skills": [
                        {"name": "Python", "level": 5},
                        {"name": "Django", "level": 4},
                        {"name": "API Design", "level": 5}
                    ],
                    "capacity": {"pointsPerSprint": 45, "currentLoad": 36}
                }
            ]
        }
        
        self.realistic_tasks = {
            "tasks": [
                {
                    "key": "TASK-101",
                    "summary": "Implement user authentication UI",
                    "priority": "High",
                    "storyPoints": 8,
                    "assignee": None,
                    "status": "To Do",
                    "requiredSkills": [
                        {"name": "React", "minLevel": 3},
                        {"name": "JavaScript", "minLevel": 4}
                    ]
                },
                {
                    "key": "TASK-102",
                    "summary": "Design and implement recommendation API",
                    "priority": "Critical",
                    "storyPoints": 13,
                    "assignee": None,
                    "status": "To Do",
                    "requiredSkills": [
                        {"name": "Python", "minLevel": 4},
                        {"name": "API Design", "minLevel": 4}
                    ]
                }
            ]
        }

    def test_realistic_task_assignment_workflow(self):
        """Test a complete task assignment workflow with realistic data"""
        api = MockJiraAPI()
        api.users_data = self.realistic_users
        api.tasks_data = self.realistic_tasks
        
        # Get unassigned tasks
        unassigned = api.get_unassigned_tasks()
        self.assertEqual(len(unassigned), 2)
        
        # Assign React task to Stacey
        result1 = api.assign_task("TASK-101", "stacey.johnson")
        self.assertTrue(result1["success"])
        
        # Assign Python task to Maya
        result2 = api.assign_task("TASK-102", "maya.patel")
        self.assertTrue(result2["success"])
        
        # Check assignments
        stacey_tasks = api.get_tasks(assignee="stacey.johnson")
        maya_tasks = api.get_tasks(assignee="maya.patel")
        
        self.assertEqual(len(stacey_tasks), 1)
        self.assertEqual(len(maya_tasks), 1)
        self.assertEqual(stacey_tasks[0]["key"], "TASK-101")
        self.assertEqual(maya_tasks[0]["key"], "TASK-102")
        
        # Check workloads
        stacey_workload = api.get_user_workload("stacey.johnson")
        maya_workload = api.get_user_workload("maya.patel")
        
        self.assertEqual(stacey_workload["totalStoryPoints"], 8)
        self.assertEqual(maya_workload["totalStoryPoints"], 13)

    def test_team_capacity_after_assignments(self):
        """Test team capacity calculation after task assignments"""
        api = MockJiraAPI()
        api.users_data = self.realistic_users
        api.tasks_data = self.realistic_tasks
        
        # Assign tasks
        api.assign_task("TASK-101", "stacey.johnson")
        api.assign_task("TASK-102", "maya.patel")
        
        # Get team overview
        overview = api.get_team_capacity_overview()
        
        # Verify team totals
        totals = overview["teamTotals"]
        self.assertEqual(totals["totalCapacity"], 85)  # 40 + 45
        self.assertEqual(totals["totalAssigned"], 21)  # 8 + 13
        
        # Verify individual utilizations
        members = {m["username"]: m for m in overview["members"]}
        
        stacey_util = members["stacey.johnson"]["workload"]["utilizationPercent"]
        maya_util = members["maya.patel"]["workload"]["utilizationPercent"]
        
        self.assertEqual(stacey_util, 20.0)  # 8/40 * 100
        self.assertAlmostEqual(maya_util, 28.9, places=1)  # 13/45 * 100


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestMockJiraAPI))
    suite.addTest(unittest.makeSuite(TestMockJiraAPIIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
