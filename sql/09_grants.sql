/*=============================================================================
  LSC Donor for All Data Lab — Grants & Permissions
  =============================================================================
  
  Additional grants for sharing access with other team members.
  Run this if you need to give other users access to the HOL artifacts.
  
  Run after: All other scripts
  =============================================================================*/

USE ROLE ACCOUNTADMIN;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Grant MARROWCO_HOL_ROLE to additional users                                  ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Replace '<USERNAME>' with the actual Snowflake username                  ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- GRANT ROLE MARROWCO_HOL_ROLE TO USER <USERNAME>;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Grant Cortex AI access (required for AI functions)                       ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Ensure Cortex functions are available
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Enable web_search for Agent (account-level setting)                      ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ NOTE: This requires ACCOUNTADMIN and enables web search for the entire   ║
-- ║ account. Only run if your organization approves external web access.     ║
-- ║                                                                          ║
-- ║ The Research Agent includes a web_search tool for finding latest GVHD    ║
-- ║ research and clinical trial publications. Without this parameter,        ║
-- ║ web search queries will return an error.                                 ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Uncomment the line below to enable web search for Cortex Agents:
-- ALTER ACCOUNT SET ENABLE_CORTEX_WEBSEARCH = TRUE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Streamlit deployment grants                                              ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

GRANT USAGE ON DATABASE MARROWCO_DONOR_LAB TO ROLE MARROWCO_HOL_ROLE;
GRANT USAGE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT SELECT ON ALL DYNAMIC TABLES IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT SELECT ON ALL VIEWS IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
-- Semantic views: MARROWCO_HOL_ROLE already owns these (OWNERSHIP grants full access)
GRANT USAGE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify all grants                                                        ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
SHOW GRANTS TO ROLE MARROWCO_HOL_ROLE;
