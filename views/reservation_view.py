"""Vue des réservations."""
from utils import ErreurMetier, formater_date
from views import console


class ReservationView:
    def __init__(self, reservation_controller):
        self.reservations = reservation_controller

    def menu(self):
        actions = {"1": self.reserver, "2": self.annuler, "3": self.file, "4": self.toutes}
        while True:
            choix = console.menu("Réservations", [
                ("1", "Réserver un livre"), ("2", "Annuler une réservation"),
                ("3", "Voir la file d'attente d'un livre"),
                ("4", "Toutes les réservations en attente"), ("0", "Retour")])
            if choix == "0":
                return
            if choix in actions:
                try:
                    actions[choix]()
                except ErreurMetier as e:
                    console.erreur(str(e))
            else:
                console.erreur("Choix invalide.")

    def reserver(self):
        livre_id = console.saisir_entier("ID du livre")
        if livre_id is None:
            return
        r = self.reservations.reserver(console.saisir("Numéro de carte du lecteur", True), livre_id)
        console.info(f"Réservation n°{r['reservation_id']} enregistrée pour « {r['titre']} » "
                     f"(position {r['position']} dans la file).")

    def annuler(self):
        numero = console.saisir_entier("N° de la réservation")
        if numero is not None:
            self.reservations.annuler(numero)
            console.info("Réservation annulée.")

    def file(self):
        livre_id = console.saisir_entier("ID du livre")
        if livre_id is None:
            return
        lignes = [[f["position"], f["reservation_id"], f["lecteur"], formater_date(f["date"])]
                  for f in self.reservations.file_attente(livre_id)]
        console.tableau(["Position", "N°", "Lecteur", "Réservé le"], lignes)

    def toutes(self):
        lignes = [[r["id"], r["titre"], f'{r["prenom"]} {r["nom"]}', r["numero_carte"],
                   formater_date(r["date_reservation"])] for r in self.reservations.lister_en_attente()]
        console.tableau(["N°", "Titre", "Lecteur", "Carte", "Réservé le"], lignes)
