"""Modèle Livre (titre, indépendamment du nombre d'exemplaires)."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Livre:
    titre: str
    auteur: str
    isbn: Optional[str] = None
    categorie: str = ""
    annee: Optional[int] = None
    id: Optional[int] = None

    @classmethod
    def depuis_ligne(cls, l):
        return cls(id=l["id"], titre=l["titre"], auteur=l["auteur"], isbn=l["isbn"],
                   categorie=l["categorie"], annee=l["annee"])
