# Calculateur de Pompes

Une application Python avec interface graphique (Tkinter) qui transforme les performances de joueurs de League of Legends en séries de pompes à effectuer. Pratique pour s'entraîner en s'amusant entre amis après une partie !

---

## Fonctionnalités

* 🎮 Saisie des performances de 1 à N joueurs (Kills, Morts, Assists, Note OP.GG).
* 🐉 Ajout d'objectifs d’équipe (Elder, Baron, Dragons, Herald, etc.).
* 📊 Calcul personnalisé du nombre de pompes à faire selon les performances.
* 🧠 Historique des parties avec filtrage par pseudo ou date.
* 👀 Détails de chaque partie disponibles en un clic dans l'historique.
* 💾 Sauvegarde automatique des résultats dans un fichier JSON.

---

## Installation

### Prérequis

* Python 3.7 ou supérieur

### Cloner le projet

```bash
git https://github.com/floshv1/pushups_calculator
cd pushups_calculator
```

### Installer les dépendances (si besoin)

```bash
pip install -r requirements.txt
```

---

## Lancer l’application

```bash
python main.py
```

> Par défaut, l'application démarre avec 1 joueur. Tu peux changer ce nombre :

```bash
python main.py --joueurs (le nombre de joueur)
```

### Example 

```bash
python main.py --joueurs 5
```

---

## Fichiers importants

### `config.yaml` (dans `config/`)

Contient les coefficients pour le calcul du nombre de pompes. Exemple :

```yaml
# Coefficients de la note OP.GG
coefficients_opgg:
  excellente:
    min: 8.5
    max: 10
    coefficient: 0.5  # Réduction
  bonne:
    min: 7
    max: 8.5
    coefficient: 1    # Normal
  moyenne:
    min: 5
    max: 7
    coefficient: 1.25 # Légère pénalité
  faible:
    min: 1
    max: 5
    coefficient: 1.5  # Punition modérée
  tres_faible:
    min: 0
    max: 1
    coefficient: 2    # Punition sévère

# Objectifs épiques
objectifs_epiques:
  elder_dragon:
    nom: "Elder"
    bonus: -7  
  baron:
    nom: "Baron"
    bonus: -6
  atakhan:
    nom: "Atakhan"
    bonus: -5

# Objectifs secondaires
objectifs_secondaires:
  herald:
    nom: "Herald"
    bonus: -4
  dragons:
    nom: "Dragons"
    bonus: -2
  grubs:
    nom: "Grubs"
    bonus: -2
  tour:
    nom: "Tour"
    bonus: -1

# Bonus des bottes triomphantes
bottes_triompantes:
  nom: "Bottes Triomphantes"
  bonus: -5  

# Performances individuelles
performances_individuelles:
  kill_assist:
    bonus: -1  # Pompes en moins pour chaque kill ou assist
  mort:
    penalite: 5  # Pompes en plus pour chaque mort
```

---

## Historique

Les résultats des parties sont enregistrés dans `data/history.json`. Tu peux les consulter dans l'application via le menu "Historique", filtrer par pseudo/date, ou cliquer sur un résultat pour afficher tous les détails de la session.

---

## Export des données

Pour réutiliser l’historique dans un autre outil (Excel, analyse...), le fichier `history.json` peut être facilement ouvert ou converti en CSV avec pandas.

---

## Auteur

Projet créé par **Floshv1** — pour motiver les joueurs à faire du sport après les games

