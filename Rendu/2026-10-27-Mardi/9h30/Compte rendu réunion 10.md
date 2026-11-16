# Compte rendu de réunion - 10

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 27 octobre 2026
- **Heure réunion :** 9h30
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Point de situation sur le classement du tournoi et la stabilisation des scores.
- Spécifications et intégration de 5 nouvelles cartes (Attaque, Économie alternative et Condition de victoire).
- Adaptation technique du bot : gestion de la défausse en boucle (Milice) et implémentation du nouvel endpoint interactif `/skip_card_reception_in_hand`.

## Notes brutes

- Bandit => 5 Cuivres, reçoit un Or une fois joué. Et piocher 3 cartes : si une carte piochée est Trésor, les autres sont défaussées (30 Or en stock et pas de compensation en Argent)
- Bureaucrate => 4 Cuivres, recevoir 1 Argent qui va dans le deck et enlever une carte Victoire de la main adverse vers sa pioche
- Chancelier => 3 Cuivres, reçoit un bonus d'achat de 2 Cuivres et possibilité de défausser notre deck (avec la commande vue hier)
- Jardins => 4 Cuivres, 1 point de victoire pour 10 cartes dans notre jeu
- Milice => 4 Cuivres, bonus d'achat de 2 Cuivres et tous les adversaires doivent défausser jusqu’à ce qu’il n’y ait plus que 3 cartes. Possiblement contrer avec la Recrue (`discard_card_from_hand`)
- `skip_card_reception_in_hand` : choisir si oui ou non on veut ignorer l’ajout de cette carte dans notre main

## Réponses & Échanges

### Nouvelles Cartes du Pool (Attaques, Effets durables & Malus)

| Carte | Type | Coût (cuivre) | Effet & Mécaniques |
| :--- | :--- | :--- | :--- |
| Bandit | Action / Attaque | 5 | **Gain personnel :** +1 Or (qui rejoint la défausse ; attention, stock limité à 30 Or sans compensation en Argent). **Attaque :** Révèle les 2 ou 3 premières cartes du deck de chaque adversaire, détruit/écarte le trésor le plus puissant (hors Cuivre) et défausse le reste. |
| Bureaucrate *(Bureaucrat)* | Action / Attaque | 4 | **Gain personnel :** +1 Argent placé directement sur le dessus de la pioche (`deck`). **Attaque :** Oblige chaque adversaire à révéler une carte Victoire de sa main pour la reposer sur le dessus de sa pioche (ralentissant son prochain tour). |
| Chancelier *(Chancellor)* | Action | 3 | **Économie :** Accorde +2 Pièces d'achat pour le tour. **Contrôle de pioche :** Déclenche la possibilité de défausser immédiatement l'intégralité de son deck pour forcer un remélange (via l'endpoint `/confirm_discard_deck`). |
| Jardins *(Gardens)* | Victoire | 4 | **Condition de PV :** +1 point de Victoire pour chaque tranche de 10 cartes possédées dans le deck total à la fin de la partie. *Synergie :* Incite à accumuler un très grand nombre de cartes (notamment en achetant massivement des Cuivres à coût 0). |
| Milice *(Militia)* | Action / Attaque | 4 | **Économie :** Accorde +2 Pièces d'achat pour le tour. **Attaque majeure :** Contraint tous les adversaires à défausser des cartes de leur main jusqu'à n'en conserver **que 3 en main** (au lieu de 5). |

### Évolutions Techniques & Nouveaux Endpoints HTTP

**Gestion de l'attaque Milice (`/discard_card_from_hand`) :**

- Lorsque la Milice est jouée contre nous, l'arbitre appelle la route POST `/discard_card_from_hand` **en boucle** jusqu'à ce que la main descende à 3 cartes.
- *Stratégie de réponse :* Prioriser la défausse des cartes « mortes » en main (Domaines, puis Cuivres si possible). Noter que la carte Recrue peut amortir cette perte en début de tour grâce à sa pioche continue.

**Nouvel endpoint POST : `/skip_card_reception_in_hand`**

- **Contexte :** Appelé lorsqu'un effet propose ou force l'ajout d'une carte directement dans notre main.
- **Payload reçu de l'arbitre :** Objet JSON contenant le nom de la carte concernée (`card_name`) et la main actuelle (`hand`).
- **Réponse attendue du bot :** Un booléen JSON strict :
  - `{"decision": true}` : Accepte d'ignorer / refuser la carte (ne pas la mettre en main).
  - `{"decision": false}` : Accepte l'ajout de la carte dans la main.
- *Règle :* Toujours renvoyer un booléen JSON natif (`true` / `false` sans guillemets).

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?
4. **Décompte des Jardins :** Est-ce à nous de compter les points de victoire des Jardins à la fin de la partie ou à l’arbitre ?
   - *Réponse :* L’arbitre compte les points en fin de partie, mais il reste intéressant de compter le nombre de cartes de notre côté pour orienter la stratégie.

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Implémenter l'endpoint POST `/skip_card_reception_in_hand` avec réponse booléenne stricte et adapter la boucle sur `/discard_card_from_hand` (Milice) | Adam Alves | Ce soir |
| Intégrer l'évaluation de la carte Jardins dans la stratégie d'achat (détection des decks massifs) | Guillaume Befre | Ce soir |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |