"""
Generic utility helpers for text sanitization, validation, and presentation.
Standalone module: utils.py does not import data, services, ui, or app.
"""

import re
from typing import Optional, Dict


def sanitize_text(text: Optional[str]) -> str:
    """Trim and clean user-provided text strings."""
    if not text:
        return ""
    return str(text).strip()


def truncate_text(text: str, max_chars: int = 120) -> str:
    """Cleanly truncate text with an ellipsis without cutting off mid-word."""
    if not text or len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return f"{truncated}..."


def validate_email(email: str) -> bool:
    """Validate that an email address follows a standard address format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_url(url: str, required_domain: Optional[str] = None) -> bool:
    """Validate that a URL starts with http(s) and optionally contains a required domain."""
    if not url or not isinstance(url, str):
        return False
    cleaned = url.strip().lower()
    if not (cleaned.startswith("http://") or cleaned.startswith("https://")):
        return False
    if required_domain and required_domain.lower() not in cleaned:
        return False
    return True


def get_category_color(category: str) -> Dict[str, str]:
    """Provide a restrained color pair (background, text, border) for category badges."""
    palette = {
        "Python Development": {"bg": "#f0fdf4", "text": "#166534", "border": "#bbf7d0"},
        "Web Development": {"bg": "#eff6ff", "text": "#1e40af", "border": "#bfdbfe"},
        "AI/ML Applications": {"bg": "#faf5ff", "text": "#6b21a8", "border": "#e9d5ff"},
        "Data & Automation": {"bg": "#fffbeb", "text": "#92400e", "border": "#fde68a"},
        "QA & Testing": {"bg": "#fef2f2", "text": "#991b1b", "border": "#fecaca"},
        "Software Development": {"bg": "#f8fafc", "text": "#334155", "border": "#cbd5e1"},
    }
    return palette.get(category, {"bg": "#f1f5f9", "text": "#475569", "border": "#e2e8f0"})


def format_duration_badge(duration: str) -> str:
    """Ensure duration string is standard."""
    return duration.strip() if duration else "8 weeks"
