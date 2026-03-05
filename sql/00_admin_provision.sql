/*=============================================================================
  LSC Donor for All Data Lab -- Multi-User Provisioning
  =============================================================================
  
  Run this script ONCE as ACCOUNTADMIN before the lab begins.
  It creates ALL shared infrastructure AND per-user isolated environments.

  Architecture:
    SHARED (created once):
      - Database:    MARROWCO_DONOR_LAB
      - Schema:      HOL (base tables, stage, file format)
      - Role:        MARROWCO_HOL_ROLE (admin role, owns shared objects)
      - Warehouse:   MARROWCO_HOL_WH (admin warehouse for data loading)

    PER-USER (created for each participant):
      - Role:        MARROWCO_HOL_ROLE_01 .. _NN
      - Warehouse:   MARROWCO_HOL_WH_01 .. _NN  (no compute contention)
      - Schema:      HOL_USER_01 .. _NN  (isolated object namespace)

  Naming Convention:
    All per-user objects use a zero-padded two-digit suffix: _01, _02, ... _20
    Object names within each schema are IDENTICAL to the single-user lab,
    so participants follow the same instructions -- just set their USER_NUM.

  Prerequisites:
    - ACCOUNTADMIN role
    - Decide how many participants (5-20)
    - Have a list of Snowflake usernames to assign

  What to do after this script:
    1. Load shared data:  Run 01_create_tables.sql + 02_load_data.sql as MARROWCO_HOL_ROLE
    2. Assign users:      GRANT ROLE MARROWCO_HOL_ROLE_01 TO USER <USERNAME>;
    3. Tell participants:  "Set USER_NUM = '01'; at the top of each script"

  FALLBACK TO SINGLE-USER MODE:
    If multi-user mode causes issues, revert to the tested single-user version:
      git checkout v1.0-single-user
    That tag points to commit 2b530f9 which was fully tested end-to-end.
    In single-user mode, use 00_bootstrap.sql instead of this script, and
    participants run scripts 01-08 without setting USER_NUM.
  =============================================================================*/

USE ROLE ACCOUNTADMIN;

-- ============================================================================
-- CONFIGURATION: Set the number of participants here
-- ============================================================================
SET NUM_USERS = 10;  -- Change this to your actual participant count (5-20)


-- ============================================================================
-- STEP 1: Create shared infrastructure
-- ============================================================================

-- Admin role (owns shared database, schema, base tables)
CREATE ROLE IF NOT EXISTS MARROWCO_HOL_ROLE
    COMMENT = 'Admin role for LSC Donor for All Data Lab -- owns shared objects';
GRANT ROLE MARROWCO_HOL_ROLE TO ROLE ACCOUNTADMIN;

-- Admin warehouse (for data loading and shared object management)
CREATE WAREHOUSE IF NOT EXISTS MARROWCO_HOL_WH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Admin warehouse for LSC Data Lab -- shared data loading';

GRANT USAGE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;
GRANT OPERATE ON WAREHOUSE MARROWCO_HOL_WH TO ROLE MARROWCO_HOL_ROLE;

-- Database
CREATE DATABASE IF NOT EXISTS MARROWCO_DONOR_LAB
    COMMENT = 'LSC Donor for All Data Lab -- Forecasting GVHD with Snowflake Intelligence';

GRANT OWNERSHIP ON DATABASE MARROWCO_DONOR_LAB TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

-- Shared schema (holds base tables, stage, file format -- read-only for participants)
USE DATABASE MARROWCO_DONOR_LAB;
CREATE SCHEMA IF NOT EXISTS HOL
    COMMENT = 'Shared schema -- base tables and staging (read-only for participants)';

GRANT OWNERSHIP ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE
    COPY CURRENT GRANTS;

-- Admin role needs full CREATE privileges on shared schema
USE ROLE ACCOUNTADMIN;
GRANT CREATE TABLE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE VIEW ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE STAGE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT CREATE FILE FORMAT ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE MARROWCO_HOL_ROLE;
GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE MARROWCO_HOL_ROLE;
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE MARROWCO_HOL_ROLE;

-- Stage and file format in shared schema
USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

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


-- ============================================================================
-- STEP 2: Create per-user environments (loop)
-- ============================================================================
USE ROLE ACCOUNTADMIN;

DECLARE
    i INTEGER DEFAULT 1;
    user_num VARCHAR;
    role_name VARCHAR;
    wh_name VARCHAR;
    schema_name VARCHAR;
