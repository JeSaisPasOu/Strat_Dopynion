# Compte rendu de réunion - 11

## Mi-journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 27 octobre 2026
- **Heure réunion :** 14h20
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Spécification du nouvel endpoint d'arbitrage dédié à l'amélioration de trésors.
- Analyse de la mécanique de transformation (effet classique type *Mine* de Dominion : écarter un trésor pour en acquérir un supérieur).
- Règles de formatage du payload et contraintes de réponse.

## Notes brutes

- `trash_money_card_for_better_money_card` => quelle carte Trésor enlever de sa main pour avoir des cartes Argent, déclenché par des cartes Action
- `money_hand` (voir enregistrement)

## Réponses & Échanges

### Nouvel Endpoint POST

Cet endpoint est déclenché par l'arbitre lors de l'activation d'une carte Action spécifique permettant d'améliorer directement la qualité de ses trésors.

- **Mécanique de la carte :**
  - Le joueur écarte (envoie au Rebut) une carte Trésor présente dans sa main.
  - En contrepartie, il gagne une carte Trésor supérieure coûtant jusqu'à 3 pièces de plus que la carte écartée.
  - *Rappel des coûts des Trésors :*
    - Écarter un Cuivre (coût 0) $\rightarrow$ permet de récupérer un Argent (coût 3).
    - Écarter un Argent (coût 3) $\rightarrow$ permet de récupérer un Or (coût 6).
- **Payload reçu de l'arbitre :**
  - Un objet JSON transmettant notamment la liste des cartes Trésor disponibles dans la main du joueur via la propriété `money_in_hand` (ou `money_hand`).
- **Format de réponse attendu du bot :**
  - Un JSON contenant la clé `decision` (le nom de la carte Trésor ciblée) :
    - Exemple : `{"decision": "<nom_carte_tresor>"}` *(ex. `"Copper"` ou `"Silver"`)*.
  - **Sécurité :** La carte désignée doit impérativement faire partie de la liste reçue dans `money_in_hand` pour éviter toute pénalité ou élimination pour coup invalide.

### Intérêt Stratégique & Priorisation

**Double avantage (Épuration + Richesse) :** Cette mécanique accélère considérablement le deck en supprimant les *Cuivres* (dépollution) tout en injectant des *Argents* ou des *Ors* sans consommer d'achat de tour.

**Heuristique recommandée :**

1. Si un **Argent** est en main et qu'il reste de l'Or en réserve $\rightarrow$ Écarter *Silver* pour récupérer *Gold*.
2. Sinon, si un **Cuivre** est en main et qu'il reste de l'Argent en réserve $\rightarrow$ Écarter *Copper* pour récupérer *Silver*.
3. Ne pas cibler l'*Or* (sauf si une carte Trésor supérieure existe dans les règles, ce qui n'est pas le cas ici).

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?
4. **Décompte des Jardins :** Est-ce à nous de compter les points de victoire des Jardins à la fin de la partie ou à l’arbitre ?
   - *Réponse :* L’arbitre compte les points en fin de partie, mais il reste intéressant de compter le nombre de cartes de notre côté pour orienter la stratégie.

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Implémenter la route POST `/trash_money_card_for_better_money_card` et ajouter le contrôle de sécurité sur `money_in_hand` | Adam Alves | Ce soir |
| Écrire la logique d'arbitrage de sélection (`Silver` $\rightarrow$ `Gold` prioritaire, sinon `Copper` $\rightarrow$ `Silver`) | Guillaume Befre | Ce soir |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |