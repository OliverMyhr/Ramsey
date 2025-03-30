import json
import os

def save_to_json(data, filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=5, ensure_ascii=False)
        
        print(f"Data lagret i {filename}")

    except Exception as e:
        print(f"Feil ved lagring av JSON-fil: {e}")