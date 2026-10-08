import tkinter as tk
from .observateur import Observateur
import yfinance as yf

class AfficherTitres(Observateur):
    def __init__(self, fenetre, titres):
        self.titres = titres

        self.frame_titres = tk.LabelFrame(fenetre, text="Gérer les titres", padx=10, pady=10)
        self.frame_titres.pack(fill=tk.X, padx=10, pady=5)

        ligne_ajout = tk.Frame(self.frame_titres)
        ligne_ajout.pack(fill=tk.X)
        self.entry_ticker = self._champ(ligne_ajout, "Ticker", width=8)
        self.entry_quantite = self._champ(ligne_ajout, "Qté", width=5, valeur_defaut="1")
        self.entry_seuil_bas_ajout = self._champ(ligne_ajout, "Alerte basse", width=7)
        self.entry_seuil_haut_ajout = self._champ(ligne_ajout, "Alerte haute", width=7)
        tk.Button(ligne_ajout, text="Ajouter", command=self.ajouter_titre).pack(side=tk.LEFT)

        tk.Label(
            self.frame_titres,
            text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
            font=("Segoe UI", 8), fg="gray"
        ).pack(anchor="w", pady=(2,5))

        ligne_liste = tk.Frame(self.frame_titres)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(ligne_liste, text="Retirer", command=self.retirer_titre).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        ligne_modif = tk.Frame(self.frame_titres)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouvelle_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouvelle_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)
        tk.Button(ligne_modif, text="Modifier sélection", command=self.modifier_selection).pack(side=tk.LEFT)

        self.label_statut_titres = tk.Label(self.frame_titres, text="", font=("Segoe UI", 9), fg="gray")
        self.label_statut_titres.pack(anchor="w", pady=(5, 0))

        self._synchroniser_liste()

    def actualiser(self, sujet):
        """Synchronise la liste avec les titres courants du sujet."""
        donnees = sujet.get_donnees()
        self.titres = donnees["titres"]
        self._synchroniser_liste()

    def _champ(self, parent, texte, width, valeur_defaut=""):
        """Ajoute un couple Label + Entry à `parent` et retourne l'Entry."""
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    def _texte_listbox(self, ticker):
        """Construit la ligne texte affichée dans la liste pour un ticker."""
        infos = self.titres[ticker]
        return (
            f"{ticker} - {infos['quantite']} action(s) "
            f"(alerte: {infos['seuil_bas']:.2f} $ / {infos['seuil_haut']:.2f} $)"
        )

    def _ticker_selectionne(self):
        """Retourne (index, ticker) du titre sélectionné dans la liste, ou None.
        Le ticker est extrait du texte affiché (avant le tiret "-")."""
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        index = selection[0]
        texte = self.listbox_titres.get(index)
        ticker = texte.split(" - ", 1)[0]
        return index, ticker

    def _synchroniser_liste(self, ticker_selectionne=None):
        self.listbox_titres.delete(0, tk.END)
        for index, ticker in enumerate(self.titres):
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
            if ticker == ticker_selectionne:
                self.listbox_titres.selection_set(index)

    def _statut(self, texte, couleur):
        """Affiche un message de statut (succès/erreur/info) sous le formulaire de gestion."""
        self.label_statut_titres.config(text=texte, fg=couleur)

    @staticmethod
    def _entier_positif(texte):
        """Convertit `texte` en entier strictement positif, ou lève ValueError."""
        valeur = int(texte)
        if valeur <= 0:
            raise ValueError
        return valeur

    @staticmethod
    def _flottant_positif(texte):
        """Convertit `texte` en nombre décimal strictement positif, ou lève ValueError."""
        valeur = float(texte)
        if valeur <= 0:
            raise ValueError
        return valeur

    @staticmethod
    def _recuperer_prix(ticker):
        """Retourne (prix, ouverture) pour un ticker, ou lève une erreur s'il est introuvable."""
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")
        return prix, info["open"]

    def ajouter_titre(self):
        """Valide le formulaire d'ajout, vérifie que le ticker existe via yfinance,
        puis l'insère dans TITRES et dans l'UI (ligne de prix + liste)."""
        ticker = self.entry_ticker.get().strip().upper()
        if not ticker:
            return
        if ticker in self.titres:
            self._statut(f"{ticker} est déjà dans le portfolio.", "orange")
            return

        try:
            quantite = self._entier_positif(self.entry_quantite.get().strip())
        except ValueError:
            self._statut("La quantité doit être un nombre entier positif.", "red")
            return

        texte_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_haut = self.entry_seuil_haut_ajout.get().strip()
        try:
            seuil_bas = self._flottant_positif(texte_bas) if texte_bas else None
            seuil_haut = self._flottant_positif(texte_haut) if texte_haut else None
        except ValueError:
            self._statut("Les alertes doivent être des nombres positifs.", "red")
            return

        try:
            prix, ouverture = self._recuperer_prix(ticker)
        except (KeyError, TypeError, ValueError) as erreur:
            self._statut(str(erreur), "red")
            return
        except Exception as erreur:
            self._statut(f"Impossible de récupérer le prix de {ticker} : {erreur}", "red")
            return

        seuil_bas = round(seuil_bas if seuil_bas is not None else prix * 0.8, 2)
        seuil_haut = round(seuil_haut if seuil_haut is not None else prix * 1.2, 2)
        if seuil_bas >= seuil_haut:
            self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
            return

        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_bas": seuil_bas,
            "seuil_haut": seuil_haut
        }
        self._synchroniser_liste(ticker)

        for entry, valeur in (
            (self.entry_ticker, ""),
            (self.entry_quantite, "1"),
            (self.entry_seuil_bas_ajout, ""),
            (self.entry_seuil_haut_ajout, ""),
        ):
            entry.delete(0, tk.END)
            if valeur:
                entry.insert(0, valeur)
        
        self._statut(f"{ticker} ajouté au portfolio ({quantite} action(s)).", "green")

    def retirer_titre(self):
        """Retire le titre sélectionné dans la liste : du portefeuille (TITRES),
        de la liste, et détruit sa ligne de prix."""
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return
        index, ticker = selectionne

        self.listbox_titres.delete(index)
        del self.titres[ticker]
        self._synchroniser_liste()
        self._statut(f"{ticker} retiré du portfolio.", "gray")

    def modifier_selection(self):
        """Met à jour la quantité et/ou les seuils d'alerte du titre sélectionné.
        Chaque champ est optionnel : seuls ceux remplis sont modifiés, mais les
        deux seuils doivent être fournis ensemble pour rester cohérents."""
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à modifier.", "orange")
            return
        index, ticker = selectionne

        texte_quantite = self.entry_nouvelle_quantite.get().strip()
        texte_bas = self.entry_nouvelle_seuil_bas.get().strip()
        texte_haut = self.entry_nouvelle_seuil_haut.get().strip()
        if not texte_quantite and not texte_bas and not texte_haut:
            self._statut("Entrez une nouvelle quantité et/ou de nouvelles alertes.", "orange")
            return

        try:
            quantite = self._entier_positif(texte_quantite) if texte_quantite else None
            if texte_bas or texte_haut:
                if not (texte_bas and texte_haut):
                    self._statut("Les deux alertes doivent être fournies ensemble.", "red")
                    return
                seuil_bas = round(self._flottant_positif(texte_bas), 2)
                seuil_haut = round(self._flottant_positif(texte_haut), 2)
                if seuil_bas >= seuil_haut:
                    self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
                    return
            else:
                seuil_bas = seuil_haut = None
        except ValueError:
            self._statut("La quantité et les alertes doivent être des nombres positifs.", "red")
            return

        changements = []
        if quantite is not None:
            self.titres[ticker]["quantite"] = quantite
            changements.append(f"{quantite} action(s)")
        if seuil_bas is not None and seuil_haut is not None:
            self.titres[ticker]["seuil_bas"] = round(seuil_bas, 2)
            self.titres[ticker]["seuil_haut"] = round(seuil_haut, 2)
            changements.append(f"alertes {seuil_bas:.2f} $ / {seuil_haut:.2f} $")

        self._synchroniser_liste(ticker)
        for entry in (
            self.entry_nouvelle_quantite,
            self.entry_nouvelle_seuil_bas,
            self.entry_nouvelle_seuil_haut,
        ):
            entry.delete(0, tk.END)
        self._statut(f"{ticker} mis à jour : {', '.join(changements)}.", "green")