/*=============================================================================
  LSC Donor for All Data Lab — Machine Learning Model
  =============================================================================
  
  Trains a GVHD risk prediction model using Snowflake ML and registers it 
  in the Snowflake Model Registry.
  
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ WHAT WE BUILD                                                           │
  │                                                                        │
  │ 1. Classification model: Predicts GVHD severity (High Risk vs Not)     │
  │ 2. Training data: Features from the DT_TRANSPLANT_ENRICHED table       │
  │ 3. Model registry: Versioned model with evaluation metrics             │
  │ 4. Inference: Apply model to score new patients                        │
  │                                                                        │
  │ This showcases Snowflake's native ML capabilities:                     │
  │   ✅ No data movement — train where data lives                         │
  │   ✅ Model Registry — version, manage, and govern models               │
  │   ✅ Evaluation metrics — AUC, precision, recall, F1                   │
  │   ✅ Feature importance — understand what drives predictions            │
  │   ✅ Seamless inference in SQL                                          │
  └─────────────────────────────────────────────────────────────────────────┘
  
  Run after: 03_dynamic_tables.sql (needs DT_TRANSPLANT_ENRICHED)
  =============================================================================*/

USE ROLE MARROWCO_HOL_ROLE;
USE WAREHOUSE MARROWCO_HOL_WH;
USE SCHEMA MARROWCO_DONOR_LAB.HOL;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 1: Prepare Training Data                                            ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Create a feature table from the enriched dynamic table with:            ║
-- ║   • Target variable: HIGH_RISK_GVHD (binary: Grade III-IV)             ║
-- ║   • Features: patient/donor demographics, treatment, risk factors       ║
-- ║   • Train/test split: 80/20 random split                               ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE TABLE ML_TRAINING_DATA AS
SELECT
    TRANSPLANT_ID,
    
    -- Target variable: predicting severe GVHD (Grade III-IV)
    CASE WHEN ACUTE_GVHD_GRADE >= 3 THEN 1 ELSE 0 END AS HIGH_RISK_GVHD,
    
    -- Patient features
    PATIENT_AGE,
    PATIENT_SEX,
    PATIENT_RACE_ETHNICITY,
    
    -- Disease features
    DIAGNOSIS_CATEGORY,
    DISEASE_RISK_CATEGORY,
    
    -- Donor features
    DONOR_TYPE,
    HLA_MATCH_SCORE,
    DONOR_AGE,
    DONOR_SEX,
    SEX_MISMATCH_FLAG,
    
    -- Treatment features
    CONDITIONING_INTENSITY,
    PTCY_BASED_PROPHYLAXIS,
    
    -- Social determinants
    SVI_SCORE,
    CENTER_REGION,
    
    -- Train/test split (80/20)
    CASE WHEN RANDOM() < 0.8 THEN 'TRAIN' ELSE 'TEST' END AS SPLIT
    
FROM DT_TRANSPLANT_ENRICHED;

-- Verify split distribution
SELECT 
    SPLIT,
    COUNT(*) AS RECORDS,
    SUM(HIGH_RISK_GVHD) AS POSITIVE_CASES,
    ROUND(SUM(HIGH_RISK_GVHD) * 100.0 / COUNT(*), 1) AS POSITIVE_RATE_PCT
FROM ML_TRAINING_DATA
GROUP BY SPLIT;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 2: Train the Classification Model                                   ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Uses Snowflake ML Classification to train a GVHD risk model.            ║
-- ║ Snowflake automatically:                                                ║
-- ║   • Handles categorical encoding                                        ║
-- ║   • Selects the best algorithm                                          ║
-- ║   • Tunes hyperparameters                                               ║
-- ║   • Computes evaluation metrics                                         ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE SNOWFLAKE.ML.CLASSIFICATION GVHD_RISK_MODEL(
    INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'ML_TRAINING_DATA'),
    TARGET_COLNAME => 'HIGH_RISK_GVHD',
    CONFIG_OBJECT => {
        'evaluate': TRUE,
        'on_error': 'skip'
    }
);

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 3: Evaluate Model Performance                                       ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Key metrics for a clinical risk prediction model:                       ║
-- ║   • AUC: Area Under ROC Curve (> 0.7 is acceptable for clinical use)   ║
-- ║   • Precision: Of predicted high-risk, how many truly are?             ║
-- ║   • Recall: Of actual high-risk, how many did we catch?                ║
-- ║   • F1: Harmonic mean of precision and recall                          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- View evaluation metrics
CALL GVHD_RISK_MODEL!SHOW_EVALUATION_METRICS();

