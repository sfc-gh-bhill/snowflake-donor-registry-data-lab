import streamlit as st

st.set_page_config(page_title="Research Agent | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_metric_card, render_info_callout,
    render_section_separator, tooltip
)
from utils.navigation import render_sidebar, render_nav_buttons, get_snowflake_session
import json, re
import _snowflake
import streamlit.components.v1 as components

apply_styles()
render_sidebar("Research Agent")

render_header("LSC Research Agent", f"AI-Powered Transplant Outcome Intelligence — Structured + Unstructured")

session = get_snowflake_session()

# ── Constants ──
AGENT_API_ENDPOINT = "/api/v2/cortex/agent:run"
AGENT_API_TIMEOUT_MS = 60000

# ── Resolve per-user schema for agent tool_resources ──
_DB = "MARROWCO_DONOR_LAB"
_SCHEMA = "HOL"
if session:
    try:
        _DB = session.get_current_database() or _DB
        _SCHEMA = session.get_current_schema() or _SCHEMA
    except Exception:
        pass
_FQN_PREFIX = f"{_DB}.{_SCHEMA}"


def _extract_from_event(data: dict, text_parts: list, sql_parts: list):
    """Extract text and SQL from a single event dict in any known format."""
    # The _snowflake API returns events where delta.content is a LIST of content blocks
    delta = data.get("delta", {})
    content = delta.get("content")

    # delta.content as a list of content blocks (primary format from _snowflake)
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if btype == "text":
                text_parts.append(block.get("text", ""))
            elif btype == "tool_results":
                tr = block.get("tool_results", {})
                tr_content = tr.get("content", [])
                if isinstance(tr_content, list):
                    for tc in tr_content:
                        if isinstance(tc, dict) and tc.get("type") == "json":
                            jr = tc.get("json", {})
                            if isinstance(jr, dict):
                                if "text" in jr:
                                    text_parts.append(jr["text"])
                                if "sql" in jr:
                                    sql_parts.append(f"\n\n```sql\n{jr['sql']}\n```")
                elif isinstance(tr_content, dict):
                    jr = tr_content.get("json", {})
                    if isinstance(jr, dict):
                        if "text" in jr:
                            text_parts.append(jr["text"])
                        if "sql" in jr:
                            sql_parts.append(f"\n\n```sql\n{jr['sql']}\n```")

    # delta.content as a single dict (alternate format)
    elif isinstance(content, dict):
        ctype = content.get("type", "")
        if ctype == "text":
            text_parts.append(content.get("text", ""))
        elif ctype in ("tool_results", "tool_use"):
            tr = content.get("tool_results", {}).get("content", {})
            if isinstance(tr, dict):
                jr = tr.get("json", {})
                if isinstance(jr, dict):
                    if "text" in jr:
                        text_parts.append(jr["text"])
                    if "sql" in jr:
                        sql_parts.append(f"\n\n```sql\n{jr['sql']}\n```")

    # Top-level content list (non-streaming / final message)
    top_content = data.get("content", [])
    if isinstance(top_content, list) and not delta:
        for block in top_content:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

    # Messages array (complete response)
    msgs = data.get("messages", [])
    if isinstance(msgs, list):
        for msg in msgs:
            if isinstance(msg, dict):
                for part in (msg.get("content") or []):
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))

    # Nested "data" key (event wrapper — e.g., {"event":"...", "data":{...}})
    inner_data = data.get("data")
    if isinstance(inner_data, str):
        try:
            inner = json.loads(inner_data)
            if isinstance(inner, dict):
                _extract_from_event(inner, text_parts, sql_parts)
        except (json.JSONDecodeError, TypeError):
            pass
    elif isinstance(inner_data, dict):
        _extract_from_event(inner_data, text_parts, sql_parts)


