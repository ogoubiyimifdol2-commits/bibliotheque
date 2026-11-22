"""Règles de gestion des livres."""
import utils
from models.livre import Livre
from repositories.exemplaire_repository import ExemplaireRepository
from repositories.livre_repository import LivreRepository
from repositories.pret_repository import PretRepository
from repositories.reservation_repository import ReservationRepository
from utils import ErreurMetier


class LivreController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.livres = LivreRepository(connexion)
        self.exemplaires = ExemplaireRepository(connexion)
        self.prets = PretRepository(connexion)
        self.reservations = ReservationRepository(connexion)

    def _valider(self, titre, auteur, isbn, categorie, annee, livre_id=None):
        titre, auteur = (titre or "").strip(), (auteur or "").strip()
        if not titre or not auteur:
            raise ErreurMetier("Le titre et l'auteur sont obligatoires.")
        isbn = utils.valider_isbn(isbn)
        if isbn:
            existant = self.livres.obtenir_par_isbn(isbn)
            if existant and existant.id != livre_id:
                raise ErreurMetier(f"Cet ISBN existe déjà : « {existant.titre} ».")
        annee = utils.entier_positif(annee, "L'année", 0) if str(annee or "").strip() else None
        return Livre(titre=titre, auteur=auteur, isbn=isbn,
                     categorie=(categorie or "").strip(), annee=annee, id=livre_id)

    def ajouter(self, titre, auteur, isbn="", categorie="", annee=""):
        livre = self._valider(titre, auteur, isbn, categorie, annee)
        livre.id = self.livres.ajouter(livre)
        self.connexion.commit()
        return livre

    def modifier(self, livre_id, titre, auteur, isbn="", categorie="", annee=""):
        if self.livres.obtenir(livre_id) is None:
            raise ErreurMetier("Livre introuvable.")
        livre = self._valider(titre, auteur, isbn, categorie, annee, livre_id)
        self.livres.modifier(livre)
        self.connexion.commit()
        return livre

    def supprimer(self, livre_id):
        if self.livres.obtenir(livre_id) is None:
            raise ErreurMetier("Livre introuvable.")
        if self.prets.livre_a_historique(livre_id):
            raise ErreurMetier("Suppression impossible : un exemplaire de ce livre a un historique de prêt.")
        self.reservations.supprimer_par_livre(livre_id)
        self.exemplaires.supprimer_par_livre(livre_id)
        self.livres.supprimer(livre_id)
        self.connexion.commit()

    def obtenir(self, livre_id):
        return self.livres.obtenir(livre_id)

    def lister(self):
        return self.livres.lister()

    def rechercher(self, terme):
        return self.livres.rechercher((terme or "").strip())

    def disponibilite(self, livre_id):
        """Renvoie (exemplaires disponibles, total d'exemplaires)."""
        total = len(self.exemplaires.lister(livre_id))
        return self.exemplaires.compter_disponibles(livre_id), total
