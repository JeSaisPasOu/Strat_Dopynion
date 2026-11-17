# Compte rendu de réunion - 16

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 17 novembre 2026
- **Heure réunion :** 9h10
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Point sur le classement général et l'évolution des scores Elo (bot officiel vs bot de test).
- Présentation de **5 nouvelles cartes** d'épuration et de transformation (déjà actives en jeu) et de leurs endpoints API associés.
- Définition des bonnes pratiques d'observation post-déploiement et répartition des tâches de la matinée.

## Notes brutes

- Nouvelles cartes auj
- FAVORIE chapelle coute 2 cuivres. Permet d'ecarter 4 cartes de notre main de notre choix. Appelle 4 fois confirme trash card from hand. Permet de cycler plus rapidement sa main
- Mine coute 5 cuivres. Elle permet d'ecarter une carte tresore de notre main pour recevoir 3 cuivres en plus. Dans la limite des stock disponibles trash money card for better mony card 
- Preteur sur gage coute 4 cuivres Permet d'ecarter un cuivre de notre main et recevoir un bon acaht de 3 cuivres confirme trash card from hand
- Renovation coute 4 cuivrs ecarter une carte de notre main remplacer vers des cartes actions. trash card from hand Ensuite l'arbitre va appeler choose (voir note audio)
- troc coute 5 cuivres + 1 action, +1 cartes supp et remettre une carte action de notre main dans la reserve et recevoir en echange une carte action qui coute 5 cuivres. Peux modifier l'issu de la partie

## Réponses & Échanges

### Bilan Tournoi & Positionnement

- **Scores actuels :** Notre bot officiel totalise **1 198 points**, tandis que le bot officieux / de test (**Alves**), lancé avant la fin de journée d'hier, atteint **1 326 points**.
- **Volatilité du classement & Règle d'observation :** Les scores évoluent très rapidement (des progressions d'environ 400 points d'Elo en 1h30 ont été observées la veille). Il est indispensable de laisser tourner le bot **10 à 15 minutes minimum** après chaque déploiement pour évaluer l'impact réel des modifications.

### Nouvelles Cartes Actives & Endpoints API Associés

Toutes ces cartes sont déjà actives sur le serveur de compétition :

| Carte | Coût (cuivre) | Fonction / Endpoint | Effet & Mécaniques |
| :--- | :---: | :--- | :--- |
| **Chapelle** *(Chapel)* | 2 | `/confirm_trash_card_from_hand` *(jusqu'à 4 appels)* | Permet d'écarter (Rebut) jusqu'à **4 cartes** de sa main au choix. *Intérêt (carte prioritaire) :* Accélère radicalement le cyclage du deck dès le début de partie en éliminant Domaines et Cuivres. |
| **Mine** | 5 | `/trash_money_card_for_better_money_card` | Permet d'écarter une carte **Trésor** de sa main pour recevoir un Trésor coûtant **jusqu'à 3 pièces de plus** (dans la limite des stocks disponibles : Cuivre $\rightarrow$ Argent, Argent $\rightarrow$ Or). |
| **Prêteur sur gages** *(Moneylender)* | 4 | `/confirm_trash_card_from_hand` | Permet d'écarter un **Cuivre** de sa main en échange d'un bon d'achat de **+3 pièces** pour le tour en cours. |
| **Rénovation** *(Remodel)* | 4 | `/trash_card_from_hand` puis `/choose_card_to_receive_in_discard` | Permet d'écarter n'importe quelle carte de sa main pour recevoir directement dans sa défausse une carte coûtant **jusqu'à 2 pièces de plus**. |
| **Troc** *(Swap)* | 5 | Interaction réserve *(remise + échange)* | **+1 Action, +1 Carte**. Permet de remettre une carte Action de sa main dans la réserve (magasin) pour recevoir en échange une carte Action coûtant **jusqu'à 5 pièces**. *Impact stratégique :* Peut retarder la fin de partie en réapprovisionnant une pile vide. |

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Vérifier et adapter la gestion des 5 nouvelles cartes sur les endpoints existants (`/confirm_trash_card_from_hand`, `/trash_card_from_hand`, `/choose_card_to_receive_in_discard`, `/trash_money_card_for_better_money_card`) et l'interaction **Troc** | Adam Alves / Guillaume Befre | Fin de matinée |
| Implémenter la logique d'épuration prioritaire pour **Chapelle** (écarter Malédictions, Domaines et Cuivres en début de partie) et **Prêteur sur gages** | Guillaume Befre / Adam Alves | Fin de matinée |
| Ajuster le scoring d'achat (priorisation de **Chapelle** en ouverture) et analyser les performances après 15 min de run | Pierre Dejean / Erwan Menard | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |