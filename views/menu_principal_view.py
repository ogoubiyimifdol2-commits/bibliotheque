"""Menu principal de BiblioIIT."""
from views import console


class MenuPrincipalView:
    def __init__(self, livre_view, exemplaire_view, lecteur_view, pret_view,
                 reservation_view, statistique_view, regle_view):
        self.sous_menus = {
            "1": livre_view.menu, "2": exemplaire_view.menu, "3": lecteur_view.menu,
            "4": pret_view.menu, "5": reservation_view.menu,
            "6": statistique_view.menu, "7": regle_view.menu}

    def executer(self):
        print("Bienvenue dans BiblioIIT - gestion de bibliothèque.")
        while True:
            choix = console.menu("BiblioIIT - Menu principal", [
                ("1", "Livres"), ("2", "Exemplaires"), ("3", "Lecteurs"),
                ("4", "Prêts et retours"), ("5", "Réservations"),
                ("6", "Statistiques"), ("7", "Règles de prêt"), ("0", "Quitter")])
            if choix == "0":
                print("Au revoir !")
                return
            if choix in self.sous_menus:
                self.sous_menus[choix]()
            else:
                console.erreur("Choix invalide.")
