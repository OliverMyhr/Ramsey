from scipy.stats import pearsonr
import pandas as pd
import drought_clean as dc
from importlib import reload

reload(dc)

fips_codes = dc.fips_codes
df = pd.read_csv("../data/filtered1_data_cleaned.csv")

def corr_analysis(df, fips_codes, var_1, var_2):

    try:

        for fips in fips_codes:

            analyze = df[df["fips"] == fips][[var_1, var_2]].dropna()

            if len(analyze) < 2:

                print(f"Not enough data for FIPS {fips}.")

                continue

            correlation, p_value = pearsonr(analyze[var_1], analyze[var_2])

            if abs(correlation) < 0.3:

                strength = "Weak correlation"

            elif abs(correlation) < 0.6:

                strength = "Moderate correlation"

            else:

                strength = "Strong correlation"

            significance = "Significant" if p_value < 0.05 else "Not significant"

            print(f"FIPS-code: {fips}")
            print(f"Correlation value: {correlation:.2f}")
            print(f"P-value: {p_value:.10f}")
            print(f"Result: {strength} | {significance}")

        return f"Done with analysis for {var_1} and {var_2}."
    
    except KeyError as e:

        return f"KeyError: {e}. Please check variable names."