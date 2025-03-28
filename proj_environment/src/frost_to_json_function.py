import json
import os

def save_to_json(data, filename):
    """
    Lagrer data til en JSON-fil.
    
    :param data: Dataen som skal lagres (må være serialiserbar til JSON)
    :param filename: Filstien hvor JSON-filen skal lagres
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=5, ensure_ascii=False)
        
        print(f"Data lagret i {filename}")

    except Exception as e:
        print(f"Feil ved lagring av JSON-fil: {e}")


