from .observateur import Observateur
from datetime import datetime

class JournalCSV(Observateur):
    def __init__(self, nom_fichier):
        self.nom_fichier = nom_fichier


    # MÉTHODE POUR ENREGISTRER LES DONNÉES DANS LE FICHIER CSV (À FAIRE)
    def actualiser(self, sujet):
        pass