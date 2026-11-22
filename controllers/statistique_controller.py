"""Statistiques de la bibliothèque."""
from repositories.pret_repository import PretRepository


class StatistiqueController:
    def __init__(self, connexion):
        self.prets = PretRepository(connexion)

    def livres_les_plus_empruntes(self, limite=10):
        return self.prets.livres_les_plus_empruntes(limite)
