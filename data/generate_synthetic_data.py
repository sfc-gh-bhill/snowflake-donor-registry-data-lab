#!/usr/bin/env python3
"""
LSC Donor for All Data Lab — Synthetic Data Generator
========================================================
Generates realistic synthetic transplant outcome and clinical notes data
grounded in published National Transplant Registry statistics and the "Donor for All" initiative.

Deterministic: uses random.seed(42) for reproducible output.
Outputs: transplant_outcomes.csv, clinical_notes.csv

Key clinical realism:
- HCT volume ~9,000/year in US; we model a 500-patient cohort (representative sample)
- Donor type distribution reflects LSC registry reality:
    MUD 8/8 (~35%), MMUD 7/8 (~25%), Haploidentical (~30%), Cord Blood (~10%)
- GVHD rates by donor type align with published literature:
    MUD 8/8: ~35-45% acute GVHD Grade II-IV
    MMUD 7/8: ~45-55%
    Haploidentical: ~25-35% (with PTCy)
    Cord Blood: ~30-40%
- Survival data reflects 1-year OS ~55-65% for AML, varies by disease/donor type
- "Donor for All" emphasis: diverse patient demographics, MMUD outcomes approaching MUD
- SVI (Social Vulnerability Index) scores correlate with outcomes
"""

import csv
import random
import datetime
import uuid
import os

random.seed(42)

# ─── Configuration ───────────────────────────────────────────────────────────

NUM_PATIENTS = 500
NUM_CLINICAL_NOTES = 800  # ~1.6 notes per transplant on average

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ─── Reference Data ──────────────────────────────────────────────────────────

DIAGNOSES = {
    "Acute Myeloid Leukemia (AML)": {"category": "Leukemia", "weight": 0.30, "severity_base": 0.6},
    "Acute Lymphoblastic Leukemia (ALL)": {"category": "Leukemia", "weight": 0.18, "severity_base": 0.55},
    "Myelodysplastic Syndrome (MDS)": {"category": "MDS/MPN", "weight": 0.15, "severity_base": 0.5},
    "Non-Hodgkin Lymphoma (NHL)": {"category": "Lymphoma", "weight": 0.08, "severity_base": 0.45},
    "Hodgkin Lymphoma (HL)": {"category": "Lymphoma", "weight": 0.04, "severity_base": 0.4},
    "Chronic Myeloid Leukemia (CML)": {"category": "Leukemia", "weight": 0.05, "severity_base": 0.45},
    "Aplastic Anemia": {"category": "Bone Marrow Failure", "weight": 0.07, "severity_base": 0.35},
    "Sickle Cell Disease": {"category": "Hemoglobinopathy", "weight": 0.05, "severity_base": 0.3},
    "Thalassemia Major": {"category": "Hemoglobinopathy", "weight": 0.03, "severity_base": 0.3},
    "Myelofibrosis": {"category": "MDS/MPN", "weight": 0.05, "severity_base": 0.55},
}

DISEASE_STAGES = ["Early", "Intermediate", "Advanced", "CR1", "CR2", "Relapsed/Refractory"]

DONOR_TYPES = {
    "MUD_8_8":  {"weight": 0.35, "gvhd_base": 0.40, "survival_bonus": 0.05, "label": "Matched Unrelated Donor (8/8)"},
    "MMUD_7_8": {"weight": 0.25, "gvhd_base": 0.50, "survival_bonus": 0.00, "label": "Mismatched Unrelated Donor (7/8)"},
    "HAPLO":    {"weight": 0.30, "gvhd_base": 0.30, "survival_bonus": 0.02, "label": "Haploidentical"},
    "CORD":     {"weight": 0.10, "gvhd_base": 0.35, "survival_bonus": -0.03, "label": "Cord Blood"},
}

CONDITIONING_REGIMENS = [
    "Myeloablative (MAC) - BuCy", "Myeloablative (MAC) - TBI/Cy",
    "Reduced Intensity (RIC) - FluBu", "Reduced Intensity (RIC) - FluMel",
    "Non-Myeloablative (NMA) - FluTBI",
]

