# DevPath Practicum — Software Engineering Internships Platform

> "Help students gain real software engineering experience through structured, practical internship projects."

A complete, production-ready Streamlit website for an engineering organization that provides practical learning opportunities and structured project internships to university students.

---

## 1. Project Purpose

DevPath bridges the gap between academic computer science theory and production-grade software engineering. Interns build practical, tangible applications, practice Git branching and test-driven validation, and graduate with a portfolio of code they can confidently discuss in technical interviews.

---

## 2. Key Features

- **Multi-Page Experience**: Discrete, focused pages for **Home**, **Internships**, **How It Works**, **Projects & Skills**, **About**, and **Apply**.
- **Centralized Data Architecture**: All internship offerings, technology stacks, project areas, and skill sets live in `data.py`. The UI dynamically adapts without needing template modifications.
- **Interactive Role Discovery**: Filter opportunities by category, skill level, and keywords. View complete deliverables, requirements, and responsibilities.
- **AI-Powered Internship Fit Assistant**: Uses Google Gemini to analyze student skills and interests, providing informational guidance on suitable tracks with an automatic rule-based fallback when offline.
- **Structured Application Pipeline**: Validates student applications, records submissions with unique tracking receipts, and provides clear backend webhook configuration hooks.
- **Production Aesthetic**: Modern software engineering visual language using restrained neutrals, crisp typography, clean cards, and responsive layouts.

---

## 3. Project Structure

The project strictly follows a 5-file Python architecture with a strict one-way dependency chain:

```
project/
│
├── app.py              # Main Streamlit entry point, page router, session state
├── ui.py               # Reusable UI components & page renderers
├── services.py         # Business logic, Gemini AI client, application dispatch
├── data.py             # Single source of truth for internships, skills, and copy
├── utils.py            # Standalone helpers (formatting, validation, sanitization)
├── requirements.txt    # Minimal dependency manifest
├── README.md           # Documentation and extension guide
└── .gitignore          # Repository hygiene and secret prevention
```

### Dependency Direction

```
app.py → ui.py → services.py → data.py
utils.py (standalone helper module imported without circular dependencies)
```

No module imports higher up the hierarchy, preventing circular dependencies.

---

## 4. Installation & Local Run

### Prerequisites
- Python 3.9+ installed
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/internship-platform.git
cd internship-platform
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
The app will launch in your default browser at `http://localhost:8501`.

---

## 5. Secrets & Configuration

The application runs out-of-the-box without requiring any API keys or external services.

### Optional: Gemini AI Configuration
To enable the live Gemini AI model in the **Internship Fit Assistant**:

1. Create a local `.streamlit/secrets.toml` file:
```toml
# .streamlit/secrets.toml (DO NOT commit this file to Git)
GEMINI_API_KEY = "your-google-gemini-api-key"

# Or nested format:
[gemini]
api_key = "your-google-gemini-api-key"
```
Alternatively, set an environment variable:
```bash
export GEMINI_API_KEY="your-google-gemini-api-key"
```

*Note: If no API key is provided, the platform automatically falls back to an intelligent, rule-based recommendation engine.*

### Optional: External Application Webhook
To forward candidate submissions to a CRM, Slack channel, or database endpoint:
```toml
SUBMISSION_WEBHOOK_URL = "https://api.yourorganization.com/internship-admissions"
```

---

## 6. Streamlit Cloud Deployment

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account.
3. Select your repository, specify branch `main`, and set main file path to `app.py`.
4. In **Advanced Settings > Secrets**, add your optional secrets:
   ```toml
   GEMINI_API_KEY = "YOUR_GEMINI_KEY"
   ```
5. Click **Deploy**. The app builds cleanly with `requirements.txt`.

---

## 7. How to Extend Centralized Data

No UI code needs to be modified when updating content. All modifications occur in `data.py`.

### How to Add a New Internship
Add a new dictionary item to `INTERNSHIPS` in `data.py`:

```python
{
    "id": "cloud-infrastructure-intern",
    "title": "Cloud Infrastructure & DevOps Intern",
    "category": "Software Development",
    "description": "Construct automated CI/CD deployment pipelines and containerize microservices.",
    "duration": "8 weeks",
    "mode": "Remote",
    "level": "Intermediate",
    "technologies": ["Docker", "GitHub Actions", "Linux", "Python"],
    "status": "Open",
    "overview": "Learn how modern software teams deploy and monitor reliable production systems.",
    "responsibilities": [
        "Write Dockerfiles for microservices",
        "Build GitHub Actions CI/CD workflows",
        "Configure automated linting and security scanners"
    ],
    "requirements": [
        "Basic familiarity with Linux command line and Git",
        "Understanding of client-server network basics"
    ],
    "skills": ["Docker", "CI/CD", "Git", "Testing", "Documentation"],
    "deliverables": [
        "Reproducible multi-container Docker Compose environment",
        "Automated deployment pipeline running unit and linting checks"
    ]
}
```
The **Internships** grid, filter dropdowns, search bar, and detail views will update automatically.

### How to Add a New Project Area
Append a new entry to `PROJECT_AREAS` in `data.py`:
```python
{
    "title": "Mobile Systems",
    "description": "Develop performant client applications for mobile platforms.",
    "details": "Build responsive cross-platform views and offline-first data caching."
}
```

### How to Add a New Skill
Append the skill name to `AVAILABLE_SKILLS` in `data.py`:
```python
AVAILABLE_SKILLS.append("Docker")
```

---

## 8. License

Licensed under the Apache 2.0 License.
