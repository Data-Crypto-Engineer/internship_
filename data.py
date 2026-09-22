"""
Centralized structured data for DevPath Software Engineering Internships.
Contains single sources of truth for internships, categories, project areas, and skill sets.
No reverse dependencies: data.py does not import any other project module.
"""

from typing import Dict, List, Any

ORGANIZATION_INFO: Dict[str, str] = {
    "name": "DevPath Practicum",
    "short_name": "DevPath",
    "tagline": "Practical software engineering internships designed to help students turn what they learn into real project experience.",
    "purpose": "Help students gain real software engineering experience through structured, practical internship projects.",
    "headline": "Learn & Build",
    "headline_support": "Practical software engineering internships designed to help students turn what they learn into real project experience.",
    "contact_email": "admissions@devpath.org",
    "github_url": "https://github.com/devpath-practicum",
    "linkedin_url": "https://linkedin.com/company/devpath-practicum",
    "about_headline": "Creating practical pathways into software engineering.",
    "about_narrative": (
        "DevPath exists to give students opportunities to gain practical experience through "
        "structured software engineering projects. We bridge the critical gap between academic theory "
        "and production-grade development practices through real codebases, direct code reviews, and tangible deliverables."
    ),
}

VALUE_PROPOSITIONS: List[Dict[str, str]] = [
    {
        "title": "Work on Projects",
        "description": "Students build practical software projects instead of only completing theoretical exercises.",
    },
    {
        "title": "Learn Engineering Practices",
        "description": "Students gain exposure to development workflows, Git, testing, documentation, collaboration, and problem solving.",
    },
    {
        "title": "Build Your Portfolio",
        "description": "Students leave with practical work they can discuss and demonstrate professionally.",
    },
]

INTERNSHIP_AREAS: List[Dict[str, str]] = [
    {
        "name": "Software Development",
        "description": "Core software architecture, system design, and multi-tier application engineering.",
        "icon": "code",
    },
    {
        "name": "Python Development",
        "description": "Idiomatic Python services, backend APIs, CLI utilities, and package development.",
        "icon": "terminal",
    },
    {
        "name": "Web Development",
        "description": "Modern frontend interfaces, client-server data synchronization, and responsive web apps.",
        "icon": "globe",
    },
    {
        "name": "AI/ML Applications",
        "description": "Applied LLM toolchains, structured prompt engineering, and intelligent workflow automation.",
        "icon": "cpu",
    },
    {
        "name": "Data & Automation",
        "description": "Data processing pipelines, structured ETL tasks, metric aggregations, and script automation.",
        "icon": "database",
    },
    {
        "name": "QA & Testing",
        "description": "Unit testing suites, regression verification, automated integration, and code quality audits.",
        "icon": "check-circle",
    },
]