GVHD_PROPHYLAXIS = {
    "MUD_8_8":  ["Tacrolimus/Methotrexate", "Tacrolimus/Sirolimus", "Tacrolimus/MMF"],
    "MMUD_7_8": ["Tacrolimus/Methotrexate", "Tacrolimus/Methotrexate + ATG", "PTCy/Tacrolimus/MMF"],
    "HAPLO":    ["PTCy/Tacrolimus/MMF", "PTCy/Sirolimus/MMF"],
    "CORD":     ["Cyclosporine/MMF", "Tacrolimus/MMF"],
}

RACE_ETHNICITY = [
    ("White/Caucasian", 0.42),
    ("Black/African American", 0.20),
    ("Hispanic/Latino", 0.18),
    ("Asian/Pacific Islander", 0.10),
    ("Native American/Alaska Native", 0.03),
    ("Multiracial", 0.05),
    ("Other/Unknown", 0.02),
]

PATIENT_SEX = [("Male", 0.55), ("Female", 0.45)]
DONOR_SEX = [("Male", 0.60), ("Female", 0.40)]

# US transplant center regions (based on National Transplant Registry reporting centers)
TRANSPLANT_CENTERS = [
    {"id": "TC001", "region": "Northeast", "state": "NY", "name": "Memorial Sloan Kettering"},
    {"id": "TC002", "region": "Northeast", "state": "MA", "name": "Dana-Farber Cancer Institute"},
    {"id": "TC003", "region": "Northeast", "state": "PA", "name": "Penn Medicine"},
    {"id": "TC004", "region": "Southeast", "state": "FL", "name": "Moffitt Cancer Center"},
    {"id": "TC005", "region": "Southeast", "state": "NC", "name": "Duke University Health Plan Co.l Center"},
    {"id": "TC006", "region": "Southeast", "state": "GA", "name": "Emory Winship Cancer Institute"},
    {"id": "TC007", "region": "Midwest", "state": "MN", "name": "University of Minnesota"},
    {"id": "TC008", "region": "Midwest", "state": "WI", "name": "Health Plan Co.l College of Wisconsin"},
    {"id": "TC009", "region": "Midwest", "state": "OH", "name": "Ohio State James Cancer Hospital"},
    {"id": "TC010", "region": "Southwest", "state": "TX", "name": "MD Anderson Cancer Center"},
    {"id": "TC011", "region": "Southwest", "state": "AZ", "name": "Mayo Clinic Arizona"},
    {"id": "TC012", "region": "West", "state": "CA", "name": "City of Hope"},
    {"id": "TC013", "region": "West", "state": "CA", "name": "Stanford Health Plan Co.l Center"},
    {"id": "TC014", "region": "West", "state": "WA", "name": "Fred Hutchinson Cancer Center"},
    {"id": "TC015", "region": "Central", "state": "CO", "name": "University of Colorado"},
]

# ─── Weighted random choice helper ──────────────────────────────────────────

def weighted_choice(options_weights):
    """Select from list of (option, weight) tuples."""
    options, weights = zip(*options_weights)
    return random.choices(options, weights=weights, k=1)[0]

def weighted_choice_dict(d, key="weight"):
    """Select from dict where values contain weight key."""
    items = list(d.items())
    weights = [v[key] for _, v in items]
    return random.choices(items, weights=weights, k=1)[0]

# ─── Generate Transplant Outcomes ────────────────────────────────────────────

