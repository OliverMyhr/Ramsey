from scipy.stats import pearsonr
import pandas as pd
import drought_clean as dc
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

reload(dc)

fips_codes = dc.fips_codes
df = pd.read_csv("../data/filtered1_data_cleaned.csv")
ignored_cols = ["fips", "date", "score"]

def corr_analysis(df, fips_codes, var_1, var_2):

    try:
        
        corr_values = []

        for fips in fips_codes:

            analyze = df[df["fips"] == fips][[var_1, var_2]].dropna()

            if len(analyze) < 2:

                print(f"Ikke nok data for FIPS {fips}.")

                continue

            correlation, p_value = pearsonr(analyze[var_1], analyze[var_2])

            if abs(correlation) < 0.3:

                strength = "Svak korrelasjon"

            elif abs(correlation) < 0.6:

                strength = "Moderat korrelasjon"

            else:

                strength = "Sterk korrelasjon"

            significance = "Signifikant" if p_value < 0.05 else "Ikke signifikant"

            print(f"FIPS kode: {fips}")
            print(f"Korrelasjonsverdi: {correlation:.2f}")
            print(f"P-verdi: {p_value:.10f}")
            print(f"Resultat: {strength} | {significance}")

            corr_values.append(round(float(correlation), 2))

        return corr_values
    
    except KeyError as e:

        return f"KeyError: {e}. Vennligst sjekk variabelnavn"

def color_corr(corr_value):
    
    if corr_value <= -0.6:

        return "mørk rød"
    
    elif corr_value <= -0.3:

        return "oransje"
    
    elif corr_value <= 0.3:

        return "gul"
    
    elif corr_value <= 0.6:

        return "grønn"
    
    else:

        return "blå"

def visualize_corr(fips_codes, corr_values, var_1, var_2):

    try:

        colors = [color_corr(corr) for corr in corr_values]

        plt.figure(figsize=(12, 8))
        bars = plt.bar(fips_codes, corr_values, color=colors)
        plt.title(f"Korrelasjon mellom {var_1} og {var_2} for hver FIPS kode", fontsize=16)
        plt.xlabel("FIPS koder", fontsize=14)
        plt.ylabel("Korrelasjonsverdi", fontsize=14)
        plt.axhline(0, color='grønn', linewidth=0.8, linestyle="--")

        for bar, r in zip(bars, corr_values):

            plt.text(bar.get_x() + bar.get_width() / 2, r + 0.01, f"{r:.2f}", ha="center", va="bottom", fontsize=12)

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.tight_layout()
        plt.show()
    
    except KeyError as e:

        return f"KeyError: {e}. Vennligst sjekk variabelnavn"
    
def corr_var1_and_rest(df, fips_codes, var, exclude=ignored_cols):

    try:

        all_corr = {}
        usable_cols = df.columns.difference(exclude + [var])

        for fips in fips_codes:

            next_set = df[df["fips"] == fips]
            new_corr_values = {}

            for col in usable_cols:

                new_data = next_set[[var, col]].dropna()

                if len(new_data) > 1:
                
                    corr_coeff, prsn_no_use = pearsonr(new_data[var], new_data[col])
                    new_corr_values[col] = round(float(corr_coeff), 2)

                else:

                    new_corr_values[col] = None
        
            all_corr[fips] = new_corr_values
    
        return all_corr
    
    except KeyError as e:
        return f"KeyError: {e}. Vennligst sjekk variabelnavn"

def visualize_corr_var1_and_rest(corr_dict, fips_codes, var):
    
    while True:

        try:
            
            print(f"Tilgjengelige FIPS koder: {fips_codes}")
            
            try:

                what_fips = int(input("Skriv FIPS kode for å visualisere korrelasjon med andre andre variabler: "))
            
            except ValueError:

                print("Invalid input. Vennligst skriv en valid (numerisk) FIPS kode.")
                continue

            if what_fips not in fips_codes:

                return f"FIPS code {what_fips} ikke funnet. Må være en av følgende: {fips_codes}"

            else:

                next_data = corr_dict.get(what_fips)

            if not next_data:

                return f"Ingen data tilgjengelig for FIPS koden {what_fips}."
            
            new_vars = list(next_data.keys())
            new_corrs = [c if c is not None else 0 for c in next_data.values()]

            new_vars.append(new_vars[0])
            new_corrs.append(new_corrs[0])

            angle_radar = np.linspace(0, 2 * np.pi, len(new_corrs), endpoint=False).tolist()

            plt.figure(figsize=(8, 8))
            ax = plt.subplot(111, polar=True)

            ax.plot(angle_radar, new_corrs, color="cyan", linewidth=1.5, linestyle="solid")
            ax.fill(angle_radar, new_corrs, color="cyan", alpha=0.25)

            ax.set_xticks(angle_radar[:-1])
            ax.set_xticklabels(new_vars[:-1], fontsize=11)
            ax.set_yticks([-1, -0.5, 0, 0.5, 1])
            ax.set_yticklabels([-1, -0.5, 0, 0.5, 1], fontsize=10)
            ax.set_title(f"Korrelasjon mellom {var} og resten av variablene i FIPS {what_fips}", fontsize=15)
            ax.grid(True)

            plt.tight_layout()
            plt.show()

            return f"Visualisering utført for {var} med FIPS {what_fips}."

        except KeyError as e:

            print(f"KeyError: {e}. Vennligst sjekk variabelnavn")
            return