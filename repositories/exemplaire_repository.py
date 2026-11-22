"""Accès à la table exemplaire."""
from models.exemplaire import Exemplaire


class ExemplaireRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def ajouter(self, ex):
        curseur = self.connexion.execute(
            "INSERT INTO exemplaire (livre_id, code_inventaire, cote, etat, disponible) "
            "VALUES (?, ?, ?, ?, ?)",
            (ex.livre_id, ex.code_inventaire, ex.cote, ex.etat, int(ex.disponible)))
        return curseur.lastrowid

    def modifier(self, ex):
        self.connexion.execute(
            "UPDATE exemplaire SET code_inventaire = ?, cote = ?, etat = ? WHERE id = ?",
            (ex.code_inventaire, ex.cote, ex.etat, ex.id))

    def supprimer(self, exemplaire_id):
        self.connexion.execute("DELETE FROM exemplaire WHERE id = ?", (exemplaire_id,))

    def supprimer_par_livre(self, livre_id):
        self.connexion.execute("DELETE FROM exemplaire WHERE livre_id = ?", (livre_id,))

    def obtenir(self, exemplaire_id):
        ligne = self.connexion.execute(
            "SELECT * FROM exemplaire WHERE id = ?", (exemplaire_id,)).fetchone()
        return Exemplaire.depuis_ligne(ligne) if ligne else None

    def obtenir_par_code(self, code):
        ligne = self.connexion.execute(
            "SELECT * FROM exemplaire WHERE code_inventaire = ?", (code,)).fetchone()
        return Exemplaire.depuis_ligne(ligne) if ligne else None

    def lister(self, livre_id=None):
        if livre_id is None:
            lignes = self.connexion.execute(
                "SELECT * FROM exemplaire ORDER BY code_inventaire").fetchall()
        else:
            lignes = self.connexion.execute(
                "SELECT * FROM exemplaire WHERE livre_id = ? ORDER BY code_inventaire",
                (livre_id,)).fetchall()
        return [Exemplaire.depuis_ligne(l) for l in lignes]

    def compter_disponibles(self, livre_id):
        """Exemplaires en bon état et actuellement rangés en rayon."""
        return self.connexion.execute(
            "SELECT COUNT(*) FROM exemplaire WHERE livre_id = ? AND etat = 'bon' AND disponible = 1",
            (livre_id,)).fetchone()[0]

    def definir_disponible(self, exemplaire_id, disponible):
        self.connexion.execute(
            "UPDATE exemplaire SET disponible = ? WHERE id = ?", (int(disponible), exemplaire_id))
