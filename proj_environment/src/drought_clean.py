import pandas as pd

df = pd.read_csv("../data/filtered1_data.csv")
min_temp = -50
max_temp = 50
fips_codes = [1001, 1003, 1005]

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

            check = input("What kind of check do you want? '1' = T2M, '2' = T2M_MIN, '3' = T2M_MAX, '4' = exit: ")

            unrealistic_T2M = unrealistic_temp_T2M(df, min_temp, max_temp)
            unrealistic_T2M_MIN = unrealistic_temp_T2M_MIN(df, min_temp, max_temp)
            unrealistic_T2M_MAX = unrealistic_temp_T2M_MAX(df, min_temp, max_temp)
            
            if check == "1":

                if unrealistic_T2M.empty:
                    return f"No unrealistic temperature values found. No need to adjust any rows."
                else:
                    return f"Unrealistic temperature values found in {len(unrealistic_T2M)} rows. The values consist of {unrealistic_T2M["T2M"].unique()}."
                
            elif check == "2":

                if unrealistic_T2M_MIN.empty:
                    return f"No unrealistic temperature values found. No need to adjust any rows."
                else:
                    return f"Unrealistic temperature values found in {len(unrealistic_T2M_MIN)} rows. The values consist of {unrealistic_T2M_MIN["T2M_MIN"].unique()}."
                
            elif check == "3":

                if unrealistic_T2M_MAX.empty:
                    return f"No unrealistic temperature values found. No need to adjust any rows."
                else:
                    return f"Unrealistic temperature values found in {len(unrealistic_T2M_MAX)} rows. The values consist of {unrealistic_T2M_MAX["T2M_MAX"].unique()}."
            
            elif check == "4":
                return f"Stopping program."
            
            else:
                print("Invalid input. Please enter '1', '2', '3', or '4'(exit).")

        except Exception as e:
            print("Something went wrong:", e)

check_unrealistic_temperature(df, min_temp, max_temp)

def replace(df, fips_codes):

    for fips in fips_codes:

        fips_df = df[df["fips"] == fips]
        mean_PS = fips_df["PS"].mean()
        std_dev = fips_df["PS"].std()

        min_PS = mean_PS - 2 * std_dev
        max_PS = mean_PS + 2 * std_dev

        df.loc[df["fips"] == fips, "PS"] = df.loc[df["fips"] == fips, "PS"].apply(lambda x: mean_PS if x < min_PS or x > max_PS else x)

        return df

def replace_to_csv(df, fips_codes):

    while True:

        try:

            replacement = input("Do you want to replace the values in the dataset? (y/n): ")

            if replacement.lower() == "y":

                df = replace(df, fips_codes)
                df["PS"] = df["PS"].round(2)
                df.to_csv("../data/filtered1_data_cleaned.csv", index = False)

                return f"New file created with replaced values."
            
            elif replacement.lower() == "n":

                return f"No new file created."
            
            else:
                print(f"Invalid input. Please enter 'y' or 'n'.")
        
        except Exception as e:
            print("Something went wrong.", e)

def find_median(df, fips_codes):
    
    while True:

        try:
            
            f_median = input("Do you wish to find the median values? (y/n): ")

            if f_median.lower() == "y":
                
                columns_available = [col for col in df.columns if col not in ["fips", "date"]]
                print(f"Columns available for median calculation: {columns_available}")
                spec_cols = input("Do you wish to find the median for specific columns or all? (Write 1 for 'specific' or 2 for 'all': ")

                map_lowercase = {col.lower(): col for col in columns_available}
                
                if spec_cols == "1":

                    choose_column = input("Which column(s) would you like to find the median for? Write column(s) in this format: 'T2M T2M_MIN' etc. (without quotes): ")
                    chosen_columns = choose_column.split()

                    invalid_columns = [col for col in chosen_columns if col not in map_lowercase]

                    if invalid_columns:
                        print(f"Invalid columns: {invalid_columns}. Try again.")
                        continue

                    chosen_columns = [map_lowercase[col] for col in chosen_columns]

                else:

                    chosen_columns = columns_available

                print(f"Available FIPS codes: {fips_codes}")
                spec_median = input("Do you wish to find median of any specific FIPS codes, or all? Write which FIPS codes in this format: '1001 1003' etc. (without quotes) or 'all' for all: ")

                if (spec_median.lower() == "all"):

                    df_filtered = df[df["fips"].isin(fips_codes)]
                    median_values = df_filtered.groupby("fips")[chosen_columns].median(numeric_only=True)

                    return median_values
                
                else:

                    try:

                        chosen_fips = list(map(int, spec_median.strip().split()))

                        valid_fips = [f for f in chosen_fips if f in fips_codes]
                        
                        if not valid_fips:
                            print("None of the provided FIPS codes are valid. Try again.")
                            continue
                        
                        df_filtered = df[df["fips"].isin(valid_fips)]
                        median_values = df_filtered.groupby("fips")[chosen_columns].median(numeric_only=True)

                        return median_values
                    
                    except ValueError:
                        print("Invalid FIPS code input. Please enter FIPS codes in this format: '1001 1003' etc. (without quotes) next time.")
        
            else:

                return f"No median value chosen."
    
        except Exception as e:
            print("Something went wrong.", e)