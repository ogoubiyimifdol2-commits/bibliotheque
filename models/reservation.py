"""Modèle Réservation (file d'attente par livre : premier arrivé, premier servi)."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Reservation:
    livre_id: int
    lecteur_id: int
    date_reservation: str
    statut: str = "en_attente"
    id: Optional[int] = None

    @classmethod
    def depuis_ligne(cls, l):
        return cls(id=l["id"], livre_id=l["livre_id"], lecteur_id=l["lecteur_id"],
                   date_reservation=l["date_reservation"], statut=l["statut"])
