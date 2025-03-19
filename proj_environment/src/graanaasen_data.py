import pandas as pd
import requests 
import json
from dotenv import 
import os

load_dotenv()

key = os.get("")
id_granaasen = "SN68090"
elements = ["air_temperature", "air_pressure"]
url = 'https://frost.met.no/observations/v0.jsonld'
time = "2025-02-01/2025-03-01"

parameters = {"sources" : id_granaasen, "elements" : elements, "referencetime" : time}

fil = requests.get(url, parameters, auth = (key, ""))
data_fil = fil.json()