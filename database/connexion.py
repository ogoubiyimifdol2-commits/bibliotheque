"""Connexion à la base SQLite."""
import os
import sqlite3

DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def chemin_base():
    """Chemin du fichier de base (modifiable avec la variable BIBLIOIIT_DB)."""
    return os.environ.get("BIBLIOIIT_DB", os.path.join(DOSSIER_PROJET, "biblioiit.db"))


def get_connection(chemin=None):
    """Ouvre une connexion SQLite avec clés étrangères et accès par nom de colonne."""
    connexion = sqlite3.connect(chemin or chemin_base())
    connexion.row_factory = sqlite3.Row
    connexion.execute("PRAGMA foreign_keys = ON")
    return connexion
