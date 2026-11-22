"""Fonctions utilitaires partagées par toute l'application."""
from datetime import date, datetime, timedelta


class ErreurMetier(Exception):
    """Règle de gestion non respectée (le message est destiné à l'utilisateur)."""


def aujourdhui():
    """Date du jour (fonction isolée pour pouvoir la simuler dans les tests)."""
    return date.today()


def depuis_iso(texte):
    """Convertit 'AAAA-MM-JJ' en objet date."""
    return datetime.strptime(texte, "%Y-%m-%d").date()


def ajouter_jours(texte_iso, nombre):
    """Ajoute des jours à une date ISO et renvoie une date ISO."""
    return (depuis_iso(texte_iso) + timedelta(days=nombre)).isoformat()


def ecart_jours(debut_iso, fin_iso):
    """Nombre de jours entre deux dates ISO (fin - début)."""
    return (depuis_iso(fin_iso) - depuis_iso(debut_iso)).days


def formater_date(texte_iso):
    """Affiche une date ISO au format JJ/MM/AAAA ('-' si vide)."""
    if not texte_iso:
        return "-"
    return depuis_iso(texte_iso).strftime("%d/%m/%Y")


def lire_date(texte):
    """Lit une date saisie (JJ/MM/AAAA ou AAAA-MM-JJ) et renvoie une date ISO."""
    texte = (texte or "").strip()
    for modele in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texte, modele).date().isoformat()
        except ValueError:
            continue
    raise ErreurMetier("Date invalide : utilisez le format JJ/MM/AAAA.")


def valider_isbn(texte):
    """Valide un ISBN-10 ou ISBN-13 (facultatif) et renvoie sa forme sans tirets, ou None."""
    brut = (texte or "").replace("-", "").replace(" ", "").upper()
    if not brut:
        return None
    if len(brut) == 13 and brut.isdigit():
        somme = sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(brut[:12]))
        if (10 - somme % 10) % 10 == int(brut[12]):
            return brut
    elif len(brut) == 10 and brut[:9].isdigit() and (brut[9].isdigit() or brut[9] == "X"):
        somme = sum((10 - i) * int(c) for i, c in enumerate(brut[:9]))
        somme += 10 if brut[9] == "X" else int(brut[9])
        if somme % 11 == 0:
            return brut
    raise ErreurMetier("ISBN invalide (laissez vide si le livre n'en a pas).")


def entier_positif(valeur, nom, minimum=0):
    """Vérifie qu'une valeur est un entier >= minimum."""
    try:
        nombre = int(valeur)
    except (TypeError, ValueError):
        raise ErreurMetier(f"{nom} doit être un nombre entier.")
    if nombre < minimum:
        raise ErreurMetier(f"{nom} doit être supérieur ou égal à {minimum}.")
    return nombre