def generate_transplant_outcomes():
    rows = []
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2024, 12, 31)
    date_range = (end_date - start_date).days

    for i in range(NUM_PATIENTS):
        transplant_id = f"TXP-{i+1:05d}"
        patient_id = f"PAT-{i+1:05d}"

        # Demographics
        patient_age = max(1, min(75, int(random.gauss(48, 18))))
        patient_sex = weighted_choice(PATIENT_SEX)
        patient_race = weighted_choice(RACE_ETHNICITY)

        # Diagnosis
        dx_name, dx_info = weighted_choice_dict(DIAGNOSES)
        diagnosis_category = dx_info["category"]

        # Disease stage (weighted toward earlier stages)
        if dx_info["severity_base"] > 0.5:
            stage_weights = [0.15, 0.20, 0.25, 0.15, 0.10, 0.15]
        else:
            stage_weights = [0.25, 0.25, 0.10, 0.20, 0.15, 0.05]
        disease_stage = random.choices(DISEASE_STAGES, weights=stage_weights, k=1)[0]

        # Donor
        donor_type_key, donor_info = weighted_choice_dict(DONOR_TYPES)
        donor_age = max(18, min(60, int(random.gauss(32, 8))))
        donor_sex = weighted_choice(DONOR_SEX)

        # HLA match score
        if donor_type_key == "MUD_8_8":
            hla_match = 8
        elif donor_type_key == "MMUD_7_8":
            hla_match = 7
        elif donor_type_key == "HAPLO":
            hla_match = random.choice([3, 4, 5])
        else:  # CORD
            hla_match = random.choice([4, 5, 6])

        # Conditioning & prophylaxis
        if patient_age > 55 or dx_info["severity_base"] < 0.4:
            conditioning = random.choice(CONDITIONING_REGIMENS[2:])  # RIC or NMA
        else:
            conditioning = random.choice(CONDITIONING_REGIMENS[:4])  # Any
        gvhd_prophylaxis = random.choice(GVHD_PROPHYLAXIS[donor_type_key])

        # Transplant date (weighted toward more recent years)
        days_offset = int(random.triangular(0, date_range, date_range * 0.7))
        transplant_date = start_date + datetime.timedelta(days=days_offset)

        # Transplant center
        center = random.choice(TRANSPLANT_CENTERS)

        # Patient geography (3-digit ZIP)
        zip_3digit = str(random.randint(100, 999))

        # SVI score (Social Vulnerability Index: 0-1, higher = more vulnerable)
        # Correlate with race/ethnicity for realism
        svi_base = {
            "White/Caucasian": 0.35, "Black/African American": 0.60,
            "Hispanic/Latino": 0.55, "Asian/Pacific Islander": 0.40,
            "Native American/Alaska Native": 0.65, "Multiracial": 0.45,
            "Other/Unknown": 0.50,
        }
        svi_score = round(max(0, min(1, random.gauss(svi_base[patient_race], 0.15))), 2)

        # ─── Outcome Modeling ────────────────────────────────────────
        # Base GVHD risk from donor type
        gvhd_risk = donor_info["gvhd_base"]

        # Age adjustment
        if patient_age > 55:
            gvhd_risk += 0.08
        elif patient_age < 18:
            gvhd_risk -= 0.05

        # Sex mismatch (female donor → male recipient increases risk)
        if donor_sex == "Female" and patient_sex == "Male":
            gvhd_risk += 0.06

        # PTCy reduces GVHD
        if "PTCy" in gvhd_prophylaxis:
            gvhd_risk -= 0.12

        # Disease severity
        gvhd_risk += dx_info["severity_base"] * 0.1

        # SVI impact (higher vulnerability slightly worsens outcomes)
        gvhd_risk += svi_score * 0.05

        # Clamp and add noise
        gvhd_risk = max(0.05, min(0.95, gvhd_risk + random.gauss(0, 0.08)))
        gvhd_risk_score = round(gvhd_risk, 2)

        # Acute GVHD grade (0-4)
        if random.random() < gvhd_risk:
            if random.random() < 0.3:
                acute_gvhd_grade = random.choice([3, 4])  # Severe
            else:
                acute_gvhd_grade = random.choice([1, 2])  # Mild-moderate
        else:
            acute_gvhd_grade = 0

        # Chronic GVHD
        chronic_probs = {0: 0.5, 1: 0.2, 2: 0.15, 3: 0.1, 4: 0.05}
        if acute_gvhd_grade >= 2:
            chronic_gvhd = random.choices(
                ["NONE", "MILD", "MODERATE", "SEVERE"],
                weights=[0.25, 0.25, 0.30, 0.20], k=1
            )[0]
        else:
            chronic_gvhd = random.choices(
                ["NONE", "MILD", "MODERATE", "SEVERE"],
                weights=[0.60, 0.20, 0.15, 0.05], k=1
            )[0]

        # Time to engraftment (days)
        engraft_base = {"MUD_8_8": 16, "MMUD_7_8": 17, "HAPLO": 18, "CORD": 24}
        time_to_engraftment = max(10, int(random.gauss(engraft_base[donor_type_key], 4)))

        # Relapse
        relapse_base = 0.25 + dx_info["severity_base"] * 0.15
        if disease_stage in ["Relapsed/Refractory", "Advanced"]:
            relapse_base += 0.15
        relapse_flag = 1 if random.random() < relapse_base else 0

        # Survival
        base_survival = 0.60 + donor_info["survival_bonus"]
        if acute_gvhd_grade >= 3:
            base_survival -= 0.20
        if relapse_flag:
            base_survival -= 0.25
        if disease_stage in ["Relapsed/Refractory", "Advanced"]:
            base_survival -= 0.10
        if svi_score > 0.7:
            base_survival -= 0.05
        base_survival = max(0.10, min(0.90, base_survival))

        if random.random() < base_survival:
            survival_status = "ALIVE"
            survival_days = random.randint(365, 2200)
        else:
            survival_status = "DECEASED"
            if acute_gvhd_grade >= 3:
                survival_days = random.randint(15, 365)
            elif relapse_flag:
                survival_days = random.randint(60, 540)
            else:
                survival_days = random.randint(30, 730)

        rows.append({
            "TRANSPLANT_ID": transplant_id,
            "PATIENT_ID": patient_id,
            "PATIENT_AGE": patient_age,
            "PATIENT_SEX": patient_sex,
            "PATIENT_RACE_ETHNICITY": patient_race,
            "DIAGNOSIS": dx_name,
            "DIAGNOSIS_CATEGORY": diagnosis_category,
            "DISEASE_STAGE": disease_stage,
            "DONOR_TYPE": donor_type_key,
            "HLA_MATCH_SCORE": hla_match,
            "DONOR_AGE": donor_age,
            "DONOR_SEX": donor_sex,
            "CONDITIONING_REGIMEN": conditioning,
            "GVHD_PROPHYLAXIS": gvhd_prophylaxis,
            "TRANSPLANT_DATE": transplant_date.isoformat(),
            "TRANSPLANT_CENTER_ID": center["id"],
            "CENTER_REGION": center["region"],
            "CENTER_STATE": center["state"],
            "TIME_TO_ENGRAFTMENT_DAYS": time_to_engraftment,
            "ACUTE_GVHD_GRADE": acute_gvhd_grade,
            "CHRONIC_GVHD": chronic_gvhd,
            "RELAPSE_FLAG": relapse_flag,
            "SURVIVAL_DAYS": survival_days,
            "SURVIVAL_STATUS": survival_status,
            "GVHD_RISK_SCORE": gvhd_risk_score,
            "PATIENT_ZIP_3DIGIT": zip_3digit,
            "SVI_SCORE": svi_score,
        })

    return rows

