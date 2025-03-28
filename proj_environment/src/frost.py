import requests
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as pdsql

load_dotenv()

key = os.getenv("FROST_API_CLIENT_ID")
url = os.getenv("FROST_URL")

id = os.getenv("ID")
#id = "SN68173"
elements = "relative_humidity, air_temperature, max(rainfall_rate PT1M), wind_from_direction"
time = "2010-01-01/2011-01-01"

test_elements = "air_temperature, wind_from_direction"
test_time = "2018-02-02/2018-02-04"
test_id = os.getenv("ID_BLINDERN")

params = {"sources" : id, "elements" : elements, "referencetime" : time}
test_params = {"sources" : test_id, "elements" : elements, "referencetime" : test_time}

def json_file(parameters):
    try:
        file = requests.get(url, params = parameters, auth = (key, ""))
        data_file = file.json()

        return data_file
        
        
    except requests.exceptions.RequestException as e:
        return f"Data kunne ikke hentes: {e}"


def understand_structure():
    import json
    understand = json_file(test_params)
    js = json.dumps(understand, indent = 5)
    key = understand.keys()

    print(key)
    print(js)


def to_df():
    js_file = json_file(params)
    data = js_file.get("data", [])

    if not data:  
        print("Ingen data mottatt.")

        return pd.DataFrame()  
    
    df = pd.DataFrame()

    for entry in data:
        observations = entry.get("observations", [])

        if not observations:  
            print(f"Entry uten observasjoner: {entry.get('sourceId', 'Ukjent sourceId')}")
            continue 

        for obs in observations:
            obs["referenceTime"] = entry.get("referenceTime", None)
            obs["sourceId"] = entry.get("sourceId", None)

        df = pd.concat([df, pd.DataFrame(observations)])

    if df.empty:  
        print("Ingen observasjoner funnet.")

        return df  

    
    keep_cols = ["referenceTime", "sourceId", "elementId", "value"]
    df = df[keep_cols]

    return df  


print(to_df())