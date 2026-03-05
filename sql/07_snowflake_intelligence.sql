/*=============================================================================
  LSC Donor for All Data Lab — Snowflake Intelligence Setup
  =============================================================================
  
  Connects the LSC Research Agent to Snowflake Intelligence for an 
  interactive, conversational analytics experience.
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ WHAT IS SNOWFLAKE INTELLIGENCE?                                         │
  │                                                                        │
  │ Snowflake Intelligence is the conversational UI layer that makes       │
  │ Cortex Agents accessible to non-technical users. It provides:          │
  │                                                                        │
  │   ✅ Auto-generated suggested questions (from verified queries)        │
  │   ✅ Interactive charts and visualizations                             │
  │   ✅ Structured + unstructured answers in one interface                │
  │   ✅ Conversation history and follow-up questions                      │
  │   ✅ Shareable with team members                                       │
  │                                                                        │
  │ UNLIKE ANY BI TOOL:                                                    │
  │ Snowflake Intelligence doesn't just show data — it tells you:          │
  │   • WHO (patient demographics, physician involvement)                  │
  │   • WHAT (outcomes, GVHD rates, survival statistics)                   │
  │   • WHERE (center performance, geographic patterns)                    │
  │   • WHEN (temporal trends, engraftment timelines)                      │
  │   • WHY (risk factors, clinical evidence from notes)                   │
  │   • HOW (treatment protocols, prophylaxis approaches)                  │
  │   • RECOMMENDATIONS (actionable insights grounded in data + evidence) │
  └─────────────────────────────────────────────────────────────────────────┘
  
  Run after: 06_create_agent.sql
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ CONNECTING TO SNOWFLAKE INTELLIGENCE                                     ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║                                                                          ║
-- ║ Snowflake Intelligence is accessed through the Snowsight UI:             ║
-- ║                                                                          ║
-- ║   1. Navigate to: AI & ML > Snowflake Intelligence                      ║
-- ║   2. Click "New Analyst" (or "+" button)                                ║
-- ║   3. Select: "Use an Agent"                                             ║
-- ║   4. Choose: MARROWCO_DONOR_LAB.HOL.MARROWCO_RESEARCH_AGENT                    ║
-- ║   5. Name it: "LSC Research Intelligence"                              ║
-- ║   6. Click "Create"                                                      ║
-- ║                                                                          ║
-- ║ The verified queries from the Semantic View will automatically          ║
-- ║ appear as suggested questions in the interface!                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ DEMO FLOW: Questions to Ask in Snowflake Intelligence                    ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Walk through these in order during the HOL to showcase each capability:  ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 1: STRUCTURED DATA — "The What"
-- Shows: Cortex Analyst querying via Semantic View with auto-generated chart
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "What is the overall GVHD rate by donor type?"
-- Expected: Table + bar chart showing GVHD rates per donor type
-- Verified query ensures consistent, trusted results

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 2: VISUALIZATION — "The How"
-- Shows: data_to_chart generating visual analytics
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "Show me a chart of monthly transplant volume trends with survival rates"
-- Expected: Time series chart showing transplant volume and outcomes over time

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 3: UNSTRUCTURED DATA — "The Why"
-- Shows: Cortex Search retrieving clinical note evidence
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "What do clinical notes say about patients who had severe skin GVHD and how they responded to treatment?"
-- Expected: Summarized clinical note excerpts about GVHD treatment response

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 4: COMBINED — "The Full Picture"
-- Shows: Agent using BOTH Analyst and Search together
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "Compare haploidentical outcomes with and without PTCy, and find clinical evidence supporting PTCy-based prophylaxis from physician notes"
-- Expected: Structured comparison table + clinical note excerpts combined

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 5: HEALTH EQUITY — "The Who" 
-- Shows: Demographic analysis with social determinants
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "How does patient race and ethnicity affect transplant outcomes, and what does social vulnerability data tell us?"
-- Expected: Race/ethnicity breakdown with SVI correlation

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 6: RECOMMENDATIONS — "The So What"
-- Shows: Agent synthesizing data into actionable insights
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "Based on all the data, what are the top 3 recommendations to improve outcomes for minority patients under the Donor for All initiative?"
-- Expected: Data-grounded recommendations combining structured analytics + clinical evidence

-- ═══════════════════════════════════════════════════════════════════════════
-- Demo 7: WEB SEARCH — "The Latest"
-- Shows: Agent searching the web for current research
-- ═══════════════════════════════════════════════════════════════════════════
-- Ask: "Search for the latest 2024-2025 publications on GVHD prevention with post-transplant cyclophosphamide"
-- Expected: Web search results with recent publication summaries
-- NOTE: web_search tool requires account-level enablement

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ PRESENTER TALKING POINTS                                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║                                                                          ║
-- ║ 1. "Notice the suggested questions — these come from the verified       ║
-- ║     queries we defined in the Semantic View. This is the trust layer."  ║
-- ║                                                                          ║
-- ║ 2. "The agent autonomously decides which tool to use. It's not a        ║
-- ║     chatbot with a script — it reasons about the best approach."         ║
-- ║                                                                          ║
-- ║ 3. "This is what Looker can't do — combine structured analytics with   ║
-- ║     unstructured clinical note search in a single answer."              ║
-- ║                                                                          ║
-- ║ 4. "The Semantic View ensures every answer is grounded in the same      ║
-- ║     trusted definitions. No conflicting metric calculations."           ║
-- ║                                                                          ║
-- ║ 5. "Snowflake Intelligence can show charts, answer follow-ups, and      ║
-- ║     be shared across the LSC team — no Looker license needed."         ║
-- ║                                                                          ║
-- ║ 6. "This is the future of analytics: ask a question, get an answer      ║
-- ║     with data, evidence, and recommendations — not just a dashboard."   ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝
