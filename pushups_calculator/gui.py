# gui.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pushups_calculator.calcul import calculate_pushups
from pushups_calculator.io import save_to_history, load_config, read_history
import os

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

                result = f"{pseudo} doit faire {final_total}({total}) pompes"
                lbl = tk.Label(result_frame, text=result)
                lbl.pack()
                result_labels.append(lbl)

                save_to_history({
                    "pseudo": pseudo,
                    "performance": performance,
                    "objectives": objectifs,
                    "note_opgg": note,
                    "pompes": total,
                })

        tk.Button(root, text="Calculer", command=calculer).pack(pady=10)

    def show_history_page():
        clear_frame()

        history = []
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)

        pseudo_filter = tk.Entry(filter_frame)
        date_filter = tk.Entry(filter_frame)

        tk.Label(filter_frame, text="Filtrer par pseudo:").grid(row=0, column=0)
        pseudo_filter.grid(row=0, column=1)

        tk.Label(filter_frame, text="Filtrer par date (YYYY-MM-DD):").grid(row=0, column=2)
        date_filter.grid(row=0, column=3)

        listbox = tk.Listbox(root, width=100)
        listbox.pack(pady=10)

        details_label = tk.Label(root, text="", justify="left", anchor="w")
        details_label.pack(pady=5)

        def update_list():
            history.clear()
            history.extend(read_history())
            listbox.delete(0, tk.END)
            for entry in history:
                if pseudo_filter.get() and pseudo_filter.get().lower() not in entry['pseudo'].lower():
                    continue
                if date_filter.get() and date_filter.get() != entry.get('date'):
                    continue
                listbox.insert(tk.END, f"{entry['date']} - {entry['pseudo']} : {entry['pompes']} pompes")


        def show_details(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                filtered = [
                    entry for entry in history
                    if (not pseudo_filter.get() or pseudo_filter.get().lower() in entry['pseudo'].lower()) and
                    (not date_filter.get() or date_filter.get() == entry.get('date'))
                ]
                entry = filtered[index]
                text = (
                    f"Pseudo: {entry['pseudo']}\n"
                    f"Date: {entry['date']}\n"
                    f"Pompes: {entry['pompes']}\n"
                    f"Note OP.GG: {entry['note_opgg']}\n"
                    f"--- Performance ---\n"
                    f"Kills: {entry['performance']['kills']}\n"
                    f"Morts: {entry['performance']['morts']}\n"
                    f"Assists: {entry['performance']['assists']}\n"
                    f"Bottes triomphantes: {'Oui' if entry['performance']['bottes_triompantes'] else 'Non'}\n"
                    f"--- Objectifs ---\n"
                    f"Elder: {entry['objectives']['elder']}\n"
                    f"Baron: {entry['objectives']['baron']}\n"
                    f"Dragons: {entry['objectives']['dragons']}\n"
                    f"Herald: {'Oui' if entry['objectives']['herald'] else 'Non'}\n"
                    f"Grubs: {'Oui' if entry['objectives']['grubs'] else 'Non'}\n"
                    f"Atakhan: {'Oui' if entry['objectives']['atakhan'] else 'Non'}\n"
                    f"Tours: {entry['objectives']['tour']}"
                )
                details_label.config(text=text)

        listbox.bind("<<ListboxSelect>>", show_details)

        tk.Button(filter_frame, text="Filtrer", command=update_list).grid(row=0, column=4)
        update_list()


    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    pages_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Pages", menu=pages_menu)
    pages_menu.add_command(label="Calculateur", command=show_calculator_page)
    pages_menu.add_command(label="Historique", command=show_history_page)

    show_calculator_page()
    root.mainloop()