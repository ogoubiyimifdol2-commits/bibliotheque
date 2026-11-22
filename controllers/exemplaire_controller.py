"""Règles de gestion des exemplaires."""
from models.exemplaire import ETATS, Exemplaire
from repositories.exemplaire_repository import ExemplaireRepository
from repositories.livre_repository import LivreRepository
from repositories.pret_repository import PretRepository
from utils import ErreurMetier


class ExemplaireController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.exemplaires = ExemplaireRepository(connexion)
        self.livres = LivreRepository(connexion)
        self.prets = PretRepository(connexion)

    @staticmethod
    def _normaliser_etat(etat):
        etat = (etat or "bon").strip().lower()
        if etat == "abime":
            etat = "abîmé"
        if etat not in ETATS:
            raise ErreurMetier("État invalide : choisissez bon, abîmé ou perdu.")
        return etat

    def ajouter(self, livre_id, code_inventaire, cote="", etat="bon"):
        if self.livres.obtenir(livre_id) is None:
            raise ErreurMetier("Livre introuvable.")
        code = (code_inventaire or "").strip()
        if not code:
            raise ErreurMetier("Le code d'inventaire est obligatoire.")
        if self.exemplaires.obtenir_par_code(code):
            raise ErreurMetier("Ce code d'inventaire existe déjà.")
        ex = Exemplaire(livre_id=livre_id, code_inventaire=code,
                        cote=(cote or "").strip(), etat=self._normaliser_etat(etat))
        ex.id = self.exemplaires.ajouter(ex)
        self.connexion.commit()
        return ex

    def modifier(self, code_inventaire, nouveau_code=None, cote=None, etat=None):
        ex = self.exemplaires.obtenir_par_code((code_inventaire or "").strip())
        if ex is None:
            raise ErreurMetier("Exemplaire introuvable.")
        if nouveau_code and nouveau_code.strip() != ex.code_inventaire:
            if self.exemplaires.obtenir_par_code(nouveau_code.strip()):
                raise ErreurMetier("Ce code d'inventaire existe déjà.")
            ex.code_inventaire = nouveau_code.strip()
        if cote is not None and cote.strip():
            ex.cote = cote.strip()
        if etat is not None and etat.strip():
            ex.etat = self._normaliser_etat(etat)
        self.exemplaires.modifier(ex)
        self.connexion.commit()
        return ex

    def supprimer(self, code_inventaire):
        ex = self.exemplaires.obtenir_par_code((code_inventaire or "").strip())
        if ex is None:
            raise ErreurMetier("Exemplaire introuvable.")
        if self.prets.exemplaire_a_historique(ex.id):
            raise ErreurMetier("Suppression impossible : cet exemplaire a un historique de prêt.")
        self.exemplaires.supprimer(ex.id)
        self.connexion.commit()

    def lister(self, livre_id=None):
        return self.exemplaires.lister(livre_id)
