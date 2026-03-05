/*=============================================================================
  LSC Donor for All Data Lab -- Grants & Permissions
  =============================================================================
  
  MULTI-USER NOTE:
    In multi-user mode, all grants are handled by 00_admin_provision.sql.
    This script is kept for reference and for enabling optional account-level
    features like web search.

  This script covers:
    1. Enabling web search for Cortex Agents (account-level, optional)
    2. Role assignment examples for multi-user mode
    3. Verification queries
  
  Run after: All other scripts
  =============================================================================*/

USE ROLE ACCOUNTADMIN;

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
-- ║ Grant Cortex AI access (already handled in provisioning, shown here      ║
-- ║ for reference if running in single-user mode)                            ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Single-user mode only:
-- GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE;

-- Multi-user mode: already granted per-user in 00_admin_provision.sql
-- GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE_01;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Assign per-user roles to actual Snowflake users                          ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Replace <USERNAME> with actual Snowflake login names.                    ║
-- ║ Each participant gets ONE role.                                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- GRANT ROLE MARROWCO_HOL_ROLE_01 TO USER JSMITH;
-- GRANT ROLE MARROWCO_HOL_ROLE_02 TO USER JDOE;
-- GRANT ROLE MARROWCO_HOL_ROLE_03 TO USER AGARCIA;
-- ...

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ Verify grants for a specific user                                        ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Check what a per-user role can access:
-- SHOW GRANTS TO ROLE MARROWCO_HOL_ROLE_01;

-- Check shared schema access:
-- SHOW GRANTS ON SCHEMA MARROWCO_DONOR_LAB.HOL;

-- Check per-user schema access:
-- SHOW GRANTS ON SCHEMA MARROWCO_DONOR_LAB.HOL_USER_01;

-- Verify a user's role assignments:
-- SHOW GRANTS TO USER JSMITH;
