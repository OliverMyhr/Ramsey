import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import drought_clean as dc
from importlib import reload
import seaborn as sns

reload(dc)

fips_codes = dc.fips_codes #Henter valgte FIPS koder fra drought_clean.py
df = pd.read_csv("../data/filtered1_data_cleaned.csv")


def preparation_pred_analysis(df, fips_codes):

    while True:

        try:

            df.dropna(inplace=True) #Fjerner NaN verdier fra datasett
            df["date"] = pd.to_datetime(df["date"]) #Konverterer dato kolonnen til datetime format

            features = ["PRECTOT", "PS", "QV2M", "T2MDEW", "WS10M", "TS"] #Kolonner som skal brukes i modellen, kan justeres
            map_lowercase = {col.lower(): col for col in features} #Lager en ordbok for å mappe lowercase til originalt kolonnenavn

            analysis = input("Vil du analysere en kolonne? (j/n): ").strip().lower() #Bruker input

            if analysis != "j":
                return f"Avslutter programmet."
            
            analyze_ftr = input(f"Hvilken kolonne vil du analysere? ({list(map_lowercase.keys())}, små bokstaver): ").strip().lower() #Bruker input for å velge hvilken feature som skal analyseres
            
            if analyze_ftr not in map_lowercase:
                #Sjekker om kolonnen finnes i kolonnelista, hvis ikke så gir den en feilmelding
                print(f"Ugyldig kolonne. Vennligst velg en av {list(map_lowercase.keys())}.")
                continue

            analyze_col = map_lowercase[analyze_ftr] #Mapper lowercase til originalt kolonnenavn)

            for fips in fips_codes:

                print(f"\nAnalyserer FIPS {fips}...")
                df_fips = df[df["fips"] == fips].dropna(subset=features + [analyze_col]) #Filtrerer datasett for valgt FIPS kode

                x = df_fips[features]
                y = df_fips[analyze_col] #Setter x og y verdier for modellen, x er kolonnelisten og y er den valgte kolonnen som skal analyseres

                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0) #Deler datasett i trenings og test sett
        
                fig, axs = plt.subplots(2, 3, figsize=(15, 8)) #Lager subplots for å vise dataene
                axs = axs.flatten()

                for i, feature in enumerate(features):

                    axs[i].scatter(x_train[feature], y_train, color="blue", alpha=0.5, label="Train data") #Plotter treningsdata
                    axs[i].scatter(x_test[feature], y_test, color="red", alpha=0.5, label="Test data") #Plotter testdata
                    axs[i].set_xlabel(feature) #Setter x akse
                    axs[i].set_ylabel(analyze_ftr) #Setter y akse
                    axs[i].legend()

                fig.suptitle(f"FIPS {fips}: Sammenheng mellom kolonnelisten {features} og {analyze_ftr}", fontsize=16) #Setter tittel til hele figuren
                plt.tight_layout()
            
            new_analysis = input("Vil du analysere en annen kolonne? (j/n): ").strip().lower()

            if new_analysis != "j":

                return f"Avslutter programmet."

        except Exception as e:

            return f"Feil: {e}." #Håndterer feil ved å returnere en feilmelding
        
def regression_analysis_scatterplot(df, fips_codes):

    while True:

        try:

            df["date"] = pd.to_datetime(df["date"]) #Konverterer dato kolonnen til datetime format
            
            vars = ["PRECTOT", "PS", "QV2M", "T2MDEW", "WS10M", "TS"] #Kolonner som skal brukes i modellen, kan justeres
            map_lowercase = {var.lower(): var for var in vars} #Lager en ordbok for å mappe lowercase til originalt kolonnenavn

            print(f"\nTilgjengelige variabler: {[v.lower() for v in vars]}") #Printer tilgjengelige variabler for brukeren
            analysis = input("Vil du analysere en kolonne? (j/n): ").strip().lower()

            if analysis != "j":

                return f"Avslutter programmet."
            
            chosen_var_input = input(f"Hvilken kolonne vil du analysere? (Små bokstaver) ").strip().lower() #Bruker input for å velge hvilken variabel som skal analyseres

            if chosen_var_input not in map_lowercase:

                return f"Ugyldig kolonne. Vennligst velg en av følgende: {list(map_lowercase.keys())}."
            
            chosen_var = map_lowercase[chosen_var_input]
            features = [v for v in vars if v != chosen_var] #Setter features til alle variabler bortsett fra den valgte variabelen
            
            print(f"Variabel som skal analyseres: {chosen_var}")
            print(f"Funksjoner som skal brukes i regresjonsmodellen: {features}")

            for fips in fips_codes:

                try:

                    print(f"Starter regresjonsanalyse for FIPS {fips}...")
                    df_fips = df[df["fips"] == fips].dropna(subset=features + [chosen_var])

                    if df_fips.empty:

                        print(f"Ingen gyldig data for FIPS {fips}. Går videre.")
                        continue

                    x = df_fips[features]
                    y = df_fips[chosen_var] #Setter x og y verdier for modellen, x er kolonnelisten og y er den valgte kolonnen som skal analyseres

                    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0) #Deler datasett i trenings og test sett
                
                    model = LinearRegression() #Lager en lineær regresjonsmodell
                    model.fit(x_train, y_train)
                    y_prediction = model.predict(x_test) #Predikerer y-verdier for test-settet

                    mse = mean_squared_error(y_test, y_prediction) #Beregner MSE
                    r2 = r2_score(y_test, y_prediction)

                    print(f"r2 score for FIPS {fips}: {r2:.3f}, MSE: {mse:.3f}")
                    #Regresjonsresultater per FIPS kode med ideell prediksjon kontra virkelige verdier
                    plt.figure(figsize=(10, 6)) #Lager en figur for å vise regresjonsresultatene
                    sns.scatterplot(x=y_test, y=y_prediction, alpha=0.6, color="blue") #Plotter testdata
                    plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="Ideel prediksjon") #Plotter en ideell prediksjon
                    plt.xlabel("Virkelige verdier")
                    plt.ylabel("Predikerte verdier")
                    plt.title(f"Regresjonsanalyse for FIPS {fips} med {chosen_var} som variabel")
                    plt.legend()
                    plt.grid(True)
                    plt.tight_layout()
                    plt.show()

                    for ft in features:

                        plt.figure(figsize=(8, 5))
                        sns.regplot(x=x_test[ft], y=y_test, scatter_kws={"alpha": 0.5}, line_kws={"color": "green"}) #Plotter regresjonslinje for hver funksjon
                        plt.xlabel(ft) #Setter x akse til funksjonen
                        plt.ylabel(chosen_var) #Setter y akse til den valgte variabelen
                        plt.title(f"FIPS {fips}: {chosen_var} som funksjon av {ft}")
                        plt.grid(True)
                        plt.tight_layout()
                        plt.show()

                except Exception as e:

                    return f"Feil under regresjonsanalyse for FIPS {fips}: {e}." #Håndterer feil ved å returnere en feilmelding underveis for vær FIPS kode
                
            break

        except Exception as e:

            return f"Feil: {e}." #Håndterer feil ved å returnere en feilmelding
        
def regression_analysis_regplot(df, fips_codes):

    df["date"] = pd.to_datetime(df["date"]) #Konverterer dato kolonnen til datetime format
    all_vars = ["PRECTOT", "PS", "QV2M", "T2M", "T2MDEW", "WS10M"] #Kolonner som skal brukes i modellen, kan justeres
    map_lowercase = {v.lower(): v for v in all_vars} #Lager en ordbok for å mappe lowercase til originalt kolonnenavn

    while True:

        try:

            print(f"\nTilgjengelige variabler: {[v.lower() for v in all_vars]}") #Printer tilgjengelige variabler for brukeren
            target_input = input("Velg en variabel (små bokstaver) eller 'n' for å avslutte: ").strip().lower()

            if target_input == 'n':
                print("Avslutter regresjonsvisualisering (regplot).")
                break

            if target_input not in map_lowercase: #Sjekker om variabelen finnes i kolonnelista, hvis ikke så gir den en feilmelding
                print(f"Ugyldig valg: {target_input}. Prøv igjen.")
                continue

            chosen_var = map_lowercase[target_input] #Mapper lowercase til originalt kolonnenavn
            features = [v for v in all_vars if v != chosen_var] #Setter features til alle variabler bortsett fra den valgte variabelen

            for fips in fips_codes: #Itererer gjennom FIPS koder for å lage regresjonslinjer for hver FIPS kode

                df_fips = df[df["fips"] == fips].dropna(subset=features + [chosen_var]) #Filtrerer datasett for valgt FIPS kode

                if df_fips.empty:

                    print(f"Hopper over FIPS {fips}, ingen gyldige data.")
                    continue

                x = df_fips[features] #Setter x verdier for modellen
                y = df_fips[chosen_var] #Setter y verdier for modellen

                x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=0) #Deler datasett i trenings og test sett

                print(f"\nFIPS {fips}: Regresjonslinjer mot {chosen_var}")

                for ft in features:

                    plt.figure(figsize=(8, 5))
                    sns.regplot(x=x_train[ft], y=y_train, scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}) #Plotter regresjonslinje for hver funksjon
                    plt.title(f"FIPS {fips} {chosen_var} som funksjon av {ft}")
                    plt.xlabel(ft)
                    plt.ylabel(chosen_var)
                    plt.grid(True) #Setter grid for bedre lesbarhet
                    plt.tight_layout()
                    plt.show()

        except Exception as e:
            print(f"Feil: {e}")

