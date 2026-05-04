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
    *   Applies **T-Tests** or **Mann-Whitney U** tests for continuous variables[cite: 1].
    *   Utilizes **Chi-Square** or **Fisher’s Exact** tests for categorical data depending on sample distribution[cite: 1].
*   **Automated Export:** Generates a structured Excel file (`CP_Epilepsy_Tables_V3.xlsx`) containing formatted tables for Demographics, Risk Factors, and CP/MRI findings[cite: 1].

---

## 📁 Repository Structure
```text
CP-Epilepsy-Risk-Analysis/
├── data/
│   └── Sample_Data.xlsx       # Randomized data for testing functionality
├── docs/
│   └── Research_Paper.pdf     # Full study documentation (originally last.pdf)
├── src/
│   └── analysisv2.py          # Primary Python analysis script
├── .gitignore                 # Prevents accidental upload of sensitive clinical data
├── README.md                  # Project documentation
└── requirements.txt           # Required Python libraries
🛠️ Installation & Setup
1. Install Dependencies
Ensure you have Python installed. Clone this repository and install the required libraries using pip:

Bash
pip install -r requirements.txt
2. Usage
Navigate to the src/ directory.

Run the analysis script:

Bash
python analysisv2.py
File Selection: A file dialog UI will appear[cite: 1]. Navigate to the data/ folder and select Sample_Data.xlsx (or your own formatted Data.xlsx file).

Results: The script will process the data and automatically generate the final results file: CP_Epilepsy_Tables_V3.xlsx[cite: 1].

👥 Research Team
Dr. Ibrahim Khasraw Ghafoor – Assistant Professor of Pediatrics  

Gailan Othman Ali – Fourth-year Medical Student[cite: 2]

Soran Salah Raouf – Fourth-year Medical Student[cite: 2]

Rawa Ahmad Salih – Fourth-year Medical Student[cite: 2]

Institution: Branch of Clinical Sciences, College of Medicine, University of Sulaimani[cite: 2].

🔒 Ethics & Privacy
To protect patient privacy and comply with clinical ethics, the raw dataset (Data.xlsx) is not included in this public repository[cite: 2].

The data/Sample_Data.xlsx file contains randomized/synthetic data created to demonstrate the script's functionality[cite: 1].

The actual study was conducted following approval from the relevant clinical and ethical authorities at the University of Sulaimani[cite: 2].

📝 License
This project is licensed under the MIT License. You are free to use, modify, and distribute this code for research purposes, provided appropriate credit is given to the original research team.
