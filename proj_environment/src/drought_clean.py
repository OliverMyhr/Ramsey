import pandas as pd

df = pd.read_csv("../data/filtered1_data.csv")
min_temp = -50
max_temp = 50
fips_codes = [1001, 1003, 1005]
ignore_col = ["fips", "date", "score"]

def unrealistic_temp_T2M(df, min_temp, max_temp):

    unrealistic_T2M = df[(df["T2M"] < min_temp) | (df["T2M"] > max_temp)]
    return unrealistic_T2M

def unrealistic_temp_T2M_MIN(df, min_temp, max_temp):
    
        unrealistic_T2M_MIN = df[(df["T2M_MIN"] < min_temp) | (df["T2M_MIN"] > max_temp)]
        return unrealistic_T2M_MIN

def unrealistic_temp_T2M_MAX(df, min_temp, max_temp):

    unrealistic_T2M_MAX = df[(df["T2M_MAX"] < min_temp) | (df["T2M_MAX"] > max_temp)]
    return unrealistic_T2M_MAX

def check_unrealistic_temperature(df, min_temp, max_temp):

    while True:

        try:

            check = input("Hva slags type sjekk vil du ha? '1' = T2M, '2' = T2M_MIN, '3' = T2M_MAX, '4' = avslutt: ")

            unrealistic_T2M = unrealistic_temp_T2M(df, min_temp, max_temp)
            unrealistic_T2M_MIN = unrealistic_temp_T2M_MIN(df, min_temp, max_temp)
            unrealistic_T2M_MAX = unrealistic_temp_T2M_MAX(df, min_temp, max_temp)
            
            if check == "1":

                if unrealistic_T2M.empty:
                    return f"Ingen urealistiske temperaturer funnet. Trenger ikke endre på noen rader."
                else:
                    return f"Urealistiske temperaturverdier funnet i {len(unrealistic_T2M)} rader. Verdiene består av {unrealistic_T2M["T2M"].unique()}."
                
            elif check == "2":

                if unrealistic_T2M_MIN.empty:
                    return f"Ingen urealistiske temperaturer funnet. Trenger ikke endre på noen rader."
                else:
                    return f"Urealistiske temperaturverdier funnet i {len(unrealistic_T2M_MIN)} rader. Verdiene består av {unrealistic_T2M_MIN["T2M_MIN"].unique()}."
                
            elif check == "3":

                if unrealistic_T2M_MAX.empty:
                    return f"Ingen urealistiske temperaturer funnet. Trenger ikke endre på noen rader."
                else:
                    return f"Urealistiske temperaturverdier funnet i {len(unrealistic_T2M_MAX)} rader. Verdiene består av {unrealistic_T2M_MAX["T2M_MAX"].unique()}."
            
            elif check == "4":
                return f"Avslutter program."
            
            else:
                print("Invalid input. Skriv enten '1', '2', '3', eller '4'(avslutt).")

        except Exception as e:
            print("Noe gikk galt", e)

def replace(df, fips_codes):
    
    ignore_cols = ignore_col.copy()

    check_col = [col for col in df.columns if col not in ignore_col]

    for fips in fips_codes:

        fips_df = df[df["fips"] == fips]

        for col in check_col:

            mean_val = fips_df[col].mean()
            std_dev = fips_df[col].std()

            min_val = mean_val - 2 * std_dev
            max_val = mean_val + 2 * std_dev

            mask = (df["fips"] == fips)
            df.loc[mask, col] = df.loc[mask, col].apply(lambda x: mean_val if x < min_val or x > max_val else x)

        return df

def replace_to_csv(df, fips_codes):

    while True:

        try:

            replacement = input("Ønsker du å erstatte verdiene i datasettet? (y/n): ")

            if replacement.lower() == "y":

                df = replace(df, fips_codes)
                ignore_cols = ignore_col.copy()
                col_round = [col for col in df.columns if col not in ignore_cols]

                df[col_round] = df[col_round].round(2)
                                   
                df.to_csv("../data/filtered1_data_cleaned.csv", index = False)

                return f"Ny fil laget med erstattede verdier."
            
            elif replacement.lower() == "n":

                return f"Ingen ny fil laget."
            
            else:
                print(f"Invalid input. Skriv 'y'(ja) eller 'n'(nei).")
        
        except Exception as e:
            print("Noe gikk galt", e)

