"""Modèle Exemplaire (copie physique d'un livre)."""
from dataclasses import dataclass
from typing import Optional

ETATS = ("bon", "abîmé", "perdu")


@dataclass
class Exemplaire:
    livre_id: int
    code_inventaire: str
    cote: str = ""
    etat: str = "bon"
    disponible: bool = True
    id: Optional[int] = None

    @classmethod
    def depuis_ligne(cls, l):
        return cls(id=l["id"], livre_id=l["livre_id"], code_inventaire=l["code_inventaire"],
                   cote=l["cote"], etat=l["etat"], disponible=bool(l["disponible"]))
