import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, fisher_exact, ttest_ind, mannwhitneyu, shapiro
import os
import tkinter as tk
from tkinter import filedialog
import warnings

# Suppress minor warnings for cleaner output
warnings.simplefilter(action='ignore', category=FutureWarning)

# ==========================================
# 1. SETUP & DATA CLEANING
# ==========================================
def load_and_clean_data(filename):
    # Handle both xlsx and csv
    if filename.lower().endswith('.csv'):
        df = pd.read_csv(filename)
    else:
        df = pd.read_excel(filename)
    
    # Rename '1' to 'Group' for clarity if needed
    if '1' in df.columns:
        df = df.rename(columns={'1': 'Group'})
    
    # --- FIX: Add .copy() to prevent SettingWithCopyWarning ---
    df = df[df['Group'].isin(['Case', 'Control'])].copy()
    
    # --- A. Clean Severity (GMFCS) ---
    gmfcs_map = {
        'Mild': 'Group A (Levels I-II)',
        'Moderate': 'Group B (Level III)',
        'Sever': 'Group C (Levels IV-V)'
    }
    df['GMFCS_Cleaned'] = df['GMFCS'].map(gmfcs_map)
    
    # --- B. Clean Classification (Hemiplegia) ---
    df['Classification_Cleaned'] = df['Classification '].replace({
        'Hemiplegia left': 'Hemiplegia', 
        'Hemiplegia right': 'Hemiplegia'
    })
    
    # --- C. Handle Multi-Select Columns ---
    def create_flag(df, source_col, keyword):
        # Helper to find column even if there are extra spaces in the name
        if source_col not in df.columns:
            possible_cols = [c for c in df.columns if source_col.strip() == c.strip()]
            if possible_cols:
                source_col = possible_cols[0]
            else:
                return pd.Series(['No'] * len(df), index=df.index)
        
        # Check for keyword (case insensitive)
        return df[source_col].astype(str).apply(lambda x: 'Yes' if keyword.lower() in x.lower() else 'No')

    # Labor Problems
    df['Flag_Asphyxia'] = create_flag(df, 'Labor problems', 'Asphyxia')
    df['Flag_Meconium'] = create_flag(df, 'Labor problems', 'Meconium')
    df['Flag_Prolonged'] = create_flag(df, 'Labor problems', 'Prolonged')
    df['Flag_FetalDistress'] = create_flag(df, 'Labor problems', 'Fetal')
    
    # Postnatal Problems
    df['Flag_NICU'] = create_flag(df, 'Postnatal  problem', 'NICU')
    df['Flag_Seizure'] = create_flag(df, 'Postnatal  problem', 'Seizure')
    df['Flag_Jaundice'] = create_flag(df, 'Postnatal  problem', 'Jaundice') # <--- NEW
    
    # Family History
    df['Flag_FamilyHx'] = create_flag(df, 'Family history of epilepsy', 'Yes')

    # MRI Findings
    df['Flag_PVL'] = create_flag(df, 'MRI', 'PVL')
    df['Flag_Atrophy'] = create_flag(df, 'MRI', 'Atrophy')
    df['Flag_Malformation'] = create_flag(df, 'MRI', 'Malformation')
    
    # New MRI Findings
    df['Flag_Diffuse'] = create_flag(df, 'MRI', 'Diffuse')       # Matches "Diffuse cortical injury"
    df['Flag_Hemorrhage'] = create_flag(df, 'MRI', 'Hem')        # Matches "Hemmorage" or "Hemorrhage"
    df['Flag_Basal'] = create_flag(df, 'MRI', 'Basal')           # Matches "Basal ganglia..."

    return df