def find_mean_value(df, fips_codes):
    
    while True:

        try:

            f_mean = input("Ønsker du å finne gjennomsnittsverdier? (y/n): ")

            if f_mean.lower() == "y":
                
                columns_available = [col for col in df.columns if col not in ["fips", "date"]]
                print(f"Tilgjengelige kolonner for utregning av gjennomsnitt: {columns_available}")
                spec_cols = input("Ønsker du å finne gjennomsnittsverdier for spesifikke kolonner eller alle? (Skriv 1 for 'spesifikke' eller 2 for 'alle': ")

                map_lowercase = {col.lower(): col for col in columns_available}
                
                if spec_cols == "1":

                    choose_column = input("Hvilke(n) kolonne(r) vil du finne gjennomsnittet for? Skriv kolonne(r) på følgende format: 'T2M T2M_MIN' osv. (uten anførselstegn): ")
                    chosen_columns = choose_column.split()

                    invalid_columns = [col for col in chosen_columns if col not in map_lowercase]

                    if invalid_columns:
                        print(f"Invalide kolonner: {invalid_columns}. Prøv igjen.")
                        continue

                    chosen_columns = [map_lowercase[col] for col in chosen_columns]

                else:

                    chosen_columns = columns_available

                print(f"Tilgjengelige FIPS koder: {fips_codes}")
                spec_mean_value = input("Ønsker du å finne gjennomsnittet for noen spesifikke FIPS koder, eller alle? Skriv ønskede FIPS koder på følgende format: '1001 1003' osv. (uten anførselstegn) eller 'alle' for alle: ")

                if (spec_mean_value.lower() == "alle"):

                    df_filtered = df[df["fips"].isin(fips_codes)]
                    mean_values = df_filtered.groupby("fips")[chosen_columns].mean(numeric_only=True)

                    mean_values = mean_values.round(2)

                    return mean_values
                
                else:

                    try:

                        chosen_fips = list(map(int, spec_mean_value.strip().split()))

                        valid_fips = [f for f in chosen_fips if f in fips_codes]
                        
                        if not valid_fips:
                            print("Ingen av de skrevne FIPS kodene er valide. Prøv igjen.")
                            continue
                        
                        df_filtered = df[df["fips"].isin(valid_fips)]
                        mean_values = df_filtered.groupby("fips")[chosen_columns].mean(numeric_only=True)

                        mean_values = mean_values.round(2)

                        return mean_values
                    
                    except ValueError:
                        print("Invalid FIPS kode input. Skriv FIPS kode(r) på følgende format: '1001 1003' osv. (uten anførselstegn) neste gang.")
        
            else:

                return f"Ingen gjennomsnittsverdi valgt."
    
        except Exception as e:
            print("Noe gikk galt", e)

def find_median(df, fips_codes):
    
    while True:

        try:
            
            f_median = input("Ønsker du å finne median verdier? (y/n): ")

            if f_median.lower() == "y":
                
                columns_available = [col for col in df.columns if col not in ["fips", "date"]]
                print(f"Tilgjengelige kolonner for beregning av median: {columns_available}")
                spec_cols = input("Ønsker du å finne median verdier for spesifikke kolonner eller alle? (Skriv 1 for 'spesifikk' eller 2 for 'alle': ")

                map_lowercase = {col.lower(): col for col in columns_available}
                
                if spec_cols == "1":

                    choose_column = input("Hvilke(n) kolonne(r) ønsker du å finne median for? Skriv kolonne(r) på følgende format: 'T2M T2M_MIN' osv. (uten anførselstegn): ")
                    chosen_columns = choose_column.split()

                    invalid_columns = [col for col in chosen_columns if col not in map_lowercase]

                    if invalid_columns:
                        print(f"Invalide kolonner: {invalid_columns}. Prøv igjen.")
                        continue

                    chosen_columns = [map_lowercase[col] for col in chosen_columns]

                else:

                    chosen_columns = columns_available

                print(f"Tilgjengelige FIPS koder: {fips_codes}")
                spec_median = input("Ønsker du å finne median for spesifikke FIPS koder, eller alle? Skriv ønskede FIPS koder på følgende format: '1001 1003' etc. (uten anførselstegn) eller 'alle' for alle: ")

                if (spec_median.lower() == "alle"):

                    df_filtered = df[df["fips"].isin(fips_codes)]
                    median_values = df_filtered.groupby("fips")[chosen_columns].median(numeric_only=True)

                    return median_values
                
                else:

                    try:

                        chosen_fips = list(map(int, spec_median.strip().split()))

                        valid_fips = [f for f in chosen_fips if f in fips_codes]
                        
                        if not valid_fips:
                            print("Ingen av de skrevne FIPS kodene er valide. Prøv igjen.")
                            continue
                        
                        df_filtered = df[df["fips"].isin(valid_fips)]
                        median_values = df_filtered.groupby("fips")[chosen_columns].median(numeric_only=True)

                        return median_values
                    
                    except ValueError:
                        print("Invalid FIPS kode input. Skriv FIPS koder på følgende format: '1001 1003' etc. (uten anførselstegn) neste gang.")
        
            else:

                return f"Ingen medianverdi valgt."
    
        except Exception as e:
            print("Noe gikk galt", e)