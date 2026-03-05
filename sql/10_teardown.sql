/*=============================================================================
  LSC Donor for All Data Lab -- Participant Teardown
  =============================================================================
  
  Removes YOUR per-user lab artifacts from the Snowflake account.
  Run this when you are finished with the lab to clean up your resources.

  WARNING: This script is DESTRUCTIVE and IRREVERSIBLE.
  All YOUR objects (DTs, models, agents, search services, Streamlit apps)
  will be permanently deleted.
  
  WHAT THIS REMOVES (your per-user schema and everything in it):
    - Streamlit App:  CELL_THERAPY_COMPASS
    - Agent:          MARROWCO_RESEARCH_AGENT
    - ML Model:       GVHD_RISK_MODEL
    - Semantic View:  MARROWCO_TRANSPLANT_ANALYTICS
    - Search Service: CLINICAL_NOTES_SEARCH
    - Dynamic Tables: DT_GVHD_ANALYTICS, DT_TRANSPLANT_ENRICHED
    - Tables:         ML_PREDICTIONS, ML_TRAINING_DATA
    - Schema:         MARROWCO_DONOR_LAB.HOL_USER_<NN>

  WHAT THIS DOES NOT REMOVE (admin-managed shared resources):
    - Database:       MARROWCO_DONOR_LAB
    - Shared Schema:  MARROWCO_DONOR_LAB.HOL (base tables, stage, file format)
    - Warehouse:      MARROWCO_HOL_WH_<NN> (admin removes via 00_admin_teardown.sql)
    - Role:           MARROWCO_HOL_ROLE_<NN> (admin removes via 00_admin_teardown.sql)

  FOR FULL TEARDOWN (admin only):
    Run 00_admin_teardown.sql to remove ALL user environments and shared infra.
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- SET YOUR USER NUMBER (assigned by the lab admin)
-- ════════════════════════════════════════════════════════════════════════════
SET USER_NUM = '01';  -- << CHANGE THIS TO YOUR ASSIGNED NUMBER (01-20)

USE ROLE IDENTIFIER('MARROWCO_HOL_ROLE_' || $USER_NUM);
USE WAREHOUSE IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM);

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 1: Drop AI/ML Objects (before dropping schema)
-- ════════════════════════════════════════════════════════════════════════════

USE SCHEMA IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM);

-- Agent
DROP AGENT IF EXISTS MARROWCO_RESEARCH_AGENT;

-- ML Model
DROP MODEL IF EXISTS GVHD_RISK_MODEL;

-- Semantic View
DROP SEMANTIC VIEW IF EXISTS MARROWCO_TRANSPLANT_ANALYTICS;

-- Cortex Search Service
DROP CORTEX SEARCH SERVICE IF EXISTS CLINICAL_NOTES_SEARCH;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 2: Drop Dynamic Tables
-- ════════════════════════════════════════════════════════════════════════════

-- Gold layer first (depends on Silver)
DROP DYNAMIC TABLE IF EXISTS DT_GVHD_ANALYTICS;

-- Silver layer
DROP DYNAMIC TABLE IF EXISTS DT_TRANSPLANT_ENRICHED;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 3: Drop ML Tables
-- ════════════════════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS ML_PREDICTIONS;
DROP TABLE IF EXISTS ML_TRAINING_DATA;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 4: Drop Streamlit App
-- ════════════════════════════════════════════════════════════════════════════

DROP STREAMLIT IF EXISTS CELL_THERAPY_COMPASS;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 5: Drop your per-user schema (CASCADE removes anything remaining)
-- ════════════════════════════════════════════════════════════════════════════

DROP SCHEMA IF EXISTS IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM) CASCADE;

-- ════════════════════════════════════════════════════════════════════════════
-- Verify Cleanup
-- ════════════════════════════════════════════════════════════════════════════

SELECT 'Participant ' || $USER_NUM || ' teardown complete -- all your lab artifacts removed.' AS STATUS;

-- ════════════════════════════════════════════════════════════════════════════
-- NOTE: Your role, warehouse, and shared data are managed by the lab admin.
-- The admin will run 00_admin_teardown.sql to clean up those resources.
-- ════════════════════════════════════════════════════════════════════════════
