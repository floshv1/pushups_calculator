# gui.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pushups_calculator.utils import generate_game_id
from pushups_calculator.calcul import calculate_pushups
from pushups_calculator.io import save_to_history, load_config, read_history

config = load_config()

def launch_app(nbPlayer = 1):
    root = tk.Tk()
    root.title("Calculateur de Pompes")

    def clear_frame():
        for widget in root.winfo_children():
            if not isinstance(widget, tk.Menu):
                widget.destroy()


    def show_calculator_page():
        clear_frame()

        joueurs_frame = tk.Frame(root)
        joueurs_frame.pack(padx=10, pady=10)

        joueurs_entries = []

        anciens_pseudos = list({entry["pseudo"] for entry in read_history()})

        for i in range(nbPlayer):  # nb_joueurs=1 ici, tu peux changer
            frame = tk.LabelFrame(joueurs_frame, text=f"Joueur {i + 1}", padx=5, pady=5)
            frame.grid(row=0, column=i, padx=5)

            pseudo_var = tk.StringVar()
            pseudo_menu = ttk.Combobox(frame, textvariable=pseudo_var)
            pseudo_menu['values'] = anciens_pseudos
            pseudo_menu.set("")

            kills = tk.Entry(frame)
            morts = tk.Entry(frame)
            assists = tk.Entry(frame)
            note = tk.Entry(frame)

            tk.Label(frame, text="Pseudo").grid(row=0, column=0)
            pseudo_menu.grid(row=1, column=0)

            tk.Label(frame, text="Kills").grid(row=2, column=0)
            kills.grid(row=3, column=0)

            tk.Label(frame, text="Morts").grid(row=4, column=0)
            morts.grid(row=5, column=0)

            tk.Label(frame, text="Assists").grid(row=6, column=0)
            assists.grid(row=7, column=0)

            tk.Label(frame, text="Note OP.GG").grid(row=8, column=0)
            note.grid(row=9, column=0)

            joueurs_entries.append({
                'pseudo': pseudo_var,
                'kills': kills,
                'morts': morts,
                'assists': assists,
                'note': note
            })

        objectifs_frame = tk.LabelFrame(root, text="Objectifs communs", padx=10, pady=10)
        objectifs_frame.pack(padx=10, pady=10)

        elder = tk.Entry(objectifs_frame)
        baron = tk.Entry(objectifs_frame)
        dragon_var = tk.IntVar()
        dragon_menu = ttk.Combobox(objectifs_frame, textvariable=dragon_var)
        dragon_menu['values'] = list(range(5))
        dragon_menu.set(0)
        tour = tk.Entry(objectifs_frame)

        tk.Label(objectifs_frame, text="Elder").grid(row=0, column=0)
        elder.grid(row=0, column=1)

        tk.Label(objectifs_frame, text="Baron").grid(row=1, column=0)
        baron.grid(row=1, column=1)

        tk.Label(objectifs_frame, text="Dragons").grid(row=2, column=0)
        dragon_menu.grid(row=2, column=1)

        tk.Label(objectifs_frame, text="Tours").grid(row=3, column=0)
        tour.grid(row=3, column=1)

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

            existing_ids = [entry.get('id') for entry in read_history()]

            game_id = generate_game_id(existing_ids)

            objectifs = {
                'elder': int(elder.get() or 0),
                'baron': int(baron.get() or 0),
                'herald': herald_var.get(),
                'dragons': dragon_var.get(),
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

                final_total = max(0, total)  # Assure que le total est au moins 0
                final_total = min(final_total, 30)  # Limite le total à 100

                result = f"{pseudo} doit faire {final_total} ({total}) pompes"
                lbl = tk.Label(result_frame, text=result)
                lbl.pack()
                result_labels.append(lbl)

                save_to_history({
                    "game_id":game_id,
                    "pseudo": pseudo,
                    "performance": performance,
                    "objectives": objectifs,
                    "note_opgg": note,
                    "pompes": total,
                })

        tk.Button(root, text="Calculer", command=calculer).pack(pady=10)

    def show_history_page():
        clear_frame()

        raw_history = read_history()

        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)


        gameId = sorted({entry.get('game_id', '') for entry in raw_history if entry.get('game_id')})
        pseudos = sorted({entry.get('pseudo', '') for entry in raw_history})
        dates = [entry.get('date', '') for entry in raw_history if 'date' in entry]
        years = sorted({int(date.split("-")[0]) for date in dates if date})
        months = list(range(1, 13))
        days = list(range(1, 32))

        # Variables filtres
        id_var = tk.StringVar()
        pseudo_var = tk.StringVar()
        year_var = tk.StringVar()
        month_var = tk.StringVar()
        day_var = tk.StringVar()

        # Filtres UI

        tk.Label(filter_frame, text="Game ID:").grid(row=0, column=0)
        id_entry = ttk.Combobox(filter_frame, textvariable=id_var, values=[''] + gameId, state="readonly", width=8)
        id_entry.grid(row=0, column=1)

        tk.Label(filter_frame, text="Pseudo:").grid(row=0, column=2)
        pseudo_menu = ttk.Combobox(filter_frame, textvariable=pseudo_var, values=[''] + pseudos, state="readonly", width=10)
        pseudo_menu.grid(row=0, column=3)

        tk.Label(filter_frame, text="Année:").grid(row=0, column=4)
        year_menu = ttk.Combobox(filter_frame, textvariable=year_var, values=[''] + [str(y) for y in years], state="readonly", width=6)
        year_menu.grid(row=0, column=5)

        tk.Label(filter_frame, text="Mois:").grid(row=0, column=6)
        month_menu = ttk.Combobox(filter_frame, textvariable=month_var, values=[''] + [f"{m:02d}" for m in months], state="readonly", width=4)
        month_menu.grid(row=0, column=7)

        tk.Label(filter_frame, text="Jour:").grid(row=0, column=8)
        day_menu = ttk.Combobox(filter_frame, textvariable=day_var, values=[''] + [f"{d:02d}" for d in days], state="readonly", width=4)
        day_menu.grid(row=0, column=9)

        tk.Button(filter_frame, text="Filtrer", command=lambda: update_table()).grid(row=0, column=10, padx=5)

        # Table
        columns = ("id", "game_id", "date", "pseudo", "pompes", "kills", "morts", "assists")
        tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
        tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # En-têtes
        tree.heading("id", text="ID")
        tree.heading("game_id", text="Game ID")
        tree.heading("date", text="Date")
        tree.heading("pseudo", text="Pseudo")
        tree.heading("pompes", text="Pompes")
        tree.heading("kills", text="Kills")
        tree.heading("morts", text="Morts")
        tree.heading("assists", text="Assists")

        # Largeur colonnes
        tree.column("id", width=60, anchor="center")
        tree.column("game_id", width=60, anchor="center")
        tree.column("date", width=100, anchor="center")
        tree.column("pseudo", width=100, anchor="center")
        tree.column("pompes", width=70, anchor="center")
        tree.column("kills", width=70, anchor="center")
        tree.column("morts", width=70, anchor="center")
        tree.column("assists", width=70, anchor="center")

        details_label = tk.Label(root, text="", justify="left", anchor="w")
        details_label.pack(pady=5, fill=tk.X)

        history = []
        sort_column = None
        sort_reverse = False

        def matches_filters(entry):
            # ID filtre (exact match)
            if id_var.get().strip():
                if str(entry.get('game_id', '')).lower() != id_var.get().strip().lower():
                    return False

            pseudo_filter = pseudo_var.get().lower()
            if pseudo_filter and entry.get('pseudo', '').lower() != pseudo_filter:
                return False

            date = entry.get('date', '')
            date_parts = date.split('-') if date else ['', '', '']

            if year_var.get() and (len(date_parts) < 1 or year_var.get() != date_parts[0]):
                return False
            if month_var.get() and (len(date_parts) < 2 or month_var.get() != date_parts[1]):
                return False
            if day_var.get() and (len(date_parts) < 3 or day_var.get() != date_parts[2]):
                return False
            return True

        def treeview_sort_column(tv, col):
            nonlocal sort_column, sort_reverse

            data_list = [(tv.set(k, col), k) for k in tv.get_children('')]

            # Essayer de convertir en int si possible pour tri numérique
            try:
                data_list = [(int(item[0]), item[1]) for item in data_list]
            except ValueError:
                pass

            if sort_column == col:
                sort_reverse = not sort_reverse
            else:
                sort_reverse = False
                sort_column = col

            data_list.sort(reverse=sort_reverse)

            # Réinsérer dans l'ordre trié
            for index, (val, k) in enumerate(data_list):
                tv.move(k, '', index)

            # Mettre à jour la flèche dans l'en-tête
            for c in columns:
                tv.heading(c, text=c.capitalize())
            arrow = " ▼" if sort_reverse else " ▲"
            tv.heading(col, text=col.capitalize() + arrow)

        def update_table():
            nonlocal history
            history = read_history()
            for row in tree.get_children():
                tree.delete(row)

            for entry in history:
                if matches_filters(entry):
                    tree.insert("", tk.END, values=(
                        entry.get('entry_id', 'N/A'),
                        entry.get('game_id', 'N/A'),
                        entry.get('date', 'N/A'),
                        entry.get('pseudo', 'N/A'),
                        entry.get('pompes', 'N/A'),
                        entry.get('performance', {}).get('kills', 'N/A'),
                        entry.get('performance', {}).get('morts', 'N/A'),
                        entry.get('performance', {}).get('assists', 'N/A'),
                    ))

            # Remettre à jour tri si déjà trié
            if sort_column:
                treeview_sort_column(tree, sort_column)

        def show_details(event):
            selected = tree.focus()
            if not selected:
                return
            values = tree.item(selected, "values")
            id_selected = values[0]
            entry = next((e for e in history if str(e.get('entry_id')) == str(id_selected)), None)

            if not entry:
                details_label.config(text="Détails indisponibles.")
                return

            text = (
                f"Game ID: {entry.get('game_id', 'N/A')}\n"
                f"Pseudo: {entry.get('pseudo', 'N/A')}\n"
                f"Date: {entry.get('date', 'N/A')}\n"
                f"Pompes: {entry.get('pompes', 'N/A')}\n"
                f"Note OP.GG: {entry.get('note_opgg', 'N/A')}\n"
                f"--- Performance ---\n"
                f"Kills: {entry.get('performance', {}).get('kills', 'N/A')}\n"
                f"Morts: {entry.get('performance', {}).get('morts', 'N/A')}\n"
                f"Assists: {entry.get('performance', {}).get('assists', 'N/A')}\n"
                f"Bottes triomphantes: {'Oui' if entry.get('performance', {}).get('bottes_triompantes') else 'Non'}\n"
                f"--- Objectifs ---\n"
                f"Elder: {entry.get('objectives', {}).get('elder', 'N/A')}\n"
                f"Baron: {entry.get('objectives', {}).get('baron', 'N/A')}\n"
                f"Dragons: {entry.get('objectives', {}).get('dragons', 'N/A')}\n"
                f"Herald: {'Oui' if entry.get('objectives', {}).get('herald') else 'Non'}\n"
                f"Grubs: {'Oui' if entry.get('objectives', {}).get('grubs') else 'Non'}\n"
                f"Atakhan: {'Oui' if entry.get('objectives', {}).get('atakhan') else 'Non'}\n"
                f"Tours: {entry.get('objectives', {}).get('tour', 'N/A')}"
            )
            details_label.config(text=text)

        tree.bind("<<TreeviewSelect>>", show_details)

        # Ajouter le tri sur chaque colonne (clic en-tête)
        for col in columns:
            tree.heading(col, command=lambda c=col: treeview_sort_column(tree, c))

        update_table()


    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    pages_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Pages", menu=pages_menu)
    pages_menu.add_command(label="Calculateur", command=show_calculator_page)
    pages_menu.add_command(label="Historique", command=show_history_page)

    show_calculator_page()
    root.mainloop()