# ── Agent REST API Helper ──
def call_agent_api(session, user_query: str) -> dict:
    """Call the Cortex Agent via _snowflake.send_snow_api_request (warehouse runtime).
    Returns dict with keys: text, sql, error."""
    try:
        payload = {
            "model": "llama3.1-70b",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_query}]
                }
            ],
            "tools": [
                {"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "transplant_analyst"}},
                {"tool_spec": {"type": "cortex_search", "name": "clinical_notes_search"}},
                {"tool_spec": {"type": "data_to_chart", "name": "chart_generator"}},
                {"tool_spec": {"type": "web_search", "name": "research_search"}},
            ],
            "tool_resources": {
                "transplant_analyst": {
                    "semantic_view": f"{_FQN_PREFIX}.MARROWCO_TRANSPLANT_ANALYTICS"
                },
                "clinical_notes_search": {
                    "name": f"{_FQN_PREFIX}.CLINICAL_NOTES_SEARCH",
                    "max_results": 5
                }
            }
        }

        resp = _snowflake.send_snow_api_request(
            "POST",
            AGENT_API_ENDPOINT,
            {},   # headers
            {},   # params
            payload,
            None, # body (use payload as json)
            AGENT_API_TIMEOUT_MS,
        )

        status = resp.get("status", 0)
        if status != 200:
            reason = resp.get("reason", "(no reason)")
            body = resp.get("content", "")[:500]
            return {"text": "", "sql": "", "error": f"Agent API error (HTTP {status}): {reason}\n{body}"}

        raw = resp.get("content", "")

        # The response may be a JSON string or a raw SSE stream.
        # First, try to parse the entire response as JSON (list of events).
        text_parts = []
        sql_parts = []

        # Try JSON array parse first (common _snowflake response format)
        try:
            content_parsed = json.loads(raw) if isinstance(raw, str) else raw

            # If it's a list of event objects (e.g., [{"event":"...", "data":"..."},...])
            if isinstance(content_parsed, list):
                for item in content_parsed:
                    if isinstance(item, dict):
                        _extract_from_event(item, text_parts, sql_parts)
                if text_parts or sql_parts:
                    return {"text": "".join(text_parts), "sql": "".join(sql_parts), "error": ""}

            # If it's a single dict response
            if isinstance(content_parsed, dict):
                _extract_from_event(content_parsed, text_parts, sql_parts)
                if text_parts or sql_parts:
                    return {"text": "".join(text_parts), "sql": "".join(sql_parts), "error": ""}

        except (json.JSONDecodeError, TypeError):
            pass

        # Fallback: Parse as SSE streaming response (line-by-line)
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line.startswith("data:"):
                data_str = line[5:].strip()
            elif line.startswith("event:"):
                continue
            else:
                data_str = line

            if not data_str or data_str == "[DONE]":
                continue

            try:
                data = json.loads(data_str)
                _extract_from_event(data, text_parts, sql_parts)
            except (json.JSONDecodeError, KeyError, TypeError):
                continue

        if text_parts or sql_parts:
            return {"text": "".join(text_parts), "sql": "".join(sql_parts), "error": ""}
        return {"text": "", "sql": "", "error": "The agent returned an empty response. Try rephrasing your question."}

    except Exception as e:
        return {"text": "", "sql": "", "error": f"Agent API call failed: {str(e)}"}

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

