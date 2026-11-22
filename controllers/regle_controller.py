"""Règles de prêt modifiables depuis le menu."""
import utils
from models.lecteur import CATEGORIES
from repositories.regle_pret_repository import ReglePretRepository
from utils import ErreurMetier


class RegleController:
    def __init__(self, connexion):
        self.connexion = connexion
        self.regles = ReglePretRepository(connexion)

    def lister(self):
        return self.regles.lister()

    def modifier(self, categorie, max_livres, duree_jours, max_renouvellements, validite_jours):
        regle = self.regles.obtenir((categorie or "").strip().lower().replace("é", "e"))
        if regle is None:
            raise ErreurMetier(f"Catégorie inconnue (choisissez {' ou '.join(CATEGORIES)}).")
        regle.max_livres = utils.entier_positif(max_livres, "Le nombre maximum de livres", 1)
        regle.duree_jours = utils.entier_positif(duree_jours, "La durée de prêt", 1)
        regle.max_renouvellements = utils.entier_positif(max_renouvellements, "Le nombre de renouvellements", 0)
        regle.validite_jours = utils.entier_positif(validite_jours, "La validité de l'inscription", 1)
        self.regles.modifier(regle)
        self.connexion.commit()
        return regle
