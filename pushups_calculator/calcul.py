from pushups_calculator.utils import get_opgg_coefficient


def calculate_pushups(performance, objectives, note_opgg, config, debug=False):
    """
    Calcule le nombre de pompes à faire selon les performances du joueur.

    Args:
        performance (dict): {'kills': int, 'morts': int, 'assists': int, 'bottes_triompantes': bool}
        objectives (dict): {'baron': int, 'herald': int, 'dragons': int, 'grubs': int, 'tour': int, ...}
        note_opgg (float): Note brute OP.GG
        config (dict): Configuration YAML chargée
        debug (bool): Affiche les détails du calcul si True

    Returns:
        int: Nombre de pompes à effectuer (minimum 0)
    """
    # Récupération des pénalités/bonus
    mort_penalty = config['performances_individuelles']['mort']['penalite']
    kill_assist_bonus = config['performances_individuelles']['kill_assist']['bonus']
    boots_bonus = config['bottes_triompantes']['bonus']

    # Étape 1 : Morts × pénalité
    total_death = performance['morts'] * mort_penalty
    if debug:
        print(f"Morts: {performance['morts']} × {mort_penalty} = {total_death}")

    rate = get_opgg_coefficient(note_opgg)
    total = total_death* rate

    if debug:
        print(f"Coefficient OP.GG : ×{rate} → {total_death} × {rate} = {total}")

    

    # Étape 2 : - (Kills + Assists)
    kill_assist_total = (performance['kills'] + performance['assists'])
    total -= kill_assist_total

    if debug:
        print(f"Réduction Kills + Assists: -({performance['kills']} + {performance['assists']}) × {abs(kill_assist_bonus)} = -{kill_assist_total}")

    # Étape 3 : - Objectifs épiques et secondaires
    objectifs_total = 0
    for obj, data in config['objectifs_epiques'].items():
        count = objectives.get(obj, 0)
        objectifs_total += count * data['bonus']
        if debug and count:
            print(f"{obj} : {count} × {data['bonus']} = {count * data['bonus']}")

    for obj, data in config['objectifs_secondaires'].items():
        count = objectives.get(obj, 0)
        objectifs_total += count * data['bonus']
        if debug and count:
            print(f"{obj} : {count} × {data['bonus']} = {count * data['bonus']}")

    total += objectifs_total
    if debug:
        print(f"Total objectifs : {objectifs_total}")

    # Étape 4 : Bonus bottes triomphantes
    if performance.get('bottes_triompantes', False):
        total += boots_bonus
        if debug:
            print(f"Bottes triomphantes : {boots_bonus}")
    
    final_total = int(round(total))
    if debug:
        print(f"Total final : {final_total}")

    return final_total

