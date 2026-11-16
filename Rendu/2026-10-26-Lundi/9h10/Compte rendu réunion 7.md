# Compte rendu de réunion - 7

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 26 octobre 2026
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

- Spécifications sur l'exécution des parties en simultané dès le lendemain (gestion multi-instances).
- Présentation et intégration de nouvelles cartes d'attaque, d'effet continu et de malus.
- Clarification définitive sur le reliquat de monnaie lors des achats multiples.

## Notes brutes

**Demain parties en simultané :**

- **Nouvelles cartes :**
  - Chambre du conseil : 5 Cuivres => +4 cartes, +1 achat ; quand on la joue, tous les adversaires piochent une carte
  - Malédiction : 0 Cuivre => compte pour -1 point de victoire
  - Au stock début de partie : 10 cartes Malédiction en fonction du nombre de personnes présentes dans la partie (éviter d’en recevoir)
  - Rivage lointain : 6 Cuivres => +2 cartes, +1 action, 1 Domaine et 2 points de victoire (10 comme les autres cartes)
  - Village agricole : 4 Cuivres => +2 actions, piocher jusqu’à avoir une carte Trésor ou Action
  - Recrue : 6 Cuivres => ne va pas dans la défausse, elle sort du jeu. Au début du tour, commencer avec +1 carte
  - La Sorcière : 5 Cuivres => piocher 2 cartes, tous les adversaires reçoivent une Malédiction de la réserve

## Réponses & Échanges

### Gestion Technique : Parties en Simultané

- **Multi-threading / Concurrence :** Dès demain, l'arbitre lancera plusieurs parties en parallèle sur le bot.
- **Architecture sans état global (Stateless) :** Le code ne doit pas reposer sur des variables globales uniques sous peine de mélanger les contextes de jeu. Toute la mémoire et la stratégie doivent être partitionnées et indexées strictement par identifiant de partie (`game_id`).

### Nouvelles Cartes du Pool (Attaques, Effets durables & Malus)

| Carte | Type | Coût (cuivre) | Effet & Mécaniques |
| :--- | :--- | :--- | :--- |
| Chambre du conseil (Council Room) | Action | 5 | +4 Cartes, +1 Achat. Tous les adversaires piochent immédiatement 1 carte. |
| Sorcière (Witch) | Action | 5 | +2 Cartes. Distribue immédiatement une Malédiction à chaque adversaire. |
| Village agricole (Farming Village) | Action | 4 | +2 Actions. Permet de révéler des cartes de la pioche jusqu'à trouver une carte Trésor ou Action (puis l'ajouter à la main). |
| Rivage lointain (Distant Shore) | Action / Victoire | 6 | +2 Cartes, +1 Action, +1 Domaine (Estate), +2 points de victoire. |
| Recrue (Hireling) | Action | 6 | Détruite. Confère +1 carte au début de chaque tour suivant jusqu'à la fin de la partie (commence avec 6 cartes en main). |
| Malédiction (Curse) | Malus | 0 | -1 Point de victoire. Réserve limitée au départ (calibrée selon le nombre de joueurs autour de la table, 10 par joueur présent dans la partie). |

### Précision de Règle : Dépense de Monnaie & Achats Multiples

Gestion du surplus : Si un joueur dispose de plus de monnaie que le coût d'une carte (ex. 3 cartes Argent générant 6 pièces pour un achat coûtant 5) :

- Le solde restant (1 pièce) reste utilisable durant le tour en cours **uniquement si** le joueur dispose d'un achat supplémentaire disponible (`+1 Achat`).
- Tout excédent d'argent non dépensé à la fin du tour est définitivement perdu (pas de report d'un tour sur l'autre).

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Vérifier et nettoyer le code pour isoler les états par `game_id` (prévention des conflits multi-parties) | Adam Alves | Ce soir |
| Intégrer les nouvelles cartes (Sorcière, Malédiction, Recrue...) dans le dictionnaire des cartes du bot | Guillaume Befre | Ce soir |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |