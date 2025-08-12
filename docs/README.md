# TaskFlow

AI-powered task assignment system that recommends the best assignee for each task using skills, availability, workload, priority, and deadlines.

## Problem & Goals

**Problem:** Managers and leads spend time deciding "who should do what," often without complete visibility into skills, workload, or deadlines.

**Goal:** Recommend the best assignee (and backups) for each task using skills, availability, workload, priority, and deadlines — with explainable reasoning and a human-in-the-loop final decision.

## Scope

### MVP (In Scope)
- Read task details from Jira for the current sprint only (title, description, story points, priority, due date, labels, status)
- Pull team member data (skills, capacity, availability)
- Generate top-3 assignee recommendations per task within the current sprint scope
- Show an explanation (why these people)
- Update assignment on confirmation and log a rationale
- Notify via Slack/Teams

### Out of Scope (MVP)
- Automatic auto-assign without approval
- Multi-project optimization across departments
- People cost modeling

### Next Phase
- Multi-sprint optimization
- Vacation/roster sync
- Learning-to-rank from feedback
- Cross-tool orchestration

## Stakeholders & Users

### Primary Users
- Team leads
- Project managers
- Scrum masters

### Secondary Users
- Engineers/analysts (receive assignments)
- HR/L&D (skills data)
- Executives (capacity reports)

### Systems Integration
- Jira/Azure DevOps
- Slack/Teams
- Calendar
- HRIS/LMS (skills)
- SSO/IdP

## Key Assumptions

- **Tasks have:** title, description, story points/effort, priority, due date, required skills (explicit or inferred via NLP)
- **Team members have:** skills (tagged), proficiency level, current workload/capacity, time zone, availability
- **Manager approves final assignment**

## Success Metrics

- Time to assign tasks down 50% (MVP target)
- Reassignment rate (due to overload/skill mismatch) down 25%
- Lead satisfaction >= 4/5
- SLA breach rate for tasks with recommendations down vs baseline

## User Stories (MVP)

1. **As a team lead**, I can view unassigned tasks with AI-suggested assignees and explanations, so I can approve quickly
2. **As a team lead**, I can filter recommendations by project, skill, priority, due date
3. **As a team lead**, I can override the suggestion and provide feedback ("too busy", "missing skill"), so the model learns
4. **As an engineer**, I receive a Slack/Teams message when a task is assigned to me, with context and due date
5. **As a manager**, I can see a capacity heatmap and current load distribution
6. **As an auditor**, I can view an assignment decision log and reasoning for compliance

## Functional Requirements

### FR-1: Integrations
- **FR-1.1:** Connect to Jira via OAuth; read tasks (status, priority, due date, labels, story points) and write assignee updates
- **FR-1.2:** HRIS/LMS import of skills & proficiency (CSV/API)
- **FR-1.3:** Calendar (Google/Microsoft) free/busy + OOO; optional
- **FR-1.4:** Slack/Teams webhooks for notifications

### FR-2: Data & Profiles
- **FR-2.1:** Maintain Member Profile: id, role, skills[], proficiency (1-5), timezone, capacity per sprint (points/hours), current workload, historical performance (optional, anonymized), preferred work types
- **FR-2.2:** Maintain Task Profile: id, project, required_skills[], difficulty/effort, priority, due date, tags, dependencies, requester, historical context

### FR-3: Recommendation Engine
- **FR-3.1:** For any task, compute a ranked list of candidates with score and explanation
- **FR-3.2:** Consider constraints: availability, hard skills, capacity (won't exceed threshold), conflict of interest (optional), time zone overlap (if needed)
- **FR-3.3:** Provide 1 primary + 2 backups
- **FR-3.4:** Display why (skill match %, remaining capacity, past similar tasks)
- **FR-3.5:** Allow manager to approve/override and push assignment to Jira

### FR-4: Learning & Feedback
- **FR-4.1:** Capture feedback on each recommendation (👍/👎 + reason)
- **FR-4.2:** Adjust future scores via simple weighting (MVP), with option to upgrade to learning-to-rank later

### FR-5: Reporting
- **FR-5.1:** Capacity heatmap by person/sprint
- **FR-5.2:** Workload balance (Gini coefficient or simple variance)
- **FR-5.3:** Reassignment and SLA metrics

## Non-Functional Requirements

- **Security:** SSO (SAML/OIDC), role-based access, encrypted at rest/in transit
- **Privacy:** No sensitive attributes (e.g., age, gender) used in scoring
- **Reliability:** 99.5% uptime (hackathon MVP: best effort)
- **Latency:** Recommendation <= 2s for a team of up to 100 users
- **Auditability:** Decision logs retained >= 12 months
- **Explainability:** Human-readable reasons for ranking

## Recommendation Logic (MVP)

### Scoring Inputs per Candidate
- **Skill fit (0-1):** cosine similarity between task required_skills and member skills (with proficiency weighting)
- **Load factor (0-1):** 1 - (current_load / capacity), clipped to [0,1]
- **Deadline pressure (0-1):** prefers candidates with near-term availability windows
- **Historical affinity (0-1):** success rate on similar tasks (optional)
- **Time zone overlap (0-1):** if collaboration windows matter

### Score Formula (Configurable Weights)
```
Score = 0.45*SkillFit + 0.30*LoadFactor + 0.15*DeadlineWindow + 0.05*HistoricalAffinity + 0.05*TimezoneOverlap
```

### Hard Constraints
- Must have all mandatory skills
- Must not exceed capacity threshold (e.g., 90%)
- Must be available before due date

### Optimization (Stretch)
Use a simple assignment optimization (Hungarian method / ILP) per sprint to minimize total lateness and load imbalance.

## Data Model

```javascript
Member {
  id, name, email, role, timezone,
  skills: [{name, level}],
  capacity_points, current_points,
  ooo_periods: []
}

Task {
  id, title, project, priority, due_date, story_points,
  required_skills: [{name, min_level}],
  labels: [], status
}

RecommendationLog {
  id, task_id,
  candidates: [{member_id, score, factors}],
  selected_member_id, approver_id, timestamp, feedback
}
```

## API Endpoints

- `POST /recommendations` - body `{ taskId }` returns ranked candidates with explanations
- `POST /assign` - body `{ taskId, memberId }` writes to Jira and logs decision
- `GET /capacity?project=ABC&sprint=12` returns capacity/load summary
- `POST /feedback` - body `{ taskId, accepted: boolean, reason?: string }`

## UI Requirements

- **Task List** with "Get Recommendation" button and chips showing top-3 with scores
- **Explainability Drawer:** for the top suggestion, show: skill match %, current load, calendar constraints, similar past tasks
- **Override & Assign** button; Notify assignee toggle
- **Capacity Heatmap** view (people × days/sprint, colored by load)
- **Filters:** project, role, skill, priority, due window

## Governance, Ethics, & Compliance

- Exclude protected attributes from model inputs
- Provide reason codes ("High skill match in X; Lowest current load; Available before DD/MM")
- Maintain appeal path: overrides and feedback update the model weights
- Log every decision for audit (who/what/why/when)

## Constraints & Edge Cases

- **Missing skill tags** - fall back to NLP keyword extraction from task description
- **Everyone at capacity** - suggest splitting the task or renegotiating the due date
- **Conflicting vacations/OOO** - exclude those members; show why excluded
- **Tasks with no mandatory skills** - rank primarily by load and historical affinity
- **Sudden priority changes** - re-run recommendations for impacted tasks

## Acceptance Criteria (MVP)

- Given a Jira task with required skills and due date, when I click "Recommend," I see 3 candidates with scores and clear explanations
- Approving an assignee updates Jira in <= 2s and posts a Slack/Teams message
- Capacity heatmap correctly reflects Jira story points across the active sprint
- Decision log shows inputs, scores, final choice, and approver

## Test Cases

- **TC-01:** Task requires React:3; candidate A has React:4 and 50% load - A ranks #1
- **TC-02:** All candidates >90% capacity - system flags overload and suggests backup plan
- **TC-03:** Candidate with perfect skill but OOO during due window - excluded with reason
- **TC-04:** Override flow: manager picks #3, submits "#1 lacks domain context" - feedback stored
- **TC-05:** Jira write succeeds and Slack message delivered to selected engineer

## MVP Build Plan

### Sprint 1
- Jira read integration
- Simple scoring engine
- UI table with recommendations + explanations
- Manual assign functionality
- Basic decision logs

### Sprint 2
- Slack/Teams notifications
- Capacity heatmap
- Feedback loop
- Admin interface for weights
- Calendar integration

## Future Enhancements

- Learning-to-rank model using historical acceptance/win rates
- Multi-objective optimization: minimize lateness + balance load + maximize skill growth
- Personalization: "stretch tasks" to upskill juniors within safe load bounds
- Scenario planner: "what if we move deadline/add person?"

---

*Ready to turn this into a Jira-ready backlog or create wireframes for the main screens.*
