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


    # MÉTHODE POUR METTRE A JOUR LA VALEUR DU PORTFOLIO (À FAIRE)
    def actualiser(self, sujet):
        pass
