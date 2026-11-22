"""Accès à la table reservation."""
from models.reservation import Reservation


class ReservationRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def creer(self, r):
        curseur = self.connexion.execute(
            "INSERT INTO reservation (livre_id, lecteur_id, date_reservation, statut) "
            "VALUES (?, ?, ?, ?)", (r.livre_id, r.lecteur_id, r.date_reservation, r.statut))
        return curseur.lastrowid

    def obtenir(self, reservation_id):
        ligne = self.connexion.execute(
            "SELECT * FROM reservation WHERE id = ?", (reservation_id,)).fetchone()
        return Reservation.depuis_ligne(ligne) if ligne else None

    def file_attente(self, livre_id):
        """Réservations en attente d'un livre, la plus ancienne en premier."""
        lignes = self.connexion.execute(
            "SELECT * FROM reservation WHERE livre_id = ? AND statut = 'en_attente' ORDER BY id",
            (livre_id,)).fetchall()
        return [Reservation.depuis_ligne(l) for l in lignes]

    def obtenir_en_attente(self, livre_id, lecteur_id):
        ligne = self.connexion.execute(
            "SELECT * FROM reservation WHERE livre_id = ? AND lecteur_id = ? "
            "AND statut = 'en_attente'", (livre_id, lecteur_id)).fetchone()
        return Reservation.depuis_ligne(ligne) if ligne else None

    def changer_statut(self, reservation_id, statut):
        self.connexion.execute(
            "UPDATE reservation SET statut = ? WHERE id = ?", (statut, reservation_id))

    def supprimer_par_lecteur(self, lecteur_id):
        self.connexion.execute("DELETE FROM reservation WHERE lecteur_id = ?", (lecteur_id,))

    def supprimer_par_livre(self, livre_id):
        self.connexion.execute("DELETE FROM reservation WHERE livre_id = ?", (livre_id,))

    def lister_en_attente_detail(self):
        return self.connexion.execute(
            "SELECT r.id, r.date_reservation, l.titre, c.numero_carte, c.nom, c.prenom "
            "FROM reservation r JOIN livre l ON l.id = r.livre_id "
            "JOIN lecteur c ON c.id = r.lecteur_id WHERE r.statut = 'en_attente' "
            "ORDER BY l.titre, r.id").fetchall()
