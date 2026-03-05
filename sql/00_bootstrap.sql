/*=============================================================================
  LSC Donor for All Data Lab — Bootstrap Infrastructure
  =============================================================================
  Run this script FIRST to create all Snowflake infrastructure.
  Idempotent: safe to run multiple times.
  
  Prerequisites:
    - ACCOUNTADMIN role (or equivalent with CREATE DATABASE/ROLE/WAREHOUSE)
    - AWS US-East-1 region (or cross-region calling enabled)
  
  What this creates:
    - Role:      MARROWCO_HOL_ROLE
    - Database:  MARROWCO_DONOR_LAB
    - Schema:    MARROWCO_DONOR_LAB.HOL
    - Warehouse: MARROWCO_HOL_WH (X-Small, auto-suspend 60s)
    - Stage:     MARROWCO_DONOR_LAB.HOL.DATA_STAGE
    - File Format: MARROWCO_DONOR_LAB.HOL.CSV_FORMAT
    - All necessary grants
  =============================================================================*/

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 1: Create Role                                                      ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS MARROWCO_HOL_ROLE
    COMMENT = 'Role for LSC Donor for All Data Lab HOL';

-- Grant role to current user so we can use it immediately
GRANT ROLE MARROWCO_HOL_ROLE TO ROLE ACCOUNTADMIN;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 2: Create Warehouse                                                 ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
CREATE WAREHOUSE IF NOT EXISTS MARROWCO_HOL_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for LSC Donor for All Data Lab HOL';

GRANT USAGE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;
GRANT OPERATE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 3: Create Database and Schema                                       ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
CREATE DATABASE IF NOT EXISTS MARROWCO_DONOR_LAB
    COMMENT = 'LSC Donor for All Data Lab — Forecasting GVHD with Snowflake Intelligence';

GRANT OWNERSHIP ON DATABASE MARROWCO_DONOR_LAB TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

USE DATABASE MARROWCO_DONOR_LAB;

CREATE SCHEMA IF NOT EXISTS HOL
    COMMENT = 'Primary schema for Hands-on Lab artifacts';

GRANT OWNERSHIP ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 4: Set Context                                                      ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 5: Create Stage and File Format                                     ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
CREATE STAGE IF NOT EXISTS DATA_STAGE
    COMMENT = 'Internal stage for uploading CSV data files';

CREATE FILE FORMAT IF NOT EXISTS CSV_FORMAT
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    COMMENT = 'Standard CSV format for lab data ingestion';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 6: Grant Required Privileges                                        ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Database-level grants
GRANT CREATE TABLE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE VIEW ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE STAGE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE FILE FORMAT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE FUNCTION ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE PROCEDURE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE STREAMLIT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- Dynamic Tables
GRANT CREATE DYNAMIC TABLE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE MARROWCO_HOL_ROLE;

-- Cortex AI features
GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- Snowflake Intelligence / Agents
GRANT CREATE AGENT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- Semantic Views
GRANT CREATE SEMANTIC VIEW ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- Cortex AI Functions (COMPLETE, EXTRACT_ANSWER, SUMMARIZE, etc.)
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE;

-- Model Registry (for ML model training)
GRANT CREATE MODEL ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 7: Verify Setup                                                     ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
SELECT 
    CURRENT_ROLE() AS ROLE,
    CURRENT_WAREHOUSE() AS WAREHOUSE,
    CURRENT_DATABASE() AS DATABASE,
    CURRENT_SCHEMA() AS SCHEMA,
    '✅ Bootstrap complete — infrastructure ready!' AS STATUS;
