"""Modèle Lecteur."""
from dataclasses import dataclass
from typing import Optional

import utils

CATEGORIES = ("etudiant", "enseignant")


@dataclass
class Lecteur:
    numero_carte: str
    nom: str
    prenom: str
    categorie: str
    date_inscription: str
    suspendu_manuel: bool = False
    suspension_fin: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def depuis_ligne(cls, l):
        return cls(id=l["id"], numero_carte=l["numero_carte"], nom=l["nom"],
                   prenom=l["prenom"], categorie=l["categorie"],
                   date_inscription=l["date_inscription"],
                   suspendu_manuel=bool(l["suspendu_manuel"]),
                   suspension_fin=l["suspension_fin"])

    def est_suspendu(self, jour_iso):
        """Suspendu manuellement, ou tant que la date de fin de suspension n'est pas atteinte."""
        return self.suspendu_manuel or (
            self.suspension_fin is not None and jour_iso < self.suspension_fin)

    def date_expiration(self, validite_jours):
        return utils.ajouter_jours(self.date_inscription, validite_jours)

    def est_expire(self, jour_iso, validite_jours):
        return jour_iso > self.date_expiration(validite_jours)
