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
    window_height = 50
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
    close_button.bind("<B1-Motion>", move_window)
