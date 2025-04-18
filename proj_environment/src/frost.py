import requests
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as pdsql
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

load_dotenv()

key = os.getenv("FROST_API_CLIENT_ID")
url = os.getenv("FROST_URL")

time = os.getenv("FROST_TIME")
id = os.getenv("FROST_ID")
elements = os.getenv("FROST_ELEMENTS")

test_time = os.getenv("FROST_TEST_TIME")
test_elements = os.getenv("FROST_TEST_ELEMENTS")
test_id = os.getenv("FROST_TEST_ID")

params = {"sources" : id, "elements" : elements, "referencetime" : time}
test_params = {"sources" : test_id, "elements" : test_elements, "referencetime" : test_time}

def json_file(parameters):
    try:
        r = requests.get(url, params = parameters, auth = (key, ""))
        data_file = r.json()

        return data_file
        
    except requests.exceptions.RequestException as e:
        return f"Data kunne ikke hentes: {e}"


def understand_structure():
    import json

    understand = json_file(test_params)
    js = json.dumps(understand, indent = 5)
    key = understand.keys()

    return f"{key}\n{js}"


def to_df():
    js_file = json_file(params)

    if not isinstance(js_file, dict) or "data" not in js_file:
        print("Feil: Ugyldig eller tom respons fra API.")

        return pd.DataFrame()  
    
    data = js_file["data"]
    
    if not data:  
        print("Ingen data mottatt.")

        return pd.DataFrame()  

    dfs = []

    for e in data:
        observations = e.get("observations", [])
        
        if not observations:
            print(f"Entry uten observasjoner: {e.get('sourceId', 'Ukjent sourceId')}")

            continue 
        
        df_e = pd.DataFrame(observations)
        
        if df_e.empty:
            continue
        
        df_e["referenceTime"] = e.get("referenceTime", None)
        df_e["sourceId"] = e.get("sourceId", None)

        dfs.append(df_e)

    if not dfs:
        print("Ingen observasjoner funnet.")

        return pd.DataFrame()  

    df = pd.concat(dfs, ignore_index=True)

    wanted = ["referenceTime", "sourceId", "elementId", "value"]
    df = df[wanted]

    df["referenceTime"] = pd.to_datetime(df["referenceTime"])

    return df  


def clean(df):
    df.dropna(subset=["value"], inplace=True)
    df["value"] = df["value"].fillna(df["value"].mean())

    return df


def analyze(df):
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame()

    source_mapping = {"SN68173" : "Gløshaugen", "SN90450" : "Tromsø", "SN68090" : "Granåsen", "SN18700" : "Blindern"}

    df["sourceId"] = df["sourceId"].str.split(":").str[0] 
    df["sourceId"] = df["sourceId"].map(source_mapping).fillna(df["sourceId"])

    query = """
    SELECT referenceTime, sourceId, elementId, AVG(value) as avg_value
    FROM df
    GROUP BY referenceTime, sourceId, elementId
    """
    result = pdsql.sqldf(query, locals())

    return result


def final_data():
    initial_df = to_df()
    
    if initial_df.empty:
        print("Ingen data tilgjengelig.")

        return pd.DataFrame()

    cleaned = clean(initial_df) 
    final = analyze(cleaned)

    return final

def pivot_data():
    df = final_data()
    pivot = df.pivot_table(values = "avg_value", index = "referenceTime", columns = "elementId")

    return pivot


def statistics():
    df = final_data()

    if df.empty:
        return "DataFrame er tom."
    
    stats = df.groupby(["sourceId", "elementId"])["avg_value"].agg(["mean", "median", "std", "min", "max", "count"])

    return stats


def relation_analysis():
    pivot = pivot_data()

    if len(pivot.columns) < 2:
        return "Ikke nok elementer for å beregne sammenhenger."

    relation = pivot.corr()

    return f"Skala mellom -1 og 1, der 1 betyr sterk sammenheng, tall nærmere 0 betyr svak sammenheng.\n\n{relation}"


def relation_analysis_plots():
    pivot = pivot_data()    
    relation = pivot.corr()

    fig, axs = plt.subplots(1, 2, figsize = (15, 5))

    try:
        sns.heatmap(relation, annot = True, cmap = "coolwarm", fmt = ".2f", square = True, ax = axs[0])
        axs[0].set_title("Sammenheng mellom elementer")
    
    except Exception as e:
            print("Feil under plotting", e)
            fig.delaxes(axs[0])

    if "air_temperature" in pivot.columns and "relative_humidity" in pivot.columns:
        sns.scatterplot(x = pivot["air_temperature"], y = pivot["relative_humidity"], ax = axs[1])
        axs[1].set_xlabel("Temperatur [°C]")
        axs[1].set_ylabel("Luftfuktighet [%]")
        axs[1].set_title("Temperatur vs Luftfuktighet")
        axs[1].grid(True)

    else:
        fig.delaxes(axs[1])
        print("Manglende data")

    plt.show()


def find_outliers():
    df = final_data()

    k1 = df["avg_value"].quantile(0.25)
    k3 = df["avg_value"].quantile(0.75)

    ikv = k3 - k1
    lower = k1 - 1.5 * ikv
    upper = k3 + 1.5 * ikv

    outliers = df[(df["avg_value"] < lower) | (df["avg_value"] > upper)]

    print(f"Antall outliers: {len(outliers)}\n")

    return outliers


def remove_outliers():
    df = final_data()

    k1 = df["avg_value"].quantile(0.25)
    k3 = df["avg_value"].quantile(0.75)

    ikv = k3 - k1
    lower = k1 - 1.5 * ikv
    upper = k3 + 1.5 * ikv

    removed = df[(df["avg_value"] >= lower) & (df["avg_value"] <= upper)]

    print(f"Originalt antall rader: {len(df)}")
    print(f"Antall rader etter fjerning av outliers: {len(removed)}\n\n")

    return removed