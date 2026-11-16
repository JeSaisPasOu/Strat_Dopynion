# Compte rendu de réunion \- 7

# Début de journée

# Projet Compétition de Royaume

## Informations générales

* **Date :** 26 octobre 2026  
* **Heure réunion** : 9h10  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
  * Pierre Dejean  
  * Erwan Menard  
  * Guillaume Befre  
  * Adam Alves  
  * Client

## Ordre du jour & Objectif de la séance

* Spécifications sur l'exécution des parties en simultané dès le lendemain (gestion multi-instances).  
* Présentation et intégration de nouvelles cartes d'attaque, d'effet continu et de malus.  
* Clarification définitive sur le reliquat de monnaie lors des achats multiples.

## Notes brutes

Demain parties en simultané

- nouvelles cartes :   
  - chambre du conseilles 5 cuivres \=\> plus 4 cartes, plus 1 achat, quand on la joue, tous les adversaires pioche une carte  
  - malediction 0cuivre \=\> compte pour \-1 points de victoire   
  - au stock debut de parti, 10 cartes malediction en fonction du nombre de personne presente dans la partie (eviter d’en recevoir)  
  - rivage montain 6 cuivres \=\> plus 2 carte, plus 1 action, 1 domaine et 2 points de victoire (10 comme les autres cartes)  
  - village agricole 4 cuivres \=\> 2 actions, piocher jusqu’a avoir une carte tresore ou action  
  - recrue 6 cuivres \=\> Va pas dans la defausse, elle sort du jeu. Au debut du tour, commencer avec plus 1 carte   
  - La sorciere 5 cuivres \=\> piocher 2 cartes, adversaire recoivent (tous) une malediction de la reserve 


## Réponses & Échanges

### Gestion Technique : Parties en Simultané

* **Multi-threading / Concurrence :** Dès demain, l'arbitre lancera plusieurs parties en parallèle sur le bot.  
* **Architecture sans état global (Stateless) :** Le code ne doit pas reposer sur des variables globales uniques sous peine de mélanger les contextes de jeu. Toute la mémoire/stratégie doit être partitionnée et indexée strictement par identifiant de partie (game\_id).

### Nouvelles Cartes du Pool (Attaques, Effets durables & Malus)

| Carte | Type | Coût (cuivre) | Effet & Mécaniques |
| :---: | :---: | :---: | :---: |
| Chambre du conseil (council Room) | Action | 5 | \+4 Cartes \+1 Achat Tous les adversaires piochent immédiatement 1 carte |
| Sorcière (Witch) | Action | 5 | \+2 Cartes Distribue immediatement une carte à chaque adversaire |
| Village agricole (Farming Village) | Action | 4 | \+2 Actions Permet de révéler des cartes de la pioche jusqu'à trouver une carte Trésor ou Action (puis l'ajouter à la main).  |
| Rivage lointain (Distant Shore) | Action/ Victoire | 6 | \+2 Cartes \+1 Action \+1 Domaine (Estate) \+2 point de victoire |
| Recrue (Hireling/ Recrue) | Action | 6 | Detruite Confère \+1 carte au début de chaque tour suivant jusqu'à la fin de la partie. (commence avec 6 cartes en main) |
| Malédiction (Curse) | Malus | 0 | \-1 Point de victoire Réserve limitée au départ (calibrée selon le nombre de joueurs autour de la table, 10 par joueur présent dans la game).  |

### Précision de Règle : Dépense de Monnaie & Achats Multiples

Gestion du surplus : Si un joueur dispose de plus de monnaie que le coût d'une carte (ex. 3 cartes Argent générant 6 pièces pour un achat coûtant 5\) :

* Le solde restant (1 pièce) reste utilisable durant le tour en cours **uniquement si** le joueur dispose d'un achat supplémentaire disponible (+1 Achat).  
* Tout excédent d'argent non dépensé à la fin du tour est définitivement perdu (pas de report d'un tour sur l'autre).

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Vérifier et nettoyer le code pour isoler les états par game\_id (prévention des conflits multi-parties)  | Adam Alves  | Ce soir |
| Intégrer les nouvelles cartes (Sorcière, Malédiction, Recrue...) dans le dictionnaire des cartes du bot  | Guillaume Befre | Ce soir |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre/Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

