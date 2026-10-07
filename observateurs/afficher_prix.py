import tkinter as tk
from .observateur import Observateur

class AfficherPrix(Observateur):
    def __init__(self, fenetre, titres):
        self.labels_prix = {}
        self.frames_prix = {}

        self.frame_prix = tk.LabelFrame(fenetre, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)
        
        for ticker in titres:
            self._creer_ligne_prix(ticker)

    def _creer_ligne_prix(self, ticker):
        """Ajoute la ligne d'affichage de prix pour un ticker (appelé au
        démarrage pour chaque titre, et à nouveau quand un titre est ajouté)."""
        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=f"{ticker}:", width=8, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)
        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame


    # MÉTHODE POUR METTRE A JOUR LES PRIX
    def actualiser(self, sujet):
        # get_donnees() fournit les prix sous la forme ticker: (prix, ouverture).
        donnees = sujet.get_donnees()
        prix_actuels = donnees["prix_actuels"]
        titres = donnees["titres"]

        for ticker in list(self.labels_prix):
            if ticker not in titres:
                self.frames_prix.pop(ticker).destroy()
                del self.labels_prix[ticker]

        for ticker in titres:
            if ticker not in self.labels_prix:
                self._creer_ligne_prix(ticker)

        for ticker, (prix, ouverture) in prix_actuels.items():
            if ticker not in titres:
                continue
            if ouverture:
                variation = (prix - ouverture) / ouverture * 100
                symbole = "▲" if variation >= 0 else "▼"
                couleur = "green" if variation >= 0 else "red"
                texte = f"{prix:.2f} $  {symbole} {abs(variation):.2f}%"
            else:
                texte = f"{prix:.2f} $  (ouverture indisponible)"
                couleur = "gray"
            self.labels_prix[ticker].config(text=texte, fg=couleur)