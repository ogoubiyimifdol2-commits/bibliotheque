"""Vue des livres et des exemplaires."""
from utils import ErreurMetier
from views import console


class LivreView:
    def __init__(self, livre_controller, exemplaire_controller):
        self.livres = livre_controller
        self.exemplaires = exemplaire_controller

    def afficher_livres(self, livres):
        lignes = []
        for l in livres:
            dispo, total = self.livres.disponibilite(l.id)
            lignes.append([l.id, l.titre, l.auteur, l.isbn or "-", l.categorie or "-",
                           l.annee or "-", f"{dispo}/{total}"])
        console.tableau(["ID", "Titre", "Auteur", "ISBN", "Catégorie", "Année", "Dispo"], lignes)

    def menu(self):
        actions = {"1": self.ajouter, "2": self.lister, "3": self.rechercher,
                   "4": self.modifier, "5": self.supprimer}
        while True:
            choix = console.menu("Livres", [
                ("1", "Ajouter un livre"), ("2", "Lister les livres"),
                ("3", "Rechercher (titre, auteur, ISBN, catégorie)"),
                ("4", "Modifier un livre"), ("5", "Supprimer un livre"), ("0", "Retour")])
            if choix == "0":
                return
            if choix in actions:
                try:
                    actions[choix]()
                except ErreurMetier as e:
                    console.erreur(str(e))
            else:
                console.erreur("Choix invalide.")

    def ajouter(self):
        livre = self.livres.ajouter(
            console.saisir("Titre", True), console.saisir("Auteur", True),
            console.saisir("ISBN (facultatif)"), console.saisir("Catégorie"),
            console.saisir("Année de publication"))
        console.info(f"Livre ajouté (ID {livre.id}). Pensez à ajouter ses exemplaires.")

    def lister(self):
        self.afficher_livres(self.livres.lister())

    def rechercher(self):
        self.afficher_livres(self.livres.rechercher(console.saisir("Mot recherché", True)))

    def modifier(self):
        livre_id = console.saisir_entier("ID du livre")
        actuel = self.livres.obtenir(livre_id) if livre_id is not None else None
        if actuel is None:
            raise ErreurMetier("Livre introuvable.")
        print("Laissez vide pour conserver la valeur actuelle.")
        self.livres.modifier(
            actuel.id,
            console.saisir(f"Titre [{actuel.titre}]") or actuel.titre,
            console.saisir(f"Auteur [{actuel.auteur}]") or actuel.auteur,
            console.saisir(f"ISBN [{actuel.isbn or ''}]") or (actuel.isbn or ""),
            console.saisir(f"Catégorie [{actuel.categorie}]") or actuel.categorie,
            console.saisir(f"Année [{actuel.annee or ''}]") or (actuel.annee or ""))
        console.info("Livre modifié.")

    def supprimer(self):
        livre_id = console.saisir_entier("ID du livre à supprimer")
        if livre_id is not None and console.confirmer("Confirmer la suppression du livre et de ses exemplaires ?"):
            self.livres.supprimer(livre_id)
            console.info("Livre supprimé.")


class ExemplaireView:
    def __init__(self, exemplaire_controller):
        self.exemplaires = exemplaire_controller

    def menu(self):
        actions = {"1": self.ajouter, "2": self.lister, "3": self.modifier, "4": self.supprimer}
        while True:
            choix = console.menu("Exemplaires", [
                ("1", "Ajouter un exemplaire"), ("2", "Lister les exemplaires d'un livre (ou tous)"),
                ("3", "Modifier un exemplaire (cote, état)"), ("4", "Supprimer un exemplaire"),
                ("0", "Retour")])
            if choix == "0":
                return
            if choix in actions:
                try:
                    actions[choix]()
                except ErreurMetier as e:
                    console.erreur(str(e))
            else:
                console.erreur("Choix invalide.")

    def ajouter(self):
        livre_id = console.saisir_entier("ID du livre")
        if livre_id is None:
            return
        ex = self.exemplaires.ajouter(
            livre_id, console.saisir("Code d'inventaire", True), console.saisir("Cote"),
            console.saisir("État (bon / abîmé / perdu) [bon]") or "bon")
        console.info(f"Exemplaire {ex.code_inventaire} ajouté.")

    def lister(self):
        texte = console.saisir("ID du livre (vide = tous)")
        livre_id = int(texte) if texte.isdigit() else None
        lignes = [[e.code_inventaire, e.livre_id, e.cote or "-", e.etat,
                   "oui" if e.disponible else "non (emprunté)"]
                  for e in self.exemplaires.lister(livre_id)]
        console.tableau(["Code", "ID livre", "Cote", "État", "Disponible"], lignes)

    def modifier(self):
        code = console.saisir("Code d'inventaire", True)
        print("Laissez vide pour conserver la valeur actuelle.")
        self.exemplaires.modifier(code, console.saisir("Nouveau code"),
                                  console.saisir("Nouvelle cote"),
                                  console.saisir("Nouvel état (bon / abîmé / perdu)"))
        console.info("Exemplaire modifié.")

    def supprimer(self):
        code = console.saisir("Code d'inventaire à supprimer", True)
        if console.confirmer("Confirmer la suppression ?"):
            self.exemplaires.supprimer(code)
            console.info("Exemplaire supprimé.")
