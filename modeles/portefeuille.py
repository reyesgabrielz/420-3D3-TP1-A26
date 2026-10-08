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

    