# ─── Generate Clinical Notes ────────────────────────────────────────────────

NOTE_TYPES = ["POST_TRANSPLANT_FOLLOWUP", "GVHD_ASSESSMENT", "DISCHARGE_SUMMARY", "RESEARCH_ANNOTATION"]

PHYSICIAN_IDS = [f"DR-{i:03d}" for i in range(1, 31)]

# Templates for realistic clinical narrative generation
FOLLOWUP_TEMPLATES = [
    "Patient is day +{day} post allogeneic HCT from {donor_type} donor for {diagnosis}. {engraft_status}. {gvhd_status}. {general_status}. Plan: {plan}.",
    "Day +{day} follow-up. {donor_type} transplant for {diagnosis}. {engraft_status}. Current medications include {prophylaxis}. {gvhd_status}. {complication}. Will continue current management and reassess in {followup} days.",
    "Routine post-transplant assessment at day +{day}. Patient received {conditioning} conditioning followed by {donor_type} HCT. {engraft_status}. {gvhd_status}. Performance status {kps}%. {plan}.",
]

GVHD_TEMPLATES = [
    "GVHD assessment day +{day}. {organ_involvement}. Current grade: {grade}. {biopsy_status}. Patient on {prophylaxis} for prophylaxis. {treatment_response}. {skin_status}. Recommend {recommendation}.",
    "Evaluated for suspected GVHD at day +{day} post-{donor_type} transplant. {symptom_detail}. {organ_involvement}. Clinical grade {grade} acute GVHD. {treatment_plan}. Close monitoring with repeat assessment in {followup} days.",
    "Day +{day} GVHD evaluation. {organ_involvement}. Staging: {staging}. Overall grade {grade}. {treatment_response}. Chimerism studies show {chimerism}% donor. {plan}.",
]

