"""Règles de gestion des lecteurs."""
import utils
from models.lecteur import CATEGORIES, Lecteur
from repositories.lecteur_repository import LecteurRepository
from repositories.pret_repository import PretRepository
from repositories.regle_pret_repository import ReglePretRepository
from repositories.reservation_repository import ReservationRepository
from utils import ErreurMetier


class LecteurController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.lecteurs = LecteurRepository(connexion)
        self.prets = PretRepository(connexion)
        self.regles = ReglePretRepository(connexion)
        self.reservations = ReservationRepository(connexion)

    @staticmethod
    def _normaliser_categorie(categorie):
        cat = (categorie or "").strip().lower().replace("é", "e")
        if cat not in CATEGORIES:
            raise ErreurMetier("Catégorie invalide : choisissez etudiant ou enseignant.")
        return cat

    def inscrire(self, numero_carte, nom, prenom, categorie, date_inscription=None):
        carte, nom, prenom = (numero_carte or "").strip(), (nom or "").strip(), (prenom or "").strip()
        if not carte or not nom or not prenom:
            raise ErreurMetier("Le numéro de carte, le nom et le prénom sont obligatoires.")
        if self.lecteurs.obtenir_par_carte(carte):
            raise ErreurMetier("Ce numéro de carte est déjà utilisé.")
        date_ins = utils.lire_date(date_inscription) if date_inscription else utils.aujourdhui().isoformat()
        lecteur = Lecteur(numero_carte=carte, nom=nom, prenom=prenom,
                          categorie=self._normaliser_categorie(categorie), date_inscription=date_ins)
        lecteur.id = self.lecteurs.ajouter(lecteur)
        self.connexion.commit()
        return lecteur

    def _obtenir(self, numero_carte):
        lecteur = self.lecteurs.obtenir_par_carte((numero_carte or "").strip())
        if lecteur is None:
            raise ErreurMetier("Aucun lecteur avec ce numéro de carte.")
        return lecteur

    def suspendre(self, numero_carte):
        lecteur = self._obtenir(numero_carte)
        self.lecteurs.definir_suspension_manuelle(lecteur.id, True)
        self.connexion.commit()

    def lever_suspension(self, numero_carte):
        """Lève la suspension manuelle et toute suspension liée à un retard."""
        lecteur = self._obtenir(numero_carte)
        self.lecteurs.definir_suspension_manuelle(lecteur.id, False)
        self.lecteurs.definir_suspension_fin(lecteur.id, None)
        self.connexion.commit()

    def supprimer(self, numero_carte):
        lecteur = self._obtenir(numero_carte)
        if self.prets.lecteur_a_historique(lecteur.id):
            raise ErreurMetier("Suppression impossible : ce lecteur a un historique de prêt.")
        self.reservations.supprimer_par_lecteur(lecteur.id)
        self.lecteurs.supprimer(lecteur.id)
        self.connexion.commit()

    def statut(self, lecteur):
        """Texte décrivant la situation du lecteur : actif, suspendu ou expiré."""
        jour = utils.aujourdhui().isoformat()
        regle = self.regles.obtenir(lecteur.categorie)
        if lecteur.est_expire(jour, regle.validite_jours):
            return "inscription expirée"
        if lecteur.suspendu_manuel:
            return "suspendu"
        if lecteur.suspension_fin and jour < lecteur.suspension_fin:
            return f"suspendu jusqu'au {utils.formater_date(lecteur.suspension_fin)}"
        return "actif"

    def lister(self):
        return self.lecteurs.lister()

    def rechercher(self, terme):
        return self.lecteurs.rechercher((terme or "").strip())

    def obtenir_par_carte(self, numero_carte):
        return self._obtenir(numero_carte)
