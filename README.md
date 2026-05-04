# Risk Factors Associated with Epilepsy in Children with Cerebral Palsy

This repository contains the Python-based statistical analysis and research documentation for a retrospective case-control study investigating predictive risk factors for epilepsy among children with cerebral palsy (CP) in Sulaimani.

---

## 📖 Project Overview
Epilepsy is a common comorbidity in children with CP, with prevalence estimates ranging from 15% to 60%. This study aims to identify contributing clinical patterns and potential risk factors—such as neonatal seizures, GMFCS severity levels, and specific MRI findings—to improve early diagnosis and management.

*   **Study Site:** Children Rehabilitation Center (CRC) in Sulaimani City, Iraq.
*   **Study Period:** March 15 to November 15, 2025.
*   **Participants:** 100 children (50 cases with epilepsy, 50 controls without) aged 2 to 10 years.

## 📊 Data Analysis Features
The analysis is powered by a Python script, `analysisv2.py`, which automates the statistical workflow to ensure methodology is consistent and reproducible:

*   **Data Cleaning:** Maps GMFCS levels, standardizes topographical classifications, and flags risk factors from multi-select clinical entries.
*   **Statistical Testing:** 
    *   Performs **Shapiro-Wilk** tests to check for normality.
    *   Applies **T-Tests** or **Mann-Whitney U** tests for continuous variables.
    *   Utilizes **Chi-Square** or **Fisher’s Exact** tests for categorical data depending on sample distribution.
*   **Automated Export:** Generates a structured Excel file (`CP_Epilepsy_Tables_V3.xlsx`) containing formatted tables for Demographics, Risk Factors, and CP/MRI findings.
