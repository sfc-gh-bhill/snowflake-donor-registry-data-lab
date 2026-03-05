import streamlit as st

st.set_page_config(page_title="Research Agent | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_info_callout,
    render_section_separator
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session

apply_styles()
render_sidebar("Research Agent")

render_header("LSC Research Agent", "AI-Powered Transplant Outcome Intelligence — Structured + Unstructured")

session = get_snowflake_session()

# ── KPI Tiles ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(render_metric_card("4", "Agent Tools", "Analyst + Search + Chart + Web"), unsafe_allow_html=True)
with col2:
    st.markdown(render_metric_card("8", "Verified Queries", "Trust Layer"), unsafe_allow_html=True)
with col3:
    st.markdown(render_metric_card("800", "Clinical Notes", "Searchable via Cortex"), unsafe_allow_html=True)
with col4:
    st.markdown(render_metric_card("500", "Structured Records", "Queryable via Analyst"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── How the Agent Works ──
st.markdown(render_section_separator(
    "How the LSC Research Agent Works",
    "An autonomous AI that reasons about which tools to use for each question"
), unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem;">
        <div style="text-align: center; padding: 1.25rem; background: rgba(41,181,232,0.1); border-radius: 12px;
                    border: 1px solid rgba(41,181,232,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
            <div style="color: #29B5E8; font-weight: 700; font-size: 0.95rem;">Cortex Analyst</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Queries structured transplant data via the Semantic View. 
                Uses verified queries for trusted answers.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(0,212,170,0.1); border-radius: 12px;
                    border: 1px solid rgba(0,212,170,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔍</div>
            <div style="color: #00D4AA; font-weight: 700; font-size: 0.95rem;">Cortex Search</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Searches 800 clinical notes using hybrid vector + keyword search.
                Finds treatment responses, clinical evidence.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(255,183,77,0.1); border-radius: 12px;
                    border: 1px solid rgba(255,183,77,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
            <div style="color: #FFB74D; font-weight: 700; font-size: 0.95rem;">Data-to-Chart</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Generates visualizations from query results.
                Bar charts, trends, comparisons on demand.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(255,107,107,0.1); border-radius: 12px;
                    border: 1px solid rgba(255,107,107,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌐</div>
            <div style="color: #FF6B6B; font-weight: 700; font-size: 0.95rem;">Web Search</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Searches the web for latest GVHD research, clinical trials, and publications.
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(render_info_callout(
    "Agent Autonomy",
    "The agent decides which tool(s) to use based on the question. A structured data question uses Analyst. "
    "A clinical evidence question uses Search. A complex question uses BOTH, then synthesizes the answer. "
    "This is fundamentally different from traditional BI where users must know which dashboard to open."
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chat Interface ──
st.markdown(render_section_separator(
    "Ask the Research Agent",
    "Type a question below or select a suggested question"
), unsafe_allow_html=True)

# Suggested questions
suggested_questions = [
    "What is the overall GVHD rate by donor type?",
    "Compare survival rates between matched and mismatched donors",
    "What do clinical notes say about severe GVHD treatment responses?",
    "How does social vulnerability affect transplant outcomes?",
    "Which patient populations have the worst outcomes?",
    "What is the impact of PTCy on haploidentical outcomes?",
]

st.markdown("**Suggested Questions:**")
sq_cols = st.columns(3)
selected_suggestion = None
for i, q in enumerate(suggested_questions):
    with sq_cols[i % 3]:
        if st.button(q, key=f"sq_{i}", use_container_width=True):
            selected_suggestion = q

# Chat state
if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = []

user_input = st.chat_input("Ask the LSC Research Agent a question...")
if selected_suggestion:
    user_input = selected_suggestion

if user_input:
    st.session_state.agent_messages.append({"role": "user", "content": user_input})

# Display chat history
for msg in st.session_state.agent_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Process new message
if user_input and session:
    with st.chat_message("assistant"):
        with st.spinner("Research Agent is thinking..."):
            try:
                result = session.sql(f"""
                    SELECT SNOWFLAKE.CORTEX.INVOKE_AGENT(
                        'MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT',
                        '{user_input.replace("'", "''")}'
                    ) AS RESPONSE
                """).collect()
                response = result[0]["RESPONSE"] if result else "No response received."
                st.markdown(response)
                st.session_state.agent_messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Agent call failed: {str(e)}\n\nMake sure you've run `sql/06_create_agent.sql` first."
                st.error(error_msg)
                st.session_state.agent_messages.append({"role": "assistant", "content": error_msg})

elif user_input and not session:
    with st.chat_message("assistant"):
        msg = ("I'm not connected to The Winter Cloud Platform right now. To use the Research Agent:\n\n"
               "1. Run the SQL scripts in order (00-06)\n"
               "2. Connect this app to your The Winter Cloud Platform account\n"
               "3. The agent will be available for natural language questions\n\n"
               "**Tip:** You can also test the agent in The Winter Cloud Platform Intelligence (AI & ML > The Winter Cloud Platform Intelligence).")
        st.markdown(msg)
        st.session_state.agent_messages.append({"role": "assistant", "content": msg})

st.markdown("<br>", unsafe_allow_html=True)

# ── The Winter Cloud Platform Intelligence Link ──
st.markdown(render_section_separator(
    "The Winter Cloud Platform Intelligence",
    "The full agent experience with auto-suggested questions, charts, and conversation history"
), unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 1.5rem 2rem; border: 1px solid rgba(41,181,232,0.3); margin: 1rem 0;">
    <p style="color: #FAFAFA; font-size: 0.95rem; line-height: 1.6;">
        For the full agent experience, use <strong style="color: #29B5E8;">The Winter Cloud Platform Intelligence</strong>:
    </p>
    <ol style="color: #8892b0; font-size: 0.85rem; line-height: 1.8; padding-left: 1.5rem;">
        <li>Navigate to <strong>AI & ML > The Winter Cloud Platform Intelligence</strong> in Snowsight</li>
        <li>Click <strong>"New Analyst"</strong> and select <strong>"Use an Agent"</strong></li>
        <li>Choose <strong>MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT</strong></li>
        <li>Verified queries appear as suggested questions automatically</li>
    </ol>
    <p style="color: #00D4AA; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">
        The Winter Cloud Platform Intelligence shows the WHO, WHAT, WHERE, WHEN, WHY, and HOW — 
        plus actionable recommendations. No other BI tool does this.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Nav ──
st.markdown("---")
render_nav_buttons("Research Agent")
