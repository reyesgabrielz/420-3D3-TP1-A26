from .sujet import Sujet
import yfinance as yf

class Portefeuille(Sujet):
    def __init__(self, titres):
        super().__init__()
        self._titres = {
            ticker: infos.copy()
            for ticker, infos in titres.items()
        }
        self.prix_actuels = {}

    def ajouter_titre(self, ticker, infos):
        ticker = ticker.strip().upper()

        if not ticker:
            raise ValueError("Le ticker ne peut pas etre vide.")

        if ticker in self._titres:
            raise ValueError(f"{ticker} est deja dans le portefeuille.")

        self._titres[ticker] = infos.copy()
        self.prix_actuels.pop(ticker, None)
        self.notifier()

    def retirer_titre(self, ticker):
        if ticker not in self._titres:
            raise ValueError(f"{ticker} n'est pas dans le portefeuille.")

        del self._titres[ticker]
        self.prix_actuels.pop(ticker, None)
        self.notifier()

    def modifier_titre(self, ticker, changements):
        if ticker not in self._titres:
            raise ValueError(f"{ticker} n'est pas dans le portefeuille.")

        self._titres[ticker].update(changements)
        self.notifier()

    def rafraichir_prix(self):
        nouveaux_prix = {}

        for ticker in self._titres:
            info = yf.Ticker(ticker).fast_info
            prix = info["last_price"]
            ouverture = info["open"]

            if prix is None:
                raise ValueError(f"Impossible de récupérer le prix pour {ticker}")

            nouveaux_prix[ticker] = (prix, ouverture)
        

        self.prix_actuels = nouveaux_prix
        self.notifier()


    def get_donnees(self):
        return {
            "titres": self._titres,
            "prix_actuels": self.prix_actuels
        }

    