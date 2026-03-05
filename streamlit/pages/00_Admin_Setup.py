import streamlit as st

st.set_page_config(page_title="Admin Setup | LSC", page_icon="❄️", layout="wide")

from utils.styles import (
    apply_styles, render_header, render_section_separator,
    render_info_callout, render_success_callout, render_warning_callout,
    render_sql_block, render_pipeline_step,
)
from utils.navigation import render_sidebar, render_nav_buttons

apply_styles()
render_sidebar("Admin Setup")

render_header(
    "Lab Admin Setup",
    "Account admin provisioning, privilege reference, and post-lab cleanup",
)

# ── Overview ──
st.markdown("""
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 1.5rem 2rem; border: 1px solid rgba(41,181,232,0.3); margin-bottom: 1.5rem;">
    <p style="color: #FAFAFA; font-size: 0.95rem; line-height: 1.6; margin: 0;">
        This page helps the <strong style="color: #29B5E8;">Account Administrator</strong> provision
        the right access for lab participants, and clean up after the lab is complete.
        The lab supports <strong style="color: #00D4AA;">multi-user mode</strong> (5-20 participants)
        with per-user isolation: each participant gets their own role, warehouse, and schema
        while sharing read-only access to base tables.
    </p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB LAYOUT
# ═══════════════════════════════════════════════════════════════════════════
tab_setup, tab_reference, tab_websearch, tab_cleanup = st.tabs([
    "Pre-Lab Setup", "Privilege Reference", "Web Search", "Post-Lab Cleanup"
])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: PRE-LAB SETUP
# ═══════════════════════════════════════════════════════════════════════════
with tab_setup:
    st.markdown(render_section_separator(
        "Pre-Lab Setup (ACCOUNTADMIN Required)",
        "Run this script once before participants begin. It creates all infrastructure and grants."
    ), unsafe_allow_html=True)

    st.markdown(render_info_callout(
        "Who runs this?",
        "An Account Administrator runs this script once. For multi-user labs (5-20 participants), "
        "use sql/00_admin_provision.sql instead -- it creates per-user roles, warehouses, and schemas. "
        "The script below is for single-user mode. After provisioning, participants use their assigned "
        "role (MARROWCO_HOL_ROLE_<NN>) for scripts 03-08. No ACCOUNTADMIN access is needed by participants."
    ), unsafe_allow_html=True)

    # User list input
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**Lab Participants**")
    st.markdown(
        '<p style="color:#8892b0;font-size:0.85rem;">Enter Snowflake usernames (one per line) '
        'to grant them the lab role. For multi-user mode, use sql/00_admin_provision.sql '
        'and assign per-user roles (MARROWCO_HOL_ROLE_01, _02, etc.).</p>',
        unsafe_allow_html=True,
    )
    user_list = st.text_area(
        "Snowflake usernames",
        placeholder="JSMITH\nAJONES\nMLEE",
        height=120,
        label_visibility="collapsed",
    )

    users = [u.strip() for u in user_list.strip().splitlines() if u.strip()] if user_list else []

    # Build the grant script
    user_grants = ""
    if users:
        user_grants = "\n".join(
            f"GRANT ROLE MARROWCO_HOL_ROLE TO USER {u};" for u in users
        )
    else:
        user_grants = "-- GRANT ROLE MARROWCO_HOL_ROLE TO USER <USERNAME>;"

    bootstrap_sql = f"""-- ============================================================================
-- LSC Donor for All Data Lab — Pre-Lab Admin Setup
-- ============================================================================
-- Run as: ACCOUNTADMIN
-- Run when: ONCE, before participants begin the lab
-- Time: ~30 seconds
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 1. CREATE ROLE                                                         │
-- └─────────────────────────────────────────────────────────────────────────┘
CREATE ROLE IF NOT EXISTS MARROWCO_HOL_ROLE
    COMMENT = 'Role for LSC Donor for All Data Lab HOL';

GRANT ROLE MARROWCO_HOL_ROLE TO ROLE ACCOUNTADMIN;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 2. CREATE WAREHOUSE                                                    │
-- └─────────────────────────────────────────────────────────────────────────┘
CREATE WAREHOUSE IF NOT EXISTS MARROWCO_HOL_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for LSC Donor for All Data Lab HOL';

GRANT USAGE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;
GRANT OPERATE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 3. CREATE DATABASE & SCHEMA                                            │
-- └─────────────────────────────────────────────────────────────────────────┘
CREATE DATABASE IF NOT EXISTS MARROWCO_DONOR_LAB
    COMMENT = 'LSC Donor for All Data Lab';

GRANT OWNERSHIP ON DATABASE MARROWCO_DONOR_LAB TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

USE DATABASE MARROWCO_DONOR_LAB;

CREATE SCHEMA IF NOT EXISTS HOL
    COMMENT = 'Primary schema for Hands-on Lab artifacts';

GRANT OWNERSHIP ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 4. SCHEMA-LEVEL CREATE GRANTS                                          │
-- └─────────────────────────────────────────────────────────────────────────┘
GRANT CREATE TABLE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE VIEW ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE STAGE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE FILE FORMAT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE FUNCTION ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE PROCEDURE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE STREAMLIT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE DYNAMIC TABLE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE AGENT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE SEMANTIC VIEW ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE MODEL ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 5. ACCOUNT-LEVEL GRANTS                                                │
-- └─────────────────────────────────────────────────────────────────────────┘
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE MARROWCO_HOL_ROLE;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE;

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 6. GRANT ROLE TO PARTICIPANTS                                          │
-- └─────────────────────────────────────────────────────────────────────────┘
{user_grants}

-- ┌─────────────────────────────────────────────────────────────────────────┐
-- │ 7. (OPTIONAL) ENABLE WEB SEARCH FOR CORTEX AGENTS                     │
-- │    Only enable if your organization approves external web access.      │
-- └─────────────────────────────────────────────────────────────────────────┘
-- ALTER ACCOUNT SET ENABLE_CORTEX_WEBSEARCH = TRUE;

-- ============================================================================
-- DONE — Participants can now run scripts 01-08 using MARROWCO_HOL_ROLE
-- ============================================================================
SELECT 'Pre-lab setup complete. Participants can begin.' AS STATUS;"""

    st.markdown("<br>", unsafe_allow_html=True)
    st.code(bootstrap_sql, language="sql")

    st.markdown(render_success_callout(
        "What happens next?",
        "After running the script above, participants open a SQL worksheet, set their role to "
        "MARROWCO_HOL_ROLE, and run scripts 01 through 08 in order. No ACCOUNTADMIN access is needed."
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: PRIVILEGE REFERENCE
# ═══════════════════════════════════════════════════════════════════════════
with tab_reference:
    st.markdown(render_section_separator(
        "Privilege Reference",
        "Which scripts need ACCOUNTADMIN vs. MARROWCO_HOL_ROLE"
    ), unsafe_allow_html=True)

    st.markdown(render_info_callout(
        "Architecture",
        "The lab follows a two-role model: ACCOUNTADMIN bootstraps the environment once, "
        "then MARROWCO_HOL_ROLE handles everything else. This mirrors real-world best "
        "practices where admins provision access and users operate within their grants."
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ACCOUNTADMIN scripts
    st.markdown("### Scripts Requiring ACCOUNTADMIN (3 of 11)")
    st.markdown("""
<div style="background: rgba(255,107,107,0.08); border-left: 4px solid #FF6B6B; border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem; margin: 0.5rem 0;">
    <table style="width:100%; border-collapse: collapse; color: #FAFAFA; font-size: 0.85rem;">
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.5rem 0; width: 25%;"><strong style="color:#FF6B6B;">00_bootstrap.sql</strong></td>
            <td style="padding: 0.5rem 0; color: #8892b0;">
                CREATE ROLE, CREATE WAREHOUSE, CREATE DATABASE, GRANT OWNERSHIP,
                all schema-level CREATE grants, GRANT EXECUTE MANAGED TASK ON ACCOUNT,
                GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER, GRANT CREATE MODEL
            </td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.5rem 0;"><strong style="color:#FF6B6B;">09_grants.sql</strong></td>
            <td style="padding: 0.5rem 0; color: #8892b0;">
                GRANT ROLE TO USER, GRANT DATABASE ROLE, ALTER ACCOUNT SET (web search),
                GRANT USAGE/SELECT on objects
            </td>
        </tr>
        <tr>
            <td style="padding: 0.5rem 0;"><strong style="color:#FF6B6B;">10_teardown.sql</strong></td>
            <td style="padding: 0.5rem 0; color: #8892b0;">
                DROP DATABASE, DROP WAREHOUSE, DROP ROLE (destructive cleanup)
            </td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # HOL_ROLE scripts
    st.markdown("### Scripts Using Only MARROWCO_HOL_ROLE (8 of 11)")
    st.markdown("""
<div style="background: rgba(0,212,170,0.08); border-left: 4px solid #00D4AA; border-radius: 0 12px 12px 0;
            padding: 1rem 1.25rem; margin: 0.5rem 0;">
    <table style="width:100%; border-collapse: collapse; color: #FAFAFA; font-size: 0.85rem;">
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0; width: 30%;"><strong style="color:#00D4AA;">01_create_tables.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE TABLE (Transplant Outcomes, Clinical Notes)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">02_load_data.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">Stage upload, COPY INTO tables</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">03_dynamic_tables.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE DYNAMIC TABLE (Silver + Gold layers)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">04_cortex_search.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE CORTEX SEARCH SERVICE on clinical notes</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">05_semantic_view.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE SEMANTIC VIEW (single source of truth)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">06_create_agent.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE AGENT (4 tools: Analyst, Search, Chart, Web Search)</td>
        </tr>
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">07_snowflake_intelligence.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">UI instructions only (no DDL)</td>
        </tr>
        <tr>
            <td style="padding: 0.4rem 0;"><strong style="color:#00D4AA;">08_ml_model.sql</strong></td>
            <td style="padding: 0.4rem 0; color: #8892b0;">CREATE ML.CLASSIFICATION model, training data, predictions</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual pipeline
    st.markdown("### Lab Execution Flow")
    st.markdown(render_pipeline_step(
        0, "Admin: Run 00_bootstrap.sql",
        "ACCOUNTADMIN creates role, warehouse, database, and grants. (~30 seconds)",
        "#FF6B6B"
    ), unsafe_allow_html=True)
    for i, (script, desc) in enumerate([
        ("01_create_tables.sql", "Create Bronze landing tables"),
        ("02_load_data.sql", "Upload CSV files and load into tables"),
        ("03_dynamic_tables.sql", "Create Silver + Gold Dynamic Tables pipeline"),
        ("04_cortex_search.sql", "Create Cortex Search Service on clinical notes"),
        ("05_semantic_view.sql", "Create Semantic View (single source of truth)"),
        ("06_create_agent.sql", "Create Cortex Agent with 4 tools"),
        ("07_snowflake_intelligence.sql", "Connect agent to Snowflake Intelligence (UI)"),
        ("08_ml_model.sql", "Train GVHD risk prediction ML model"),
    ], 1):
        st.markdown(render_pipeline_step(
            i, f"Participant: Run {script}", desc, "#00D4AA"
        ), unsafe_allow_html=True)
    st.markdown(render_pipeline_step(
        9, "Admin: Run 09_grants.sql (optional)",
        "Grant role to additional users, enable web search",
        "#FF6B6B"
    ), unsafe_allow_html=True)
    st.markdown(render_pipeline_step(
        10, "Admin: Run 10_teardown.sql (post-lab)",
        "Drop all objects, warehouse, and role",
        "#FF6B6B"
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Grants detail
    st.markdown("### Complete Grant Summary for MARROWCO_HOL_ROLE")
    st.markdown("""
<div style="background: linear-gradient(145deg, #1a1f35 0%, #0d1117 100%); border-radius: 16px;
            padding: 1.5rem 2rem; border: 1px solid rgba(255,255,255,0.1); margin: 0.5rem 0;">
    <table style="width:100%; border-collapse: collapse; color: #FAFAFA; font-size: 0.85rem;">
        <thead>
            <tr style="border-bottom: 2px solid #29B5E8;">
                <th style="text-align:left; padding: 0.5rem 0; color: #29B5E8;">Grant</th>
                <th style="text-align:left; padding: 0.5rem 0; color: #29B5E8;">Scope</th>
                <th style="text-align:left; padding: 0.5rem 0; color: #29B5E8;">Enables</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">OWNERSHIP</td>
                <td style="color: #8892b0;">DATABASE, SCHEMA</td>
                <td style="color: #8892b0;">Full control of lab objects</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">USAGE, OPERATE</td>
                <td style="color: #8892b0;">WAREHOUSE</td>
                <td style="color: #8892b0;">Run queries, resume warehouse</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE TABLE/VIEW/STAGE/...</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">All DDL within HOL schema</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE DYNAMIC TABLE</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">Dynamic Tables pipeline</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE CORTEX SEARCH SERVICE</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">Cortex Search on clinical notes</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE AGENT</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">Cortex Agent creation</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE SEMANTIC VIEW</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">Semantic View for Cortex Analyst</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE MODEL</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">ML model training and registry</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">CREATE STREAMLIT</td>
                <td style="color: #8892b0;">SCHEMA</td>
                <td style="color: #8892b0;">Deploy Streamlit app</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 0.4rem 0; color: #00D4AA;">EXECUTE MANAGED TASK</td>
                <td style="color: #8892b0;">ACCOUNT</td>
                <td style="color: #8892b0;">Dynamic Table refresh scheduling</td>
            </tr>
            <tr>
                <td style="padding: 0.4rem 0; color: #00D4AA;">SNOWFLAKE.CORTEX_USER</td>
                <td style="color: #8892b0;">DATABASE ROLE</td>
                <td style="color: #8892b0;">Cortex AI functions (COMPLETE, SUMMARIZE, etc.)</td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: WEB SEARCH
# ═══════════════════════════════════════════════════════════════════════════
with tab_websearch:
    st.markdown(render_section_separator(
        "Web Search Enablement (Optional)",
        "Account-level parameter to enable the Research Agent's web search tool"
    ), unsafe_allow_html=True)

    st.markdown(render_info_callout(
        "What does this enable?",
        "The Research Agent includes a web_search tool that finds the latest GVHD research, "
        "clinical trial results, and transplant publications from the public web. "
        "Without this parameter enabled, web search queries return an error. "
        "All other agent tools (Analyst, Search, Chart) work without it."
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**To enable (ACCOUNTADMIN required):**")
    st.code("ALTER ACCOUNT SET ENABLE_CORTEX_WEBSEARCH = TRUE;", language="sql")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**To disable after the lab:**")
    st.code("ALTER ACCOUNT UNSET ENABLE_CORTEX_WEBSEARCH;", language="sql")

    st.markdown(render_warning_callout(
        "Security Note",
        "This is an account-level setting that enables web search for ALL Cortex Agents in the account. "
        "When enabled, the agent can make outbound requests to the public internet to retrieve search results. "
        "Only enable if your organization approves external web access for AI features."
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(render_success_callout(
        "Without web search",
        "The lab is fully functional without web search. The agent still answers questions using "
        "Cortex Analyst (structured data), Cortex Search (clinical notes), and Data-to-Chart "
        "(visualizations). Web search is an optional enhancement for demo purposes."
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: POST-LAB CLEANUP
# ═══════════════════════════════════════════════════════════════════════════
with tab_cleanup:
    st.markdown(render_section_separator(
        "Post-Lab Cleanup (ACCOUNTADMIN Required)",
        "Revoke all permissions and remove all lab artifacts"
    ), unsafe_allow_html=True)

    st.markdown(render_warning_callout(
        "Destructive Operation",
        "This script permanently deletes ALL lab data, models, agents, and objects. "
        "Run only when the lab is complete and participants no longer need access."
    ), unsafe_allow_html=True)

    # Build revoke script with user list
    user_revokes = ""
    if users:
        user_revokes = "\n".join(
            f"REVOKE ROLE MARROWCO_HOL_ROLE FROM USER {u};" for u in users
        )
    else:
        user_revokes = "-- REVOKE ROLE MARROWCO_HOL_ROLE FROM USER <USERNAME>;"

    teardown_sql = f"""-- ============================================================================
-- LSC Donor for All Data Lab -- Post-Lab Cleanup
-- ============================================================================
-- Run as: ACCOUNTADMIN
-- Run when: After the lab is complete
-- WARNING: This is DESTRUCTIVE and IRREVERSIBLE
--
-- For multi-user mode, use sql/00_admin_teardown.sql instead -- it drops
-- all per-user environments (roles, warehouses, schemas) in a loop.
-- The script below handles single-user mode cleanup.
-- ============================================================================

USE ROLE ACCOUNTADMIN;

-- 1. REVOKE ROLE FROM PARTICIPANTS
{user_revokes}

-- 2. DISABLE WEB SEARCH (if it was enabled)
ALTER ACCOUNT UNSET ENABLE_CORTEX_WEBSEARCH;

-- 3. DROP DATABASE (cascades all schemas, tables, DTs, agents, models, etc.)
DROP DATABASE IF EXISTS MARROWCO_DONOR_LAB;

-- 4. DROP WAREHOUSE
DROP WAREHOUSE IF EXISTS MARROWCO_HOL_WH;

-- 5. REVOKE ACCOUNT-LEVEL GRANTS & DROP ROLE
-- REVOKE EXECUTE MANAGED TASK ON ACCOUNT FROM ROLE MARROWCO_HOL_ROLE;
DROP ROLE IF EXISTS MARROWCO_HOL_ROLE;

-- ============================================================================
-- DONE -- All lab artifacts have been removed
-- ============================================================================
SELECT 'Teardown complete -- all lab artifacts removed.' AS STATUS;"""

    st.markdown("<br>", unsafe_allow_html=True)
    st.code(teardown_sql, language="sql")

    st.markdown(render_success_callout(
        "Clean slate",
        "After running this script, the account is returned to its pre-lab state. "
        "No lab artifacts, roles, warehouses, or databases remain."
    ), unsafe_allow_html=True)


# ── Nav ──
st.markdown("---")
render_nav_buttons("Admin Setup")
