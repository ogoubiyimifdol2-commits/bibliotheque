"""Ajoute des données d'exemple à la base (10 livres, 19 exemplaires, 5 lecteurs).

À lancer MANUELLEMENT, une seule fois, sur une base vide :  python donnees_exemple.py
Ce script n'est jamais exécuté automatiquement par l'application.
"""
import sys

from controllers.exemplaire_controller import ExemplaireController
from controllers.lecteur_controller import LecteurController
from controllers.livre_controller import LivreController
from database.connexion import get_connection
from database.schema import creer_tables
from utils import ErreurMetier, aujourdhui, ajouter_jours

# (titre, auteur, ISBN ou "" , catégorie, année, nombre d'exemplaires)
LIVRES = [
    ("Le Petit Prince", "Antoine de Saint-Exupéry", "9782070612758", "Roman", 1943, 3),
    ("L'Étranger", "Albert Camus", "9782070360024", "Roman", 1942, 2),
    ("Une si longue lettre", "Mariama Bâ", "", "Roman", 1979, 2),
    ("Things Fall Apart", "Chinua Achebe", "9780385474542", "Roman", 1958, 2),
    ("1984", "George Orwell", "9780451524935", "Science-fiction", 1949, 2),
    ("Clean Code", "Robert C. Martin", "9780132350884", "Informatique", 2008, 2),
    ("The Pragmatic Programmer", "Andrew Hunt et David Thomas", "9780135957059", "Informatique", 2019, 1),
    ("Python Crash Course", "Eric Matthes", "9781593279288", "Informatique", 2019, 2),
    ("Sapiens", "Yuval Noah Harari", "9780062316097", "Histoire", 2011, 1),
    ("Les Damnés de la terre", "Frantz Fanon", "", "Essai", 1961, 2),
]

# (carte, nom, prénom, catégorie, inscrit il y a N jours)
LECTEURS = [
    ("L-0001", "Diallo", "Awa", "etudiant", 40),
    ("L-0002", "Mensah", "Koffi", "etudiant", 120),
    ("L-0003", "Ndiaye", "Fatou", "etudiant", 200),
    ("E-0001", "Traoré", "Moussa", "enseignant", 300),
    ("E-0002", "Sow", "Aminata", "enseignant", 60),
]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    connexion = get_connection()
    creer_tables(connexion)
    livres = LivreController(connexion)
    exemplaires = ExemplaireController(connexion)
    lecteurs = LecteurController(connexion)

    if livres.lister() or lecteurs.lister():
        print("La base contient déjà des données : aucune donnée d'exemple n'a été ajoutée.")
        print("Pour repartir de zéro, supprimez le fichier biblioiit.db puis relancez ce script.")
        return

    try:
        nb_exemplaires = 0
        for numero, (titre, auteur, isbn, categorie, annee, quantite) in enumerate(LIVRES, start=1):
            livre = livres.ajouter(titre, auteur, isbn, categorie, str(annee))
            for k in range(1, quantite + 1):
                exemplaires.ajouter(livre.id, f"INV-{numero:03d}-{k}",
                                    f"{categorie[:3].upper()}-{numero:03d}", "bon")
                nb_exemplaires += 1
        jour = aujourdhui().isoformat()
        for carte, nom, prenom, categorie, anciennete in LECTEURS:
            lecteurs.inscrire(carte, nom, prenom, categorie, ajouter_jours(jour, -anciennete))
    except ErreurMetier as e:
        print(f"Erreur : {e}")
        return
    print(f"Données ajoutées : {len(LIVRES)} livres, {nb_exemplaires} exemplaires, "
          f"{len(LECTEURS)} lecteurs.")


if __name__ == "__main__":
    main()
