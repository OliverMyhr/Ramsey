import requests
import os
from dotenv import load_dotenv
import pandas as pd
import pandasql as pdsql

load_dotenv()

key = os.getenv("frost_api_client_id")
url = os.getenv("frost_url")
id = os.getenv("id_granaasen")

elements = "relative_humidity, air_temperature, mean(air_temperature P1D), max(rainfall_rate PT1M), wind_from_direction"

time = "2024-10-01/2025-03-20"
test_time = "2025-02-02/2025-02-04"

params = {"sources" : id, "elements" : elements, "referencetime" : time}
test_params = {"sources" : id, "elements" : elements, "referencetime" : test_time}

def file(parameters):
    try:
        f = requests.get(url, params = parameters, auth = (key, ""))
        data_file = f.json()

        return data_file
    
    except requests.exceptions.RequestException as e:
        print(f"Data kunne ikke hentes: {e}")


def understand_structure():
    import json
    f = file(test_params)

    
    print(f.keys())
    print(json.dumps(f, indent = 5))

def setUp_file():
    setUp = file(params)
    data = setUp.get("data")
    liste = []

    for entry in data:
        tidspunkt = entry.get("referenceTime", "")
        sted = entry.get("source")

        
        row_data = {"sted": sted, "tidspunkt": tidspunkt}

        for obs in entry.get("observations"):
            element = obs.get("elementId")
            value = obs.get("value")
            row_data[element] = value  

        
        liste.append(pd.Series(row_data))

    df = pd.DataFrame(liste)
    
    print(df)


setUp_file()