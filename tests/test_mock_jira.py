#!/usr/bin/env python3
"""
Tests for Mock JIRA API
Ensures mock functionality works correctly for testing
"""

import sys
import os
import pytest

# Add the src/api directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'api'))

from mock_jira_api import MockJiraAPI

class TestMockJiraAPI:
    def setup_method(self):
        """Set up test fixtures"""
        self.mock_jira = MockJiraAPI()
    
    def test_get_users(self):
        """Test getting users from mock API"""
        users = self.mock_jira.get_users()
        assert isinstance(users, list)
        assert len(users) > 0
        
        # Check user structure
        user = users[0]
        assert 'username' in user
        assert 'displayName' in user
        assert 'skills' in user
        assert 'capacity' in user
    
    def test_get_user_by_username(self):
        """Test getting specific user by username"""
        users = self.mock_jira.get_users()
        if users:
            username = users[0]['username']
            user = self.mock_jira.get_user(username)
            assert user is not None
            assert user['username'] == username
        
        # Test non-existent user
        non_existent = self.mock_jira.get_user('non_existent_user')
        assert non_existent is None
    
    def test_get_tasks(self):
        """Test getting tasks from mock API"""
        tasks = self.mock_jira.get_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) > 0
        
        # Check task structure
        task = tasks[0]
        assert 'key' in task
        assert 'summary' in task
        assert 'priority' in task
        assert 'storyPoints' in task
        assert 'requiredSkills' in task
    
    def test_get_unassigned_tasks(self):
        """Test getting unassigned tasks"""
        unassigned = self.mock_jira.get_unassigned_tasks()
        assert isinstance(unassigned, list)
        
        # All returned tasks should be unassigned
        for task in unassigned:
            assert task.get('assignee') is None
    
    def test_assign_task(self):
        """Test task assignment functionality"""
        # Get an unassigned task and a user
        unassigned_tasks = self.mock_jira.get_unassigned_tasks()
        users = self.mock_jira.get_users()
        
        if unassigned_tasks and users:
            task_key = unassigned_tasks[0]['key']
            username = users[0]['username']
            
            # Assign the task
            result = self.mock_jira.assign_task(task_key, username)
            
            assert result['success'] is True
            assert task_key in result['message']
            assert username in result['message']
            
            # Verify the task is now assigned
            tasks = self.mock_jira.get_tasks(assignee=username)
            assigned_task = next((t for t in tasks if t['key'] == task_key), None)
            assert assigned_task is not None
            assert assigned_task['assignee'] == username
    
    def test_assign_nonexistent_task(self):
        """Test assigning a non-existent task"""
        result = self.mock_jira.assign_task('NONEXISTENT-999', 'some_user')
        assert result['success'] is False
        assert 'not found' in result['message'].lower()
    
    def test_get_user_workload(self):
        """Test user workload calculation"""
        users = self.mock_jira.get_users()
        if users:
            username = users[0]['username']
            workload = self.mock_jira.get_user_workload(username)
            
            assert 'username' in workload
            assert 'assignedTasks' in workload
            assert 'totalStoryPoints' in workload
            assert 'maxCapacity' in workload
            assert 'utilizationPercent' in workload
            assert 'availableCapacity' in workload
            
            assert workload['username'] == username
            assert isinstance(workload['assignedTasks'], int)
            assert isinstance(workload['totalStoryPoints'], (int, float))
            assert isinstance(workload['utilizationPercent'], (int, float))
    
    def test_get_team_capacity_overview(self):
        """Test team capacity overview"""
        overview = self.mock_jira.get_team_capacity_overview()
        
        assert 'members' in overview
        assert 'teamTotals' in overview
        
        assert isinstance(overview['members'], list)
        assert 'totalCapacity' in overview['teamTotals']
        assert 'totalAssigned' in overview['teamTotals']
        assert 'averageUtilization' in overview['teamTotals']
    
    def test_task_assignment_updates_workload(self):
        """Test that task assignment updates user workload"""
        users = self.mock_jira.get_users()
        unassigned_tasks = self.mock_jira.get_unassigned_tasks()
        
        if users and unassigned_tasks:
            username = users[0]['username']
            task_key = unassigned_tasks[0]['key']
            task_points = unassigned_tasks[0]['storyPoints']
            
            # Get initial workload
            initial_workload = self.mock_jira.get_user_workload(username)
            initial_points = initial_workload['totalStoryPoints']
            
            # Assign task
            self.mock_jira.assign_task(task_key, username)
            
            # Check updated workload
            updated_workload = self.mock_jira.get_user_workload(username)
            updated_points = updated_workload['totalStoryPoints']
            
            assert updated_points == initial_points + task_points

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
