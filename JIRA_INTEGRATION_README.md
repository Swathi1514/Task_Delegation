# TaskFlow JIRA Integration Architecture

## Overview

TaskFlow now supports both **Real JIRA** integration and **Mock JIRA** for testing. The application can seamlessly switch between these modes based on configuration.

## Architecture Components

### 1. Real JIRA API (`src/api/jira_api.py`)
- **Purpose**: Production integration with actual JIRA instances
- **Features**:
  - OAuth 2.0 authentication with JIRA
  - Read tasks from current sprint
  - Fetch team member profiles
  - Assign tasks to users
  - Calculate workload and capacity
- **Dependencies**: `jira` Python library
- **Configuration**: `config/jira_config.json`

### 2. Mock JIRA API (`src/api/mock_jira_api.py`)
- **Purpose**: Testing and development without JIRA dependency
- **Features**:
  - Simulates all JIRA API functionality
  - Uses local JSON data files
  - Perfect for unit testing and demos
  - No external dependencies
- **Data Sources**: `src/data/mock_jira_*.json`

### 3. Unified API Service (`src/api/api_service.py`)
- **Purpose**: Provides a single interface that can switch between real and mock
- **Features**:
  - Automatic fallback from real to mock if connection fails
  - Consistent API interface regardless of backend
  - Web API wrapper for HTTP-like requests
  - Configuration-driven mode selection

## Usage

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For real JIRA integration only
pip install jira>=3.4.0
```

### Configuration

#### Real JIRA Setup
1. Create API token at: https://id.atlassian.com/manage-profile/security/api-tokens
2. Update `config/jira_config.json`:
```json
{
  "server": "https://your-domain.atlassian.net",
  "email": "your-email@company.com", 
  "api_token": "your-api-token",
  "project_key": "YOUR_PROJECT"
}
```

#### Environment Variables (Alternative)
```bash
export JIRA_SERVER="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT_KEY="YOUR_PROJECT"
```

### Running the Application

#### Production Mode (Real JIRA)
```bash
# Start web application
npm start

# Start API service with real JIRA
npm run start:api

# Or directly
cd src/api && python3 api_service.py
```

#### Development/Testing Mode (Mock JIRA)
```bash
# Start web application
npm start

# Start mock API service
npm run start:api:mock

# Or directly
cd src/api && python3 mock_jira_api.py
```

#### Testing
```bash
# Run all tests (uses mock JIRA)
npm test

# Run mock JIRA tests specifically
npm run test:mock

# Or directly
cd tests && python3 -m pytest test_mock_jira.py -v
```

### Web Interface

#### Access with Real JIRA
```
http://localhost:8000?api=real
```

#### Access with Mock JIRA (Default)
```
http://localhost:8000
```

The web interface includes a toggle button to switch between Real and Mock JIRA modes dynamically.

## API Endpoints

### Unified API Service Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/info` | GET | Get API configuration info |
| `/api/users` | GET | Get all team members |
| `/api/users/{username}` | GET | Get specific user |
| `/api/tasks` | GET | Get tasks (with optional filters) |
| `/api/tasks/unassigned` | GET | Get unassigned tasks |
| `/api/assign` | POST | Assign task to user |
| `/api/workload` | GET | Get user workload |
| `/api/capacity` | GET | Get team capacity overview |

### Example API Usage

```python
from api_service import TaskFlowWebAPI

# Initialize with real JIRA
api = TaskFlowWebAPI(use_real_jira=True)

# Get unassigned tasks
response = api.handle_request('/api/tasks/unassigned')
print(response['data'])  # List of unassigned tasks

# Assign a task
response = api.handle_request('/api/assign', 'POST', {
    'task_key': 'SCRUM-123',
    'assignee': 'john.doe'
})
print(response['message'])  # Assignment result
```

## File Structure

```
Task_Delegation/
├── src/
│   ├── api/
│   │   ├── jira_api.py          # Real JIRA integration
│   │   ├── mock_jira_api.py     # Mock JIRA for testing
│   │   └── api_service.py       # Unified API service
│   ├── data/
│   │   ├── mock_jira_users.json # Mock user data
│   │   └── mock_jira_tasks.json # Mock task data
│   └── web/
│       ├── integration.js       # Updated frontend integration
│       └── index.html          # Web interface
├── config/
│   └── jira_config.json        # JIRA configuration
├── tests/
│   └── test_mock_jira.py       # Mock JIRA tests
├── requirements.txt            # Python dependencies
└── package.json               # Updated npm scripts
```

## Development Workflow

### 1. Development Phase
- Use Mock JIRA for rapid development
- No external dependencies required
- Fast iteration and testing

### 2. Testing Phase
- Run comprehensive tests with Mock JIRA
- Validate all functionality works correctly
- Test edge cases and error handling

### 3. Integration Phase
- Configure Real JIRA credentials
- Test with actual JIRA instance
- Validate data mapping and field configurations

### 4. Production Phase
- Deploy with Real JIRA configuration
- Monitor API calls and performance
- Fallback to Mock JIRA if needed for demos

## Key Benefits

1. **Flexibility**: Switch between real and mock without code changes
2. **Testing**: Comprehensive testing without external dependencies
3. **Development**: Fast development cycle with mock data
4. **Reliability**: Automatic fallback if real JIRA is unavailable
5. **Consistency**: Same API interface regardless of backend

## Troubleshooting

### Real JIRA Connection Issues
- Verify API token is valid and not expired
- Check JIRA server URL and project key
- Ensure user has proper permissions
- Review firewall and network settings

### Mock JIRA Issues
- Verify JSON data files exist and are valid
- Check file permissions
- Ensure Python path includes src/api directory

### General Issues
- Check Python dependencies are installed
- Verify configuration files are properly formatted
- Review console logs for detailed error messages

## Future Enhancements

1. **Skills Management**: Integration with HR systems for skill data
2. **Capacity Planning**: Integration with Tempo or similar tools
3. **Advanced Filtering**: More sophisticated task filtering options
4. **Real-time Updates**: WebSocket support for live updates
5. **Multi-Project**: Support for multiple JIRA projects
6. **Custom Fields**: Configurable custom field mapping
