"""Règles de gestion des réservations (file d'attente par livre)."""
import utils
from models.reservation import Reservation
from repositories.exemplaire_repository import ExemplaireRepository
from repositories.lecteur_repository import LecteurRepository
from repositories.livre_repository import LivreRepository
from repositories.pret_repository import PretRepository
from repositories.reservation_repository import ReservationRepository
from utils import ErreurMetier


class ReservationController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.reservations = ReservationRepository(connexion)
        self.lecteurs = LecteurRepository(connexion)
        self.livres = LivreRepository(connexion)
        self.exemplaires = ExemplaireRepository(connexion)
        self.prets = PretRepository(connexion)

    def reserver(self, numero_carte, livre_id):
        lecteur = self.lecteurs.obtenir_par_carte((numero_carte or "").strip())
        if lecteur is None:
            raise ErreurMetier("Aucun lecteur avec ce numéro de carte.")
        livre = self.livres.obtenir(livre_id)
        if livre is None:
            raise ErreurMetier("Livre introuvable.")
        if not self.exemplaires.lister(livre_id):
            raise ErreurMetier("Ce livre n'a aucun exemplaire.")
        if self.reservations.obtenir_en_attente(livre_id, lecteur.id):
            raise ErreurMetier("Ce lecteur a déjà réservé ce livre.")
        if self.prets.lecteur_emprunte_livre(lecteur.id, livre_id):
            raise ErreurMetier("Ce lecteur emprunte déjà ce livre.")
        file = self.reservations.file_attente(livre_id)
        if self.exemplaires.compter_disponibles(livre_id) > len(file):
            raise ErreurMetier("Un exemplaire est disponible : empruntez-le directement.")
        r = Reservation(livre_id, lecteur.id, utils.aujourdhui().isoformat())
        r.id = self.reservations.creer(r)
        self.connexion.commit()
        return {"reservation_id": r.id, "position": len(file) + 1, "titre": livre.titre}

    def annuler(self, reservation_id):
        r = self.reservations.obtenir(reservation_id)
        if r is None or r.statut != "en_attente":
            raise ErreurMetier("Aucune réservation en attente avec ce numéro.")
        self.reservations.changer_statut(r.id, "annulee")
        self.connexion.commit()

    def lister_en_attente(self):
        return self.reservations.lister_en_attente_detail()

    def file_attente(self, livre_id):
        """Liste de dictionnaires (position, lecteur, date) pour un livre."""
        if self.livres.obtenir(livre_id) is None:
            raise ErreurMetier("Livre introuvable.")
        resultat = []
        for rang, r in enumerate(self.reservations.file_attente(livre_id), start=1):
            lecteur = self.lecteurs.obtenir(r.lecteur_id)
            resultat.append({"position": rang, "reservation_id": r.id,
                             "lecteur": f"{lecteur.prenom} {lecteur.nom} ({lecteur.numero_carte})",
                             "date": r.date_reservation})
        return resultat
