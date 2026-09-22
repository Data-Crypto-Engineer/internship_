"""
UI Presentation layer rendering clean, accessible Streamlit interfaces.
Strict one-way dependency: ui.py imports services.py and utils.py only.
Never imports app.py.
"""

import streamlit as st
from typing import Dict, Any, Optional
from services import (
    fetch_internships,
    get_internship_by_id,
    get_all_categories,
    get_organization_meta,
    get_value_propositions,
    get_internship_areas,
    get_project_areas,
    get_available_skills,
    get_how_it_works_steps,
    get_intern_expectations,
    get_our_approach,
    get_ai_response,
    submit_application,
)
from utils import (
    sanitize_text,
    truncate_text,
    get_category_color,
)


def apply_custom_styles() -> None:
    """Inject modern, restrained CSS styling adhering to the professional software aesthetic."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a;
            background-color: #fafbfc;
        }

        /* Ensure top Streamlit header does not overlap or cut off navigation ribbon and buttons */
        header[data-testid="stHeader"] {
            background-color: rgba(250, 251, 252, 0.95) !important;
            z-index: 50 !important;
        }

        .block-container, [data-testid="stAppViewBlockContainer"] {
            padding-top: 5.75rem !important;
            padding-bottom: 3rem !important;
            max-width: 1080px !important;
        }

        /* Navigation bar styling */
        .nav-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 2rem;
        }

        .nav-brand {
            font-weight: 700;
            font-size: 1.25rem;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
        }

        .nav-badge {
            background-color: #f1f5f9;
            color: #475569;
            font-size: 0.75rem;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
        }

        /* Hero styling */
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #0f172a;
            line-height: 1.15;
            margin-bottom: 1rem;
        }

        .hero-support {
            font-size: 1.25rem;
            line-height: 1.6;
            color: #475569;
            max-width: 680px;
            margin-bottom: 1.75rem;
        }

        /* Card components */
        .custom-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
            transition: all 0.15s ease-in-out;
            height: 100%;
        }

        .custom-card:hover {
            border-color: #cbd5e1;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        }

        .card-category {
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: inline-block;
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            margin-bottom: 0.75rem;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.3;
            margin-bottom: 0.5rem;
        }

        .card-meta {
            display: flex;
            gap: 0.75rem;
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 0.85rem;
            font-weight: 500;
        }

        .tech-tag {
            display: inline-block;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            color: #334155;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
        }

        .status-pill-open {
            background: #ecfdf5;
            color: #065f46;
            border: 1px solid #a7f3d0;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.1rem 0.45rem;
            border-radius: 4px;
        }

        /* Detail view box */
        .detail-header {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }

        .detail-meta-item {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 0.25rem;
        }
        .detail-meta-val {
            font-weight: 600;
            color: #0f172a;
            font-size: 0.95rem;
        }

        /* Footer */
        .footer-container {
            border-top: 1px solid #e2e8f0;
            padding-top: 2rem;
            margin-top: 4rem;
            color: #64748b;
            font-size: 0.875rem;
        }

        /* Button override refinement */
        .stButton>button {
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            white-space: nowrap !important;
            padding: 0.35rem 0.55rem !important;
            transition: all 0.15s ease !important;
        }

        /* Streamlit info & warning banners */
        .stAlert {
            border-radius: 6px !important;
            font-size: 0.9rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar() -> None:
    """Render the top navigation bar with clean buttons for seamless routing."""
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    col_brand, col_nav1, col_nav2, col_nav3, col_nav4, col_nav5, col_cta = st.columns(
        [2.3, 0.9, 1.2, 1.3, 1.65, 0.85, 1.2]
    )

    with col_brand:
        if st.button("DevPath Practicum", key="nav_logo", help="Return to Home"):
            st.session_state.current_page = "Home"
            st.session_state.selected_internship_id = None
            st.rerun()

    pages = [
        ("Home", "nav_home", col_nav1),
        ("Internships", "nav_internships", col_nav2),
        ("How It Works", "nav_how_it_works", col_nav3),
        ("Projects & Skills", "nav_projects_skills", col_nav4),
        ("About", "nav_about", col_nav5),
    ]

    for page_name, btn_key, col in pages:
        with col:
            is_active = st.session_state.get("current_page") == page_name
            label = f"**{page_name}**" if is_active else page_name
            if st.button(label, key=btn_key):
                st.session_state.current_page = page_name
                st.session_state.selected_internship_id = None
                st.rerun()

    with col_cta:
        if st.button("Apply Now", key="nav_apply_cta", type="primary"):
            st.session_state.current_page = "Apply"
            st.rerun()

    st.markdown("<hr style='margin-top:0.5rem; margin-bottom:2rem; border-color:#e2e8f0;'>", unsafe_allow_html=True)


# ==============================================================================
# PAGE RENDERERS
# ==============================================================================

def render_home_page() -> None:
    """Render the focused Home page per Section 5 specification."""
    meta = get_organization_meta()

    # 1. Hero Section
    st.markdown(f"<div class='hero-title'>{meta['headline']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-support'>{meta['headline_support']}</div>", unsafe_allow_html=True)

    cta_col1, cta_col2, _ = st.columns([1.5, 1.5, 3])
    with cta_col1:
        if st.button("Explore Internships", key="hero_explore_btn", type="primary"):
            st.session_state.current_page = "Internships"
            st.rerun()
    with cta_col2:
        if st.button("How It Works", key="hero_how_btn"):
            st.session_state.current_page = "How It Works"
            st.rerun()

    st.markdown("<div style='margin-top: 3.5rem;'></div>", unsafe_allow_html=True)

    # 2. Three-Part Value Section
    st.markdown("### Practical Learning Foundation")
    val_cols = st.columns(3)
    values = get_value_propositions()
    for idx, col in enumerate(val_cols):
        if idx < len(values):
            val = values[idx]
            with col:
                st.markdown(
                    f"""
                    <div class='custom-card'>
                        <div style='font-size:0.85rem; font-weight:700; color:#2563eb; margin-bottom:0.4rem;'>0{idx+1}</div>
                        <div style='font-size:1.15rem; font-weight:700; color:#0f172a; margin-bottom:0.5rem;'>{val['title']}</div>
                        <div style='font-size:0.9rem; color:#475569; line-height:1.5;'>{val['description']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("<div style='margin-top: 3.5rem;'></div>", unsafe_allow_html=True)

    # 3. Compact Internship Areas Section (Dynamically generated from data)
    st.markdown("### Internship Areas")
    st.markdown(
        "<p style='color:#64748b; font-size:0.95rem; margin-bottom:1.5rem;'>Explore structured project tracks designed around modern engineering disciplines.</p>",
        unsafe_allow_html=True,
    )

    areas = get_internship_areas()
    area_cols = st.columns(3)
    for idx, area in enumerate(areas):
        with area_cols[idx % 3]:
            st.markdown(
                f"""
                <div class='custom-card' style='margin-bottom:1rem;'>
                    <div style='font-size:1rem; font-weight:700; color:#0f172a; margin-bottom:0.35rem;'>{area['name']}</div>
                    <div style='font-size:0.85rem; color:#64748b; line-height:1.4;'>{area['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)

    # 4. Small Closing CTA Section
    st.markdown(
        """
        <div style='background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:2rem; text-align:center;'>
            <div style='font-size:1.35rem; font-weight:700; color:#0f172a; margin-bottom:0.5rem;'>Ready to start building?</div>
            <div style='color:#64748b; font-size:0.95rem; margin-bottom:1.25rem;'>Explore open positions and review project deliverables.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cta_bottom_col1, cta_bottom_col2, cta_bottom_col3 = st.columns([1.5, 1.5, 1.5])
    with cta_bottom_col2:
        if st.button("View Open Internships", key="cta_bottom_btn", type="primary", use_container_width=True):
            st.session_state.current_page = "Internships"
            st.rerun()


def render_internships_page() -> None:
    """Render the primary discovery page per Section 6 specification."""
    selected_id = st.session_state.get("selected_internship_id")
    if selected_id:
        render_internship_detail_view(selected_id)
        return

    st.markdown("## Software Engineering Internships")
    st.markdown(
        "<p style='color:#475569; font-size:1.05rem; margin-bottom:1.5rem;'>Explore current internship opportunities and find a project aligned with your interests and skills.</p>",
        unsafe_allow_html=True,
    )

    # Filter Bar
    filter_col1, filter_col2, filter_col3 = st.columns([1.8, 1.5, 1])
    with filter_col1:
        search_query = st.text_input("Search internships or technologies", placeholder="e.g. Python, REST APIs, testing...")
    with filter_col2:
        categories = get_all_categories()
        selected_cat = st.selectbox("Category", categories, index=0)
    with filter_col3:
        level_filter = st.selectbox("Skill Level", ["All Levels", "Beginner", "Intermediate"], index=0)

    # Internship Fit Assistant (Gemini Feature - Section 17)
    with st.expander("🔍 Internship Fit Assistant (AI Guidance)", expanded=False):
        render_fit_assistant_ui()

    st.markdown("<hr style='margin: 1.5rem 0; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # Fetch dynamic internships from services
    internships = fetch_internships(
        category_filter=selected_cat,
        search_query=search_query,
        level_filter=level_filter,
    )

    if not internships:
        st.info("No internships match your active filters. Try adjusting your search query or category.")
        return

    st.markdown(f"<div style='font-size:0.85rem; color:#64748b; margin-bottom:1rem;'>Showing {len(internships)} available opportunities</div>", unsafe_allow_html=True)

    card_cols = st.columns(2)
    for idx, item in enumerate(internships):
        with card_cols[idx % 2]:
            render_single_internship_card(item)


def render_single_internship_card(item: Dict[str, Any]) -> None:
    """Render a single modular internship card."""
    cat_style = get_category_color(item.get("category", ""))
    tech_tags = "".join([f"<span class='tech-tag'>{t}</span>" for t in item.get("technologies", [])])

    st.markdown(
        f"""
        <div class='custom-card' style='margin-bottom:1.25rem;'>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;'>
                <span class='card-category' style='background:{cat_style["bg"]}; color:{cat_style["text"]}; border:1px solid {cat_style["border"]};'>
                    {item.get('category')}
                </span>
                <span class='status-pill-open'>{item.get('status', 'Open')}</span>
            </div>
            <div class='card-title'>{item.get('title')}</div>
            <div class='card-meta'>
                <span>⏳ {item.get('duration')}</span>
                <span>•</span>
                <span>🌐 {item.get('mode')}</span>
                <span>•</span>
                <span>📊 {item.get('level')}</span>
            </div>
            <div style='font-size:0.9rem; color:#475569; line-height:1.5; margin-bottom:1rem;'>
                {truncate_text(item.get('description', ''), 140)}
            </div>
            <div style='margin-bottom:1rem;'>
                {tech_tags}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("View Details", key=f"details_{item['id']}", use_container_width=True):
            st.session_state.selected_internship_id = item["id"]
            st.rerun()
    with btn_col2:
        if st.button("Apply", key=f"apply_{item['id']}", type="primary", use_container_width=True):
            st.session_state.preselected_internship = item["title"]
            st.session_state.current_page = "Apply"
            st.rerun()


def render_internship_detail_view(internship_id: str) -> None:
    """Render the complete internship description view per Section 6."""
    item = get_internship_by_id(internship_id)
    if not item:
        st.error("Internship details could not be found.")
        if st.button("Back to Internships"):
            st.session_state.selected_internship_id = None
            st.rerun()
        return

    if st.button("← Back to all internships", key="back_to_list"):
        st.session_state.selected_internship_id = None
        st.rerun()

    cat_style = get_category_color(item.get("category", ""))

    st.markdown(
        f"""
        <div class='detail-header'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                <div>
                    <span class='card-category' style='background:{cat_style["bg"]}; color:{cat_style["text"]}; border:1px solid {cat_style["border"]};'>
                        {item.get('category')}
                    </span>
                    <h1 style='font-size:2rem; font-weight:800; color:#0f172a; margin-top:0.5rem; margin-bottom:0.75rem;'>
                        {item.get('title')}
                    </h1>
                </div>
                <span class='status-pill-open' style='font-size:0.85rem; padding:0.25rem 0.65rem;'>Status: {item.get('status', 'Open')}</span>
            </div>
            <div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:1rem; margin-top:1.25rem; border-top:1px solid #f1f5f9; padding-top:1rem;'>
                <div>
                    <div class='detail-meta-item'>Duration</div>
                    <div class='detail-meta-val'>{item.get('duration')}</div>
                </div>
                <div>
                    <div class='detail-meta-item'>Work Mode</div>
                    <div class='detail-meta-val'>{item.get('mode')}</div>
                </div>
                <div>
                    <div class='detail-meta-item'>Target Level</div>
                    <div class='detail-meta-val'>{item.get('level')}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Overview
    st.markdown("### Overview")
    st.markdown(f"<p style='color:#334155; line-height:1.6;'>{item.get('overview')}</p>", unsafe_allow_html=True)

    # 2. What you will work on & Skills you will practice
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### What you will work on")
        for resp in item.get("responsibilities", []):
            st.markdown(f"- {resp}")

    with col_right:
        st.markdown("### Skills you will practice")
        for sk in item.get("skills", []):
            st.markdown(f"- {sk}")

    st.markdown("<hr style='margin: 1.5rem 0; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # 3. Expected Deliverables & Requirements
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("### Expected Deliverables")
        for deliv in item.get("deliverables", []):
            st.markdown(f"- {deliv}")

    with col_d2:
        st.markdown("### Requirements")
        for req in item.get("requirements", []):
            st.markdown(f"- {req}")

    st.markdown("<hr style='margin: 1.5rem 0; border-color:#e2e8f0;'>", unsafe_allow_html=True)

    # Application Method & CTA
    st.markdown("### Application Method")
    st.markdown(
        "<p style='color:#475569; font-size:0.95rem;'>Applications are reviewed on a rolling basis. Submit your details through our structured application form to be considered.</p>",
        unsafe_allow_html=True,
    )

    if st.button(f"Apply for {item['title']}", type="primary", key="apply_from_detail"):
        st.session_state.preselected_internship = item["title"]
        st.session_state.selected_internship_id = None
        st.session_state.current_page = "Apply"
        st.rerun()


def render_fit_assistant_ui() -> None:
    """Render the AI Fit Assistant inside an interactive container."""
    st.markdown(
        "<p style='font-size:0.9rem; color:#475569; margin-bottom:1rem;'>"
        "Enter your current skills, interests, and background to receive an informational recommendation of which internship track best suits you."
        "</p>",
        unsafe_allow_html=True,
    )

    fa_col1, fa_col2 = st.columns(2)
    with fa_col1:
        user_skills = st.text_input("Your current skills / coursework", placeholder="e.g. Python, Git, basic SQL, algorithms")
    with fa_col2:
        user_interests = st.text_input("Topics you want to explore", placeholder="e.g. backend APIs, machine learning, web apps")

    user_background = st.text_input("Academic year or experience level", placeholder="e.g. 2nd year Computer Science student")

    if st.button("Analyze My Fit", key="btn_run_fit"):
        with st.spinner("Analyzing internship alignment..."):
            result = get_ai_response(user_skills, user_interests, user_background)

            if result.get("status") == "fallback":
                st.info(result.get("message"))

            st.markdown(
                f"""
                <div style='background:#ffffff; border:1px solid #cbd5e1; border-radius:6px; padding:1.25rem; margin-top:1rem;'>
                    <div style='font-size:0.8rem; font-weight:700; color:#2563eb; text-transform:uppercase; margin-bottom:0.5rem;'>
                        Recommendation Engine ({result.get('powered_by')})
                    </div>
                    <div style='font-size:0.9rem; color:#1e293b; line-height:1.6;'>
                        {result.get('recommendation')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_how_it_works_page() -> None:
    """Render the 4-step progression and expectations per Section 7 specification."""
    st.markdown("## How It Works")
    st.markdown(
        "<p style='color:#475569; font-size:1.05rem; margin-bottom:2.5rem;'>Our structured 4-step framework helps students transition from academic coursework to practical software engineering execution.</p>",
        unsafe_allow_html=True,
    )

    # 4-Step Layout
    steps = get_how_it_works_steps()
    step_cols = st.columns(4)
    for idx, step in enumerate(steps):
        with step_cols[idx]:
            st.markdown(
                f"""
                <div class='custom-card' style='height:100%;'>
                    <div style='font-size:1.1rem; font-weight:800; color:#2563eb; font-family:"JetBrains Mono", monospace; margin-bottom:0.5rem;'>
                        {step['number']}
                    </div>
                    <div style='font-size:1.15rem; font-weight:700; color:#0f172a; margin-bottom:0.5rem;'>
                        {step['title']}
                    </div>
                    <div style='font-size:0.875rem; color:#475569; line-height:1.5;'>
                        {step['description']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 3.5rem;'></div>", unsafe_allow_html=True)

    # Expectations Section
    st.markdown("### What We Expect From Interns")
    st.markdown(
        "<p style='color:#64748b; font-size:0.95rem; margin-bottom:1.5rem;'>We prioritize consistency and a proactive engineering mindset over existing mastery.</p>",
        unsafe_allow_html=True,
    )

    expectations = get_intern_expectations()
    exp_cols = st.columns(3)
    for idx, exp in enumerate(expectations):
        with exp_cols[idx % 3]:
            st.markdown(
                f"""
                <div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:6px; padding:1.25rem; margin-bottom:1rem;'>
                    <div style='font-weight:700; color:#0f172a; font-size:0.95rem; margin-bottom:0.25rem;'>• {exp['trait']}</div>
                    <div style='font-size:0.85rem; color:#64748b; line-height:1.4;'>{exp['detail']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_projects_and_skills_page() -> None:
    """Render Section A (Project Areas) and Section B (Skills) per Section 8 specification."""
    st.markdown("## Projects & Skills")
    st.markdown(
        "<p style='color:#475569; font-size:1.05rem; margin-bottom:2rem;'>Explore the technical domains and practical capabilities developed through our structured project milestones.</p>",
        unsafe_allow_html=True,
    )

    # SECTION A — PROJECT AREAS
    st.markdown("### Project Areas")
    project_areas = get_project_areas()
    pa_cols = st.columns(2)
    for idx, pa in enumerate(project_areas):
        with pa_cols[idx % 2]:
            st.markdown(
                f"""
                <div class='custom-card' style='margin-bottom:1rem;'>
                    <div style='font-size:1.15rem; font-weight:700; color:#0f172a; margin-bottom:0.35rem;'>{pa['title']}</div>
                    <div style='font-size:0.9rem; font-weight:600; color:#2563eb; margin-bottom:0.5rem;'>{pa['description']}</div>
                    <div style='font-size:0.85rem; color:#64748b; line-height:1.5;'>{pa['details']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

    # SECTION B — SKILLS
    st.markdown("### Engineering Skills")
    st.markdown(
        "<p style='color:#64748b; font-size:0.95rem; margin-bottom:1.5rem;'>"
        "<em>Depending on the internship, students may work with:</em>"
        "</p>",
        unsafe_allow_html=True,
    )

    skills = get_available_skills()
    tags_html = "".join([f"<span class='tech-tag' style='font-size:0.85rem; padding:0.35rem 0.75rem; margin:0.3rem;'>{sk}</span>" for sk in skills])
    st.markdown(
        f"""
        <div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:1.75rem; margin-bottom:1.5rem;'>
            <div style='display:flex; flex-wrap:wrap; gap:0.25rem;'>
                {tags_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_about_page() -> None:
    """Render the About page per Section 9 specification."""
    meta = get_organization_meta()
    st.markdown(f"## {meta['about_headline']}")
    st.markdown(
        f"<p style='color:#475569; font-size:1.1rem; line-height:1.6; max-width:800px; margin-bottom:2.5rem;'>{meta['about_narrative']}</p>",
        unsafe_allow_html=True,
    )

    # Core Themes
    col_t1, col_t2, col_t3 = st.columns(3)
    themes = [
        ("Learning by Building", "Practical codebases replace abstract theory."),
        ("Accessible Opportunities", "Opportunities open to all motivated students."),
        ("Responsible Technology Use", "Emphasis on verified, defensive programming."),
    ]
    for idx, col in enumerate([col_t1, col_t2, col_t3]):
        with col:
            st.markdown(
                f"""
                <div class='custom-card'>
                    <div style='font-size:1rem; font-weight:700; color:#0f172a; margin-bottom:0.35rem;'>{themes[idx][0]}</div>
                    <div style='font-size:0.85rem; color:#64748b; line-height:1.4;'>{themes[idx][1]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='margin-top: 3.5rem;'></div>", unsafe_allow_html=True)

    # Our Approach
    st.markdown("### Our Approach")
    approach = get_our_approach()
    app_cols = st.columns(2)
    for idx, item in enumerate(approach):
        with app_cols[idx % 2]:
            st.markdown(
                f"""
                <div class='custom-card' style='margin-bottom:1rem;'>
                    <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;'>
                        <span style='background:#f1f5f9; color:#334155; font-size:0.75rem; font-weight:700; padding:0.15rem 0.45rem; border-radius:4px;'>
                            {item['number']}
                        </span>
                        <span style='font-size:1.1rem; font-weight:700; color:#0f172a;'>{item['principle']}</span>
                    </div>
                    <div style='font-size:0.9rem; font-weight:600; color:#2563eb; margin-bottom:0.35rem;'>{item['summary']}</div>
                    <div style='font-size:0.85rem; color:#64748b; line-height:1.5;'>{item['elaboration']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_apply_page() -> None:
    """Render the application form per Section 10 & 11 specification."""
    st.markdown("## Apply for an Internship")
    st.markdown(
        "<p style='color:#475569; font-size:1.05rem; margin-bottom:1.5rem;'>"
        "Tell us about yourself, your interests, and the type of software engineering work you want to explore."
        "</p>",
        unsafe_allow_html=True,
    )

    internships = fetch_internships()
    titles = [i["title"] for i in internships]

    preselected = st.session_state.get("preselected_internship")
    default_idx = 0
    if preselected and preselected in titles:
        default_idx = titles.index(preselected)

    with st.form("internship_application_form"):
        st.markdown("#### 1. Candidate Information")
        c1, c2 = st.columns(2)
        with c1:
            full_name = st.text_input("Full Name *", placeholder="Ada Lovelace")
            email = st.text_input("Email Address *", placeholder="ada@university.edu")
        with c2:
            university = st.text_input("University / Institution *", placeholder="State University")
            field_of_study = st.text_input("Field of Study", placeholder="Computer Science / Engineering")

        c3, c4 = st.columns(2)
        with c3:
            grad_year = st.text_input("Current Year / Graduation Year", placeholder="e.g. Sophomore / Class of 2027")
        with c4:
            internship_area = st.selectbox("Internship Area *", titles, index=default_idx)

        st.markdown("#### 2. Profiles & Project Portfolio")
        c5, c6 = st.columns(2)
        with c5:
            github_url = st.text_input("GitHub URL", placeholder="https://github.com/username")
        with c6:
            linkedin_url = st.text_input("LinkedIn URL", placeholder="https://linkedin.com/in/username")

        relevant_skills = st.text_input("Relevant Skills", placeholder="e.g. Python, Git, React, SQLite")
        previous_projects = st.text_area("Previous Projects or Coursework (optional)", placeholder="Briefly describe 1 or 2 projects or assignments you have completed.")

        st.markdown("#### 3. Motivation & Availability")
        why_interested = st.text_area(
            "Why are you interested in this internship? *",
            placeholder="Explain what you hope to build and learn through structured engineering practice.",
            help="Minimum 20 characters.",
        )
        availability = st.text_input("Estimated Weekly Availability", placeholder="e.g. 10–15 hours/week, remote")

        resume_file = st.file_uploader("Upload Resume / CV (PDF or Markdown)", type=["pdf", "txt", "md"])

        st.markdown("#### 4. Consent")
        consent = st.checkbox(
            "I consent to the collection and evaluation of my application details for internship admission purposes. *",
            value=False,
        )

        submitted = st.form_submit_button("Submit Application", type="primary")

    if submitted:
        application_payload = {
            "full_name": full_name,
            "email": email,
            "university": university,
            "field_of_study": field_of_study,
            "graduation_year": grad_year,
            "github_url": github_url,
            "linkedin_url": linkedin_url,
            "internship_area": internship_area,
            "relevant_skills": relevant_skills,
            "previous_projects": previous_projects,
            "why_interested": why_interested,
            "availability": availability,
            "consent": consent,
            "resume_filename": resume_file.name if resume_file else "None provided",
        }

        result = submit_application(application_payload)
        if result.get("success"):
            st.success(result.get("message"))
            st.balloons()
            st.markdown(
                """
                <div style='background:#f0fdf4; border:1px solid #bbf7d0; border-radius:6px; padding:1.25rem; margin-top:1rem;'>
                    <div style='font-weight:700; color:#166534; margin-bottom:0.25rem;'>Next Steps</div>
                    <div style='font-size:0.875rem; color:#166534; line-height:1.5;'>
                        1. A copy of your submission ID has been logged.<br>
                        2. Admissions mentors review candidate profiles weekly.<br>
                        3. Selected applicants receive an invitation to an asynchronous technical problem walkthrough.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error(result.get("message"))

    # Configurable Backend Guidance Box (Section 10 & 11)
    with st.expander("ℹ️ Developer Backend Configuration Note"):
        st.markdown(
            """
            **Integration Architecture:**
            Applications are currently processed through `services.submit_application()`.
            To hook up an external database or webhook (e.g. CRM, Slack, Google Sheets, or REST API),
            configure the environment variable:
            ```bash
            export SUBMISSION_WEBHOOK_URL="https://api.yourorganization.com/admissions"
            ```
            or define it inside `.streamlit/secrets.toml`:
            ```toml
            SUBMISSION_WEBHOOK_URL = "https://api.yourorganization.com/admissions"
            ```
            The submission service will automatically forward structured JSON payloads without requiring UI changes.
            """
        )


def render_footer() -> None:
    """Render minimal footer adhering to Section 23 specification."""
    meta = get_organization_meta()
    st.markdown(
        f"""
        <div class='footer-container'>
            <div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;'>
                <div>
                    <div style='font-weight:700; color:#0f172a; font-size:1rem;'>{meta['name']}</div>
                    <div style='font-size:0.85rem; color:#64748b;'>{meta['tagline']}</div>
                </div>
                <div style='font-size:0.85rem; display:flex; gap:1.5rem;'>
                    <span>Contact: {meta['contact_email']}</span>
                </div>
            </div>
            <div style='margin-top:1.5rem; font-size:0.75rem; color:#94a3b8;'>
                &copy; 2026 {meta['name']}. Structured, practical software engineering learning for students.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
