# TaskFlow - AI-Powered Task Assignment System

AI-powered task assignment system that recommends the best assignee for each task using skills, availability, workload, priority, and deadlines.

## 🚀 Quick Start

### Run the Web Application
```bash
cd src/web
python3 -m http.server 8000
```
Visit: **http://localhost:8000**

### Run the Mock JIRA API Demo
```bash
cd src/api
python3 mock_jira_api.py
```

## 📁 Project Structure

```
TaskFlow/
├── README.md                    # This file
├── package.json                 # Project configuration
├── 
├── docs/                        # Documentation
│   ├── README.md               # Detailed project documentation
│   ├── TECHNICAL_SPEC.md       # Technical specifications
│   ├── INTEGRATION_GUIDE.md    # Integration guide
│   ├── MOCK_JIRA_SETUP.md     # Mock JIRA setup guide
│   ├── Jira_Tasks.md           # Additional task examples
│   └── UI_SPEC.md              # UI requirements
├── 
├── src/                         # Source code
│   ├── web/                    # Web application
│   │   ├── index.html          # Main UI
│   │   ├── styles.css          # UI styles
│   │   ├── script.js           # UI functionality
│   │   ├── integration.js      # Mock data integration
│   │   └── integration.css     # Integration styles
│   ├── 
│   ├── api/                    # API layer
│   │   └── mock_jira_api.py    # Mock JIRA API simulator
│   └── 
│   └── data/                   # Data files
│       ├── mock_jira_users.json    # User profiles
│       └── mock_jira_tasks.json    # Task definitions
├── 
└── config/                     # Configuration files
    └── (future config files)
```

## 🎯 Features

- **Smart AI Recommendations** - Skill-based task assignment
- **Real-time Capacity Management** - Team workload visualization
- **Interactive Dashboard** - Professional web interface
- **Mock JIRA Integration** - No JIRA access required for testing
- **Explainable AI** - Clear reasoning for recommendations

## 👥 Demo Users

- **Stacey** - Frontend Specialist (React, JavaScript, UI/UX)
- **Maya** - Senior Backend Developer (Python, Django, AWS)
- **Supraja** - Full Stack Developer & QA Engineer (Java, Testing, React)

## 📋 Demo Tasks

- **TASK-101** - User Authentication UI (suits Stacey)
- **TASK-102** - Recommendation API (suits Maya)
- **TASK-103** - Testing Framework (suits Supraja)
- **TASK-104** - Database Schema (suits Maya)
- **TASK-105** - Capacity Dashboard (suits Stacey)

## 📚 Documentation

For detailed documentation, see the `docs/` directory:
- [Technical Specifications](docs/TECHNICAL_SPEC.md)
- [Integration Guide](docs/INTEGRATION_GUIDE.md)
- [Mock JIRA Setup](docs/MOCK_JIRA_SETUP.md)

## 🛠️ Development

### Prerequisites
- Python 3.7+
- Modern web browser
- Basic HTTP server (built into Python)

### Local Development
1. Clone the repository
2. Navigate to `src/web/`
3. Start HTTP server: `python3 -m http.server 8000`
4. Open browser to `http://localhost:8000`

## 🎮 Try It Out

1. **Get Recommendations**: Click "Get Recommendation" on any task
2. **Assign Tasks**: Click "Assign" on recommended candidates
3. **View Capacity**: Switch to "Capacity Heatmap" tab
4. **Test API**: Run the Python demo in `src/api/`

---

**Ready to revolutionize task assignment with AI!** 🚀