DISCHARGE_TEMPLATES = [
    "Discharge summary: {age}yo {sex} with {diagnosis} ({stage}) who underwent {donor_type} HCT on {date}. Hospital course: {course}. Engraftment day +{engraft_day}. {gvhd_status}. Discharge medications: {meds}. Follow-up: outpatient in {followup} days.",
    "Patient discharged day +{engraft_day} following {conditioning} {donor_type} transplant for {diagnosis}. {course}. Neutrophil engraftment achieved. {gvhd_status}. {infection_status}. Discharge condition: {condition}.",
]

RESEARCH_TEMPLATES = [
    "Research annotation: This {donor_type} transplant case demonstrates {finding}. Patient {patient_id} with {diagnosis} showed {outcome_detail}. Relevant to ongoing {study_area} research. HLA match: {hla}/8. {note}.",
    "Case flagged for {study_area} analysis. {age}yo {race} patient with {diagnosis} received {donor_type} graft ({hla}/8 match). {outcome_detail}. {svi_note}. Data contributed to National Transplant Registry registry.",
]


def generate_note_text(note_type, patient_data):
    """Generate realistic clinical note text based on patient data."""
    p = patient_data
    day = random.randint(14, 365)
    donor_label = DONOR_TYPES[p["DONOR_TYPE"]]["label"]

    # Common fragments
    engraft_options = [
        f"Neutrophil engraftment achieved on day +{p['TIME_TO_ENGRAFTMENT_DAYS']}",
        f"ANC >500 first noted on day +{p['TIME_TO_ENGRAFTMENT_DAYS']}, platelet engraftment pending",
        f"Full engraftment confirmed on day +{p['TIME_TO_ENGRAFTMENT_DAYS']} with ANC >1000",
    ]
    engraft_status = random.choice(engraft_options)

    gvhd_options = {
        0: ["No evidence of GVHD at this time", "No signs or symptoms of acute GVHD", "GVHD screening negative"],
        1: ["Mild skin rash consistent with Grade I GVHD", "Stage 1 skin GVHD noted, maculopapular rash <25% BSA"],
        2: ["Grade II acute GVHD with skin and upper GI involvement", "Moderate GVHD: skin stage 2, liver stage 1"],
        3: ["Grade III acute GVHD with significant skin and GI involvement requiring systemic therapy", "Severe GVHD with stage 3 skin, stage 2 GI. Started ruxolitinib."],
        4: ["Grade IV acute GVHD with multiorgan involvement. Critical. ICU consultation requested.", "Life-threatening GVHD: stage 4 skin, stage 3 GI, stage 2 liver. Escalating immunosuppression."],
    }
    gvhd_status = random.choice(gvhd_options.get(p["ACUTE_GVHD_GRADE"], gvhd_options[0]))

    general_options = [
        "Patient tolerating oral medications well", "Appetite improving, mild fatigue persists",
        "Oral intake adequate, no fever", "Patient ambulatory, mild mucositis resolving",
        "Some nausea managed with ondansetron", "Improving energy levels, CMV monitoring negative",
    ]
    general_status = random.choice(general_options)

    plan_options = [
        "Continue current immunosuppression, taper per protocol",
        "Continue monitoring, repeat labs in 1 week",
        "Adjust tacrolimus levels, continue surveillance",
        "Initiate slow taper of immunosuppression",
        "Continue supportive care, reassess at next visit",
    ]
    plan = random.choice(plan_options)

    kps = random.choice([60, 70, 80, 90, 100])

    if note_type == "POST_TRANSPLANT_FOLLOWUP":
        template = random.choice(FOLLOWUP_TEMPLATES)
        return template.format(
            day=day, donor_type=donor_label, diagnosis=p["DIAGNOSIS"],
            engraft_status=engraft_status, gvhd_status=gvhd_status,
            general_status=general_status, plan=plan, prophylaxis=p["GVHD_PROPHYLAXIS"],
            complication=random.choice(["No infectious complications", "CMV reactivation treated with valganciclovir",
                                         "BK viruria noted, monitoring", "No significant complications"]),
            conditioning=p["CONDITIONING_REGIMEN"], kps=kps, followup=random.choice([7, 14, 21, 28]),
        )

    elif note_type == "GVHD_ASSESSMENT":
        organ_options = [
            "Skin involvement: maculopapular rash on trunk and extremities",
            "GI involvement: watery diarrhea ~500mL/day, nausea",
            "Skin and GI involvement noted", "Liver enzymes mildly elevated, skin clear",
            "Skin stage 2 with pruritic rash involving >50% BSA",
            "Upper GI: persistent nausea and anorexia. Lower GI: diarrhea resolving",
        ]
        treatment_options = [
            "Responding well to topical steroids",
            "Started on systemic methylprednisolone 2mg/kg",
            "Ruxolitinib added as second-line therapy",
            "Current regimen controlling symptoms adequately",
            "Partial response to steroids, considering ruxolitinib",
        ]
        template = random.choice(GVHD_TEMPLATES)
        return template.format(
            day=day, donor_type=donor_label, organ_involvement=random.choice(organ_options),
            grade=p["ACUTE_GVHD_GRADE"], biopsy_status=random.choice(["Skin biopsy confirmed", "Biopsy pending", "Clinical diagnosis"]),
            prophylaxis=p["GVHD_PROPHYLAXIS"],
            treatment_response=random.choice(treatment_options),
            skin_status=random.choice(["Skin improving", "Stable findings", "New lesions noted"]),
            recommendation=random.choice(["Continue current therapy", "Escalate immunosuppression", "Add ECP", "Dermatology consult"]),
            symptom_detail=random.choice(["Patient reports new skin rash and diarrhea", "Increasing liver enzymes noted on labs",
                                           "New onset pruritus and erythema", "Worsening oral mucositis with odynophagia"]),
            treatment_plan=random.choice(["Initiate topical steroids and reassess", "Start systemic steroids",
                                           "Optimize current prophylaxis doses", "Add budesonide for GI GVHD"]),
            staging=f"Skin {random.randint(0,4)}, Liver {random.randint(0,3)}, GI {random.randint(0,3)}",
            chimerism=random.choice([95, 97, 98, 99, 100]),
            followup=random.choice([3, 5, 7, 14]), plan=plan,
        )

    elif note_type == "DISCHARGE_SUMMARY":
        course_options = [
            "Uncomplicated post-transplant course",
            "Course complicated by febrile neutropenia treated with broad-spectrum antibiotics",
            "Prolonged neutropenia with mucositis, now resolving",
            "CMV reactivation day +21 treated with ganciclovir, now resolved",
            "Mild VOD managed with supportive care, now improving",
        ]
        template = random.choice(DISCHARGE_TEMPLATES)
        return template.format(
            age=p["PATIENT_AGE"], sex=p["PATIENT_SEX"].lower(), diagnosis=p["DIAGNOSIS"],
            stage=p["DISEASE_STAGE"], donor_type=donor_label, date=p["TRANSPLANT_DATE"],
            course=random.choice(course_options), engraft_day=p["TIME_TO_ENGRAFTMENT_DAYS"],
            gvhd_status=gvhd_status,
            meds=f"{p['GVHD_PROPHYLAXIS']}, acyclovir, fluconazole, trimethoprim-sulfamethoxazole",
            followup=random.choice([5, 7, 10, 14]),
            conditioning=p["CONDITIONING_REGIMEN"],
            infection_status=random.choice(["No active infections", "Completing antiviral course", "All cultures negative"]),
            condition=random.choice(["stable", "good", "fair, improving"]),
        )

    else:  # RESEARCH_ANNOTATION
        findings = [
            "outcomes consistent with emerging data on PTCy-based haploidentical transplantation",
            "improved engraftment kinetics with this donor-recipient HLA configuration",
            "the importance of SVI-adjusted outcome analysis in transplant equity research",
            "a case supporting expanded donor pool access through the Donor for All initiative",
            "correlation between pre-transplant disease burden and post-transplant complications",
            "utility of reduced intensity conditioning in older patients with acceptable toxicity",
        ]
        study_areas = [
            "GVHD biomarker", "transplant equity", "donor selection optimization",
            "conditioning intensity", "long-term outcomes", "health disparities",
        ]
        outcome_detail_options = [
            f"{'favorable' if p['SURVIVAL_STATUS'] == 'ALIVE' else 'adverse'} outcome with survival of {p['SURVIVAL_DAYS']} days",
            f"acute GVHD grade {p['ACUTE_GVHD_GRADE']}, chronic GVHD: {p['CHRONIC_GVHD'].lower()}",
        ]
        svi_notes = [
            f"SVI score {p['SVI_SCORE']} suggests {'higher social vulnerability' if p['SVI_SCORE'] > 0.5 else 'lower social vulnerability'}",
            f"Social determinants assessment: SVI {p['SVI_SCORE']}, {p['PATIENT_RACE_ETHNICITY']} patient from ZIP {p['PATIENT_ZIP_3DIGIT']}",
        ]
        template = random.choice(RESEARCH_TEMPLATES)
        return template.format(
            donor_type=donor_label, finding=random.choice(findings),
            patient_id=p["PATIENT_ID"], diagnosis=p["DIAGNOSIS"],
            outcome_detail=random.choice(outcome_detail_options),
            study_area=random.choice(study_areas), hla=p["HLA_MATCH_SCORE"],
            note=random.choice(["Flagged for multivariable analysis", "Include in annual outcomes report",
                                 "Relevant for upcoming National Transplant Registry publication", "Cross-reference with LSC registry data"]),
            age=p["PATIENT_AGE"], race=p["PATIENT_RACE_ETHNICITY"], svi_note=random.choice(svi_notes),
        )


