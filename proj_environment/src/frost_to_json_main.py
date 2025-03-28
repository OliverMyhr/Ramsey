import os
from frost import json_file as jf
from frost import final_data as fd
from frost_to_json_function import save_to_json as sj
from frost import params as p

def main():
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