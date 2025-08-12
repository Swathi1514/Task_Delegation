#!/usr/bin/env python3
"""
JIRA Discovery Script
Helps discover available projects and configuration in your JIRA instance
"""

from jira import JIRA
import json
import os

def load_config():
    """Load JIRA configuration"""
    config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'jira_config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    
    return {
        "server": "https://swathi1514.atlassian.net",
        "email": "swathi1514@gmail.com",
        "api_token": "ATATT3xFfGF0kf81vZuO6E7oB3wit6Dx0t2042lPdGi1-injn_dOw-AE_txDe7_uKSP6RaOK02-6feF-s1a2_542EIAB8oSoRLDRPVy6B8y4AN5Jlh2qAnOVL9E3VkVYYCMFh9poxrnHHGySGePc9NgBHkMx3tgrwEIoP0AxXnvo7FldWwz7QrA=60675AEB"
    }

def main():
    print("🔍 JIRA Discovery Tool")
    print("=" * 50)
    
    config = load_config()
    
    try:
        # Connect to JIRA
        jira = JIRA(
            server=config['server'],
            basic_auth=(config['email'], config['api_token'])
        )
        print(f"✅ Connected to JIRA: {config['server']}")
        
        # Get current user info
        print(f"\n👤 Current User: {jira.current_user()}")
        
        # List all projects
        print("\n📋 Available Projects:")
        projects = jira.projects()
        
        if not projects:
            print("  No projects found or no access to projects")
        else:
            for project in projects:
                print(f"  • {project.key}: {project.name}")
                print(f"    Description: {getattr(project, 'description', 'No description')}")
                print(f"    Lead: {getattr(project, 'lead', 'Unknown')}")
                print()
        
        # If we have projects, let's explore the first one
        if projects:
            first_project = projects[0]
            print(f"\n🔍 Exploring Project: {first_project.key}")
            
            # Get issues from the project
            try:
                issues = jira.search_issues(f'project = "{first_project.key}"', maxResults=5)
                print(f"  Found {len(issues)} issues (showing first 5):")
                
                for issue in issues:
                    print(f"    • {issue.key}: {issue.fields.summary}")
                    print(f"      Status: {issue.fields.status.name}")
                    print(f"      Type: {issue.fields.issuetype.name}")
                    if issue.fields.assignee:
                        print(f"      Assignee: {issue.fields.assignee.displayName}")
                    else:
                        print(f"      Assignee: Unassigned")
                    print()
                
            except Exception as e:
                print(f"  ❌ Error fetching issues: {e}")
            
            # Get project users
            try:
                assignable_users = jira.search_assignable_users_for_projects('', [first_project.key])
                print(f"  👥 Assignable Users ({len(assignable_users)}):")
                for user in assignable_users[:5]:  # Show first 5
                    print(f"    • {user.displayName} ({user.name})")
                    if hasattr(user, 'emailAddress'):
                        print(f"      Email: {user.emailAddress}")
                    print()
                
            except Exception as e:
                print(f"  ❌ Error fetching users: {e}")
        
        # Suggest configuration
        if projects:
            suggested_project = projects[0].key
            print(f"\n💡 Suggested Configuration:")
            print(f"Update config/jira_config.json with:")
            print(json.dumps({
                "server": config['server'],
                "email": config['email'],
                "api_token": "YOUR_API_TOKEN",
                "project_key": suggested_project
            }, indent=2))
        
    except Exception as e:
        print(f"❌ Failed to connect to JIRA: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API token is valid")
        print("2. Verify the server URL is correct")
        print("3. Ensure your account has proper permissions")
        print("4. Check if your IP is allowed (if IP restrictions are enabled)")

if __name__ == "__main__":
    main()
