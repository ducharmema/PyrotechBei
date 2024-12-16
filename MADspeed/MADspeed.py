import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta
import pyperclip
import keyboard
import re
import pyautogui
import os

#**************************************************************************************************
# Déclaration des variables globales
#**************************************************************************************************
folder_number_global = None
folder_number_flag_global = True
first_pass = False
current_dossier = 0
floating_window = None

#**************************************************************************************************
# Définition des fonctions
#**************************************************************************************************
def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Information", f"'{text}' a été copié dans le presse-papier.")

def log_info(info, dossier_number):
    log_file_path = f"{dossier_number}.log"
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {info}\n")
    if os.path.exists(log_file_path):
        print(f"Log file '{log_file_path}' created successfully.")

def get_existing_info(dossier_number):
    info = {"date_sinistre": None, "adresse_sinistre": None, "dossier_client": None, "dossier_number": dossier_number}
    log_file_path = f"{dossier_number}.log"
    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                date_match = re.search(r"Date du sinistre: ([\d-]+)", line)
                adresse_match = re.search(r"Adresse du sinistre: (.+?) -", line)
                client_match = re.search(r"Numéro de dossier client: (\d+)", line)
                if date_match:
                    info["date_sinistre"] = date_match.group(1)
                if adresse_match:
                    info["adresse_sinistre"] = adresse_match.group(1)
                if client_match:
                    info["dossier_client"] = client_match.group(1)
    except FileNotFoundError:
        pass
    return info
    
def get_general_info():
    global folder_number_global
    log_file_path = "general.log"
    try:
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                dossier_match = re.search(r"Numéro du dossier: (\d+)", line)
                if dossier_match:
                    folder_number_global = dossier_match.group(1)
                else:
                    folder_number_global = "00000000"
    except FileNotFoundError:
        with open(log_file_path, 'w') as log_file:
            log_file.write("Dossier: 00000000")
        folder_number_global = "00000000"
    return folder_number_global

def create_floating_window(folder_number):
    global floating_window
    if floating_window:
        floating_window.destroy()

    # Créer une nouvelle fenêtre flottante
    floating_window = tk.Toplevel(root)
    floating_window.title("MADspeedV1")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 300
    window_height = 15
    x_position = (screen_width - window_width) // 2
    y_position = screen_height - window_height - 50  # Ajuster cette valeur si nécessaire pour être juste au-dessus de la barre des tâches
    floating_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    floating_window.overrideredirect(True)  # Supprime les bordures de la fenêtre
    floating_window.attributes("-topmost", True)  # Toujours au premier plan

    # Ajouter une étiquette pour afficher le titre et le numéro de dossier
    label = tk.Label(floating_window, text=f"MADspeedV1 - Dossier: {folder_number}", bg="lightgrey")
    label.pack(expand=True, fill='both')

    # Ajouter un bouton "X" pour fermer la fenêtre
    close_button = tk.Button(floating_window, text="X", command=floating_window.destroy, bg="red", fg="white")
    close_button.place(relx=1, x=-20, y=0, anchor='ne')

    # Permettre de déplacer la fenêtre
    def move_window(event):
        floating_window.geometry(f"+{event.x_root}+{event.y_root}")
    
    label.bind("<B1-Motion>", move_window)

def select_date(folder_number):
    def on_select():
        selected_date = cal.selection_get().strftime('%d-%m-%Y')
        text_to_copy = f"{folder_number}-{selected_date}-MAD"
        copy_to_clipboard(text_to_copy)
        log_info(f"Numéro du dossier: {folder_number} - Date sélectionnée: {selected_date}", folder_number)
        cal_window.destroy()

    cal_window = tk.Toplevel(root)
    cal_window.title("Sélectionner une date")
    cal = Calendar(cal_window, selectmode='day')
    cal.pack(pady=20)
    tk.Button(cal_window, text="Sélectionner", command=on_select).pack(pady=10)

