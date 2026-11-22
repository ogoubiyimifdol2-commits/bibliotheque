"""Création des tables et des règles de prêt par défaut."""

TABLES = """
CREATE TABLE IF NOT EXISTS livre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    isbn TEXT UNIQUE,
    categorie TEXT NOT NULL DEFAULT '',
    annee INTEGER
);
CREATE TABLE IF NOT EXISTS exemplaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL REFERENCES livre(id),
    code_inventaire TEXT NOT NULL UNIQUE,
    cote TEXT NOT NULL DEFAULT '',
    etat TEXT NOT NULL DEFAULT 'bon' CHECK (etat IN ('bon', 'abîmé', 'perdu')),
    disponible INTEGER NOT NULL DEFAULT 1 CHECK (disponible IN (0, 1))
);
CREATE TABLE IF NOT EXISTS lecteur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_carte TEXT NOT NULL UNIQUE,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    categorie TEXT NOT NULL CHECK (categorie IN ('etudiant', 'enseignant')),
    date_inscription TEXT NOT NULL,
    suspendu_manuel INTEGER NOT NULL DEFAULT 0,
    suspension_fin TEXT
);
CREATE TABLE IF NOT EXISTS pret (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exemplaire_id INTEGER NOT NULL REFERENCES exemplaire(id),
    lecteur_id INTEGER NOT NULL REFERENCES lecteur(id),
    date_pret TEXT NOT NULL,
    date_echeance TEXT NOT NULL,
    date_retour TEXT,
    nb_renouvellements INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livre_id INTEGER NOT NULL REFERENCES livre(id),
    lecteur_id INTEGER NOT NULL REFERENCES lecteur(id),
    date_reservation TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'en_attente'
        CHECK (statut IN ('en_attente', 'honoree', 'annulee'))
);
CREATE TABLE IF NOT EXISTS regle_pret (
    categorie TEXT PRIMARY KEY CHECK (categorie IN ('etudiant', 'enseignant')),
    max_livres INTEGER NOT NULL,
    duree_jours INTEGER NOT NULL,
    max_renouvellements INTEGER NOT NULL,
    validite_jours INTEGER NOT NULL DEFAULT 365
);
"""

# (catégorie, max livres, durée en jours, renouvellements, validité de l'inscription en jours)
REGLES_PAR_DEFAUT = [
    ("etudiant", 2, 15, 1, 365),
    ("enseignant", 3, 30, 1, 365),
]


def creer_tables(connexion):
    """Crée les tables manquantes et les règles par défaut (sans écraser l'existant)."""
    connexion.executescript(TABLES)
    connexion.executemany(
        "INSERT OR IGNORE INTO regle_pret VALUES (?, ?, ?, ?, ?)", REGLES_PAR_DEFAUT
    )
    connexion.commit()
