"""Modèle RèglePrêt (une ligne par catégorie de lecteur)."""
from dataclasses import dataclass


@dataclass
class ReglePret:
    categorie: str
    max_livres: int
    duree_jours: int
    max_renouvellements: int
    validite_jours: int = 365

    @classmethod
    def depuis_ligne(cls, l):
        return cls(categorie=l["categorie"], max_livres=l["max_livres"],
                   duree_jours=l["duree_jours"], max_renouvellements=l["max_renouvellements"],
                   validite_jours=l["validite_jours"])
