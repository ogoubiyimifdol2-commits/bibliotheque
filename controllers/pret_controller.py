"""Règles de gestion des prêts, retours et renouvellements."""
import utils
from models.pret import Pret
from repositories.exemplaire_repository import ExemplaireRepository
from repositories.lecteur_repository import LecteurRepository
from repositories.livre_repository import LivreRepository
from repositories.pret_repository import PretRepository
from repositories.regle_pret_repository import ReglePretRepository
from repositories.reservation_repository import ReservationRepository
from utils import ErreurMetier


class PretController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.exemplaires = ExemplaireRepository(connexion)
        self.lecteurs = LecteurRepository(connexion)
        self.livres = LivreRepository(connexion)
        self.prets = PretRepository(connexion)
        self.regles = ReglePretRepository(connexion)
        self.reservations = ReservationRepository(connexion)

    # ---------------------------------------------------------------- prêt
    def emprunter(self, numero_carte, code_inventaire):
        """Enregistre un prêt si toutes les règles sont respectées (sinon ErreurMetier)."""
        lecteur = self.lecteurs.obtenir_par_carte((numero_carte or "").strip())
        if lecteur is None:
            raise ErreurMetier("Aucun lecteur avec ce numéro de carte.")
        ex = self.exemplaires.obtenir_par_code((code_inventaire or "").strip())
        if ex is None:
            raise ErreurMetier("Aucun exemplaire avec ce code d'inventaire.")
        livre = self.livres.obtenir(ex.livre_id)
        regle = self.regles.obtenir(lecteur.categorie)
        jour = utils.aujourdhui().isoformat()

        if lecteur.est_expire(jour, regle.validite_jours):
            raise ErreurMetier("Prêt refusé : l'inscription du lecteur a expiré le "
                               f"{utils.formater_date(lecteur.date_expiration(regle.validite_jours))}.")
        if lecteur.est_suspendu(jour):
            fin = f" jusqu'au {utils.formater_date(lecteur.suspension_fin)}" if (
                not lecteur.suspendu_manuel and lecteur.suspension_fin) else ""
            raise ErreurMetier(f"Prêt refusé : le lecteur est suspendu{fin}.")
        if self.prets.lecteur_a_un_retard(lecteur.id, jour):
            raise ErreurMetier("Prêt refusé : le lecteur a un prêt en retard.")
        if self.prets.compter_en_cours_lecteur(lecteur.id) >= regle.max_livres:
            raise ErreurMetier(f"Prêt refusé : limite de {regle.max_livres} livre(s) atteinte "
                               f"pour la catégorie {lecteur.categorie}.")
        if ex.etat != "bon":
            raise ErreurMetier(f"Prêt refusé : l'exemplaire est en état « {ex.etat} ».")
        if not ex.disponible:
            raise ErreurMetier("Prêt refusé : cet exemplaire est déjà emprunté.")

        # File d'attente : les premiers réservataires passent avant les autres lecteurs.
        file = self.reservations.file_attente(ex.livre_id)
        disponibles = self.exemplaires.compter_disponibles(ex.livre_id)
        reservation = self.reservations.obtenir_en_attente(ex.livre_id, lecteur.id)
        if reservation is not None:
            rang = [r.id for r in file].index(reservation.id) + 1
            if rang > disponibles:
                raise ErreurMetier(f"Prêt refusé : vous êtes en position {rang} dans la file d'attente, "
                                   "les exemplaires disponibles sont réservés aux lecteurs précédents.")
        elif disponibles <= len(file):
            raise ErreurMetier("Prêt refusé : les exemplaires disponibles de ce livre sont réservés "
                               "par d'autres lecteurs.")

        echeance = utils.ajouter_jours(jour, regle.duree_jours)
        pret_id = self.prets.creer(Pret(ex.id, lecteur.id, jour, echeance))
        self.exemplaires.definir_disponible(ex.id, False)
        if reservation is not None:
            self.reservations.changer_statut(reservation.id, "honoree")
        self.connexion.commit()
        return {"pret_id": pret_id, "titre": livre.titre, "echeance": echeance}

    # -------------------------------------------------------------- retour
    def retourner(self, code_inventaire):
        """Enregistre un retour ; en cas de retard, suspend le lecteur autant de jours que de retard."""
        ex = self.exemplaires.obtenir_par_code((code_inventaire or "").strip())
        if ex is None:
            raise ErreurMetier("Aucun exemplaire avec ce code d'inventaire.")
        pret = self.prets.obtenir_en_cours_par_exemplaire(ex.id)
        if pret is None:
            raise ErreurMetier("Cet exemplaire n'est pas actuellement emprunté.")
        jour = utils.aujourdhui().isoformat()
        self.prets.cloturer(pret.id, jour)
        self.exemplaires.definir_disponible(ex.id, True)

        retard = max(0, utils.ecart_jours(pret.date_echeance, jour))
        fin_suspension = None
        if retard > 0:
            lecteur = self.lecteurs.obtenir(pret.lecteur_id)
            fin_suspension = utils.ajouter_jours(jour, retard)
            if lecteur.suspension_fin and lecteur.suspension_fin > fin_suspension:
                fin_suspension = lecteur.suspension_fin
            self.lecteurs.definir_suspension_fin(lecteur.id, fin_suspension)

        file = self.reservations.file_attente(ex.livre_id)
        prochain = None
        if file:
            suivant = self.lecteurs.obtenir(file[0].lecteur_id)
            prochain = f"{suivant.prenom} {suivant.nom} (carte {suivant.numero_carte})"
        self.connexion.commit()
        return {"retard_jours": retard, "suspension_fin": fin_suspension,
                "prochain_reservataire": prochain}

    # ------------------------------------------------------- renouvellement
    def renouveler(self, code_inventaire):
        ex = self.exemplaires.obtenir_par_code((code_inventaire or "").strip())
        if ex is None:
            raise ErreurMetier("Aucun exemplaire avec ce code d'inventaire.")
        pret = self.prets.obtenir_en_cours_par_exemplaire(ex.id)
        if pret is None:
            raise ErreurMetier("Cet exemplaire n'est pas actuellement emprunté.")
        lecteur = self.lecteurs.obtenir(pret.lecteur_id)
        regle = self.regles.obtenir(lecteur.categorie)
        jour = utils.aujourdhui().isoformat()

        if pret.date_echeance < jour:
            raise ErreurMetier("Renouvellement refusé : le prêt est en retard.")
        if any(r.lecteur_id != lecteur.id for r in self.reservations.file_attente(ex.livre_id)):
            raise ErreurMetier("Renouvellement refusé : le livre est réservé par un autre lecteur.")
        if pret.nb_renouvellements >= regle.max_renouvellements:
            raise ErreurMetier("Renouvellement refusé : maximum de "
                               f"{regle.max_renouvellements} renouvellement(s) atteint.")
        nouvelle = utils.ajouter_jours(pret.date_echeance, regle.duree_jours)
        self.prets.renouveler(pret.id, nouvelle)
        self.connexion.commit()
        return {"nouvelle_echeance": nouvelle}

    # --------------------------------------------------------- consultation
    def lister_en_cours(self):
        return self.prets.lister_en_cours()

    def lister_en_retard(self):
        return self.prets.lister_en_retard(utils.aujourdhui().isoformat())
