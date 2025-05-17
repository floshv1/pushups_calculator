import json
import os
import yaml
from datetime import datetime


MAX_HISTORY_ENTRIES = 100
HISTORY_PATH = "data/history.json"

filepath = "/config/config_parameter.yaml"
absolute_path = os.path.abspath(os.getcwd() + filepath) 

def load_config(file_path = absolute_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_history(path=HISTORY_PATH):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return json.load(f)

def save_to_history(entry, path=HISTORY_PATH):
    from pushups_calculator.utils import generate_incremental_id
    history = load_history(path)

    # Ajout du timestamp
    entry['date'] = datetime.today().strftime("%Y-%m-%d")
    
    # Générer un ID unique incrémental
    entry['entry_id'] = generate_incremental_id(history)
    
    history.append(entry)

    # Limite le nombre d’entrées
    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]

    with open(path, 'w') as f:
        json.dump(history, f, indent=4)

    print(f"✅ Entrée ajoutée à l'historique avec ID {entry['entry_id']}.")

def read_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    return []