components.html("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body { margin: 0; padding: 0; background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }</style>
</head><body>
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 0;">
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem;">
        <div style="text-align: center; padding: 1.25rem; background: rgba(41,181,232,0.1); border-radius: 12px;
                    border: 1px solid rgba(41,181,232,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">&#x1F4CA;</div>
            <div style="color: #29B5E8; font-weight: 700; font-size: 0.95rem;">Cortex Analyst</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Queries structured transplant data via the Semantic View.
                Uses verified queries for trusted answers.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(0,212,170,0.1); border-radius: 12px;
                    border: 1px solid rgba(0,212,170,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">&#x1F50D;</div>
            <div style="color: #00D4AA; font-weight: 700; font-size: 0.95rem;">Cortex Search</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Searches 800 clinical notes using hybrid vector + keyword search.
                Finds treatment responses, clinical evidence.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(255,183,77,0.1); border-radius: 12px;
                    border: 1px solid rgba(255,183,77,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">&#x1F4C8;</div>
            <div style="color: #FFB74D; font-weight: 700; font-size: 0.95rem;">Data-to-Chart</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Generates visualizations from query results.
                Bar charts, trends, comparisons on demand.
            </div>
        </div>
        <div style="text-align: center; padding: 1.25rem; background: rgba(255,107,107,0.1); border-radius: 12px;
                    border: 1px solid rgba(255,107,107,0.3);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">&#x1F310;</div>
            <div style="color: #FF6B6B; font-weight: 700; font-size: 0.95rem;">Web Search</div>
            <div style="color: #8892b0; font-size: 0.75rem; margin-top: 0.25rem;">
                Searches the web for latest GVHD research, clinical trials, and publications.
            </div>
        </div>
    </div>
</div>
</body></html>""", height=250, scrolling=False)

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
            result = call_agent_api(session, user_input)

        if result["error"]:
            st.error(result["error"])
            st.session_state.agent_messages.append({"role": "assistant", "content": result["error"]})
        else:
            # Show the agent's text interpretation
            if result["text"]:
                st.markdown(result["text"])

            # Extract raw SQL from the sql_parts (strip markdown fences)
            raw_sql = result["sql"]
            sql_query = ""
            if raw_sql:
                # Remove markdown code fences if present
                match = re.search(r"```sql\s*(.*?)\s*```", raw_sql, re.DOTALL)
                if match:
                    sql_query = match.group(1).strip()
                else:
                    sql_query = raw_sql.strip()

            # Execute the SQL and display results
            if sql_query:
                # Strip trailing comments
                sql_clean = re.sub(r"--[^\n]*$", "", sql_query).strip().rstrip(";")
                try:
                    df = session.sql(sql_clean).to_pandas()
                    if not df.empty:
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("The query returned no results.")
                except Exception as e:
                    st.warning(f"Could not execute the generated query: {str(e)}")

                # Show SQL in expander
                with st.expander("View Generated SQL"):
                    st.code(sql_query, language="sql")

            # Build the stored message (text only, table renders live)
            display_msg = result["text"] or "See the results above."
            st.session_state.agent_messages.append({"role": "assistant", "content": display_msg})

elif user_input and not session:
    with st.chat_message("assistant"):
        msg = ("I'm not connected to Snowflake right now. To use the Research Agent:\n\n"
               "1. Run the SQL scripts in order (00-06)\n"
               "2. Connect this app to your Snowflake account\n"
               "3. The agent will be available for natural language questions\n\n"
               "**Tip:** You can also test the agent in Snowflake Intelligence (AI & ML > Snowflake Intelligence).")
        st.markdown(msg)
        st.session_state.agent_messages.append({"role": "assistant", "content": msg})

st.markdown("<br>", unsafe_allow_html=True)

# ── Snowflake Intelligence Link ──
st.markdown(render_section_separator(
    "Snowflake Intelligence",
    "The full agent experience with auto-suggested questions, charts, and conversation history"
), unsafe_allow_html=True)

st.markdown(f"""
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 1.5rem 2rem; border: 1px solid rgba(41,181,232,0.3); margin: 1rem 0;">
    <p style="color: #FAFAFA; font-size: 0.95rem; line-height: 1.6;">
        For the full agent experience, use <strong style="color: #29B5E8;">Snowflake Intelligence</strong>:
    </p>
    <ol style="color: #8892b0; font-size: 0.85rem; line-height: 1.8; padding-left: 1.5rem;">
        <li>Navigate to <strong>AI &amp; ML &gt; Snowflake Intelligence</strong> in Snowsight</li>
        <li>Click <strong>"New Analyst"</strong> and select <strong>"Use an Agent"</strong></li>
        <li>Choose your agent: <strong>{_FQN_PREFIX}.MARROWCO_RESEARCH_AGENT</strong></li>
        <li>Verified queries appear as suggested questions automatically</li>
    </ol>
    <p style="color: #00D4AA; font-size: 0.85rem; margin-top: 0.5rem; font-weight: 600;">
        Snowflake Intelligence shows the WHO, WHAT, WHERE, WHEN, WHY, and HOW —
        plus actionable recommendations. No other BI tool does this.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Nav ──
st.markdown("---")
render_nav_buttons("Research Agent")
