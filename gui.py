# gui.py
import tkinter as tk
from pushups_calculator.calcul import calculate_pushups
from pushups_calculator.io import save_to_history, load_config

config = load_config()

def run(nb_joueurs=1):
    root = tk.Tk()
    root.title("Calculateur de Pompes")

    joueurs_frame = tk.Frame(root)
    joueurs_frame.pack(padx=10, pady=10)

    joueurs_entries = []

    # Champs pour chaque joueur
    for i in range(nb_joueurs):
        frame = tk.LabelFrame(joueurs_frame, text=f"Joueur {i + 1}", padx=5, pady=5)
        frame.grid(row=0, column=i, padx=5)

        pseudo = tk.Entry(frame)
        kills = tk.Entry(frame)
        morts = tk.Entry(frame)
        assists = tk.Entry(frame)
        note = tk.Entry(frame)

        tk.Label(frame, text="Pseudo").grid(row=0, column=0)
        pseudo.grid(row=1, column=0)

        tk.Label(frame, text="Kills").grid(row=2, column=0)
        kills.grid(row=3, column=0)

        tk.Label(frame, text="Morts").grid(row=4, column=0)
        morts.grid(row=5, column=0)

        tk.Label(frame, text="Assists").grid(row=6, column=0)
        assists.grid(row=7, column=0)

        tk.Label(frame, text="Note OP.GG").grid(row=8, column=0)
        note.grid(row=9, column=0)

        joueurs_entries.append({
            'pseudo': pseudo,
            'kills': kills,
            'morts': morts,
            'assists': assists,
            'note': note
        })

    # Objectifs communs
    objectifs_frame = tk.LabelFrame(root, text="Objectifs communs", padx=10, pady=10)
    objectifs_frame.pack(padx=10, pady=10)

    elder = tk.Entry(objectifs_frame)
    baron = tk.Entry(objectifs_frame)
    dragon = tk.Entry(objectifs_frame)
    tour = tk.Entry(objectifs_frame)

    tk.Label(objectifs_frame, text="Elder").grid(row=0, column=0)
    elder.grid(row=0, column=1)

    tk.Label(objectifs_frame, text="Baron").grid(row=1, column=0)
    baron.grid(row=1, column=1)

    tk.Label(objectifs_frame, text="Dragons").grid(row=2, column=0)
    dragon.grid(row=2, column=1)

    tk.Label(objectifs_frame, text="Tours").grid(row=3, column=0)
    tour.grid(row=3, column=1)

    # Objectifs avec cases à cocher
    herald_var = tk.IntVar()
    atakhan_var = tk.IntVar()
    grubs_var = tk.IntVar()
    boots_var = tk.IntVar()

    tk.Checkbutton(objectifs_frame, text="Herald", variable=herald_var).grid(row=0, column=2)
    tk.Checkbutton(objectifs_frame, text="Atakhan", variable=atakhan_var).grid(row=1, column=2)
    tk.Checkbutton(objectifs_frame, text="Grubs", variable=grubs_var).grid(row=2, column=2)
    tk.Checkbutton(objectifs_frame, text="Bottes Triomphantes", variable=boots_var).grid(row=3, column=2)

    result_frame = tk.Frame(root)
    result_frame.pack(pady=10)

    result_labels = []

    def calculer():
        for label in result_labels:
            label.destroy()
        result_labels.clear()

        objectifs = {
            'elder': int(elder.get() or 0),
            'baron': int(baron.get() or 0),
            'herald': herald_var.get(),
            'dragons': int(dragon.get() or 0),
            'grubs': grubs_var.get(),
            'atakhan': atakhan_var.get(),
            'tour': int(tour.get() or 0)
        }

        for entry in joueurs_entries:
            performance = {
                'kills': int(entry['kills'].get() or 0),
                'morts': int(entry['morts'].get() or 0),
                'assists': int(entry['assists'].get() or 0),
                'bottes_triompantes': boots_var.get()
            }
            note = float(entry['note'].get() or 0)
            pseudo = entry['pseudo'].get() or "Joueur inconnu"

            total = calculate_pushups(performance, objectifs, note, config, debug=True)

            result = f"{pseudo} doit faire {total} pompes"
            lbl = tk.Label(result_frame, text=result)
            lbl.pack()
            result_labels.append(lbl)

            save_to_history({
                "pseudo": pseudo,
                "performance": performance,
                "objectives": objectifs,
                "note_opgg": note,
                "pompes": total
            })

    tk.Button(root, text="Calculer", command=calculer).pack(pady=10)

    root.mainloop()
