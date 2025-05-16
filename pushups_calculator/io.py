import json
import os
import yaml
from datetime import datetime
import hashlib

MAX_HISTORY_ENTRIES = 100
HISTORY_PATH = "data/historique.json"

filepath = "/config/config.yaml"
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

def compute_entry_hash(entry):
    """Crée une signature unique à partir de la performance et des objectifs"""
    entry_str = json.dumps({
        'performance': entry.get('performance', {}),
        'objectives': entry.get('objectives', {}),
        'note_opgg': entry.get('note_opgg', 0)
    }, sort_keys=True)
    return hashlib.sha256(entry_str.encode()).hexdigest()

def save_to_history(entry, path=HISTORY_PATH):
    history = load_history(path)

    # Ajout du timestamp
    entry['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Générer une empreinte unique pour éviter les doublons
    entry_hash = compute_entry_hash(entry)
    if any(compute_entry_hash(e) == entry_hash for e in history):
        print("⚠️  Entrée déjà présente dans l'historique. Ignorée.")
        return

    history.append(entry)

    # Limite le nombre d’entrées
    if len(history) > MAX_HISTORY_ENTRIES:
        history = history[-MAX_HISTORY_ENTRIES:]

    with open(path, 'w') as f:
        json.dump(history, f, indent=4)

    print("✅ Entrée ajoutée à l'historique.")