-- View feature importance — which factors drive GVHD risk?
CALL GVHD_RISK_MODEL!SHOW_FEATURE_IMPORTANCE();

-- View global training metrics
CALL GVHD_RISK_MODEL!SHOW_TRAINING_LOGS();

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 4: Generate Predictions on Test Set                                 ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ Score the test set and compare predictions to actual outcomes.           ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

CREATE OR REPLACE TABLE ML_PREDICTIONS AS
SELECT 
    t.*,
    GVHD_RISK_MODEL!PREDICT(
        INPUT_DATA => OBJECT_CONSTRUCT(
            'PATIENT_AGE', t.PATIENT_AGE,
            'PATIENT_SEX', t.PATIENT_SEX,
            'PATIENT_RACE_ETHNICITY', t.PATIENT_RACE_ETHNICITY,
            'DIAGNOSIS_CATEGORY', t.DIAGNOSIS_CATEGORY,
            'DISEASE_RISK_CATEGORY', t.DISEASE_RISK_CATEGORY,
            'DONOR_TYPE', t.DONOR_TYPE,
            'HLA_MATCH_SCORE', t.HLA_MATCH_SCORE,
            'DONOR_AGE', t.DONOR_AGE,
            'DONOR_SEX', t.DONOR_SEX,
            'SEX_MISMATCH_FLAG', t.SEX_MISMATCH_FLAG,
            'CONDITIONING_INTENSITY', t.CONDITIONING_INTENSITY,
            'PTCY_BASED_PROPHYLAXIS', t.PTCY_BASED_PROPHYLAXIS,
            'SVI_SCORE', t.SVI_SCORE,
            'CENTER_REGION', t.CENTER_REGION
        )
    ) AS PREDICTION_RESULT,
    PREDICTION_RESULT['class']::INT AS PREDICTED_HIGH_RISK,
    PREDICTION_RESULT['probability'][1]::FLOAT AS RISK_PROBABILITY
FROM ML_TRAINING_DATA t
WHERE SPLIT = 'TEST';

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 5: Confusion Matrix & Accuracy                                      ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

-- Confusion matrix
SELECT 
    'Actual: ' || HIGH_RISK_GVHD || ' → Predicted: ' || PREDICTED_HIGH_RISK AS OUTCOME,
    COUNT(*) AS COUNT
FROM ML_PREDICTIONS
GROUP BY HIGH_RISK_GVHD, PREDICTED_HIGH_RISK
ORDER BY HIGH_RISK_GVHD, PREDICTED_HIGH_RISK;

-- Overall accuracy
SELECT 
    COUNT(*) AS TOTAL_TEST,
    SUM(CASE WHEN HIGH_RISK_GVHD = PREDICTED_HIGH_RISK THEN 1 ELSE 0 END) AS CORRECT,
    ROUND(SUM(CASE WHEN HIGH_RISK_GVHD = PREDICTED_HIGH_RISK THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS ACCURACY_PCT,
    '✅ Model evaluation complete' AS STATUS
FROM ML_PREDICTIONS;

-- Risk distribution
SELECT 
    CASE 
        WHEN RISK_PROBABILITY < 0.3 THEN 'Low Risk (<30%)'
        WHEN RISK_PROBABILITY < 0.6 THEN 'Moderate Risk (30-60%)'
        ELSE 'High Risk (>60%)'
    END AS RISK_BUCKET,
    COUNT(*) AS PATIENT_COUNT,
    ROUND(AVG(HIGH_RISK_GVHD) * 100, 1) AS ACTUAL_POSITIVE_RATE
FROM ML_PREDICTIONS
GROUP BY 1
ORDER BY 1;

-- ╔═══════════════════════════════════════════════════════════════════════════╗
-- ║ STEP 6: Register Model (for production use)                              ║
-- ╠═══════════════════════════════════════════════════════════════════════════╣
-- ║ The model is automatically registered when created with                  ║
-- ║ SNOWFLAKE.ML.CLASSIFICATION. You can view it in the Model Registry:     ║
-- ║                                                                          ║
-- ║   SHOW MODELS IN SCHEMA MARROWCO_DONOR_LAB.HOL;                            ║
-- ║                                                                          ║
-- ║ In a production workflow, you would:                                     ║
-- ║   1. Train multiple model versions                                      ║
-- ║   2. Compare evaluation metrics across versions                         ║
-- ║   3. Promote the best version to "default"                              ║
-- ║   4. Use for real-time scoring via Dynamic Tables or Streamlit          ║
-- ╚═══════════════════════════════════════════════════════════════════════════╝

SHOW MODELS IN SCHEMA MARROWCO_DONOR_LAB.HOL;
