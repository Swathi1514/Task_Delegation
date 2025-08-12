# TaskFlow Project Structure

## 📁 Organized Directory Layout

```
TaskFlow/
├── README.md                    # Main project overview
├── package.json                 # Project configuration & scripts
├── STRUCTURE.md                 # This file - project structure guide
├── 
├── 📚 docs/                     # Documentation
│   ├── README.md               # Detailed project documentation
│   ├── TECHNICAL_SPEC.md       # Technical specifications
│   ├── INTEGRATION_GUIDE.md    # Integration guide
│   ├── MOCK_JIRA_SETUP.md     # Mock JIRA setup guide
│   ├── Jira_Tasks.md           # Additional task examples
│   └── UI_SPEC.md              # UI requirements
├── 
├── 💻 src/                      # Source code
│   ├── 🌐 web/                 # Web application
│   │   ├── index.html          # Main UI
│   │   ├── styles.css          # UI styles
│   │   ├── script.js           # UI functionality
│   │   ├── integration.js      # Mock data integration
│   │   └── integration.css     # Integration styles
│   ├── 
│   ├── 🔌 api/                 # API layer
│   │   └── mock_jira_api.py    # Mock JIRA API simulator
│   └── 
│   └── 📊 data/                # Data files
│       ├── mock_jira_users.json    # User profiles
│       └── mock_jira_tasks.json    # Task definitions
├── 
└── ⚙️ config/                   # Configuration files
    └── (future config files)
```

## 🎯 Directory Purposes

### 📚 `/docs/` - Documentation
- **Purpose**: All project documentation and guides
- **Contents**: Technical specs, integration guides, setup instructions
- **Usage**: Reference materials for developers and users

### 💻 `/src/` - Source Code
- **Purpose**: All application source code
- **Structure**: Organized by component type (web, api, data)

#### 🌐 `/src/web/` - Web Application
- **Purpose**: Frontend web interface
- **Contents**: HTML, CSS, JavaScript files
- **Usage**: Serve with HTTP server for the TaskFlow UI

#### 🔌 `/src/api/` - API Layer
- **Purpose**: Backend API and simulation code
- **Contents**: Python API simulators and future backend code
- **Usage**: Run Python scripts for API functionality

#### 📊 `/src/data/` - Data Files
- **Purpose**: Mock data and configuration files
- **Contents**: JSON files with user profiles and task definitions
- **Usage**: Data source for testing and development

### ⚙️ `/config/` - Configuration
- **Purpose**: Application configuration files
- **Contents**: Future config files for different environments
- **Usage**: Environment-specific settings

## 🚀 Quick Commands

### Start Web Application
```bash
# Method 1: Using npm script
npm start

# Method 2: Direct command
cd src/web && python3 -m http.server 8000
```

### Run API Demo
```bash
# Method 1: Using npm script
npm run start:api

# Method 2: Direct command
cd src/api && python3 mock_jira_api.py
```

### Development Server
```bash
npm run dev  # Starts on port 3000
```

### Serve Documentation
```bash
npm run docs  # Serves docs on port 8080
```

## 📋 File Relationships

```
Web App (src/web/) 
    ↓ loads data from
Data Files (src/data/)
    ↓ also used by
API Simulator (src/api/)
    ↓ documented in
Documentation (docs/)
```

## 🔄 Migration Benefits

### ✅ **Better Organization**
- Clear separation of concerns
- Logical grouping of related files
- Easier navigation and maintenance

### ✅ **Scalability**
- Room for growth in each category
- Easy to add new components
- Professional project structure

### ✅ **Development Workflow**
- Clear entry points for different tasks
- Standardized npm scripts
- Consistent file paths

### ✅ **Collaboration**
- Easy for new developers to understand
- Clear ownership of different areas
- Standard project conventions

## 🛠️ Development Guidelines

### Adding New Files
- **Web components**: Add to `src/web/`
- **API endpoints**: Add to `src/api/`
- **Data files**: Add to `src/data/`
- **Documentation**: Add to `docs/`
- **Configuration**: Add to `config/`

### File Naming Conventions
- **HTML/CSS/JS**: lowercase with hyphens (e.g., `task-list.js`)
- **Python**: lowercase with underscores (e.g., `task_manager.py`)
- **JSON**: lowercase with underscores (e.g., `user_profiles.json`)
- **Docs**: UPPERCASE for main docs (e.g., `README.md`)

### Path References
- **From web to data**: `../data/filename.json`
- **From api to data**: `../data/filename.json`
- **From root to any**: `src/component/filename`

---

**This organized structure makes TaskFlow more professional, maintainable, and scalable!** 🎉