# ==========================================
# 2. STATISTICAL FUNCTIONS
# ==========================================
def get_stats_cat(df, col, group_col='Group'):
    """Returns a list of rows for the dataframe with CLEANER P-values"""
    # Robust column finding (handles spaces)
    if col not in df.columns:
         possible_cols = [c for c in df.columns if col.strip() == c.strip()]
         if possible_cols:
             col = possible_cols[0]
         else:
             return []

    cross = pd.crosstab(df[col], df[group_col])
    
    if 'Case' not in cross.columns: cross['Case'] = 0
    if 'Control' not in cross.columns: cross['Control'] = 0
    cross = cross[['Case', 'Control']]
    
    # P-Value Logic
    if cross.min().min() < 5 or cross.shape != (2,2):
        if cross.shape == (2,2):
            _, p = fisher_exact(cross)
            test = "Fisher's Exact"
        else:
            _, p, _, _ = chi2_contingency(cross)
            test = "Chi-Square"
    else:
        _, p, _, _ = chi2_contingency(cross)
        test = "Chi-Square"
        
    rows = []
    total_case = df[df[group_col]=='Case'].shape[0]
    total_ctrl = df[df[group_col]=='Control'].shape[0]

    # --- Only show P-value on the first row of the group ---
    for i, idx in enumerate(cross.index):
        c_n = cross.loc[idx, 'Case']
        c_p = (c_n / total_case) * 100
        ctl_n = cross.loc[idx, 'Control']
        ctl_p = (ctl_n / total_ctrl) * 100
        
        # Only set P-value and Test name for the FIRST item (i==0)
        p_display = p if i == 0 else ""
        test_display = test if i == 0 else ""

        rows.append({
            'Variable': idx,
            'CP with Epilepsy (N)': f"{c_n} ({c_p:.1f}%)",
            'CP without Epilepsy (N)': f"{ctl_n} ({ctl_p:.1f}%)",
            'P-Value': p_display,
            'Test Used': test_display
        })
    return rows

def get_stats_cont(df, col, group_col='Group'):
    # Robust column finding
    if col not in df.columns:
         possible_cols = [c for c in df.columns if col.strip() == c.strip()]
         if possible_cols:
             col = possible_cols[0]
         else:
             return []

    case = df[df[group_col]=='Case'][col].dropna()
    ctrl = df[df[group_col]=='Control'][col].dropna()
    
    if len(case) < 3 or len(ctrl) < 3: 
        p_norm = 0 
    else:
        _, p_norm = shapiro(pd.concat([case, ctrl]))
    
    if p_norm > 0.05: # Normal
        stat, p = ttest_ind(case, ctrl)
        test = "T-Test"
        res_case = f"{case.mean():.2f} ± {case.std():.2f}"
        res_ctrl = f"{ctrl.mean():.2f} ± {ctrl.std():.2f}"
    else: # Not Normal
        stat, p = mannwhitneyu(case, ctrl)
        test = "Mann-Whitney"
        res_case = f"{case.median():.2f} [{case.quantile(0.25):.2f}-{case.quantile(0.75):.2f}]"
        res_ctrl = f"{ctrl.median():.2f} [{ctrl.quantile(0.25):.2f}-{ctrl.quantile(0.75):.2f}]"
        
    return [{
        'Variable': f"{col} (Mean/Median)",
        'CP with Epilepsy (N)': res_case,
        'CP without Epilepsy (N)': res_ctrl,
        'P-Value': p,
        'Test Used': test
    }]