INTERNSHIPS: List[Dict[str, Any]] = [
    {
        "id": "python-software-engineer",
        "title": "Python Software Engineering Intern",
        "category": "Python Development",
        "description": "Build modular backend services, API integrations, and developer automation tools in a structured team workflow.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Beginner–Intermediate",
        "technologies": ["Python", "Git", "REST APIs", "Pytest"],
        "status": "Open",
        "overview": (
            "This internship immerses you in hands-on backend development. You will build modular Python utilities "
            "and API microservices while adopting production engineering hygiene: branch management, automated unit tests, "
            "and structured code reviews."
        ),
        "responsibilities": [
            "Develop and test RESTful service endpoints and structured data parsers",
            "Implement input validation, schema enforcement, and robust error handling",
            "Write comprehensive unit test suites using Pytest with mocked dependencies",
            "Participate in pull request reviews and follow team Git branching standards",
            "Document codebase architecture and reproducible local deployment steps",
        ],
        "requirements": [
            "Basic to intermediate understanding of Python syntax and core data structures",
            "Familiarity with basic Git commands (clone, branch, commit, push)",
            "Willingness to commit 10–15 hours per week consistently",
            "Curiosity and proactive asynchronous communication",
        ],
        "skills": ["Python", "Git", "GitHub", "APIs", "Testing", "Debugging", "Documentation"],
        "deliverables": [
            "Fully functional Python REST service repository with clean commit history",
            "Automated test suite reaching high branch coverage",
            "Technical architectural README and API specification document",
            "Demonstrable project showcase write-up for engineering interviews",
        ],
    },
    {
        "id": "web-app-engineer",
        "title": "Web Application Engineering Intern",
        "category": "Web Development",
        "description": "Develop accessible, responsive user interfaces and integrate client applications with real-world REST and WebSocket APIs.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Intermediate",
        "technologies": ["TypeScript", "React", "Tailwind CSS", "REST APIs"],
        "status": "Open",
        "overview": (
            "Focus on client-side engineering, responsive component architecture, and state management. You will build "
            "production-grade interfaces that prioritize usability, web performance, and clean API integration."
        ),
        "responsibilities": [
            "Construct reusable UI component libraries adhering to strict accessibility standards",
            "Integrate third-party RESTful endpoints and handle async loading and error states",
            "Optimize render performance and streamline bundle sizes",
            "Refactor code for modularity, readability, and type safety",
            "Collaborate on sprint planning and technical documentation",
        ],
        "requirements": [
            "Experience with HTML, CSS, JavaScript, and modern component frameworks",
            "Understanding of client-server architecture and HTTP request cycles",
            "Ability to turn wireframes into pixel-perfect responsive layouts",
            "Consistent weekly participation in progress reviews",
        ],
        "skills": ["TypeScript", "APIs", "Git", "GitHub", "Debugging", "Problem Solving", "Documentation"],
        "deliverables": [
            "Complete, deployable web application hosted with continuous deployment",
            "Component storybook or interactive style documentation",
            "Performance audit report with accessibility scores",
            "Portfolio-ready project demo",
        ],
    },
    {
        "id": "applied-ai-engineer",
        "title": "Applied AI & LLM Systems Intern",
        "category": "AI/ML Applications",
        "description": "Construct software that integrates modern AI APIs, structured prompt workflows, and automated evaluations.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Intermediate",
        "technologies": ["Python", "Gemini API", "APIs", "Streamlit", "JSON Schema"],
        "status": "Open",
        "overview": (
            "Learn how to responsibly harness large language models inside real software products. Rather than treating AI "
            "as a black box, you will engineer structured schema validation, fallback mechanisms, and evaluation benchmarks."
        ),
        "responsibilities": [
            "Design structured prompt pipelines enforcing strict JSON outputs",
            "Implement defensive fallback routines for API rate limits and connection anomalies",
            "Build intuitive Streamlit and web interfaces for end-user interaction",
            "Measure output quality using systematic evaluation heuristics",
            "Analyze cost, latency, and token efficiency tradeoffs",
        ],
        "requirements": [
            "Solid foundational Python skills and experience consuming web APIs",
            "Interest in generative AI tooling and structured output generation",
            "Attention to edge-case handling and defensive programming",
            "Dedication to responsible, safe AI development practices",
        ],
        "skills": ["Python", "APIs", "Prompt Engineering", "AI Integration", "Streamlit", "Testing"],
        "deliverables": [
            "Production-ready AI-integrated tool with interactive user interface",
            "Evaluation harness verifying reliability and schema adherence",
            "Technical postmortem on latency, model selection, and prompt refinement",
            "Interactive video demonstration or live portfolio link",
        ],
    },
    {
        "id": "data-automation-engineer",
        "title": "Data Engineering & Automation Intern",
        "category": "Data & Automation",
        "description": "Build automated data transformation pipelines, report generators, and tools that eliminate repetitive manual tasks.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Beginner–Intermediate",
        "technologies": ["Python", "SQL", "APIs", "Automation", "Git"],
        "status": "Open",
        "overview": (
            "Focus on streamlining operations and wrangling datasets. You will write automated scrapers, data sanitizers, "
            "and scheduled batch tasks that transform messy inputs into clean, queryable records."
        ),
        "responsibilities": [
            "Construct ingestion scripts that extract data from APIs and disparate file formats",
            "Design relational schemas and write optimized SQL queries",
            "Automate recurring reporting tasks and alert mechanisms",
            "Validate data integrity with deterministic sanity checks",
            "Package automation tools with clean command-line interfaces",
        ],
        "requirements": [
            "Familiarity with Python scripting and basic SQL querying",
            "Problem-solving mindset focused on eliminating manual bottlenecks",
            "Comfort working with tabular data and common file formats (CSV, JSON)",
            "Disciplined approach to logging and exception tracing",
        ],
        "skills": ["Python", "SQL", "APIs", "Git", "Problem Solving", "Documentation"],
        "deliverables": [
            "Automated ETL workflow with comprehensive error logging",
            "Structured relational database schema with seed scripts",
            "Executable CLI or dashboard for scheduled pipeline monitoring",
            "Technical architecture document detailing pipeline flow",
        ],
    },
    {
        "id": "qa-test-engineer",
        "title": "Quality Assurance & Test Engineering Intern",
        "category": "QA & Testing",
        "description": "Master software reliability by engineering end-to-end test suites, regression checks, and automated validation gates.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Beginner–Intermediate",
        "technologies": ["Python", "Pytest", "Git", "CI/CD", "Testing"],
        "status": "Open",
        "overview": (
            "Quality is what separates hobbyist code from production software. In this role, you will learn the art of "
            "breaking code constructively, writing test specifications, and implementing continuous testing pipelines."
        ),
        "responsibilities": [
            "Formulate detailed test plans from functional software specifications",
            "Write modular unit, integration, and regression test suites",
            "Configure automated CI/CD workflows to execute tests on pull requests",
            "Identify, document, and reproduce edge-case defects with clear issue logs",
            "Measure test execution performance and eliminate flaky test patterns",
        ],
        "requirements": [
            "Foundational programming experience in Python or JavaScript",
            "Analytical mindset with keen attention to detail and boundary cases",
            "Desire to learn automated verification frameworks and CI tools",
            "Clear written communication when documenting bug reproduction steps",
        ],
        "skills": ["Testing", "Debugging", "Git", "GitHub", "Documentation", "Problem Solving"],
        "deliverables": [
            "Automated test harness integrated with GitHub Actions",
            "Comprehensive test plan matrix covering critical user workflows",
            "Bug report registry demonstrating structured triage practices",
            "Guide on software quality practices for peer engineers",
        ],
    },
    {
        "id": "fullstack-software-engineer",
        "title": "Full-Stack Software Engineering Intern",
        "category": "Software Development",
        "description": "Design and build end-to-end applications bridging client UI, database models, and server-side business logic.",
        "duration": "8 weeks",
        "mode": "Remote",
        "level": "Intermediate",
        "technologies": ["Python", "TypeScript", "SQL", "REST APIs", "Git"],
        "status": "Open",
        "overview": (
            "Experience the complete lifecycle of a software product. You will architect database schemas, construct backend "
            "controllers, build interactive user interfaces, and deploy the entire system to a cloud environment."
        ),
        "responsibilities": [
            "Architect end-to-end features spanning database, backend, and frontend",
            "Design normalized relational database tables and relationship constraints",
            "Build type-safe API communication layers between client and server",
            "Implement secure authentication mechanisms and session management",
            "Containerize applications for predictable local development and hosting",
        ],
        "requirements": [
            "Prior exposure to both frontend (HTML/JS) and backend (Python/Node) development",
            "Familiarity with SQL database querying and object relational mapping",
            "Understanding of client-server security fundamentals",
            "Ability to work independently across multiple stack layers",
        ],
        "skills": ["Python", "TypeScript", "SQL", "APIs", "Git", "GitHub", "Problem Solving", "Debugging"],
        "deliverables": [
            "Production-deployed full-stack web application with custom domain",
            "System architecture diagram and database schema ERD",
            "End-to-end test suite verifying core business transactions",
            "Recorded technical demo explaining key architectural decisions",
        ],
    },
]

PROJECT_AREAS: List[Dict[str, str]] = [
    {
        "title": "Software Applications",
        "description": "Build practical applications using modern development tools.",
        "details": "Architect multi-tier applications, implement separation of concerns, and produce maintainable codebases designed for team collaboration.",
    },
    {
        "title": "AI Applications",
        "description": "Build software that integrates AI APIs and useful workflows.",
        "details": "Implement structured LLM orchestration, type-safe schema validation, prompt benchmarking, and defensive API error handling.",
    },
    {
        "title": "Automation",
        "description": "Create tools that reduce repetitive tasks.",
        "details": "Construct task orchestrators, file processing pipelines, batch synchronizers, and developer CLI utilities.",
    },
    {
        "title": "Web Applications",
        "description": "Develop functional web applications and interfaces.",
        "details": "Build responsive, accessible user interfaces with clean state management and robust client-server API contracts.",
    },
    {
        "title": "Data Applications",
        "description": "Work with data processing, analysis, and visualization.",
        "details": "Design relational models, query complex datasets, clean heterogeneous inputs, and generate actionable visual dashboards.",
    },
    {
        "title": "Testing & QA",
        "description": "Learn testing, debugging, validation, and quality practices.",
        "details": "Implement unit and integration testing suites, automate regression checks in CI, and master structured debugging techniques.",
    },
]

AVAILABLE_SKILLS: List[str] = [
    "Python",
    "Git",
    "GitHub",
    "APIs",
    "SQL",
    "Streamlit",
    "Testing",
    "Debugging",
    "Documentation",
    "REST APIs",
    "Prompt Engineering",
    "AI Integration",
    "Problem Solving",
]

HOW_IT_WORKS_STEPS: List[Dict[str, str]] = [
    {
        "number": "01",
        "title": "Explore",
        "description": "Browse available internships and choose an area that interests you.",
    },
    {
        "number": "02",
        "title": "Apply",
        "description": "Submit your application and relevant background information.",
    },
    {
        "number": "03",
        "title": "Build",
        "description": "Work through practical software engineering tasks and projects.",
    },
    {
        "number": "04",
        "title": "Complete",
        "description": "Finish your project work, document your contribution, and receive completion recognition where applicable.",
    },
]

INTERN_EXPECTATIONS: List[Dict[str, str]] = [
    {"trait": "Curiosity", "detail": "A genuine desire to understand how systems work beneath the surface."},
    {"trait": "Consistency", "detail": "Steady, reliable progress each week rather than last-minute cramming."},
    {"trait": "Willingness to learn", "detail": "Receptiveness to constructive code review feedback and refactoring."},
    {"trait": "Communication", "detail": "Proactive updates, clear issue descriptions, and collaborative teamwork."},
    {"trait": "Responsible use of AI tools", "detail": "Using AI as an accelerator for learning and debugging, never for unverified copy-paste code."},
    {"trait": "Ability to work independently", "detail": "Self-directed problem investigation before asking for assistance."},
]

OUR_APPROACH: List[Dict[str, str]] = [
    {
        "number": "1",
        "principle": "Practical",
        "summary": "Projects should produce something tangible.",
        "elaboration": "Interns work on actual working codebases rather than abstract quizzes or multiple-choice assessments.",
    },
    {
        "number": "2",
        "principle": "Structured",
        "summary": "Interns receive clear objectives and expected deliverables.",
        "elaboration": "Every project phase has milestones, acceptance criteria, and explicit technical benchmarks.",
    },
    {
        "number": "3",
        "principle": "Learning-focused",
        "summary": "The goal is development of skills and professional habits.",
        "elaboration": "We emphasize foundational engineering discipline: Git hygiene, test-driven validation, and clean architecture.",
    },
    {
        "number": "4",
        "principle": "Portfolio-oriented",
        "summary": "Students should be able to explain what they built and what they learned.",
        "elaboration": "Deliverables are structured so students can comfortably walk through technical decisions in job interviews.",
    },
]
