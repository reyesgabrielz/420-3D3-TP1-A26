import tkinter as tk
from views.styles import POLICE, POLICE_VALEUR
from .observateur import Observateur

class AfficherPortfolio(Observateur):
    def __init__(self, fenetre):
        frame_portfolio = tk.LabelFrame(fenetre, text="Mon portfolio", padx=10, pady=10)
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)
        self.label_valeur = tk.Label(frame_portfolio, text="Valeur totale : calcul en cours...", font=POLICE_VALEUR)
        self.label_valeur.pack()
        self.label_variation = tk.Label(frame_portfolio, text="", font=POLICE)
        self.label_variation.pack()


    # MÉTHODE POUR METTRE A JOUR LA VALEUR DU PORTFOLIO
    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]
        titres = donnees["titres"]

        valeur_totale = sum(
            prix * titres[ticker]["quantite"]
            for ticker, (prix, _) in prix_actuels.items() if ticker in titres
        )
        self.label_valeur.config(text=f"Valeur totale : {valeur_totale:.2f} $")

        if any(ouverture is None or ouverture == 0
               for ticker, (_, ouverture) in prix_actuels.items() if ticker in titres):
            self.label_variation.config(text="Variation indisponible", fg="gray")
            return

        valeur_ouverture = sum(
            ouverture * titres[ticker]["quantite"]
            for ticker, (_, ouverture) in prix_actuels.items() if ticker in titres
        )
        variation = valeur_totale - valeur_ouverture
        symbole = "▲" if variation >= 0 else "▼"
        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg="green" if variation >= 0 else "red",
        )
