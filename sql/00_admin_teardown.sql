/*=============================================================================
  LSC Donor for All Data Lab -- Multi-User Teardown
  =============================================================================
  
  Removes ALL lab artifacts from your Snowflake account, including all
  per-user environments and shared infrastructure.

  WARNING: This script is DESTRUCTIVE and IRREVERSIBLE.

  Run as: ACCOUNTADMIN
  Run when: After the lab is complete and all participants are done.

  What this removes:
    Per-user (for each participant):
      - Schema:      HOL_USER_01 .. _NN  (cascades all objects inside)
      - Warehouse:   MARROWCO_HOL_WH_01 .. _NN
      - Role:        MARROWCO_HOL_ROLE_01 .. _NN

    Shared:
      - Database:    MARROWCO_DONOR_LAB  (cascades HOL schema and all objects)
      - Warehouse:   MARROWCO_HOL_WH
      - Role:        MARROWCO_HOL_ROLE
  =============================================================================*/

USE ROLE ACCOUNTADMIN;

-- ============================================================================
-- CONFIGURATION: Must match the number used during provisioning
-- ============================================================================
SET NUM_USERS = 10;  -- Change this to match your 00_admin_provision.sql value


-- ============================================================================
-- STEP 1: (Optional) Disable web search if it was enabled
-- ============================================================================
-- ALTER ACCOUNT UNSET ENABLE_CORTEX_WEBSEARCH;


-- ============================================================================
-- STEP 2: Drop all per-user environments
-- ============================================================================
DECLARE
    i INTEGER DEFAULT 1;
    user_num VARCHAR;
    role_name VARCHAR;
    wh_name VARCHAR;
    schema_name VARCHAR;
BEGIN
    WHILE (i <= $NUM_USERS) DO
        user_num := LPAD(i::VARCHAR, 2, '0');
        role_name := 'MARROWCO_HOL_ROLE_' || user_num;
        wh_name := 'MARROWCO_HOL_WH_' || user_num;
        schema_name := 'HOL_USER_' || user_num;

        -- Drop per-user schema (cascades all objects: DTs, semantic views, agents, models, etc.)
        EXECUTE IMMEDIATE 'DROP SCHEMA IF EXISTS MARROWCO_DONOR_LAB.IDENTIFIER(?) CASCADE' 
            USING (schema_name);

        -- Drop per-user warehouse
        EXECUTE IMMEDIATE 'DROP WAREHOUSE IF EXISTS IDENTIFIER(?)' 
            USING (wh_name);

        -- Revoke account-level grants before dropping role
        BEGIN
            EXECUTE IMMEDIATE 'REVOKE EXECUTE MANAGED TASK ON ACCOUNT FROM ROLE IDENTIFIER(?)' 
                USING (role_name);
        EXCEPTION
            WHEN OTHER THEN NULL;  -- Ignore if already revoked
        END;

        -- Drop per-user role
        EXECUTE IMMEDIATE 'DROP ROLE IF EXISTS IDENTIFIER(?)' 
            USING (role_name);

        i := i + 1;
    END WHILE;

    RETURN 'Dropped ' || $NUM_USERS || ' user environments.';
END;


-- ============================================================================
-- STEP 3: Drop shared infrastructure
-- ============================================================================

-- Drop the entire database (cascades the shared HOL schema and any remaining per-user schemas)
DROP DATABASE IF EXISTS MARROWCO_DONOR_LAB;

-- Drop admin warehouse
DROP WAREHOUSE IF EXISTS MARROWCO_HOL_WH;

-- Revoke account-level grants from admin role
REVOKE EXECUTE MANAGED TASK ON ACCOUNT FROM ROLE MARROWCO_HOL_ROLE;

-- Drop admin role
DROP ROLE IF EXISTS MARROWCO_HOL_ROLE;


-- ============================================================================
-- VERIFICATION
-- ============================================================================
SELECT 'Teardown complete -- all lab artifacts removed for ' || $NUM_USERS || ' users.' AS STATUS;
