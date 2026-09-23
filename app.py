"""
DevPath Practicum - Software Engineering Internships Platform
Main Streamlit application entry point.
Strict one-way dependency: app.py imports ui.py only.
Run with: streamlit run app.py
"""

import streamlit as st
from ui import (
    apply_custom_styles,
    render_navbar,
    render_home_page,
    render_internships_page,
    render_how_it_works_page,
    render_projects_and_skills_page,
    render_about_page,
    render_apply_page,
    render_admin_portal,
    render_footer,
)

# 1. Page Configuration (Centered max-width layout)
st.set_page_config(
    page_title="DevPath Practicum | Software Engineering Internships",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Session State Initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "selected_internship_id" not in st.session_state:
    st.session_state.selected_internship_id = None

if "preselected_internship" not in st.session_state:
    st.session_state.preselected_internship = None

# 3. Apply Custom Restrained Styles
apply_custom_styles()

# 4. Top Navigation Bar
render_navbar()

# 5. Page Routing Controller
page = st.session_state.current_page

if page == "Home":
    render_home_page()
elif page == "Internships":
    render_internships_page()
elif page == "How It Works":
    render_how_it_works_page()
elif page == "Projects & Skills":
    render_projects_and_skills_page()
elif page == "About":
    render_about_page()
elif page == "Apply":
    render_apply_page()
elif page == "Admissions":
    render_admin_portal()
else:
    render_home_page()

# 6. Global Footer
render_footer()
