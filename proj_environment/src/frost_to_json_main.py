import os
from frost_data_collection import json_file as jf
from frost_data_collection import final_data as fd
from frost_to_json_function import save_to_json as sj
from frost_data_collection import params as p

def main(): # Bruker funksjonen fra frost_to_json_function til å lagre API data til json fil i data mappen
    base_path = os.path.dirname(os.path.abspath(__file__))  
    
    
    initial_json_path = os.path.join(base_path, '../data/initial_data.json')
    final_json_path = os.path.join(base_path, '../data/final_data.json')

    print(f"Initial JSON path: {initial_json_path}")
    print(f"Final JSON path: {final_json_path}")
    
    initial_data = jf(p)
    final_dataframe = fd()

    sj(initial_data, initial_json_path)
    sj(final_dataframe.to_dict(orient='records'), final_json_path)

main()