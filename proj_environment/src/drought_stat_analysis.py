from scipy.stats import pearsonr
import pandas as pd
import drought_clean as dc
from importlib import reload
import matplotlib.pyplot as plt
import numpy as np

reload(dc) #Importerer modul, bruker reload() for å være sikker på at all kode er oppdatert

fips_codes = dc.fips_codes #Henter valgte FIPS koder
df = pd.read_csv("../data/filtered1_data_cleaned.csv")
ignored_cols = ["fips", "date", "score"] #Disse kolonnene skal ikke brukes i korrelasjonsanalysen (ikke målte verdier)

def corr_analysis(df, fips_codes, var_1, var_2):

    try:
        
        corr_values = [] #Lager en tom liste for å lagre korrelasjonsverdier

        for fips in fips_codes: #Itererer gjennom hver FIPS kode fra ønskt liste med FIPS koder

            analyze = df[df["fips"] == fips][[var_1, var_2]].dropna() #Filtrerer data for hver FIPS kode og fjerner eventuelle NaN verdier

            if len(analyze) < 2: #Må ha minst 2 datapunkter for at korrelasjonsanalysen skal gi mening

                print(f"Ikke nok data for FIPS {fips}.")

                continue #Fortsetter til neste FIPS kode

            correlation, p_value = pearsonr(analyze[var_1], analyze[var_2]) #Utfører korrelasjonsanalyse med pearsonr() funksjonen fra scipy.stats

            if abs(correlation) < 0.3: #Et valgt intervall for å definere styrke på korrelasjonen

                strength = "Svak korrelasjon"

            elif abs(correlation) < 0.6:

                strength = "Moderat korrelasjon"

            else:

                strength = "Sterk korrelasjon"

            significance = "Signifikant" if p_value < 0.05 else "Ikke signifikant" #P-verdier under 0.05 er typisk signifikante

            #Skriver ut diverse verdier for hver FIPS kode

            print(f"FIPS kode: {fips}")
            print(f"Korrelasjonsverdi: {correlation:.2f}")
            print(f"P-verdi: {p_value:.10f}")
            print(f"Resultat: {strength} | {significance}")

            corr_values.append(round(float(correlation), 2)) #Legger til korrelasjonsverdi i listen fra tidligere

        return corr_values
    
    except KeyError as e:

        return f"KeyError: {e}. Vennligst sjekk variabelnavn" #Håndterer KeyError hvis variabelnavnene ikke finnes i datasettet

def color_corr(corr_value): #EN funksjon for definere farge basert på korrelasjonsverdier
    
    if corr_value <= -0.6:

        return "dark red"
    
    elif corr_value <= -0.3:

        return "orange"
    
    elif corr_value <= 0.3:

        return "yellow"
    
    elif corr_value <= 0.6:

        return "green"
    
    else:

        return "blue"

def visualize_corr(fips_codes, corr_values, var_1, var_2): #Funksjon for å visualisere korrelasjonsverdier med matplotlib

    try:

        colors = [color_corr(corr) for corr in corr_values]

        plt.figure(figsize=(12, 8)) #Seter figurstørrelse
        bars = plt.bar(fips_codes, corr_values, color=colors) #ager stolpediagram for hver FIPS kode med korrelasjonsverdier og farger
        plt.title(f"Korrelasjon mellom {var_1} og {var_2} for hver FIPS kode", fontsize=16) #Tittel
        plt.xlabel("FIPS koder", fontsize=14) #Tittel på x-aksen, og størrelse
        plt.ylabel("Korrelasjonsverdi", fontsize=14) #Tittel på y-aksen, og størrelse
        plt.axhline(0, color='green', linewidth=0.8, linestyle="--") #Legger til horisontal linje på 0 for å skille mellom positive og negative korrelasjonsverdier

        for bar, r in zip(bars, corr_values): #Itererer gjennom hver stolpe og korrelasjonsverdi for å legge til tekst på toppen av hver stolpe

            plt.text(bar.get_x() + bar.get_width() / 2, r + 0.01, f"{r:.2f}", ha="center", va="bottom", fontsize=12) #Skriver tekst på toppen av hver stolpe

        #Størrelse på aksene

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.tight_layout() #For å unngå overlapping av elementer i figuren
        plt.show() #Visualiserer for brukeren
    
    except KeyError as e:

        return f"KeyError: {e}. Vennligst sjekk variabelnavn" #Håndterer KeyError hvis variabelnavnene ikke finnes i datasettet
    
