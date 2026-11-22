"""Accès à la table pret (y compris les requêtes de consultation avec jointures)."""
from models.pret import Pret

_SELECT_DETAIL = """
SELECT p.id, p.date_pret, p.date_echeance, p.nb_renouvellements,
       e.code_inventaire, l.titre, l.auteur,
       r.numero_carte, r.nom, r.prenom
FROM pret p
JOIN exemplaire e ON e.id = p.exemplaire_id
JOIN livre l ON l.id = e.livre_id
JOIN lecteur r ON r.id = p.lecteur_id
"""


class PretRepository:
    def __init__(self, connexion):
        self.connexion = connexion

    def creer(self, pret):
        curseur = self.connexion.execute(
            "INSERT INTO pret (exemplaire_id, lecteur_id, date_pret, date_echeance) "
            "VALUES (?, ?, ?, ?)",
            (pret.exemplaire_id, pret.lecteur_id, pret.date_pret, pret.date_echeance))
        return curseur.lastrowid

    def obtenir_en_cours_par_exemplaire(self, exemplaire_id):
        ligne = self.connexion.execute(
            "SELECT * FROM pret WHERE exemplaire_id = ? AND date_retour IS NULL",
            (exemplaire_id,)).fetchone()
        return Pret.depuis_ligne(ligne) if ligne else None

    def compter_en_cours_lecteur(self, lecteur_id):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret WHERE lecteur_id = ? AND date_retour IS NULL",
            (lecteur_id,)).fetchone()[0]

    def lecteur_a_un_retard(self, lecteur_id, jour_iso):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret WHERE lecteur_id = ? AND date_retour IS NULL "
            "AND date_echeance < ?", (lecteur_id, jour_iso)).fetchone()[0] > 0

    def lecteur_emprunte_livre(self, lecteur_id, livre_id):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret p JOIN exemplaire e ON e.id = p.exemplaire_id "
            "WHERE p.lecteur_id = ? AND e.livre_id = ? AND p.date_retour IS NULL",
            (lecteur_id, livre_id)).fetchone()[0] > 0

    def cloturer(self, pret_id, date_retour):
        self.connexion.execute(
            "UPDATE pret SET date_retour = ? WHERE id = ?", (date_retour, pret_id))

    def renouveler(self, pret_id, nouvelle_echeance):
        self.connexion.execute(
            "UPDATE pret SET date_echeance = ?, nb_renouvellements = nb_renouvellements + 1 "
            "WHERE id = ?", (nouvelle_echeance, pret_id))

    def lecteur_a_historique(self, lecteur_id):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret WHERE lecteur_id = ?", (lecteur_id,)).fetchone()[0] > 0

    def exemplaire_a_historique(self, exemplaire_id):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret WHERE exemplaire_id = ?", (exemplaire_id,)).fetchone()[0] > 0

    def livre_a_historique(self, livre_id):
        return self.connexion.execute(
            "SELECT COUNT(*) FROM pret p JOIN exemplaire e ON e.id = p.exemplaire_id "
            "WHERE e.livre_id = ?", (livre_id,)).fetchone()[0] > 0

    def lister_en_cours(self):
        return self.connexion.execute(
            _SELECT_DETAIL + "WHERE p.date_retour IS NULL ORDER BY p.date_echeance").fetchall()

    def lister_en_retard(self, jour_iso):
        return self.connexion.execute(
            _SELECT_DETAIL + "WHERE p.date_retour IS NULL AND p.date_echeance < ? "
            "ORDER BY p.date_echeance", (jour_iso,)).fetchall()

    def livres_les_plus_empruntes(self, limite):
        return self.connexion.execute(
            "SELECT l.titre, l.auteur, COUNT(*) AS nb_prets FROM pret p "
            "JOIN exemplaire e ON e.id = p.exemplaire_id JOIN livre l ON l.id = e.livre_id "
            "GROUP BY l.id ORDER BY nb_prets DESC, l.titre LIMIT ?", (limite,)).fetchall()
