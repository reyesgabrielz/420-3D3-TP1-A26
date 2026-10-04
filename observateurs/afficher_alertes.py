import tkinter as tk
from .observateur import Observateur

class AfficherAlertes(Observateur):
    def __init__(self, fenetre):
        frame_alertes = tk.LabelFrame(fenetre, text="Alertes", padx=10, pady=10)
        frame_alertes.pack(fill=tk.X, padx=10, pady=5)
        self.label_alertes = tk.Label(
            frame_alertes, text="Aucune alerte", fg="gray", justify=tk.LEFT, wraplength=380
        )
        self.label_alertes.pack(anchor="w")
        
        self.label_maj = tk.Label(fenetre, text="", font=("Segoe UI", 9), fg="gray")
        self.label_maj.pack(pady=5)


    # MÉTHODE POUR METTRE A JOUR LES ALERTES (À FAIRE)
    def actualiser(self, sujet):
        pass