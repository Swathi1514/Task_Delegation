#!/usr/bin/env python3
"""
Simple Test Runner for TaskFlow Backend
Basic test runner that works with the current setup
"""

import sys
import os
import unittest
import time

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/api'))


def run_basic_tests():
    """Run basic functionality tests"""
    print("🚀 TaskFlow Backend - Basic Tests")
    print("=" * 50)
    
    # Test 1: Import and initialize MockJiraAPI
    print("🧪 Test 1: MockJiraAPI Import and Initialization")
    try:
        from mock_jira_api import MockJiraAPI
        api = MockJiraAPI()
        print(f"   ✅ MockJiraAPI imported successfully")
        print(f"   ✅ Users loaded: {len(api.get_users())}")
        print(f"   ✅ Tasks loaded: {len(api.get_tasks())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Basic API Operations
    print("\n🧪 Test 2: Basic API Operations")
    try:
        # Test user retrieval
        users = api.get_users()
        assert len(users) > 0, "No users found"
        print(f"   ✅ Retrieved {len(users)} users")
        
        # Test specific user retrieval
        user = api.get_user("stacey.johnson")
        assert user is not None, "Stacey not found"
        assert user["displayName"] == "Stacey", "Wrong user data"
        print(f"   ✅ Retrieved specific user: {user['displayName']}")
        
        # Test task retrieval
        tasks = api.get_tasks()
        assert len(tasks) > 0, "No tasks found"
        print(f"   ✅ Retrieved {len(tasks)} tasks")
        
        # Test unassigned tasks
        unassigned = api.get_unassigned_tasks()
        print(f"   ✅ Found {len(unassigned)} unassigned tasks")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 3: Task Assignment
    print("\n🧪 Test 3: Task Assignment")
    try:
        # Get first unassigned task
        unassigned_tasks = api.get_unassigned_tasks()
        if unassigned_tasks:
            task = unassigned_tasks[0]
            result = api.assign_task(task["key"], "stacey.johnson")
            assert result["success"], "Task assignment failed"
            print(f"   ✅ Assigned task {task['key']} to stacey.johnson")
            
            # Verify assignment
            assigned_tasks = api.get_tasks(assignee="stacey.johnson")
            assert len(assigned_tasks) > 0, "No assigned tasks found"
            print(f"   ✅ Verified assignment: {len(assigned_tasks)} tasks assigned")
        else:
            print("   ⚠️  No unassigned tasks available for testing")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 4: Workload Calculation
    print("\n🧪 Test 4: Workload Calculation")
    try:
        workload = api.get_user_workload("stacey.johnson")
        assert "username" in workload, "Invalid workload data"
        assert "totalStoryPoints" in workload, "Missing story points"
        print(f"   ✅ Calculated workload for stacey.johnson:")
        print(f"      - Total Story Points: {workload['totalStoryPoints']}")
        print(f"      - Utilization: {workload['utilizationPercent']}%")
        print(f"      - Available Capacity: {workload['availableCapacity']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 5: Team Capacity Overview
    print("\n🧪 Test 5: Team Capacity Overview")
    try:
        overview = api.get_team_capacity_overview()
        assert "members" in overview, "Missing members data"
        assert "teamTotals" in overview, "Missing team totals"
        
        members = overview["members"]
        totals = overview["teamTotals"]
        
        print(f"   ✅ Team capacity overview:")
        print(f"      - Team Members: {len(members)}")
        print(f"      - Total Capacity: {totals['totalCapacity']} points")
        print(f"      - Total Assigned: {totals['totalAssigned']} points")
        print(f"      - Average Utilization: {totals['averageUtilization']}%")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 6: Error Handling
    print("\n🧪 Test 6: Error Handling")
    try:
        # Test non-existent user
        user = api.get_user("nonexistent.user")
        assert user is None, "Should return None for non-existent user"
        print("   ✅ Correctly handled non-existent user")
        
        # Test non-existent task assignment
        result = api.assign_task("NONEXISTENT-001", "stacey.johnson")
        assert not result["success"], "Should fail for non-existent task"
        print("   ✅ Correctly handled non-existent task assignment")
        
        # Test workload for non-existent user
        workload = api.get_user_workload("nonexistent.user")
        assert "error" in workload, "Should return error for non-existent user"
        print("   ✅ Correctly handled workload request for non-existent user")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    return True


def run_recommendation_tests():
    """Run basic recommendation engine tests"""
    print("\n🧪 Recommendation Engine Tests")
    print("=" * 50)
    
    try:
        # Import the recommendation engine from the test file
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'unit'))
        from test_recommendation_engine import RecommendationEngine
        
        engine = RecommendationEngine()
        print("   ✅ RecommendationEngine imported successfully")
        
        # Test skill fit calculation
        user_skills = [{"name": "React", "level": 4}]
        required_skills = [{"name": "React", "minLevel": 3}]
        skill_fit = engine.calculate_skill_fit(user_skills, required_skills)
        assert skill_fit == 1.0, f"Expected 1.0, got {skill_fit}"
        print(f"   ✅ Skill fit calculation: {skill_fit}")
        
        # Test capacity factor calculation
        capacity_factor = engine.calculate_capacity_factor(20, 40)
        assert capacity_factor == 0.5, f"Expected 0.5, got {capacity_factor}"
        print(f"   ✅ Capacity factor calculation: {capacity_factor}")
        
        # Test hard constraints
        user = {
            "skills": [{"name": "React", "level": 4}],
            "capacity": {"pointsPerSprint": 40, "currentLoad": 20}
        }
        task = {"requiredSkills": [{"name": "React", "minLevel": 3}]}
        
        meets_constraints, message = engine.check_hard_constraints(user, task)
        assert meets_constraints, f"Should meet constraints: {message}"
        print(f"   ✅ Hard constraints check: {message}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    """Main test function"""
    start_time = time.time()
    
    # Run basic tests
    basic_success = run_basic_tests()
    
    # Run recommendation tests
    recommendation_success = run_recommendation_tests()
    
    end_time = time.time()
    
    # Print summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"Basic API Tests: {'✅ PASSED' if basic_success else '❌ FAILED'}")
    print(f"Recommendation Tests: {'✅ PASSED' if recommendation_success else '❌ FAILED'}")
    print(f"Execution Time: {end_time - start_time:.2f}s")
    
    overall_success = basic_success and recommendation_success
    print(f"Overall Status: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    return 0 if overall_success else 1


if __name__ == '__main__':
    sys.exit(main())
