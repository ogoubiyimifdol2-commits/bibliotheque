"""Accès à la table regle_pret."""
from models.regle_pret import ReglePret


class ReglePretRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def obtenir(self, categorie):
        ligne = self.connexion.execute(
            "SELECT * FROM regle_pret WHERE categorie = ?", (categorie,)).fetchone()
        return ReglePret.depuis_ligne(ligne) if ligne else None

    def lister(self):
        lignes = self.connexion.execute(
            "SELECT * FROM regle_pret ORDER BY categorie").fetchall()
        return [ReglePret.depuis_ligne(l) for l in lignes]

    def modifier(self, r):
        self.connexion.execute(
            "UPDATE regle_pret SET max_livres = ?, duree_jours = ?, max_renouvellements = ?, "
            "validite_jours = ? WHERE categorie = ?",
            (r.max_livres, r.duree_jours, r.max_renouvellements, r.validite_jours, r.categorie))
