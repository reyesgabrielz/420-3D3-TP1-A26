import csv
from .observateur import Observateur
from datetime import datetime

class JournalCSV(Observateur):
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier


    # MÉTHODE POUR ENREGISTRER LES DONNÉES DANS LE FICHIER CSV
    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.nom_fichier, "a", encoding="utf-8", newline="") as fichier:
            writer = csv.writer(fichier)
            for ticker, (prix, ouverture) in donnees["prix_actuels"].items():
                if ticker not in donnees["titres"]:
                    continue
                writer.writerow([
                    horodatage, ticker, f"{prix:.2f}",
                    f"{ouverture:.2f}" if ouverture is not None else "",
                ])