def show_options(folder_number):
    global folder_number_global
    folder_number_global = folder_number  # Mettre à jour la variable globale
    options_window = tk.Toplevel(root)
    options_window.title("Sélectionner une option")

    def option1():
        today = datetime.now().strftime('%d-%m-%Y')
        text_to_copy = f"{folder_number}-{today}-MAD"
        copy_to_clipboard(text_to_copy)
        log_info(f"Numéro du dossier: {folder_number} - Date sélectionnée: {today}", folder_number)
        options_window.destroy()

    def option2():
        yesterday = (datetime.now() - timedelta(1)).strftime('%d-%m-%Y')
        text_to_copy = f"{folder_number}-{yesterday}-MAD"
        copy_to_clipboard(text_to_copy)
        log_info(f"Numéro du dossier: {folder_number} - Date sélectionnée: {yesterday}", folder_number)
        options_window.destroy()

    def option3():
        select_date(folder_number)
        options_window.destroy()

    tk.Button(options_window, text="1) Sélectionne la DATE du jour", command=option1).pack(pady=10)
    tk.Button(options_window, text="2) Sélectionne la date d'hier", command=option2).pack(pady=10)
    tk.Button(options_window, text="3) Sélectionne une date dans le calendrier", command=option3).pack(pady=10)

def request_folder_number():
    global folder_number_global
    folder_number_global = simpledialog.askstring("Entrer le numéro du dossier", "Numéro du dossier:", parent=root)
		
def rename_file():
    show_options(folder_number_global)  
		
def toggle_floating_window():
    global folder_number_flag_global, floating_window
    folder_number_flag_global = not folder_number_flag_global
	
    if folder_number_flag_global:
        create_floating_window(folder_number_global)  # Créer la fenêtre flottante
    else:
        if floating_window:
            floating_window.destroy()  # tue la fenêtre generale flottante
		
def request_sinistre_info():
    dossier_number = folder_number_global
    info = get_existing_info(dossier_number)

    if all(info.values()):
        # Si toutes les informations sont trouvées dans le fichier log, les utiliser directement
        text_to_copy = f"Incendie au {info['adresse_sinistre']} du {info['date_sinistre']} -V.D.: {info['dossier_client']} - N.D.: {info['dossier_number']}"
        copy_to_clipboard(text_to_copy)
        pyautogui.typewrite(text_to_copy)
    else:
        # Sinon, demander les informations manquantes à l'utilisateur
        date_sinistre = info["date_sinistre"] if info["date_sinistre"] else simpledialog.askstring("Date du sinistre", "Entrer la date du sinistre (JJ-MM-YYYY):", parent=root)
        adresse_sinistre = info["adresse_sinistre"] if info["adresse_sinistre"] else simpledialog.askstring("Adresse du sinistre", "Entrer l'adresse du sinistre:", parent=root)
        dossier_client = info["dossier_client"] if info["dossier_client"] else simpledialog.askstring("Numéro de dossier client", "Entrer le numéro de dossier client:", parent=root)

        if date_sinistre and adresse_sinistre and dossier_client and dossier_number:
            log_info(f"Date du sinistre: {date_sinistre} - Adresse du sinistre: {adresse_sinistre} - Numéro de dossier client: {dossier_client} - Numéro du dossier: {dossier_number}", dossier_number)
            text_to_copy = f"Incendie au {adresse_sinistre} du {date_sinistre} -V.D.: {dossier_client} - N.D.: {dossier_number}"
            copy_to_clipboard(text_to_copy)
            pyautogui.typewrite(text_to_copy)

def on_alt_h():
    root.after(0, toggle_floating_window)
	
def on_alt_r():
    root.after(0, rename_file)

def on_alt_s():
    root.after(0, request_sinistre_info)
def on_alt_a():
    root.after(0, request_folder_number)	

#**************************************************************************************************
# Début du main
#**************************************************************************************************

try:
    # Initialiser Tkinter avant toute autre chose
    root = tk.Tk()
    root.withdraw()    
    
    # Vérifier et créer general.log si nécessaire
    general_log_path = "general.log" 
    if not os.path.exists(general_log_path):
        with open(general_log_path, 'w') as log_file:
            log_file.write("Dossier: 00000000")
            
    if not first_pass:
        first_pass = True
        folder_number_global = get_general_info()  # Initialiser folder_number_global avec get_general_info()
        if folder_number_global:
            create_floating_window(folder_number_global)  # Créer la fenêtre flottante

    
    keyboard.add_hotkey('alt+h', on_alt_h)
    keyboard.add_hotkey('alt+r', on_alt_r)
    keyboard.add_hotkey('alt+s', on_alt_s)
    keyboard.add_hotkey('alt+a', on_alt_a)

    # Mémorisation du dossier courant
    if folder_number_global != current_dossier:
        current_dossier = folder_number_global
        log_info(current_dossier, "general")
        
    root.mainloop()
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
    input("Appuyez sur Entrée pour fermer...")

#**************************************************************************************************
# Fin du main
#**************************************************************************************************