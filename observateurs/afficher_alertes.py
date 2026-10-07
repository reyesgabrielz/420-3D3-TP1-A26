from datetime import datetime
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


    # MÉTHODE POUR METTRE A JOUR LES ALERTES
    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]
        alertes = []
        for ticker, (prix, _) in donnees["prix_actuels"].items():
            if ticker not in titres:
                continue
            seuil_haut = titres[ticker]["seuil_haut"]
            seuil_bas = titres[ticker]["seuil_bas"]
            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut ({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )
            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas ({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        self.label_alertes.config(
            text="\n".join(alertes) if alertes else "Aucune alerte",
            fg="red" if alertes else "gray",
        )
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_maj.config(text=f"Dernière mise à jour : {horodatage}", fg="gray")