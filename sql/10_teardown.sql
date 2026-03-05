/*=============================================================================
  LSC Donor for All Data Lab — Teardown / Cleanup Script
  =============================================================================
  
  Removes ALL lab artifacts from your Snowflake account.
  Run this when you are finished with the lab to clean up resources.
  
  WARNING: This script is DESTRUCTIVE and IRREVERSIBLE.
  All data, models, agents, and objects will be permanently deleted.
  
  What this removes:
    - Streamlit App:  CELL_THERAPY_COMPASS
    - Agent:          MARROWCO_RESEARCH_AGENT
    - ML Model:       GVHD_RISK_MODEL
    - Semantic View:  MARROWCO_TRANSPLANT_ANALYTICS
    - Search Service: CLINICAL_NOTES_SEARCH
    - Dynamic Tables: DT_GVHD_ANALYTICS, DT_TRANSPLANT_ENRICHED
    - Tables:         ML_PREDICTIONS, ML_TRAINING_DATA, CLINICAL_NOTES, 
                      TRANSPLANT_OUTCOMES
    - Stage:          DATA_STAGE
    - File Format:    CSV_FORMAT
    - Schema:         MARROWCO_DONOR_LAB.HOL
    - Database:       MARROWCO_DONOR_LAB
    - Warehouse:      MARROWCO_HOL_WH
    - Role:           MARROWCO_HOL_ROLE
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 1: Switch to ACCOUNTADMIN
-- ════════════════════════════════════════════════════════════════════════════
USE ROLE ACCOUNTADMIN;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 2: Drop AI/ML Objects (must drop before schema/database)
-- ════════════════════════════════════════════════════════════════════════════

-- Agent
DROP AGENT IF EXISTS MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT;

-- ML Model
DROP MODEL IF EXISTS MARROWCO_DONOR_LAB.HOL.GVHD_RISK_MODEL;

-- Semantic View
DROP SEMANTIC VIEW IF EXISTS MARROWCO_DONOR_LAB.HOL.MARROWCO_TRANSPLANT_ANALYTICS;

-- Cortex Search Service
DROP CORTEX SEARCH SERVICE IF EXISTS MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES_SEARCH;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 3: Drop Dynamic Tables
-- ════════════════════════════════════════════════════════════════════════════

-- Gold layer first (depends on Silver)
DROP DYNAMIC TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.DT_GVHD_ANALYTICS;

-- Silver layer
DROP DYNAMIC TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.DT_TRANSPLANT_ENRICHED;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 4: Drop Tables
-- ════════════════════════════════════════════════════════════════════════════

DROP TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.ML_PREDICTIONS;
DROP TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.ML_TRAINING_DATA;
DROP TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.CLINICAL_NOTES;
DROP TABLE IF EXISTS MARROWCO_DONOR_LAB.HOL.TRANSPLANT_OUTCOMES;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 5: Drop Stage and File Format
-- ════════════════════════════════════════════════════════════════════════════

DROP STAGE IF EXISTS MARROWCO_DONOR_LAB.HOL.DATA_STAGE;
DROP FILE FORMAT IF EXISTS MARROWCO_DONOR_LAB.HOL.CSV_FORMAT;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 6: Drop Database (cascades schema and any remaining objects)
-- ════════════════════════════════════════════════════════════════════════════

DROP DATABASE IF EXISTS MARROWCO_DONOR_LAB;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 7: Drop Warehouse
-- ════════════════════════════════════════════════════════════════════════════

DROP WAREHOUSE IF EXISTS MARROWCO_HOL_WH;

-- ════════════════════════════════════════════════════════════════════════════
-- STEP 8: Drop Role
-- ════════════════════════════════════════════════════════════════════════════

DROP ROLE IF EXISTS MARROWCO_HOL_ROLE;

-- ════════════════════════════════════════════════════════════════════════════
-- Verify Cleanup
-- ════════════════════════════════════════════════════════════════════════════

SELECT 'Teardown complete — all lab artifacts removed.' AS STATUS;
