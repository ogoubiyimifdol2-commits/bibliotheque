"""Vue des lecteurs."""
from utils import ErreurMetier, formater_date
from views import console


class LecteurView:
    def __init__(self, lecteur_controller):
        self.lecteurs = lecteur_controller

    def afficher(self, lecteurs):
        lignes = [[l.numero_carte, l.nom, l.prenom, l.categorie,
                   formater_date(l.date_inscription), self.lecteurs.statut(l)] for l in lecteurs]
        console.tableau(["Carte", "Nom", "Prénom", "Catégorie", "Inscrit le", "Statut"], lignes)

    def menu(self):
        actions = {"1": self.inscrire, "2": self.lister, "3": self.rechercher,
                   "4": self.suspendre, "5": self.lever, "6": self.supprimer}
        while True:
            choix = console.menu("Lecteurs", [
                ("1", "Inscrire un lecteur"), ("2", "Lister les lecteurs"),
                ("3", "Rechercher un lecteur"), ("4", "Suspendre un lecteur"),
                ("5", "Lever une suspension"), ("6", "Supprimer un lecteur"), ("0", "Retour")])
            if choix == "0":
                return
            if choix in actions:
                try:
                    actions[choix]()
                except ErreurMetier as e:
                    console.erreur(str(e))
            else:
                console.erreur("Choix invalide.")

    def inscrire(self):
        lecteur = self.lecteurs.inscrire(
            console.saisir("Numéro de carte", True), console.saisir("Nom", True),
            console.saisir("Prénom", True),
            console.saisir("Catégorie (etudiant / enseignant)", True),
            console.saisir("Date d'inscription JJ/MM/AAAA (vide = aujourd'hui)"))
        console.info(f"Lecteur inscrit : {lecteur.prenom} {lecteur.nom}.")

    def lister(self):
        self.afficher(self.lecteurs.lister())

    def rechercher(self):
        self.afficher(self.lecteurs.rechercher(console.saisir("Nom, prénom ou carte", True)))

    def suspendre(self):
        self.lecteurs.suspendre(console.saisir("Numéro de carte", True))
        console.info("Lecteur suspendu.")

    def lever(self):
        self.lecteurs.lever_suspension(console.saisir("Numéro de carte", True))
        console.info("Suspension levée.")

    def supprimer(self):
        carte = console.saisir("Numéro de carte à supprimer", True)
        if console.confirmer("Confirmer la suppression ?"):
            self.lecteurs.supprimer(carte)
            console.info("Lecteur supprimé.")
