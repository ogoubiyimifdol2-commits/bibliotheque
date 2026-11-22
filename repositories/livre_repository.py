"""Accès à la table livre."""
from models.livre import Livre


class LivreRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def ajouter(self, livre):
        curseur = self.connexion.execute(
            "INSERT INTO livre (titre, auteur, isbn, categorie, annee) VALUES (?, ?, ?, ?, ?)",
            (livre.titre, livre.auteur, livre.isbn, livre.categorie, livre.annee))
        return curseur.lastrowid

    def modifier(self, livre):
        self.connexion.execute(
            "UPDATE livre SET titre = ?, auteur = ?, isbn = ?, categorie = ?, annee = ? WHERE id = ?",
            (livre.titre, livre.auteur, livre.isbn, livre.categorie, livre.annee, livre.id))

    def supprimer(self, livre_id):
        self.connexion.execute("DELETE FROM livre WHERE id = ?", (livre_id,))

    def obtenir(self, livre_id):
        ligne = self.connexion.execute("SELECT * FROM livre WHERE id = ?", (livre_id,)).fetchone()
        return Livre.depuis_ligne(ligne) if ligne else None

    def obtenir_par_isbn(self, isbn):
        ligne = self.connexion.execute("SELECT * FROM livre WHERE isbn = ?", (isbn,)).fetchone()
        return Livre.depuis_ligne(ligne) if ligne else None

    def lister(self):
        lignes = self.connexion.execute("SELECT * FROM livre ORDER BY titre").fetchall()
        return [Livre.depuis_ligne(l) for l in lignes]

    def rechercher(self, terme):
        """Recherche dans le titre, l'auteur, l'ISBN et la catégorie."""
        motif = f"%{terme}%"
        lignes = self.connexion.execute(
            "SELECT * FROM livre WHERE titre LIKE ? OR auteur LIKE ? "
            "OR IFNULL(isbn, '') LIKE ? OR categorie LIKE ? ORDER BY titre",
            (motif, motif, motif, motif)).fetchall()
        return [Livre.depuis_ligne(l) for l in lignes]
