#!/usr/bin/env python3
"""
Mann-Whitney U Test Script

Usage:
    python3 mann_whitney_u_test.py

Requirements:
    pip install scipy numpy

Input file:
    Reads the data-processing output directly (single source of truth):
    ../2_data_processing/output_data/lab_summary.csv
"""

import os
import csv
import numpy as np
from scipy import stats

# 1. Read the data (data-processing output)
HERE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(HERE, "..", "2_data_processing", "output_data", "lab_summary.csv")

if not os.path.exists(INPUT):
    raise SystemExit(
        f"Input file not found: {os.path.normpath(INPUT)}\n\n"
        "This file is produced by ../2_data_processing/plastic_footprint.py. It holds\n"
        "one row per laboratory and is therefore not redistributed with this repository\n"
        "(see README, 'About the survey data'). Run the data-processing step first."
    )

with open(INPUT) as f:
    reader = csv.DictReader(f)
    labs = list(reader)

# 2. Split into ITC and non-ITC groups 
itc_plastic = []
itc_co2 = []
nonitc_plastic = []
nonitc_co2 = []

for lab in labs:
    plastic = float(lab["total_plastic_kg"])
    co2 = float(lab["total_co2e_kg"])

    if lab["itc_status"] == "ITC":
        itc_plastic.append(plastic)
        itc_co2.append(co2)
    else:
        nonitc_plastic.append(plastic)
        nonitc_co2.append(co2)

# 3. Mann-Whitney U test 
u_plastic, p_plastic = stats.mannwhitneyu(
    itc_plastic, nonitc_plastic, alternative="two-sided"
)
u_co2, p_co2 = stats.mannwhitneyu(
    itc_co2, nonitc_co2, alternative="two-sided"
)

#  4. Print the results 
print("=" * 60)
print("MANN-WHITNEY U TEST RESULTS")
print("=" * 60)

print(f"\nTotal labs: {len(labs)}")
print(f"ITC: {len(itc_plastic)}, non-ITC: {len(nonitc_plastic)}")

print(f"\n--- PLASTIC CONSUMPTION (kg) ---")
print(f"ITC     median: {np.median(itc_plastic):.1f}  mean: {np.mean(itc_plastic):.1f}")
print(f"non-ITC median: {np.median(nonitc_plastic):.1f}  mean: {np.mean(nonitc_plastic):.1f}")
print(f"U = {u_plastic:.0f}, p = {p_plastic:.4f}")

print(f"\n--- CARBON FOOTPRINT (kg CO₂e) ---")
print(f"ITC     median: {np.median(itc_co2):.1f}  mean: {np.mean(itc_co2):.1f}")
print(f"non-ITC median: {np.median(nonitc_co2):.1f}  mean: {np.mean(nonitc_co2):.1f}")
print(f"U = {u_co2:.0f}, p = {p_co2:.4f}")
