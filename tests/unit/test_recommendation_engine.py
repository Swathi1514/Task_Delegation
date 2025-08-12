#!/usr/bin/env python3
"""
Unit Tests for Recommendation Engine
Tests the core recommendation logic and scoring algorithms
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/api'))


class RecommendationEngine:
    """
    Recommendation Engine for TaskFlow
    Implements the core recommendation logic extracted from integration.js
    """
    
    def __init__(self):
        self.skill_weight = 0.7
        self.capacity_weight = 0.3
    
    def calculate_skill_fit(self, user_skills, required_skills):
        """Calculate skill fit score (0-1)"""
        if not required_skills:
            return 1.0
        
        skill_matches = 0
        total_requirements = len(required_skills)
        
        for req_skill in required_skills:
            user_skill = next((s for s in user_skills if s["name"] == req_skill["name"]), None)
            if user_skill:
                # Score based on how much user skill exceeds minimum requirement
                skill_ratio = min(user_skill["level"] / req_skill["minLevel"], 1.0)
                skill_matches += skill_ratio
        
        return skill_matches / total_requirements if total_requirements > 0 else 0
    
    def calculate_capacity_factor(self, current_load, max_capacity):
        """Calculate capacity factor (0-1)"""
        if max_capacity <= 0:
            return 0
        
        utilization = current_load / max_capacity
        return max(0, 1 - utilization)
    
    def calculate_score(self, user, task):
        """Calculate overall recommendation score"""
        skill_fit = self.calculate_skill_fit(
            user.get("skills", []), 
            task.get("requiredSkills", [])
        )
        
        capacity = user.get("capacity", {})
        capacity_factor = self.calculate_capacity_factor(
            capacity.get("currentLoad", 0),
            capacity.get("pointsPerSprint", 40)
        )
        
        # Weighted score
        score = (self.skill_weight * skill_fit) + (self.capacity_weight * capacity_factor)
        return min(score, 1.0)
    
    def check_hard_constraints(self, user, task):
        """Check if user meets hard constraints for the task"""
        required_skills = task.get("requiredSkills", [])
        user_skills = user.get("skills", [])
        
        # Check mandatory skills
        for req_skill in required_skills:
            user_skill = next((s for s in user_skills if s["name"] == req_skill["name"]), None)
            if not user_skill or user_skill["level"] < req_skill["minLevel"]:
                return False, f"Missing required skill: {req_skill['name']} (level {req_skill['minLevel']}+)"
        
        # Check capacity constraint (90% threshold)
        capacity = user.get("capacity", {})
        current_load = capacity.get("currentLoad", 0)
        max_capacity = capacity.get("pointsPerSprint", 40)
        
        if current_load / max_capacity >= 0.9:
            return False, "User at capacity limit (90%+)"
        
        return True, "All constraints met"
    
    def generate_recommendations(self, users, task, max_recommendations=3):
        """Generate ranked recommendations for a task"""
        candidates = []
        
        for user in users:
            # Check hard constraints first
            meets_constraints, constraint_msg = self.check_hard_constraints(user, task)
            
            if meets_constraints:
                score = self.calculate_score(user, task)
                candidates.append({
                    "user": user,
                    "score": score,
                    "constraint_status": constraint_msg
                })
            else:
                # Include in results but with zero score for transparency
                candidates.append({
                    "user": user,
                    "score": 0.0,
                    "constraint_status": constraint_msg,
                    "excluded": True
                })
        
        # Sort by score (descending) and take top N
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:max_recommendations]


class TestRecommendationEngine(unittest.TestCase):
    """Test cases for RecommendationEngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = RecommendationEngine()
        
        self.sample_users = [
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
            },
            {
                "id": "user_003",
                "username": "supraja.reddy",
                "displayName": "Supraja",
                "skills": [
                    {"name": "Java", "level": 4},
                    {"name": "Testing", "level": 5},
                    {"name": "React", "level": 3}
                ],
                "capacity": {"pointsPerSprint": 42, "currentLoad": 30}
            }
        ]
        
        self.sample_tasks = {
            "react_task": {
                "key": "TASK-101",
                "summary": "React UI task",
                "requiredSkills": [
                    {"name": "React", "minLevel": 3},
                    {"name": "JavaScript", "minLevel": 4}
                ],
                "storyPoints": 8
            },
            "python_task": {
                "key": "TASK-102",
                "summary": "Python API task",
                "requiredSkills": [
                    {"name": "Python", "minLevel": 4},
                    {"name": "API Design", "minLevel": 4}
                ],
                "storyPoints": 13
            },
            "testing_task": {
                "key": "TASK-103",
                "summary": "Testing task",
                "requiredSkills": [
                    {"name": "Testing", "minLevel": 4}
                ],
                "storyPoints": 5
            }
        }
    
    def test_calculate_skill_fit_perfect_match(self):
        """Test skill fit calculation with perfect skill match"""
        user_skills = [{"name": "React", "level": 4}]
        required_skills = [{"name": "React", "minLevel": 3}]
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 1.0)
    
    def test_calculate_skill_fit_exact_match(self):
        """Test skill fit calculation with exact skill level match"""
        user_skills = [{"name": "React", "level": 3}]
        required_skills = [{"name": "React", "minLevel": 3}]
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 1.0)
    
    def test_calculate_skill_fit_partial_match(self):
        """Test skill fit calculation with partial skill match"""
        user_skills = [{"name": "React", "level": 2}]
        required_skills = [{"name": "React", "minLevel": 4}]
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 0.5)  # 2/4 = 0.5
    
    def test_calculate_skill_fit_missing_skill(self):
        """Test skill fit calculation with missing required skill"""
        user_skills = [{"name": "Python", "level": 5}]
        required_skills = [{"name": "React", "minLevel": 3}]
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 0.0)
    
    def test_calculate_skill_fit_multiple_skills(self):
        """Test skill fit calculation with multiple skills"""
        user_skills = [
            {"name": "React", "level": 4},
            {"name": "JavaScript", "level": 5}
        ]
        required_skills = [
            {"name": "React", "minLevel": 3},
            {"name": "JavaScript", "minLevel": 4}
        ]
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 1.0)  # Both skills exceed requirements
    
    def test_calculate_skill_fit_no_requirements(self):
        """Test skill fit calculation with no skill requirements"""
        user_skills = [{"name": "React", "level": 4}]
        required_skills = []
        
        skill_fit = self.engine.calculate_skill_fit(user_skills, required_skills)
        
        self.assertEqual(skill_fit, 1.0)
    
    def test_calculate_capacity_factor_low_load(self):
        """Test capacity factor calculation with low current load"""
        capacity_factor = self.engine.calculate_capacity_factor(10, 40)
        
        self.assertEqual(capacity_factor, 0.75)  # 1 - (10/40) = 0.75
    
    def test_calculate_capacity_factor_high_load(self):
        """Test capacity factor calculation with high current load"""
        capacity_factor = self.engine.calculate_capacity_factor(35, 40)
        
        self.assertEqual(capacity_factor, 0.125)  # 1 - (35/40) = 0.125
    
    def test_calculate_capacity_factor_at_capacity(self):
        """Test capacity factor calculation at full capacity"""
        capacity_factor = self.engine.calculate_capacity_factor(40, 40)
        
        self.assertEqual(capacity_factor, 0.0)
    
    def test_calculate_capacity_factor_over_capacity(self):
        """Test capacity factor calculation over capacity"""
        capacity_factor = self.engine.calculate_capacity_factor(50, 40)
        
        self.assertEqual(capacity_factor, 0.0)  # Should not go negative
    
    def test_calculate_score_high_skill_low_load(self):
        """Test score calculation for user with high skills and low load"""
        user = self.sample_users[0]  # Stacey - React expert, 60% capacity
        task = self.sample_tasks["react_task"]
        
        score = self.engine.calculate_score(user, task)
        
        # Should be high score due to perfect skill match and reasonable capacity
        self.assertGreater(score, 0.8)
    
    def test_calculate_score_perfect_skill_high_load(self):
        """Test score calculation for user with perfect skills but high load"""
        user = self.sample_users[1]  # Maya - Python expert, 80% capacity
        task = self.sample_tasks["python_task"]
        
        score = self.engine.calculate_score(user, task)
        
        # Should be good score but reduced due to high capacity usage
        self.assertGreater(score, 0.7)
        self.assertLess(score, 0.9)
    
    def test_check_hard_constraints_success(self):
        """Test hard constraints check with valid user"""
        user = self.sample_users[0]  # Stacey
        task = self.sample_tasks["react_task"]
        
        meets_constraints, message = self.engine.check_hard_constraints(user, task)
        
        self.assertTrue(meets_constraints)
        self.assertEqual(message, "All constraints met")
    
    def test_check_hard_constraints_missing_skill(self):
        """Test hard constraints check with missing required skill"""
        user = self.sample_users[0]  # Stacey (no Python skills)
        task = self.sample_tasks["python_task"]
        
        meets_constraints, message = self.engine.check_hard_constraints(user, task)
        
        self.assertFalse(meets_constraints)
        self.assertIn("Missing required skill: Python", message)
    
    def test_check_hard_constraints_insufficient_skill_level(self):
        """Test hard constraints check with insufficient skill level"""
        user = self.sample_users[2]  # Supraja (React level 3)
        task = {
            "requiredSkills": [{"name": "React", "minLevel": 4}]
        }
        
        meets_constraints, message = self.engine.check_hard_constraints(user, task)
        
        self.assertFalse(meets_constraints)
        self.assertIn("Missing required skill: React", message)
    
    def test_check_hard_constraints_at_capacity_limit(self):
        """Test hard constraints check with user at capacity limit"""
        user = {
            "skills": [{"name": "React", "level": 5}],
            "capacity": {"pointsPerSprint": 40, "currentLoad": 36}  # 90% capacity
        }
        task = self.sample_tasks["react_task"]
        
        meets_constraints, message = self.engine.check_hard_constraints(user, task)
        
        self.assertFalse(meets_constraints)
        self.assertIn("capacity limit", message)
    
    def test_generate_recommendations_react_task(self):
        """Test recommendation generation for React task"""
        task = self.sample_tasks["react_task"]
        
        recommendations = self.engine.generate_recommendations(self.sample_users, task)
        
        # Should return 3 recommendations
        self.assertEqual(len(recommendations), 3)
        
        # Stacey should be top recommendation (React expert)
        top_recommendation = recommendations[0]
        self.assertEqual(top_recommendation["user"]["username"], "stacey.johnson")
        self.assertGreater(top_recommendation["score"], 0.8)
        self.assertFalse(top_recommendation.get("excluded", False))
    
    def test_generate_recommendations_python_task(self):
        """Test recommendation generation for Python task"""
        task = self.sample_tasks["python_task"]
        
        recommendations = self.engine.generate_recommendations(self.sample_users, task)
        
        # Maya should be top recommendation (Python expert)
        top_recommendation = recommendations[0]
        self.assertEqual(top_recommendation["user"]["username"], "maya.patel")
        self.assertGreater(top_recommendation["score"], 0.7)
    
    def test_generate_recommendations_testing_task(self):
        """Test recommendation generation for Testing task"""
        task = self.sample_tasks["testing_task"]
        
        recommendations = self.engine.generate_recommendations(self.sample_users, task)
        
        # Supraja should be top recommendation (Testing expert)
        top_recommendation = recommendations[0]
        self.assertEqual(top_recommendation["user"]["username"], "supraja.reddy")
        self.assertGreater(top_recommendation["score"], 0.8)
    
    def test_generate_recommendations_with_exclusions(self):
        """Test recommendation generation with users excluded by constraints"""
        # Create task requiring very high skill level
        difficult_task = {
            "requiredSkills": [{"name": "React", "minLevel": 6}]  # Higher than any user
        }
        
        recommendations = self.engine.generate_recommendations(self.sample_users, difficult_task)
        
        # All users should be excluded due to insufficient skill level
        for rec in recommendations:
            self.assertTrue(rec.get("excluded", False))
            self.assertEqual(rec["score"], 0.0)
    
    def test_generate_recommendations_max_limit(self):
        """Test recommendation generation with custom max limit"""
        task = self.sample_tasks["react_task"]
        
        recommendations = self.engine.generate_recommendations(self.sample_users, task, max_recommendations=2)
        
        # Should return only 2 recommendations
        self.assertEqual(len(recommendations), 2)
    
    def test_recommendation_scoring_consistency(self):
        """Test that recommendation scoring is consistent and deterministic"""
        task = self.sample_tasks["react_task"]
        
        # Generate recommendations multiple times
        recommendations1 = self.engine.generate_recommendations(self.sample_users, task)
        recommendations2 = self.engine.generate_recommendations(self.sample_users, task)
        
        # Results should be identical
        self.assertEqual(len(recommendations1), len(recommendations2))
        
        for i in range(len(recommendations1)):
            self.assertEqual(
                recommendations1[i]["user"]["username"],
                recommendations2[i]["user"]["username"]
            )
            self.assertEqual(
                recommendations1[i]["score"],
                recommendations2[i]["score"]
            )


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecommendationEngine))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