def generate_clinical_notes(transplant_rows):
    notes = []
    note_counter = 0

    for patient in transplant_rows:
        # Each patient gets 1-3 notes
        num_notes = random.choices([1, 2, 3], weights=[0.30, 0.45, 0.25], k=1)[0]

        for _ in range(num_notes):
            if note_counter >= NUM_CLINICAL_NOTES:
                break
            note_counter += 1

            note_type = random.choices(
                NOTE_TYPES,
                weights=[0.35, 0.30, 0.20, 0.15],
                k=1
            )[0]

            # Note date: transplant date + random offset
            base_date = datetime.date.fromisoformat(patient["TRANSPLANT_DATE"])
            offset = random.randint(7, 400)
            note_date = base_date + datetime.timedelta(days=offset)

            notes.append({
                "NOTE_ID": f"NOTE-{note_counter:05d}",
                "TRANSPLANT_ID": patient["TRANSPLANT_ID"],
                "NOTE_DATE": note_date.isoformat(),
                "NOTE_TYPE": note_type,
                "PHYSICIAN_ID": random.choice(PHYSICIAN_IDS),
                "NOTE_TEXT": generate_note_text(note_type, patient),
            })

        if note_counter >= NUM_CLINICAL_NOTES:
            break

    return notes

# ─── Validation ──────────────────────────────────────────────────────────────

