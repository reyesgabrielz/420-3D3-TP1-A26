# TP1 — Suiveur de portefeuille boursier

## Présentation

Ce projet refactorise une application de suivi de portefeuille boursier en appliquant le **patron Observateur**.

Les prix sont récupérés avec `yfinance` toutes les 30 secondes. Le portefeuille notifie ensuite les observateurs pour actualiser les affichages et enregistrer les données.

## Installation et lancement

Créer l’environnement virtuel :

```bash
python -m venv venv
```

L’activer selon votre système :

```powershell
# Windows — PowerShell
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source venv/bin/activate
```

Installer les dépendances et lancer l’application :

```bash
pip install -r requirements.txt
python main.py
```

## Fonctionnalités actuelles

- Affichage des prix et de leur variation depuis l’ouverture.
- Calcul et affichage de la valeur totale du portefeuille.
- Alertes visuelles selon les seuils définis pour chaque titre.
- Enregistrement des prix dans `portfolio.csv` à chaque rafraîchissement.

L’ajout, la modification et le retrait des titres restent à intégrer dans la version refactorisée.

## Organisation du projet

- `main.py` : crée les objets, abonne les observateurs et programme le rafraîchissement.
- `modeles/` : contient la classe abstraite `Sujet` et le sujet concret `Portefeuille`.
- `observateurs/` : contient la classe abstraite `Observateur` et les quatre observateurs concrets.
- `views/` : contient la fenêtre principale et les styles de l’interface.
- `docs/UML.png` : présente le diagramme de classes.
- `app.py` : conserve l’application originale avant le refactoring.

## Fonctionnement du patron Observateur

`Portefeuille` conserve les titres et les prix. Sa méthode `rafraichir_prix()` récupère les prix, puis appelle `notifier()`.

Chaque observateur abonné reçoit cet appel dans sa méthode `actualiser(sujet)` et récupère les données avec `get_donnees()`, qui retourne un dictionnaire.

Les quatre observateurs sont :

- **AfficherPrix** : affiche les prix et leurs variations.
- **AfficherPortfolio** : calcule et affiche la valeur totale et sa variation.
- **AfficherAlertes** : affiche les alertes selon les seuils.
- **JournalCSV** : observateur non visuel qui enregistre les prix dans un fichier CSV.