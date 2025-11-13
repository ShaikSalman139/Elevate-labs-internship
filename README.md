# Data Cleaning Task — Amazon dataset

This repository contains the results of the data cleaning & preprocessing task.

## Files included
- `cleaned_amazon.csv` — cleaned dataset produced by the pipeline
- `cleaning_summary.txt` — step-by-step log of what was done

## What I did (short)
- Removed columns with >50% missing values (if any).
- Trimmed and lowercased string columns.
- Parsed date-like columns to datetime where possible.
- Converted numeric-like strings to numeric columns.
- Dropped exact duplicate rows.
- Imputed missing values: numeric -> median, categorical -> mode/unknown, datetime -> mode/earliest.
- Capped numeric outliers using the IQR rule.
- Standardized column names to lowercase with underscores.

## How to reproduce
Run the included Jupyter notebook or the `cleaning_script.py` (not included here) with Python 3.x and pandas installed.

## Notes
- Be careful reviewing columns that were auto-converted; verify currency and percentage columns if present.
- If more domain knowledge is available (e.g., product categories, price units), refine imputation and outlier strategy accordingly.# Elevate-labs-internship
tasks
