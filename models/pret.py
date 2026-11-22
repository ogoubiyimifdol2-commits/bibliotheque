"""Modèle Prêt."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pret:
    exemplaire_id: int
    lecteur_id: int
    date_pret: str
    date_echeance: str
    date_retour: Optional[str] = None
    nb_renouvellements: int = 0
    id: Optional[int] = None

    @classmethod
    def depuis_ligne(cls, l):
        return cls(id=l["id"], exemplaire_id=l["exemplaire_id"], lecteur_id=l["lecteur_id"],
                   date_pret=l["date_pret"], date_echeance=l["date_echeance"],
                   date_retour=l["date_retour"], nb_renouvellements=l["nb_renouvellements"])
