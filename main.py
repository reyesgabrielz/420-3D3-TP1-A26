from views.fenetre_principale import FenetrePrincipale
from observateurs.afficher_prix import AfficherPrix
from observateurs.afficher_portfolio import AfficherPortfolio
from observateurs.afficher_alertes import AfficherAlertes
from observateurs.afficher_titres import AfficherTitres
from observateurs.journal_csv import JournalCSV
from modeles.portefeuille import Portefeuille

TITRES = {
    "AAPL": {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
    "GOOGL": {"quantite": 5, "seuil_haut": 160.0, "seuil_bas": 120.0},
    "MSFT": {"quantite": 8, "seuil_haut": 430.0, "seuil_bas": 380.0},
}

INTERVALLE_MS = 30000  # Fréquence de rafraîchissement des prix (30 secondes)

if __name__ == "__main__":
    portefeuille = Portefeuille(TITRES)
    app = FenetrePrincipale()
    affichage_prix = AfficherPrix(app.fenetre, TITRES)
    affichage_titres = AfficherTitres(app.fenetre, portefeuille)
    affichage_portfolio = AfficherPortfolio(app.fenetre)
    affichage_alertes = AfficherAlertes(app.fenetre)
    journal_csv = JournalCSV("portfolio.csv")

    portefeuille.abonner(affichage_prix)
    portefeuille.abonner(affichage_titres)
    portefeuille.abonner(affichage_portfolio)
    portefeuille.abonner(affichage_alertes)
    portefeuille.abonner(journal_csv)

    def rafraichir():
        try:
            portefeuille.rafraichir_prix()  # Ici
        except Exception as erreur:
            print(f"Erreur de rafraîchissement : {erreur}")
        finally:
            app.fenetre.after(INTERVALLE_MS, rafraichir)

    app.fenetre.after(0, rafraichir)
    app.fenetre.mainloop()

    app.fenetre.mainloop()