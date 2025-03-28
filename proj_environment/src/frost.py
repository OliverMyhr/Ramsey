import requests
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as pdsql

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