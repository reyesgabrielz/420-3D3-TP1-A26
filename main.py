from views.fenetre_principale import FenetrePrincipale
from observateurs.afficher_prix import AfficherPrix
from observateurs.afficher_portfolio import AfficherPortfolio
from observateurs.afficher_alertes import AfficherAlertes
from observateurs.journal_csv import JournalCSV

TITRES = {
    "AAPL": {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
    "GOOGL": {"quantite": 5, "seuil_haut": 160.0, "seuil_bas": 120.0},
    "MSFT": {"quantite": 8, "seuil_haut": 430.0, "seuil_bas": 380.0},
}

INTERVALLE_MS = 30000  # Fréquence de rafraîchissement des prix (30 secondes)

if __name__ == "__main__":
    app = FenetrePrincipale()
    affichage_prix = AfficherPrix(app.fenetre, TITRES)
    affichage_portfolio = AfficherPortfolio(app.fenetre)
    affichage_alertes = AfficherAlertes(app.fenetre)
    journal_csv = JournalCSV("portfolio.csv")
    app.fenetre.mainloop()