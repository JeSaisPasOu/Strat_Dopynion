# Compte rendu de réunion - 1

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 7 octobre 2026
- **Heure réunion :** 10h40
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour / Sujet réel

Clarification des règles fondamentales et des spécifications techniques de la compétition :

- Critères de fin de partie et élimination.
- Structure du deck, composition de départ et zones de jeu.
- Composition de la réserve (magasin) et rôle de l'arbitre.
- Livrables techniques immédiats.

**Questions qu’il reste à poser :**

- Qu’est-ce qui termine une partie : Objectifs ? Jeu de cartes fini ? Nombre de tours ?
- Est-ce qu’il faut des cartes obligatoires pour tous les royaumes du jeu ? A-t-on des cartes personnalisées selon le royaume ? Si oui, a-t-il des cartes en tête qu’il souhaite ? Si oui, a-t-il commencé à réfléchir à une ligne directionnelle de la stratégie ?
- Quelles sont les limites du nombre de cartes jouables par tour ?
- Y a-t-il des malus à travers des intempéries ou des maladies qui pénalisent notre royaume ?
- Peut-on attaquer les autres royaumes ?
- Possibilité de faire des alliances entre les royaumes ?

## Notes brutes

- La partie se termine quand (fin de partie pour tous les joueurs)
- Possibilité d’acheter des cartes Provinces dans la boutique (critère 1 de fin de partie)
- 3 piles du magasin (réserve) vides, ça met fin à la partie (critère 2)
- 150 tours de jeu (critère 3)
- Si on fait un truc pas autorisé, on est éliminé de la partie
- Démarrage ressources : 7 Cuivres, 3 Domaines (carte point de victoire) (l’arbitre va les mélanger)
- Ratio de monnaie
- Deck, main et défausse (à moi), le rebut (poubelle) et magasin (pile commune à tous les joueurs)
- À la fin du tour, on récupère 5 cartes
- Peut-être carte spéciale (carte action)
- Fin de journée, mettre en place le serveur HTTP pour rentrer dans la compétition (template par défaut : passer son tour)
- https://dopynion-template.lecalamar.fr (voir photo Adam)
- Compter les points : regarde l’ensemble des cartes
- L'arbitre va décider des cartes présentes dans la réserve (60 cartes Cuivre, 40 Argent et 30 Or), cartes point de victoire : 12 cartes points de victoire s'il y a 3 ou 4 royaumes, sinon 8 pour 2 joueurs.

## Réponses & Échanges

### Conditions de Fin de Partie & Pénalités

Une partie prend fin immédiatement pour l'ensemble des joueurs dès qu'au moins l'un des trois critères suivants est validé :

1. **Épuisement des cartes Victoire (Provinces ou autre)** dans la boutique.
2. **Épuisement de 3 piles quelconques** de la réserve (magasin).
3. **Atteinte de la limite de 150 tours**.

> **Règle d'arbitrage / Disqualification :** Toute action non autorisée ou coup illégal entraîne l'élimination immédiate du joueur de la partie.

### Espaces de Jeu & Gestion du Tour

- **Zones personnelles du joueur :**
  - **Deck (Pioche) :** Pioche personnelle.
  - **Main :** Cartes en main (complétée à **5 cartes** à la fin de chaque tour, peut varier en fonction du jeu).
  - **Défausse :** Cartes jouées ou défaussées.
  - Si plus de cartes dans le deck, l’arbitre mélange les cartes de la défausse et les replace dans le deck.
- **Zones communes :**
  - **Magasin (Réserve) :** Piles de cartes accessibles à l'achat par tous les joueurs.
  - **Rebut (Poubelle) :** Zone commune pour les cartes retirées définitivement du jeu.
- **Comptage des points :** Le décompte final prend en compte l'ensemble des cartes possédées (Deck + Main + Défausse).

### Configuration Initiale & Composition de la Réserve

- **Deck de départ d'un joueur (10 cartes mélangées par l'arbitre) :**
  - $7\times$ Cuivres (Monnaie)
  - $3\times$ Domaines (Points de victoire)
- **Configuration de la Réserve (gérée par l'arbitre) :**
  - **Cartes Trésor :**
    - Cuivre : 60 cartes
    - Argent : 40 cartes
    - Or : 30 cartes
    - *Ratio entre les différents niveaux de trésors (à définir avec le client).*
  - **Cartes Point de Victoire :**
    - 2 joueurs : 8 cartes points de victoire
    - 3 ou 4 royaumes : 12 cartes points de victoire
  - **Cartes Action :** à approfondir à la prochaine réunion, pas encore très clair.
    - Possibilité d'intégrer des cartes spéciales selon la configuration retenue par l'arbitre.

### Aspect Technique & Infrastructure

- **Serveur HTTPS du Bot :** Doit être opérationnel d'ici la fin de journée pour inscrire l'équipe à la compétition et gagner des points face aux autres équipes.
- **Comportement initial :** Démarrer avec le comportement par défaut (passer son tour).
- **Ressource technique :** Template disponible à l'adresse suivante : [https://dopynion-template.lecalamar.fr](https://dopynion-template.lecalamar.fr).

## Décisions & Actions à Mener

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Configuration hébergeur web | Guillaume Befre | Fin de journée |
| Mise en place de l’API | Adam Alves | Fin de journée |
| Création du repository GitHub | Pierre Dejean | Immédiat |
| Déployer le serveur HTTP avec le template de base (*passer son tour*) | Adam Alves | Fin de journée |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |