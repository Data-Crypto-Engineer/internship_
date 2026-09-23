"""
Services module providing single-point integrations for data queries, AI guidance, and submissions.
Strict one-way dependency: services.py imports data.py and utils.py only.
Never imports ui.py or app.py.
"""

import os
import uuid
import datetime
import json
import csv
import io
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
from data import (
    INTERNSHIPS,
    INTERNSHIP_AREAS,
    PROJECT_AREAS,
    AVAILABLE_SKILLS,
    HOW_IT_WORKS_STEPS,
    INTERN_EXPECTATIONS,
    OUR_APPROACH,
    ORGANIZATION_INFO,
    VALUE_PROPOSITIONS,
)
from utils import sanitize_text, validate_email

# In-memory and local persistent storage file for candidate applications
APPLICATIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "applications.json")
_APPLICATIONS_CACHE: List[Dict[str, Any]] = []


def _load_persisted_applications() -> List[Dict[str, Any]]:
    """Safely load persisted application records from local JSON storage."""
    if os.path.exists(APPLICATIONS_FILE):
        try:
            with open(APPLICATIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            return []
    return []


def _persist_application_record(record: Dict[str, Any]) -> None:
    """Safely persist a new application record to disk."""
    try:
        records = _load_persisted_applications()
        records.append(record)
        with open(APPLICATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


# ==============================================================================
# 1. INTERNSHIP DATA SERVICE (One dedicated function for fetching internships)
# ==============================================================================

def fetch_internships(
    category_filter: Optional[str] = None,
    search_query: Optional[str] = None,
    level_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Centralized function to fetch and filter internship opportunities.
    Supports future transition to JSON, SQLite, or an external API without touching UI code.
    """
    results = list(INTERNSHIPS)

    if category_filter and category_filter != "All Areas":
        results = [
            item for item in results
            if item.get("category", "").lower() == category_filter.lower()
        ]

    if level_filter and level_filter != "All Levels":
        results = [
            item for item in results
            if level_filter.lower() in item.get("level", "").lower()
        ]

    if search_query:
        query = search_query.strip().lower()
        filtered = []
        for item in results:
            searchable_blob = " ".join([
                item.get("title", ""),
                item.get("category", ""),
                item.get("description", ""),
                item.get("overview", ""),
                " ".join(item.get("technologies", [])),
                " ".join(item.get("skills", [])),
            ]).lower()
            if query in searchable_blob:
                filtered.append(item)
        results = filtered

    return results


def get_internship_by_id(internship_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a single internship specification by its unique identifier."""
    if not internship_id:
        return None
    for item in INTERNSHIPS:
        if item.get("id") == internship_id:
            return item
    return None


def get_all_categories() -> List[str]:
    """Retrieve distinct categories for filters."""
    categories = sorted(list({item["category"] for item in INTERNSHIPS}))
    return ["All Areas"] + categories


def get_organization_meta() -> Dict[str, str]:
    """Provide organization identity information."""
    return ORGANIZATION_INFO


def get_value_propositions() -> List[Dict[str, str]]:
    """Provide primary value propositions."""
    return VALUE_PROPOSITIONS


def get_internship_areas() -> List[Dict[str, str]]:
    """Provide high-level internship practice areas."""
    return INTERNSHIP_AREAS


def get_project_areas() -> List[Dict[str, str]]:
    """Provide project areas with descriptive summaries."""
    return PROJECT_AREAS


def get_available_skills() -> List[str]:
    """Provide master list of skills practiced."""
    return AVAILABLE_SKILLS


def get_how_it_works_steps() -> List[Dict[str, str]]:
    """Provide the 4-step internship progression."""
    return HOW_IT_WORKS_STEPS


def get_intern_expectations() -> List[Dict[str, str]]:
    """Provide concise intern attributes."""
    return INTERN_EXPECTATIONS


def get_our_approach() -> List[Dict[str, str]]:
    """Provide organization educational principles."""
    return OUR_APPROACH


# ==============================================================================
# 2. GEMINI AI SERVICE (One dedicated function for AI responses)
# ==============================================================================

def get_ai_response(
    skills_input: str,
    interests_input: str,
    experience_input: str,
) -> Dict[str, Any]:
    """
    Dedicated function to interface with the Gemini API for the 'Internship Fit Assistant'.
    Fails gracefully if the API or key is unavailable, returning an informational fallback.
    Never rejects or accepts applicants; only provides informational guidance.
    """
    # 1. Resolve API key from Streamlit secrets or OS environment safely
    api_key = None
    try:
        import streamlit as st  # Local import for safe secrets resolution
        if hasattr(st, "secrets"):
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key and "gemini" in st.secrets:
                api_key = st.secrets["gemini"].get("api_key")
    except Exception:
        pass

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    cleaned_skills = sanitize_text(skills_input)
    cleaned_interests = sanitize_text(interests_input)
    cleaned_experience = sanitize_text(experience_input)

    # 2. If no key is configured, provide an intelligent deterministic recommendation
    if not api_key:
        fallback_summary = _generate_rule_based_recommendation(
            cleaned_skills, cleaned_interests, cleaned_experience
        )
        return {
            "status": "fallback",
            "message": "AI assistance is currently unavailable. You can still explore all internships normally.",
            "recommendation": fallback_summary,
            "powered_by": "Rule-based Engine (Gemini API key not configured)",
        }

    # 3. Call Google Generative AI
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        available_titles = ", ".join([item["title"] for item in INTERNSHIPS])

        prompt = f"""
You are the Internship Fit Assistant for DevPath Practicum, a software engineering startup offering structured student internships.
Your goal is to provide concise, friendly, and realistic guidance to help a student identify which internship area best aligns with their stated background.

IMPORTANT RULES:
- Do NOT accept or reject the applicant.
- Keep the tone encouraging, technical, professional, and concise (under 180 words).
- Recommend 1 or 2 specific roles from this list: {available_titles}.
- Explain WHY those roles match their skills or interests.
- Suggest 1 practical skill or concept they can review to prepare.

Applicant Details:
- Stated Skills: {cleaned_skills or 'Not specified'}
- Areas of Interest: {cleaned_interests or 'Not specified'}
- Current Experience / Background: {cleaned_experience or 'Undergraduate student'}

Provide your response in structured Markdown with:
**Recommended Track(s):** ...
**Why this aligns:** ...
**Suggested Preparation:** ...
"""
        response = model.generate_content(prompt)
        text = response.text if hasattr(response, "text") else ""
        if text:
            return {
                "status": "success",
                "message": "Fit analysis generated successfully.",
                "recommendation": text.strip(),
                "powered_by": "Gemini AI",
            }
        else:
            raise ValueError("Empty response from AI service.")

    except Exception:
        # Fails gracefully without exposing credentials, stack traces, or internal paths
        fallback_summary = _generate_rule_based_recommendation(
            cleaned_skills, cleaned_interests, cleaned_experience
        )
        return {
            "status": "fallback",
            "message": "AI assistance is currently unavailable. You can still explore all internships normally.",
            "recommendation": fallback_summary,
            "powered_by": "Rule-based Engine (Service Fallback)",
        }


def _generate_rule_based_recommendation(skills: str, interests: str, experience: str) -> str:
    """Deterministic, helpful matching when Gemini is offline or unconfigured."""
    text_corpus = f"{skills} {interests} {experience}".lower()

    if any(k in text_corpus for k in ["ai", "llm", "machine learning", "prompt", "nlp", "model"]):
        return (
            "**Recommended Track:** Applied AI & LLM Systems Intern\n\n"
            "**Why this aligns:** Your stated interest in intelligent workflows and machine learning makes our AI track a strong match. You'll work with structured schemas, prompt engineering, and defensive API integration.\n\n"
            "**Suggested Preparation:** Review REST API interactions in Python and experiment with structured JSON outputs."
        )
    elif any(k in text_corpus for k in ["react", "web", "frontend", "html", "css", "javascript", "typescript", "ui", "tailwind"]):
        return (
            "**Recommended Track:** Web Application Engineering Intern\n\n"
            "**Why this aligns:** Your background in modern web tools aligns directly with building responsive, accessible client applications and interfacing with backend services.\n\n"
            "**Suggested Preparation:** Practice state management and handling asynchronous API loading states in React or TypeScript."
        )
    elif any(k in text_corpus for k in ["sql", "data", "automation", "etl", "pipeline", "pandas", "database"]):
        return (
            "**Recommended Track:** Data Engineering & Automation Intern\n\n"
            "**Why this aligns:** You show interest in wrangling datasets and automating manual workflows. This track builds reliable ingestion scripts and normalized relational models.\n\n"
            "**Suggested Preparation:** Practice writing multi-table SQL queries and handling dirty CSV/JSON files in Python."
        )
    elif any(k in text_corpus for k in ["test", "qa", "pytest", "quality", "debugging", "ci", "cd"]):
        return (
            "**Recommended Track:** Quality Assurance & Test Engineering Intern\n\n"
            "**Why this aligns:** Attention to reliability and test-driven development is central to this track. You will learn to construct automated CI pipelines and comprehensive regression suites.\n\n"
            "**Suggested Preparation:** Familiarize yourself with basic Pytest fixtures and writing reproducible bug reports."
        )
    else:
        return (
            "**Recommended Track:** Python Software Engineering Intern\n\n"
            "**Why this aligns:** Python provides a balanced, production-proven foundation for modular backend architecture, Git workflows, and test coverage.\n\n"
            "**Suggested Preparation:** Practice core Python data structures and basic Git branch workflows (commit, push, PR)."
        )


# ==============================================================================
# 3. APPLICATION SUBMISSION SERVICE (One dedicated function for applications)
# ==============================================================================

def submit_application(application_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dedicated function to process student internship applications.
    Does not pretend an external backend exists if none is configured.
    Provides a clean, configurable submission pipeline with full validation.
    """
    full_name = sanitize_text(application_data.get("full_name"))
    email = sanitize_text(application_data.get("email"))
    internship_area = sanitize_text(application_data.get("internship_area"))
    university = sanitize_text(application_data.get("university"))
    interest_statement = sanitize_text(application_data.get("why_interested"))
    consent = bool(application_data.get("consent"))

    # Validation rules
    if not full_name:
        return {"success": False, "message": "Please provide your Full Name."}
    if not email or not validate_email(email):
        return {"success": False, "message": "Please provide a valid email address."}
    if not internship_area:
        return {"success": False, "message": "Please select an Internship Area."}
    if not university:
        return {"success": False, "message": "Please specify your University or Educational Institution."}
    if not consent:
        return {
            "success": False,
            "message": "Please agree to the application data processing consent to proceed.",
        }

    # Generate receipt identifier
    app_id = f"APP-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    record = {
        "id": app_id,
        "submitted_at": timestamp,
        "full_name": full_name,
        "email": email,
        "university": university,
        "field_of_study": sanitize_text(application_data.get("field_of_study")),
        "graduation_year": sanitize_text(application_data.get("graduation_year")),
        "github_url": sanitize_text(application_data.get("github_url")),
        "linkedin_url": sanitize_text(application_data.get("linkedin_url")),
        "internship_area": internship_area,
        "relevant_skills": sanitize_text(application_data.get("relevant_skills")),
        "previous_projects": sanitize_text(application_data.get("previous_projects")),
        "why_interested": interest_statement,
        "availability": sanitize_text(application_data.get("availability")),
        "resume_filename": application_data.get("resume_filename", "None provided"),
    }

    _APPLICATIONS_CACHE.append(record)
    _persist_application_record(record)

    # Configurable webhook dispatch hook (if developer configures SUBMISSION_WEBHOOK_URL)
    webhook_url = None
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "SUBMISSION_WEBHOOK_URL" in st.secrets:
            webhook_url = st.secrets["SUBMISSION_WEBHOOK_URL"]
    except Exception:
        pass
    if not webhook_url:
        webhook_url = os.environ.get("SUBMISSION_WEBHOOK_URL")

    if webhook_url:
        try:
            payload_bytes = json.dumps(record).encode("utf-8")
            req = urllib.request.Request(
                webhook_url,
                data=payload_bytes,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "DevPath-Admissions/1.0",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                pass
        except Exception:
            # Continue gracefully so user submission is never halted if webhook is unreachable
            pass

    return {
        "success": True,
        "application_id": app_id,
        "message": (
            f"Your application has been received successfully! Receipt ID: {app_id}. "
            "Our admissions mentors review applications on a rolling weekly basis."
        ),
        "record": record,
    }


def get_all_applications() -> List[Dict[str, Any]]:
    """
    Retrieve all stored applications from local disk and runtime memory.
    Returns list of candidate dictionaries ordered newest first.
    """
    persisted = _load_persisted_applications()
    combined = []
    seen_ids = set()

    for item in list(reversed(_APPLICATIONS_CACHE)) + list(reversed(persisted)):
        rec_id = item.get("id")
        if rec_id and rec_id not in seen_ids:
            seen_ids.add(rec_id)
            combined.append(item)

    return combined


def export_applications_csv() -> str:
    """Generate a clean CSV string of all stored applications for 1-click download."""
    records = get_all_applications()
    output = io.StringIO()
    fieldnames = [
        "id",
        "submitted_at",
        "full_name",
        "email",
        "university",
        "field_of_study",
        "graduation_year",
        "internship_area",
        "relevant_skills",
        "previous_projects",
        "why_interested",
        "availability",
        "github_url",
        "linkedin_url",
        "resume_filename",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in records:
        writer.writerow(row)
    return output.getvalue()


def verify_admin_passcode(passcode: str) -> bool:
    """
    Verify admin passcode against secrets or environment variable.
    Defaults to 'admin123' for immediate accessibility without requiring prior setup.
    """
    target_key = "admin123"
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "ADMIN_KEY" in st.secrets:
                target_key = str(st.secrets["ADMIN_KEY"])
            elif "admin_key" in st.secrets:
                target_key = str(st.secrets["admin_key"])
    except Exception:
        pass

    env_key = os.environ.get("ADMIN_KEY") or os.environ.get("ADMIN_PASSCODE")
    if env_key:
        target_key = env_key

    return passcode.strip() == target_key.strip()


def get_cached_applications_count() -> int:
    """Helper for testing or administrative monitoring."""
    return len(get_all_applications())