# ==========================================
# 3. MAIN EXECUTION & EXCEL EXPORT
# ==========================================
def main():
    print("Opening file dialog... Please select your Excel or CSV file.")
    
    root = tk.Tk()
    root.withdraw() 
    root.lift()     
    
    input_file = filedialog.askopenfilename(
        title="Select your Data File",
        filetypes=[("Excel/CSV files", "*.xlsx *.csv")]
    )
    
    if not input_file:
        print("No file selected. Exiting.")
        return

    print(f"Selected: {input_file}")
    print("Processing data...")
    
    df = load_and_clean_data(input_file)
    
    table1_data = []
    table2_data = []
    table3_data = []

    # --- TABLE 1: DEMOGRAPHICS ---
    table1_data.extend(get_stats_cont(df, 'Age of mother at birth'))
    
    table1_data.append({'Variable': '--- SEX ---', 'P-Value': ''}) 
    table1_data.extend(get_stats_cat(df, 'Sex'))
    
    # NEW: Birth Weight
    table1_data.append({'Variable': '--- BIRTH WEIGHT ---', 'P-Value': ''}) 
    table1_data.extend(get_stats_cat(df, 'weight at birth'))

    # NEW: Multiple Gestation
    table1_data.append({'Variable': '--- MULTIPLE GESTATION ---', 'P-Value': ''}) 
    table1_data.extend(get_stats_cat(df, 'Product of multiple gestation'))

    table1_data.append({'Variable': '--- CONSANGUINITY ---', 'P-Value': ''})
    table1_data.extend(get_stats_cat(df, 'Consanguinity '))
    
    table1_data.append({'Variable': '--- GMFCS LEVEL ---', 'P-Value': ''})
    table1_data.extend(get_stats_cat(df, 'GMFCS_Cleaned'))

    # --- TABLE 2: RISK FACTORS ---
    table2_data.append({'Variable': '--- GESTATIONAL AGE ---', 'P-Value': ''})
    table2_data.extend(get_stats_cat(df, 'Gestational age'))
    
    # NEW: Mode of Delivery
    table2_data.append({'Variable': '--- MODE OF DELIVERY ---', 'P-Value': ''})
    table2_data.extend(get_stats_cat(df, 'Mode of delivery'))
    
    binary_vars_lab = [
        ('Family History of Epilepsy', 'Flag_FamilyHx'),
        ('Asphyxia', 'Flag_Asphyxia'), 
        ('Meconium Aspiration', 'Flag_Meconium'), 
        ('Prolonged Labor', 'Flag_Prolonged'),
        ('Fetal Distress', 'Flag_FetalDistress'),
        ('NICU Admission', 'Flag_NICU'), 
        ('Neonatal Seizures', 'Flag_Seizure'),
        ('Jaundice', 'Flag_Jaundice')   # <--- NEW
    ]
    
    table2_data.append({'Variable': '--- BINARY RISK FACTORS ---', 'P-Value': ''})
    for name, col in binary_vars_lab:
        rows = get_stats_cat(df, col)
        # Filter to only keep the "Yes" row
        yes_row = [r for r in rows if r['Variable'] == 'Yes']
        if yes_row:
            yes_row[0]['Variable'] = name 
            
            # Ensure P-value shows for this single row
            if yes_row[0]['P-Value'] == "": 
                 full_rows = get_stats_cat(df, col) 
                 p_row = full_rows[0]
                 yes_row[0]['P-Value'] = p_row['P-Value']
                 yes_row[0]['Test Used'] = p_row['Test Used']
                 
            table2_data.extend(yes_row)

    # --- TABLE 3: CP & MRI ---
    table3_data.append({'Variable': '--- CP TYPE ---', 'P-Value': ''})
    table3_data.extend(get_stats_cat(df, 'CP type'))
    
    table3_data.append({'Variable': '--- TOPOGRAPHY ---', 'P-Value': ''})
    table3_data.extend(get_stats_cat(df, 'Classification_Cleaned'))
    
    mri_vars = [
        ('PVL', 'Flag_PVL'), 
        ('Brain Atrophy', 'Flag_Atrophy'), 
        ('Malformation', 'Flag_Malformation'),
        ('Diffuse Cortical Injury', 'Flag_Diffuse'), # <--- NEW
        ('Hemorrhage', 'Flag_Hemorrhage'),           # <--- NEW
        ('Basal Ganglia/Thalamic', 'Flag_Basal')     # <--- NEW
    ]
    
    table3_data.append({'Variable': '--- MRI FINDINGS ---', 'P-Value': ''})
    for name, col in mri_vars:
        rows = get_stats_cat(df, col)
        yes_row = [r for r in rows if r['Variable'] == 'Yes']
        if yes_row:
            yes_row[0]['Variable'] = name 
            
            # Fix P-value visibility
            full_rows = get_stats_cat(df, col)
            p_row = full_rows[0]
            yes_row[0]['P-Value'] = p_row['P-Value']
            yes_row[0]['Test Used'] = p_row['Test Used']
            
            table3_data.extend(yes_row)

    # --- EXPORT TO EXCEL ---
    output_file = 'CP_Epilepsy_Tables_V3.xlsx'
    
    def clean_p(data_list):
        for row in data_list:
            if isinstance(row['P-Value'], (float, int)):
                if row['P-Value'] < 0.001:
                    row['P-Value'] = "<0.001"
                else:
                    row['P-Value'] = round(row['P-Value'], 3)
        return pd.DataFrame(data_list)

    df1 = clean_p(table1_data)
    df2 = clean_p(table2_data)
    df3 = clean_p(table3_data)

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Table 1 - Demographics', index=False)
        df2.to_excel(writer, sheet_name='Table 2 - Risk Factors', index=False)
        df3.to_excel(writer, sheet_name='Table 3 - CP & MRI', index=False)
        
    print(f"Success! Tables saved to: {output_file}")
    try:
        os.system(f"open '{output_file}'")
    except:
        pass

if __name__ == "__main__":
    main()