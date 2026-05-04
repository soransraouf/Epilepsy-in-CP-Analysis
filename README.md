# Risk Factors Associated with Epilepsy in Children with Cerebral Palsy

This repository contains the data analysis scripts and documentation for our retrospective case-control study investigating the predictive risk factors for epilepsy among children with cerebral palsy (CP). 

## 📖 Abstract & Background
Epilepsy is a common comorbidity in children with CP, with prevalence estimates ranging from 15% to 60%. This study aims to identify contributing clinical patterns and potential risk factors associated with epilepsy to improve early diagnosis and effective management.

* **Location:** Children Rehabilitation Center (CRC) in Sulaimani City, Iraq.
* **Study Period:** March 15 to November 15, 2025.
* **Cohort:** 100 children (50 cases, 50 controls) aged 2 to 10 years[cite: 2].

## 📊 Methodology & Features
Our Python-based analysis automates the data cleaning and statistical evaluation of demographic data, birth complications, maternal/family history, and neonatal factors[cite: 1, 2]. 

The script performs the following:
* **Data Cleaning:** Maps GMFCS severity levels, cleans classification variables, and extracts binary flags for multi-select columns like labor problems and MRI findings.
* **Statistical Testing:** Automatically applies Shapiro-Wilk tests for normality, followed by T-Tests or Mann-Whitney U tests for continuous variables. It uses Chi-Square or Fisher's Exact tests for categorical variables based on sample sizes[cite: 1].
* **Export:** Generates a formatted Excel file (`CP_Epilepsy_Tables_V3.xlsx`) containing three organized tables: Demographics, Risk Factors, and CP & MRI findings[cite: 1].

## 🛠️ Installation & Setup
To run this analysis locally, ensure you have Python installed. 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/CP-Epilepsy-Risk-Analysis.git](https://github.com/YourUsername/CP-Epilepsy-Risk-Analysis.git)
   cd CP-Epilepsy-Risk-Analysis
