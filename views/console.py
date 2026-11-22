"""Outils d'affichage et de saisie communs à toutes les vues (aucune logique métier)."""


def titre(texte):
    print()
    print("=" * 60)
    print(texte.upper())
    print("=" * 60)


def saisir(invite, obligatoire=False):
    """Demande un texte à l'utilisateur (répète tant qu'il est obligatoire et vide)."""
    while True:
        valeur = input(invite + " : ").strip()
        if valeur or not obligatoire:
            return valeur
        print("Ce champ est obligatoire.")


def saisir_entier(invite):
    """Demande un nombre entier ; renvoie None si la saisie n'est pas un entier."""
    valeur = saisir(invite)
    try:
        return int(valeur)
    except ValueError:
        print("Veuillez saisir un nombre entier.")
        return None


def confirmer(question):
    return input(question + " (o/n) : ").strip().lower() in ("o", "oui")


def info(message):
    print("[OK] " + message)


def erreur(message):
    print("[!] " + message)


def tableau(entetes, lignes):
    """Affiche un tableau texte aligné."""
    if not lignes:
        print("(aucun résultat)")
        return
    lignes = [[("" if c is None else str(c)) for c in ligne] for ligne in lignes]
    largeurs = [max(len(entetes[i]), *(len(l[i]) for l in lignes)) for i in range(len(entetes))]
    print(" | ".join(e.ljust(largeurs[i]) for i, e in enumerate(entetes)))
    print("-+-".join("-" * w for w in largeurs))
    for ligne in lignes:
        print(" | ".join(c.ljust(largeurs[i]) for i, c in enumerate(ligne)))


def menu(titre_menu, options):
    """Affiche un menu {numéro: libellé} et renvoie le choix saisi."""
    titre(titre_menu)
    for numero, libelle in options:
        print(f"  {numero}. {libelle}")
    return input("Votre choix : ").strip()
