import random
from datetime import datetime
from pushups_calculator.io import load_config


config = load_config()

def get_opgg_coefficient(note_opgg, config=config):
    for niveau in config['coefficients_opgg'].values():
        if niveau['min'] <= note_opgg < niveau['max']:
            return niveau['coefficient']
    # Si la note est exactement égale au max (ex: 10)
    return config['coefficients_opgg']['excellente']['coefficient']


def generate_game_id(existing_ids):
    while True:
        now_part = datetime.now().strftime("%M%S")     # e.g. 1452
        rand_part = str(random.randint(10, 99))         # e.g. 38
        new_id = now_part + rand_part                  # e.g. 145238
        if new_id not in existing_ids:
            return new_id
        

def generate_incremental_id(history):
    """
    Génère un ID incrémental à 6 chiffres sous forme de string, basé sur l'historique.
    Si pas d'ID dans l'historique, commence à 000001.
    """
    if not history:
        return "000001"
    
    # Récupère tous les IDs et convertit en int
    ids = [int(entry.get('entry_id', '0')) for entry in history if entry.get('entry_id', '').isdigit()]
    max_id = max(ids) if ids else 0
    new_id = max_id + 1
    
    return f"{new_id:06d}"