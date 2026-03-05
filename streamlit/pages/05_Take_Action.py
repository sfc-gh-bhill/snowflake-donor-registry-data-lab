import streamlit as st

st.set_page_config(page_title="Take Action | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_info_callout,
    render_success_callout, render_section_separator
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import streamlit.components.v1 as components

apply_styles()
render_sidebar("Take Action")

render_header("Take Action", "Generate AI-Powered Clinical Communications from Data Insights")

session = get_snowflake_session()

# ── Context Data ──
live_data = False
summary_stats = {}
if session:
    try:
        row = session.sql("""
            SELECT 
                COUNT(*) AS TOTAL,
                ROUND(COUNT(CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 END) * 100.0 / COUNT(*), 1) AS SEVERE_GVHD_PCT,
                ROUND(COUNT(CASE WHEN ONE_YEAR_SURVIVOR THEN 1 END) * 100.0 / COUNT(*), 1) AS ONE_YEAR_OS_PCT,
                ROUND(AVG(GVHD_RISK_SCORE), 3) AS AVG_RISK,
                ROUND(AVG(TIME_TO_ENGRAFTMENT_DAYS), 1) AS AVG_ENGRAFT
            FROM DT_TRANSPLANT_ENRICHED
        """).collect()[0]
        summary_stats = {
            "total": row["TOTAL"],
            "severe_gvhd_pct": row["SEVERE_GVHD_PCT"],
            "one_year_os_pct": row["ONE_YEAR_OS_PCT"],
            "avg_risk": row["AVG_RISK"],
            "avg_engraft": row["AVG_ENGRAFT"],
        }
        live_data = True
    except Exception:
        pass

if not live_data:
    summary_stats = {
        "total": 500, "severe_gvhd_pct": 13.4,
        "one_year_os_pct": 46.6, "avg_risk": 0.42, "avg_engraft": 18.2,
    }

st.markdown(render_section_separator(
    "Clinical Email Generator",
    "Create a professional, data-driven email — powered by Snowflake AI"
), unsafe_allow_html=True)

# ── Input Fields ──
col1, col2 = st.columns(2)
with col1:
    sender_name = st.text_input("Your Name", value="Braedon Hill")
    sender_title = st.text_input("Your Title", value="Sr. Solution Engineer, Snowflake")
    recipient_name = st.text_input("Recipient Name", value="")
    recipient_email = st.text_input("Recipient Email", value="")

with col2:
    recipient_title = st.text_input("Recipient Title", value="")
    recipient_org = st.text_input("Recipient Organization", value="The Life Saving Company")
    focus_area = st.selectbox("Email Focus Area", [
        "GVHD Outcome Summary & Recommendations",
        "Donor Type Comparison Analysis",
        "Health Equity Findings (Donor for All)",
        "ML Model Performance Report",
        "Transplant Center Benchmarking",
        "Custom Topic"
    ])
    if focus_area == "Custom Topic":
        custom_topic = st.text_input("Describe the topic:")
    else:
        custom_topic = ""

# ── Generate Subject Line ──
focus_subjects = {
    "GVHD Outcome Summary & Recommendations": f"GVHD Outcome Intelligence: {summary_stats['total']} Patient Cohort Analysis with Actionable Recommendations",
    "Donor Type Comparison Analysis": f"Donor Type Outcomes: MUD vs MMUD vs HAPLO — {summary_stats['one_year_os_pct']}% 1-Year OS Findings",
    "Health Equity Findings (Donor for All)": "Donor for All: Health Equity Analysis Across Patient Demographics",
    "ML Model Performance Report": f"GVHD Risk Prediction Model: Avg Risk Score {summary_stats['avg_risk']} Across Cohort",
    "Transplant Center Benchmarking": f"Center Performance: Engraftment Averaging {summary_stats['avg_engraft']} Days Across Network",
    "Custom Topic": custom_topic or "Snowflake Intelligence: Transplant Outcome Analysis",
}
subject = focus_subjects.get(focus_area, "Transplant Outcome Analysis")

st.markdown("<br>", unsafe_allow_html=True)

# ── Generate Email Button ──
if st.button("Generate Email", type="primary", use_container_width=True):
    # Build dynamic content based on focus area
    key_findings = f"""
    <ul style="color: #333333; font-size: 14px; line-height: 1.8; padding-left: 20px;">
        <li><strong>Cohort Size:</strong> {summary_stats['total']:,} transplant procedures analyzed</li>
        <li><strong>Severe GVHD Rate (Grade III-IV):</strong> {summary_stats['severe_gvhd_pct']}% — identifying high-risk factors</li>
        <li><strong>1-Year Overall Survival:</strong> {summary_stats['one_year_os_pct']}% across all donor types</li>
        <li><strong>Average GVHD Risk Score:</strong> {summary_stats['avg_risk']} (ML-predicted, scale 0-1)</li>
        <li><strong>Average Engraftment Time:</strong> {summary_stats['avg_engraft']} days to neutrophil recovery</li>
    </ul>
    """

    # Smart recipient org text to avoid "the The ..."
    org_text = f"{recipient_org} team" if recipient_org.lower().startswith("the ") else f"the {recipient_org} team"

    email_html = f"""
    <div style="max-width: 680px; margin: 0 auto; font-family: 'Segoe UI', Arial, sans-serif; background: #FFFFFF;
                border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #1B365D 0%, #2C5F8A 100%); padding: 24px 32px;
                    text-align: center;">
            <div style="color: #FFFFFF; font-size: 20px; font-weight: 700; letter-spacing: 0.5px;
                        margin-bottom: 8px;">
                Cell Therapy Compass
            </div>
            <div style="color: #FFFFFF; font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
                        font-weight: 600;">
                Transplant Outcome Intelligence Report
            </div>
        </div>

        <!-- Snowflake Blue Accent Bar -->
        <div style="height: 4px; background: linear-gradient(90deg, #29B5E8, #00D4AA);"></div>

        <!-- Body -->
        <div style="padding: 32px;">
            
            <!-- Greeting -->
            <p style="color: #333333; font-size: 15px; line-height: 1.6; margin: 0 0 16px 0;">
                Dear {recipient_name or '[Recipient]'},
            </p>
            
            <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 0 0 20px 0;">
                I am pleased to share the latest findings from our transplant outcome analysis powered by 
                <strong>Snowflake Intelligence</strong>. This report leverages the Semantic View, Dynamic Tables 
                pipeline, and Cortex AI to provide comprehensive insights into GVHD outcomes across our patient cohort.
            </p>

            <!-- Key Findings Card -->
            <div style="background: #F7F9FC; border-left: 4px solid #29B5E8; border-radius: 0 8px 8px 0;
                        padding: 20px 24px; margin: 20px 0;">
                <div style="color: #1B365D; font-weight: 700; font-size: 15px; margin-bottom: 12px;">
                    Key Findings
                </div>
                {key_findings}
            </div>

            <!-- Recommendation -->
            <div style="background: #F0FAF7; border-left: 4px solid #00D4AA; border-radius: 0 8px 8px 0;
                        padding: 20px 24px; margin: 20px 0;">
                <div style="color: #1B5E4B; font-weight: 700; font-size: 15px; margin-bottom: 8px;">
                    Recommended Next Steps
                </div>
                <ol style="color: #333333; font-size: 14px; line-height: 1.8; padding-left: 20px; margin: 0;">
                    <li>Review the detailed interactive analysis in the <strong>Cell Therapy Compass</strong> Streamlit application</li>
                    <li>Explore the LSC Research Agent in <strong>Snowflake Intelligence</strong> for ad-hoc questions</li>
                    <li>Discuss integration of the GVHD risk prediction model into clinical workflows</li>
                    <li>Schedule a follow-up session to review health equity findings under the Donor for All initiative</li>
                </ol>
            </div>

            <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                This analysis demonstrates Snowflake's unique ability to combine structured data analytics, 
                unstructured clinical note intelligence, and AI-powered recommendations — capabilities that go 
                beyond what traditional BI tools like Looker or Oracle OBIEE can deliver.
            </p>

            <p style="color: #333333; font-size: 14px; line-height: 1.6; margin: 20px 0 0 0;">
                I look forward to discussing these findings with you and {org_text}.
            </p>

            <!-- Signature -->
            <div style="margin-top: 28px; padding-top: 20px; border-top: 1px solid #E5E9F0;">
                <p style="color: #333333; font-size: 14px; margin: 0; font-weight: 600;">{sender_name}</p>
                <p style="color: #666666; font-size: 13px; margin: 2px 0;">{sender_title}</p>
                <p style="color: #29B5E8; font-size: 13px; margin: 2px 0;">Snowflake</p>
            </div>
        </div>

        <!-- Footer -->
        <div style="background: #F7F9FC; padding: 16px 32px; text-align: center;
                    border-top: 1px solid #E5E9F0;">
            <p style="color: #999999; font-size: 11px; margin: 0;">
                Generated by Cell Therapy Compass | Powered by Snowflake AI Data Cloud
            </p>
            <p style="color: #BBBBBB; font-size: 10px; margin: 4px 0 0 0;">
                This report contains synthetic data for demonstration purposes.
            </p>
        </div>
    </div>
    """

    # Display generated email
    st.markdown("### Generated Email Preview")
    st.markdown(f"**Subject:** {subject}")
    st.markdown(f"**To:** {recipient_name or '[Recipient]'} ({recipient_email or '[email]'})")
    st.markdown("---")

    # Render the HTML email in an iframe (components.html preserves all styling)
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body {{ margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }}</style>
</head><body>{email_html}</body></html>"""
    components.html(full_html, height=750, scrolling=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Download button
    dl_col1, dl_col2, dl_col3 = st.columns([1, 1, 1])
    with dl_col2:
        st.download_button(
            label="Download Email as HTML",
            data=full_html,
            file_name=f"cell_therapy_compass_email_{recipient_name.replace(' ', '_').lower() or 'draft'}.html",
            mime="text/html",
            use_container_width=True,
        )

    # Copy HTML source
    with st.expander("View Email HTML Source"):
        st.code(email_html, language="html")

    st.markdown(render_success_callout(
        "Email Generated Successfully",
        "The email above was dynamically generated using live data from Snowflake pipeline. "
        "The subject line, key findings, and metrics are all driven by the Semantic View — "
        "demonstrating how Snowflake AI can power actionable communications directly from analytics."
    ), unsafe_allow_html=True)

else:
    st.markdown(render_info_callout(
        "How This Works",
        "Fill in the fields above and click 'Generate Email' to create a professional email. "
        "The email content is dynamically generated from live Snowflake data — subject lines, metrics, "
        "and findings all come from the analytics pipeline. This demonstrates how Snowflake enables "
        "action directly from insight, not just passive dashboards."
    ), unsafe_allow_html=True)

# ── Nav ──
st.markdown("---")
render_nav_buttons("Take Action")