BEGIN
    WHILE (i <= $NUM_USERS) DO
        -- Zero-pad the user number
        user_num := LPAD(i::VARCHAR, 2, '0');
        role_name := 'MARROWCO_HOL_ROLE_' || user_num;
        wh_name := 'MARROWCO_HOL_WH_' || user_num;
        schema_name := 'HOL_USER_' || user_num;

        -- ── Create per-user role ──
        EXECUTE IMMEDIATE 'CREATE ROLE IF NOT EXISTS IDENTIFIER(?) COMMENT = ?' 
            USING (role_name, 'Participant role ' || user_num || ' for LSC Data Lab');
        EXECUTE IMMEDIATE 'GRANT ROLE IDENTIFIER(?) TO ROLE ACCOUNTADMIN' USING (role_name);

        -- ── Create per-user warehouse ──
        EXECUTE IMMEDIATE '
            CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER(?)
                WAREHOUSE_SIZE = ''X-SMALL''
                AUTO_SUSPEND = 60
                AUTO_RESUME = TRUE
                INITIALLY_SUSPENDED = TRUE
                COMMENT = ?' 
            USING (wh_name, 'Participant ' || user_num || ' warehouse -- LSC Data Lab');
        EXECUTE IMMEDIATE 'GRANT USAGE ON WAREHOUSE IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (wh_name, role_name);
        EXECUTE IMMEDIATE 'GRANT OPERATE ON WAREHOUSE IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (wh_name, role_name);

        -- ── Create per-user schema ──
        EXECUTE IMMEDIATE '
            CREATE SCHEMA IF NOT EXISTS MARROWCO_DONOR_LAB.IDENTIFIER(?)
                COMMENT = ?' 
            USING (schema_name, 'Participant ' || user_num || ' workspace -- isolated lab environment');
        EXECUTE IMMEDIATE '
            GRANT OWNERSHIP ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) 
            TO ROLE IDENTIFIER(?) COPY CURRENT GRANTS' 
            USING (schema_name, role_name);

        -- ── Grant database-level access ──
        EXECUTE IMMEDIATE 'GRANT USAGE ON DATABASE MARROWCO_DONOR_LAB TO ROLE IDENTIFIER(?)' 
            USING (role_name);

        -- ── Grant read-only access to shared HOL schema (base tables) ──
        EXECUTE IMMEDIATE 'GRANT USAGE ON SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE IDENTIFIER(?)' 
            USING (role_name);
        EXECUTE IMMEDIATE '
            GRANT SELECT ON ALL TABLES IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE IDENTIFIER(?)' 
            USING (role_name);
        EXECUTE IMMEDIATE '
            GRANT SELECT ON FUTURE TABLES IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE IDENTIFIER(?)' 
            USING (role_name);
        EXECUTE IMMEDIATE '
            GRANT USAGE ON ALL STAGES IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE IDENTIFIER(?)' 
            USING (role_name);
        EXECUTE IMMEDIATE '
            GRANT USAGE ON ALL FILE FORMATS IN SCHEMA MARROWCO_DONOR_LAB.HOL TO ROLE IDENTIFIER(?)' 
            USING (role_name);

        -- ── Grant CREATE privileges on per-user schema ──
        EXECUTE IMMEDIATE 'GRANT CREATE TABLE ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE VIEW ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE STAGE ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE FILE FORMAT ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE FUNCTION ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE PROCEDURE ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE STREAMLIT ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE DYNAMIC TABLE ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE AGENT ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE SEMANTIC VIEW ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);
        EXECUTE IMMEDIATE 'GRANT CREATE MODEL ON SCHEMA MARROWCO_DONOR_LAB.IDENTIFIER(?) TO ROLE IDENTIFIER(?)' 
            USING (schema_name, role_name);

        -- ── Account-level grants ──
        EXECUTE IMMEDIATE 'GRANT EXECUTE MANAGED TASK ON ACCOUNT TO ROLE IDENTIFIER(?)' 
            USING (role_name);
        EXECUTE IMMEDIATE 'GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER(?)' 
            USING (role_name);

        i := i + 1;
    END WHILE;

    RETURN 'Provisioned ' || $NUM_USERS || ' user environments successfully.';
END;


-- ============================================================================
-- STEP 3: Assign roles to participants
-- ============================================================================
-- Uncomment and customize these lines with actual Snowflake usernames:
--
-- GRANT ROLE MARROWCO_HOL_ROLE_01 TO USER JSMITH;
-- GRANT ROLE MARROWCO_HOL_ROLE_02 TO USER AJONES;
-- GRANT ROLE MARROWCO_HOL_ROLE_03 TO USER MLEE;
-- ... continue for each participant ...


-- ============================================================================
-- STEP 4: (Optional) Enable web search for Cortex Agents
-- ============================================================================
-- ALTER ACCOUNT SET ENABLE_CORTEX_WEBSEARCH = TRUE;


-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Check all roles created
SHOW ROLES LIKE 'MARROWCO_HOL_ROLE%';

-- Check all warehouses created
SHOW WAREHOUSES LIKE 'MARROWCO_HOL_WH%';

-- Check all schemas created
SHOW SCHEMAS IN DATABASE MARROWCO_DONOR_LAB;

SELECT 'Provisioning complete. ' || $NUM_USERS || ' user environments ready.' AS STATUS;