def validate_data(outcomes, notes):
    print(f"\n{'='*60}")
    print("DATA VALIDATION REPORT")
    print(f"{'='*60}")

    # Outcomes validation
    print(f"\n--- Transplant Outcomes ({len(outcomes)} rows) ---")
    assert len(outcomes) == NUM_PATIENTS, f"Expected {NUM_PATIENTS} rows, got {len(outcomes)}"
    print(f"  ✓ Row count: {len(outcomes)}")

    # Donor type distribution
    donor_dist = {}
    for r in outcomes:
        donor_dist[r["DONOR_TYPE"]] = donor_dist.get(r["DONOR_TYPE"], 0) + 1
    print("  Donor type distribution:")
    for dt, count in sorted(donor_dist.items()):
        pct = count / len(outcomes) * 100
        print(f"    {dt}: {count} ({pct:.1f}%)")

    # GVHD grade distribution
    gvhd_dist = {}
    for r in outcomes:
        g = r["ACUTE_GVHD_GRADE"]
        gvhd_dist[g] = gvhd_dist.get(g, 0) + 1
    print("  Acute GVHD grade distribution:")
    for g in sorted(gvhd_dist.keys()):
        pct = gvhd_dist[g] / len(outcomes) * 100
        print(f"    Grade {g}: {gvhd_dist[g]} ({pct:.1f}%)")

    # Survival
    alive = sum(1 for r in outcomes if r["SURVIVAL_STATUS"] == "ALIVE")
    print(f"  Survival: {alive}/{len(outcomes)} ({alive/len(outcomes)*100:.1f}%) alive")

    # Race distribution
    race_dist = {}
    for r in outcomes:
        race_dist[r["PATIENT_RACE_ETHNICITY"]] = race_dist.get(r["PATIENT_RACE_ETHNICITY"], 0) + 1
    print("  Race/Ethnicity distribution:")
    for race, count in sorted(race_dist.items(), key=lambda x: -x[1]):
        pct = count / len(outcomes) * 100
        print(f"    {race}: {count} ({pct:.1f}%)")

    # Notes validation
    print(f"\n--- Clinical Notes ({len(notes)} rows) ---")
    print(f"  ✓ Row count: {len(notes)}")

    # FK integrity
    outcome_ids = {r["TRANSPLANT_ID"] for r in outcomes}
    note_fk_valid = all(n["TRANSPLANT_ID"] in outcome_ids for n in notes)
    print(f"  ✓ FK integrity (all TRANSPLANT_IDs valid): {note_fk_valid}")

    # Note type distribution
    note_type_dist = {}
    for n in notes:
        note_type_dist[n["NOTE_TYPE"]] = note_type_dist.get(n["NOTE_TYPE"], 0) + 1
    print("  Note type distribution:")
    for nt, count in sorted(note_type_dist.items()):
        pct = count / len(notes) * 100
        print(f"    {nt}: {count} ({pct:.1f}%)")

    # Average note length
    avg_len = sum(len(n["NOTE_TEXT"]) for n in notes) / len(notes)
    print(f"  Average note length: {avg_len:.0f} chars")

    print(f"\n{'='*60}")
    print("ALL VALIDATIONS PASSED ✓")
    print(f"{'='*60}\n")


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating synthetic transplant outcome data...")
    outcomes = generate_transplant_outcomes()

    print("Generating synthetic clinical notes...")
    notes = generate_clinical_notes(outcomes)

    # Write CSVs
    outcomes_path = os.path.join(OUTPUT_DIR, "transplant_outcomes.csv")
    with open(outcomes_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=outcomes[0].keys())
        writer.writeheader()
        writer.writerows(outcomes)
    print(f"Wrote {outcomes_path}")

    notes_path = os.path.join(OUTPUT_DIR, "clinical_notes.csv")
    with open(notes_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=notes[0].keys())
        writer.writeheader()
        writer.writerows(notes)
    print(f"Wrote {notes_path}")

    # Validate
    validate_data(outcomes, notes)
