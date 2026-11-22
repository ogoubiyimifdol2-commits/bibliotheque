"""Accès à la table lecteur."""
from models.lecteur import Lecteur


class LecteurRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def ajouter(self, l):
        curseur = self.connexion.execute(
            "INSERT INTO lecteur (numero_carte, nom, prenom, categorie, date_inscription) "
            "VALUES (?, ?, ?, ?, ?)",
            (l.numero_carte, l.nom, l.prenom, l.categorie, l.date_inscription))
        return curseur.lastrowid

    def supprimer(self, lecteur_id):
        self.connexion.execute("DELETE FROM lecteur WHERE id = ?", (lecteur_id,))

    def obtenir(self, lecteur_id):
        ligne = self.connexion.execute(
            "SELECT * FROM lecteur WHERE id = ?", (lecteur_id,)).fetchone()
        return Lecteur.depuis_ligne(ligne) if ligne else None

    def obtenir_par_carte(self, numero_carte):
        ligne = self.connexion.execute(
            "SELECT * FROM lecteur WHERE numero_carte = ?", (numero_carte,)).fetchone()
        return Lecteur.depuis_ligne(ligne) if ligne else None

    def lister(self):
        lignes = self.connexion.execute("SELECT * FROM lecteur ORDER BY nom, prenom").fetchall()
        return [Lecteur.depuis_ligne(l) for l in lignes]

    def rechercher(self, terme):
        motif = f"%{terme}%"
        lignes = self.connexion.execute(
            "SELECT * FROM lecteur WHERE nom LIKE ? OR prenom LIKE ? OR numero_carte LIKE ? "
            "ORDER BY nom, prenom", (motif, motif, motif)).fetchall()
        return [Lecteur.depuis_ligne(l) for l in lignes]

    def definir_suspension_manuelle(self, lecteur_id, suspendu):
        self.connexion.execute(
            "UPDATE lecteur SET suspendu_manuel = ? WHERE id = ?", (int(suspendu), lecteur_id))

    def definir_suspension_fin(self, lecteur_id, date_fin):
        self.connexion.execute(
            "UPDATE lecteur SET suspension_fin = ? WHERE id = ?", (date_fin, lecteur_id))
