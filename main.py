"""Point d'entrée de BiblioIIT : python main.py"""
import sys

from controllers.exemplaire_controller import ExemplaireController
from controllers.lecteur_controller import LecteurController
from controllers.livre_controller import LivreController
from controllers.pret_controller import PretController
from controllers.regle_controller import RegleController
from controllers.reservation_controller import ReservationController
from controllers.statistique_controller import StatistiqueController
from database.connexion import get_connection
from database.schema import creer_tables
from views.lecteur_view import LecteurView
from views.livre_view import ExemplaireView, LivreView
from views.menu_principal_view import MenuPrincipalView
from views.pret_view import PretView
from views.regle_view import RegleView, StatistiqueView
from views.reservation_view import ReservationView


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    connexion = get_connection()
    creer_tables(connexion)

    livres = LivreController(connexion)
    exemplaires = ExemplaireController(connexion)
    menu = MenuPrincipalView(
        LivreView(livres, exemplaires),
        ExemplaireView(exemplaires),
        LecteurView(LecteurController(connexion)),
        PretView(PretController(connexion)),
        ReservationView(ReservationController(connexion)),
        StatistiqueView(StatistiqueController(connexion)),
        RegleView(RegleController(connexion)))
    try:
        menu.executer()
    except (KeyboardInterrupt, EOFError):
        print("\nAu revoir !")
    finally:
        connexion.close()


if __name__ == "__main__":
    main()
