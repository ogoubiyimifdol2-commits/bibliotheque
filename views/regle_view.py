"""Vue du menu « Règles de prêt » et des statistiques."""
from utils import ErreurMetier
from views import console


class RegleView:
    def __init__(self, regle_controller):
        self.regles = regle_controller

    def afficher(self):
        console.tableau(
            ["Catégorie", "Livres max", "Durée (jours)", "Renouvellements", "Validité inscription (jours)"],
            [[r.categorie, r.max_livres, r.duree_jours, r.max_renouvellements, r.validite_jours]
             for r in self.regles.lister()])

    def menu(self):
        while True:
            choix = console.menu("Règles de prêt", [
                ("1", "Afficher les règles"), ("2", "Modifier les règles d'une catégorie"),
                ("0", "Retour")])
            if choix == "0":
                return
            try:
                if choix == "1":
                    self.afficher()
                elif choix == "2":
                    self.modifier()
                else:
                    console.erreur("Choix invalide.")
            except ErreurMetier as e:
                console.erreur(str(e))

    def modifier(self):
        self.afficher()
        categorie = console.saisir("Catégorie (etudiant / enseignant)", True)
        self.regles.modifier(
            categorie, console.saisir("Nombre maximum de livres", True),
            console.saisir("Durée de prêt en jours", True),
            console.saisir("Nombre maximum de renouvellements", True),
            console.saisir("Validité de l'inscription en jours (365 = 1 an)", True))
        console.info("Règles mises à jour.")


class StatistiqueView:
    def __init__(self, statistique_controller):
        self.statistiques = statistique_controller

    def menu(self):
        console.titre("Livres les plus empruntés")
        console.tableau(["Titre", "Auteur", "Nombre de prêts"],
                        [[l["titre"], l["auteur"], l["nb_prets"]]
                         for l in self.statistiques.livres_les_plus_empruntes(10)])
