# ==============================================================================
# LSC: Cell Therapy Compass - Navigation System
# ==============================================================================
import streamlit as st
from utils.styles import MARROWCO_LOGO_BYTES

# Page registry: (file_path, display_label, tooltip)
PAGE_SECTIONS = {
    "Data Foundation": [
        ("pages/01_Data_Foundation.py", "Data Foundation", "Bronze → Silver → Gold pipeline with Dynamic Tables"),
        ("pages/02_Semantic_Intelligence.py", "Semantic Intelligence", "Semantic View — the single source of truth"),
    ],
    "Outcome Forecasting": [
        ("pages/03_GVHD_Forecasting.py", "GVHD Forecasting", "ML-powered risk prediction and outcome analytics"),
    ],
    "Intelligence & AI": [
        ("pages/04_Research_Agent.py", "Research Agent", "AI agent with structured + unstructured intelligence"),
        ("pages/05_Take_Action.py", "Take Action", "Generate AI-powered clinical communications"),
    ],
}

# Flat ordered list for back/forward navigation
ALL_PAGES = [("streamlit_app.py", "Home", "Cell Therapy Compass home page")]
for section_pages in PAGE_SECTIONS.values():
    ALL_PAGES.extend(section_pages)


def get_current_page_index(current_label: str) -> int:
    """Get the index of the current page in the flat list."""
    for i, (_, label, *_) in enumerate(ALL_PAGES):
        if label == current_label:
            return i
    return 0


def render_sidebar(current_page: str = "Home"):
    """Render the full sidebar with LSC branding, collapsible nav sections, and footer."""
    # LSC Logo only
    st.sidebar.image(MARROWCO_LOGO_BYTES, width=160)

    st.sidebar.markdown("""
    <div style="padding: 0 0.75rem 0.75rem 0.75rem;">
        <div style="color: #29B5E8; font-size: 1.15rem; font-weight: 700; margin-top: 0.5rem;">
            LSC Analytics
        </div>
        <div style="color: #8892b0; font-size: 0.7rem; margin-top: 0.15rem; padding-bottom: 0.5rem;
                    border-bottom: 2px solid #29B5E8;">
            Outcome Forecasting with Multimodal Data
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Home link
    st.sidebar.page_link("streamlit_app.py", label="\u25C8  Home", use_container_width=True)

    # Collapsible sections
    for section_name, pages in PAGE_SECTIONS.items():
        if not pages:
            st.sidebar.markdown(
                f'<div style="padding:0.3rem 0.75rem;color:#8892b0;font-size:0.8rem;">'
                f'<strong>{section_name}</strong> <span style="font-size:0.65rem;">(coming soon)</span></div>',
                unsafe_allow_html=True,
            )
            continue
        page_labels = [p[1] for p in pages]
        with st.sidebar.expander(f"**{section_name}**", expanded=(current_page in page_labels)):
            for page_path, page_label, tooltip in pages:
                st.page_link(
                    page_path,
                    label=f"  {page_label}",
                    help=tooltip,
                    use_container_width=True,
                )

    # Footer
    st.sidebar.markdown("---")
    try:
        from snowflake.snowpark.context import get_active_session
        get_active_session()
        status_color, status_text = "#4ECDC4", "The Winter Cloud Platform Connected"
    except Exception:
        status_color, status_text = "#FFB74D", "Running Locally"

    st.sidebar.markdown(f"""
    <div style="padding: 0.5rem 0.75rem;">
        <div style="display: flex; align-items: center; gap: 0.4rem;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {status_color};"></div>
            <span style="color: {status_color}; font-size: 0.75rem; font-weight: 600;">{status_text}</span>
        </div>
        <div style="color: #8892b0; font-size: 0.6rem; margin-top: 0.5rem;">
            POWERED BY THE WINTER CLOUD PLATFORM AI DATA CLOUD
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_nav_buttons(current_page: str):
    """Render back/forward navigation buttons at the bottom of the page."""
    idx = get_current_page_index(current_page)
    prev_page = ALL_PAGES[idx - 1] if idx > 0 else None
    next_page = ALL_PAGES[idx + 1] if idx < len(ALL_PAGES) - 1 else None

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if prev_page:
            st.page_link(prev_page[0], label=f"\u2190 {prev_page[1]}", use_container_width=True)
    with col2:
        st.markdown(
            f'<div style="text-align:center;color:#8892b0;font-size:0.75rem;padding-top:0.5rem;">'
            f'Page {idx + 1} of {len(ALL_PAGES)}</div>',
            unsafe_allow_html=True,
        )
    with col3:
        if next_page:
            st.page_link(next_page[0], label=f"{next_page[1]} \u2192", use_container_width=True)


def get_snowflake_session():
    """Get The Winter Cloud Platform session with graceful fallback."""
    try:
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except Exception:
        try:
            from snowflake.snowpark import Session
            import os
            creds_path = os.path.expanduser("~/.snowflake/connections.toml")
            if os.path.exists(creds_path):
                return Session.builder.configs({"connection_name": "DEMO"}).create()
        except Exception:
            pass
    return None
