/*=============================================================================
  LSC Donor for All Data Lab -- Snowflake Intelligence Setup
  =============================================================================
  
  Connects the LSC Research Agent to Snowflake Intelligence for an 
  interactive, conversational analytics experience.

  WHAT IS SNOWFLAKE INTELLIGENCE?
    Snowflake Intelligence is the conversational UI layer that makes
    Cortex Agents accessible to non-technical users. It provides:
      + Auto-generated suggested questions (from verified queries)
      + Interactive charts and visualizations
      + Structured + unstructured answers in one interface
      + Conversation history and follow-up questions
      + Shareable with team members

  Run after: 06_create_agent.sql
  =============================================================================*/

-- ════════════════════════════════════════════════════════════════════════════
-- SET YOUR USER NUMBER (assigned by the lab admin)
-- ════════════════════════════════════════════════════════════════════════════
SET USER_NUM = '01';  -- << CHANGE THIS TO YOUR ASSIGNED NUMBER (01-20)

USE ROLE IDENTIFIER('MARROWCO_HOL_ROLE_' || $USER_NUM);
USE WAREHOUSE IDENTIFIER('MARROWCO_HOL_WH_' || $USER_NUM);
USE SCHEMA IDENTIFIER('MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM);

SET MY_SCHEMA = 'MARROWCO_DONOR_LAB.HOL_USER_' || $USER_NUM;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ CONNECTING TO SNOWFLAKE INTELLIGENCE                                     ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║                                                                          ║
-- ║ Snowflake Intelligence is accessed through the Snowsight UI:             ║
-- ║                                                                          ║
-- ║   1. Navigate to: AI & ML > Snowflake Intelligence                      ║
-- ║   2. Click "New Analyst" (or "+" button)                                ║
-- ║   3. Select: "Use an Agent"                                             ║
-- ║   4. Choose your agent from your schema:                                ║
-- ║      HOL_USER_<NN>.MARROWCO_RESEARCH_AGENT                              ║
-- ║   5. Name it: "LSC Research Intelligence"                               ║
-- ║   6. Click "Create"                                                      ║
-- ║                                                                          ║
-- ║ The verified queries from the Semantic View will automatically          ║
-- ║ appear as suggested questions in the interface!                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Show your agent's fully-qualified name for the UI
SELECT $MY_SCHEMA || '.MARROWCO_RESEARCH_AGENT' AS YOUR_AGENT_PATH;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ DEMO FLOW: Questions to Ask in Snowflake Intelligence                    ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Walk through these in order during the HOL to showcase each capability:  ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Demo 1: STRUCTURED DATA -- "The What"
-- Ask: "What is the overall GVHD rate by donor type?"

-- Demo 2: VISUALIZATION -- "The How"
-- Ask: "Show me a chart of monthly transplant volume trends with survival rates"

-- Demo 3: UNSTRUCTURED DATA -- "The Why"
-- Ask: "What do clinical notes say about patients who had severe skin GVHD and how they responded to treatment?"

-- Demo 4: COMBINED -- "The Full Picture"
-- Ask: "Compare haploidentical outcomes with and without PTCy, and find clinical evidence supporting PTCy-based prophylaxis from physician notes"

-- Demo 5: HEALTH EQUITY -- "The Who"
-- Ask: "How does patient race and ethnicity affect transplant outcomes, and what does social vulnerability data tell us?"

-- Demo 6: RECOMMENDATIONS -- "The So What"
-- Ask: "Based on all the data, what are the top 3 recommendations to improve outcomes for minority patients under the Donor for All initiative?"

-- Demo 7: WEB SEARCH -- "The Latest"
-- Ask: "Search for the latest 2024-2025 publications on GVHD prevention with post-transplant cyclophosphamide"
-- NOTE: web_search tool requires account-level enablement

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ PRESENTER TALKING POINTS                                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║                                                                          ║
-- ║ 1. "Notice the suggested questions -- these come from the verified      ║
-- ║     queries we defined in the Semantic View. This is the trust layer."  ║
-- ║                                                                          ║
-- ║ 2. "The agent autonomously decides which tool to use. It's not a        ║
-- ║     chatbot with a script -- it reasons about the best approach."        ║
-- ║                                                                          ║
-- ║ 3. "This is what Looker can't do -- combine structured analytics with   ║
-- ║     unstructured clinical note search in a single answer."              ║
-- ║                                                                          ║
-- ║ 4. "The Semantic View ensures every answer is grounded in the same      ║
-- ║     trusted definitions. No conflicting metric calculations."           ║
-- ║                                                                          ║
-- ║ 5. "Snowflake Intelligence can show charts, answer follow-ups, and      ║
-- ║     be shared across the team -- no Looker license needed."             ║
-- ║                                                                          ║
-- ║ 6. "This is the future of analytics: ask a question, get an answer      ║
-- ║     with data, evidence, and recommendations -- not just a dashboard."  ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
