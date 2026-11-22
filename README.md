# BiblioIIT

Application console de gestion de bibliothèque, écrite en **Python 3** (bibliothèque standard uniquement) avec **SQLite** et une architecture **MVC**. Elle sert à numériser la gestion d'une vraie bibliothèque physique : livres, exemplaires, lecteurs, prêts, réservations et statistiques.

## Fonctionnalités

- **Livres** et **exemplaires** : ajout, liste, modification, suppression (chaque exemplaire a un code d'inventaire unique, une cote, un état *bon / abîmé / perdu* et une disponibilité).
- **Recherche** de livres par titre, auteur, ISBN ou catégorie (l'ISBN est facultatif et vérifié s'il est saisi).
- **Lecteurs** : inscription (numéro de carte unique, catégorie étudiant ou enseignant), suspension et levée de suspension.
- **Prêts** : emprunt, retour, renouvellement, liste des prêts en cours et des prêts en retard.
- **Réservations** avec file d'attente (premier arrivé, premier servi).
- **Statistiques** : livres les plus empruntés.
- **Règles de prêt** modifiables depuis le menu « Règles de prêt ».

## Lancement

Prérequis : Python 3.9 ou plus récent, aucune installation de paquet nécessaire.

```
python main.py
```

La base `biblioiit.db` est créée automatiquement, **vide**, dans le dossier du projet au premier lancement.
Pour utiliser un autre fichier de base, définissez la variable d'environnement `BIBLIOIIT_DB`.

## Règles

Règles par défaut (modifiables dans le menu « Règles de prêt ») :

| Catégorie  | Livres max | Durée   | Renouvellements | Validité de l'inscription |
|------------|-----------:|--------:|----------------:|---------------------------|
| Étudiant   | 2          | 15 jours | 1              | 1 an (365 jours)          |
| Enseignant | 3          | 30 jours | 1              | 1 an (365 jours)          |

Règles de gestion :

- **Prêt refusé** si : lecteur suspendu, limite de livres atteinte, lecteur ayant un prêt en retard, inscription expirée (ou exemplaire déjà emprunté, abîmé ou perdu).
- **File d'attente** : si un livre est réservé, les exemplaires disponibles sont réservés aux premiers de la file.
- **Retard** : au retour, le lecteur est suspendu pendant autant de jours que de jours de retard.
- **Renouvellement refusé** si : prêt en retard, livre réservé par un autre lecteur, maximum de renouvellements atteint. Un renouvellement ajoute la durée de prêt de la catégorie à l'échéance.
- **Suppression interdite** pour un lecteur, un exemplaire (ou un livre) ayant un historique de prêt.

## Architecture

Architecture MVC. Flux : **Vue -> Contrôleur -> Repository/Modèle -> Contrôleur -> Vue**. Les vues n'ont aucune logique métier : elles se limitent à l'affichage et à la saisie.

```
main.py               point d'entrée (assemble modèles, contrôleurs et vues)
utils.py              dates, validation d'ISBN, exception ErreurMetier
donnees_exemple.py    données d'exemple (lancé manuellement)
database/             connexion SQLite et création des tables
models/               objets métier (Livre, Exemplaire, Lecteur, Pret, Reservation, ReglePret)
repositories/         accès SQL, un fichier par table
controllers/          règles de gestion
views/                menus, affichage et saisie
```

Tables : `livre`, `exemplaire`, `lecteur`, `pret`, `reservation`, `regle_pret`.

## Données d'exemple (optionnel)

La base est vide au démarrage. Pour tester l'application avec des données fictives (10 livres, 19 exemplaires, 5 lecteurs), lancez **manuellement** :

```
python donnees_exemple.py
```

Le script n'est jamais exécuté automatiquement et refuse de s'exécuter si la base contient déjà des données. Pour repartir de zéro, supprimez le fichier `biblioiit.db`.
