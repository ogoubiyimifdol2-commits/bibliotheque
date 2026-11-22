"""Vue des prêts, retours et renouvellements."""
from utils import ErreurMetier, formater_date
from views import console


class PretView:
    def __init__(self, pret_controller):
        self.prets = pret_controller

    def afficher(self, prets):
        lignes = [[p["id"], p["code_inventaire"], p["titre"], f'{p["prenom"]} {p["nom"]}',
                   p["numero_carte"], formater_date(p["date_pret"]),
                   formater_date(p["date_echeance"]), p["nb_renouvellements"]] for p in prets]
        console.tableau(["N°", "Exemplaire", "Titre", "Lecteur", "Carte", "Prêté le",
                         "Échéance", "Renouv."], lignes)

    def menu(self):
        actions = {"1": self.emprunter, "2": self.retourner, "3": self.renouveler,
                   "4": self.en_cours, "5": self.en_retard}
        while True:
            choix = console.menu("Prêts et retours", [
                ("1", "Emprunter"), ("2", "Retourner"), ("3", "Renouveler"),
                ("4", "Prêts en cours"), ("5", "Prêts en retard"), ("0", "Retour")])
            if choix == "0":
                return
            if choix in actions:
                try:
                    actions[choix]()
                except ErreurMetier as e:
                    console.erreur(str(e))
            else:
                console.erreur("Choix invalide.")

    def emprunter(self):
        r = self.prets.emprunter(console.saisir("Numéro de carte du lecteur", True),
                                 console.saisir("Code d'inventaire de l'exemplaire", True))
        console.info(f"Prêt enregistré : « {r['titre']} », à rendre avant le "
                     f"{formater_date(r['echeance'])}.")

    def retourner(self):
        r = self.prets.retourner(console.saisir("Code d'inventaire de l'exemplaire", True))
        console.info("Retour enregistré.")
        if r["retard_jours"] > 0:
            console.erreur(f"Retard de {r['retard_jours']} jour(s) : le lecteur est suspendu jusqu'au "
                           f"{formater_date(r['suspension_fin'])}.")
        if r["prochain_reservataire"]:
            console.info(f"À prévenir (réservation en attente) : {r['prochain_reservataire']}.")

    def renouveler(self):
        r = self.prets.renouveler(console.saisir("Code d'inventaire de l'exemplaire", True))
        console.info(f"Prêt renouvelé jusqu'au {formater_date(r['nouvelle_echeance'])}.")

    def en_cours(self):
        self.afficher(self.prets.lister_en_cours())

    def en_retard(self):
        self.afficher(self.prets.lister_en_retard())
