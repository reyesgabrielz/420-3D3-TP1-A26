import tkinter as tk
from .styles import POLICE, POLICE_TITRE


class FenetrePrincipale:
    def __init__(self):
            self.fenetre = tk.Tk()
            self.fenetre.title("Portfolio Tracker")
            self.fenetre.resizable(False, False)
            self.fenetre.option_add("*Font", POLICE)

            tk.Label(self.fenetre, text="Portfolio Tracker", font=POLICE_TITRE).pack(pady=10)