def corr_var1_and_rest(df, fips_codes, var, exclude=ignored_cols): #Funksjon for å lage korrelasjonsmatrise for en valgt variabel og resten av datasettet

    try:

        all_corr = {} #Lager et tomt dictionary for å lagre korrelasjonsverdier for hver FIPS kode
        usable_cols = df.columns.difference(exclude + [var]) #Liste med kbrukbare kolonner i analysen (alle bortsett fra de som er i exclude og variabel vi ønsker å analysere)

        for fips in fips_codes: #Itererer gjennom hver FIPS kode

            next_set = df[df["fips"] == fips] #Filtrerer datasettet for hver FIPS kode
            new_corr_values = {} #Lager et tomt dictionary for å lagre korrelasjonsverdier for hver kolonne i datasettet

            for col in usable_cols: #Itererer gjennom hver (brukbar) kolonne i datasettet

                new_data = next_set[[var, col]].dropna() 

                if len(new_data) > 1: 
                
                    corr_coeff, prsn_no_use = pearsonr(new_data[var], new_data[col]) #prsn_no_use er p-verdien fra pearsonr() funksjonen (trengs ikke her)
                    new_corr_values[col] = round(float(corr_coeff), 2)

                else:

                    new_corr_values[col] = None #Ikke nok data for å beregne korrelasjonsverdi
        
            all_corr[fips] = new_corr_values #Lagrer korrelasjonsverdier for hver FIPS kode i dictionary
    
        return all_corr 
    
    except KeyError as e:
        return f"KeyError: {e}. Vennligst sjekk variabelnavn" #Håndterer KeyError hvis variabelnavnene ikke finnes i datasettet

def visualize_corr_var1_and_rest(corr_dict, fips_codes, var): #Funksjon for å visualisere korrelasjonsmatrise for en valgt variabel og resten av datasettet, her med spider chart
    
    while True:

        try:
            
            print(f"Tilgjengelige FIPS koder: {fips_codes}")
            
            try:

                what_fips = int(input("Skriv FIPS kode for å visualisere korrelasjon med andre andre variabler: ")) #Kan kun visualisere for en FIPS kode om gangen
            
            except ValueError:

                print("Invalid input. Vennligst skriv en valid (numerisk) FIPS kode.")
                continue

            if what_fips not in fips_codes:

                return f"FIPS code {what_fips} ikke funnet. Må være en av følgende: {fips_codes}"

            else:

                next_data = corr_dict.get(what_fips) #Henter korrelasjonsverdier for valgt FIPS kode

            if not next_data: #Hvis vi ikke finner data for valgt FIPS kode

                return f"Ingen data tilgjengelig for FIPS koden {what_fips}."
            
            new_vars = list(next_data.keys()) 
            new_corrs = [c if c is not None else 0 for c in next_data.values()] #Setter korrelasjonsverdier til 0 hvis det ikke er nok data for å beregne korrelasjonsverdi
            
            #Legger til første variabel/korrelasjonsverdi på slutten av listen for å lage en lukket sirkel i spider chart

            new_vars.append(new_vars[0])
            new_corrs.append(new_corrs[0])

            angle_radar = np.linspace(0, 2 * np.pi, len(new_corrs), endpoint=False).tolist()

            plt.figure(figsize=(8, 8)) #Figurstørrelse
            ax = plt.subplot(111, polar=True) #Setter subplot til polar for spider chart

            ax.plot(angle_radar, new_corrs, color="cyan", linewidth=1.5, linestyle="solid") #Plotter linjen for korrelasjonsverdier
            ax.fill(angle_radar, new_corrs, color="cyan", alpha=0.25) #Fyller området under linjen med farge

            ax.set_xticks(angle_radar[:-1]) #Setter x-aksen til vinklene for hver variabel
            ax.set_xticklabels(new_vars[:-1], fontsize=11)
            ax.set_yticks([-1, -0.5, 0, 0.5, 1])
            ax.set_yticklabels([-1, -0.5, 0, 0.5, 1], fontsize=10)
            ax.set_title(f"Korrelasjon mellom {var} og resten av variablene i FIPS {what_fips}", fontsize=15) #Tittel på spider chartet
            ax.grid(True) #Legger til rutenett for bedre lesbarhet

            plt.tight_layout()
            plt.show()

            return f"Visualisering utført for {var} med FIPS {what_fips}."

        except KeyError as e:

            print(f"KeyError: {e}. Vennligst sjekk variabelnavn") #Håndterer KeyError hvis variabelnavnene ikke finnes i datasettet
            return