def regression_analysis_lineplot(df, fips_codes):
    
    df["date"] = pd.to_datetime(df["date"]) #Konverterer dato kolonnen til datetime format
    all_vars = ["PRECTOT", "PS", "QV2M", "T2M", "T2MDEW", "WS10M"] #Kolonner som skal brukes i modellen, kan justeres
    map_lowercase = {v.lower(): v for v in all_vars} #Lager en ordbok for å mappe lowercase til originalt kolonnenavn

    while True:

        try:

            print(f"\nTilgjengelige variabler: {[v.lower() for v in all_vars]}") #Printer tilgjengelige variabler for brukeren
            var_input = input("Velg en variabel (små bokstaver) eller 'n' for å avslutte: ").strip().lower()

            if var_input == 'n':

                print("Avslutter regresjonsvisualisering (linjeplot).")
                break

            if var_input not in map_lowercase: #Sjekker om variabelen finnes i kolonnelista, hvis ikke så gir den en feilmelding

                print(f"Ugyldig variabel: {var_input}. Prøv igjen.")
                continue

            chosen_var = map_lowercase[var_input] #Mapper lowercase til originalt kolonnenavn
            features = [v for v in all_vars if v != chosen_var] #Setter features til alle variabler bortsett fra den valgte variabelen

            for fips in fips_codes:

                df_fips = df[df["fips"] == fips].dropna(subset=features + [chosen_var]) #Filtrerer datasett for valgt FIPS kode

                if df_fips.empty: #Sjekker om datasettet er tomt etter filtrering

                    print(f"Hopper over FIPS {fips}, ingen gyldige data.")
                    continue

                df_fips = df_fips.sort_values("date") #Sorter dataene etter dato for å lage en linjeplot
                x = df_fips[features] #Setter x verdier for modellen
                y = df_fips[chosen_var] #Setter y verdier for modellen

                model = LinearRegression() #Lager en lineær regresjonsmodell
                model.fit(x, y)
                df_fips["prediction"] = model.predict(x)

                print(f"\nFIPS {fips}: Faktisk vs. predikert {chosen_var} over tid")
                plt.figure(figsize=(10, 5)) #Lager en figur for å vise regresjonsresultatene
                sns.lineplot(x="date", y=chosen_var, data=df_fips, label="Faktisk", color="blue") #Plotter faktiske verdier
                sns.lineplot(x="date", y="prediction", data=df_fips, label="Predikert", color="orange", linestyle="--") #Plotter predikerte verdier
                plt.title(f"FIPS {fips}: Faktisk vs. Predikert {chosen_var} over tid")
                plt.xlabel("Dato")
                plt.ylabel(chosen_var)
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()

        except Exception as e:
            return f"Feil: {e}" #Håndterer feil ved å returnere en feilmelding

def regression_analysis_barplot(df, fips_codes):

    df["date"] = pd.to_datetime(df["date"])
    all_vars = ["PRECTOT", "PS", "QV2M", "T2M", "T2MDEW", "WS10M"]
    map_lowercase = {v.lower(): v for v in all_vars}

    while True:

        try:

            print(f"\nTilgjengelige variabler: {[v.lower() for v in all_vars]}")
            var_input = input("Velg en variabel (små bokstaver) eller 'n' for å avslutte: ").strip().lower()

            if var_input == 'n':

                print("Avslutter regresjonsvisualisering (søylediagram).")
                break

            if var_input not in map_lowercase:

                print(f"Ugyldig variabel: {var_input}. Prøv igjen.")
                continue

            chosen_var = map_lowercase[var_input]
            features = [v for v in all_vars if v != chosen_var]

            for fips in fips_codes:

                df_fips = df[df["fips"] == fips].dropna(subset=features + [chosen_var])

                if df_fips.empty:

                    print(f"Hopper over FIPS {fips}, ingen gyldige data.")
                    continue

                df_fips = df_fips.sort_values("date")
                x = df_fips[features]
                y = df_fips[chosen_var]

                model = LinearRegression()
                model.fit(x, y)
                df_fips["prediction"] = model.predict(x)

                plot_df = df_fips[["date", chosen_var, "prediction"]].melt(id_vars="date", 
                                                                           var_name="Type", 
                                                                           value_name="Verdi")

                print(f"\nFIPS {fips}: Faktisk vs. predikert {chosen_var} som søylediagram")

                plt.figure(figsize=(14, 6))
                sns.barplot(data=plot_df, x="date", y="Verdi", hue="Type", dodge=True)
                plt.title(f"FIPS {fips}: Faktisk vs. Predikert {chosen_var} over tid")
                plt.xlabel("Dato")
                plt.ylabel(chosen_var)
                plt.xticks(rotation=45)
                plt.legend(title="")
                plt.grid(True, axis='y')
                plt.tight_layout()
                plt.show()

        except Exception as e:
            return f"Feil: {e}"