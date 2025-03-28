import pandas as pd

df = pd.read_csv("../data/filtered1_data.csv")
min_temp = -50
max_temp = 50

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