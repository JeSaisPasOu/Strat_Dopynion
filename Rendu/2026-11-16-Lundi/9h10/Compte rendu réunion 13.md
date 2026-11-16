# Compte rendu de réunion - 13

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 16 novembre 2026
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

- Point sur le classement général du tournoi et l'évolution des performances.
- Correction d'un bug d'arbitrage impactant la durée des parties à 2 joueurs.
- Présentation en avant-première de 7 nouvelles cartes (déjà actives sur le serveur) et de leurs endpoints API associés.
- Plan d'action immédiat pour creuser l'écart au classement.

## Notes brutes

- Bug : 8 cartes au lieu de 12 corrigé (parties qui finissent plus tôt)
- Carte Aventurier coûte 6 Cuivres : prendre des cartes du deck jusqu’à 2 cartes Trésor
- Carte Cave coûte 2 Cuivres : +1 action, défausser autant de cartes de notre main que voulu et piocher le même nombre de cartes (`confirm_discard_card_from_hand`)
- Festin coûte 4 Cuivres : doit jeter cette carte à la poubelle (`choose_card_to_receive_in_discard`)
- Diseuse de bonne aventure (`Fortune Teller`) coûte 3 Cuivres : +2 Cuivres en bonus d'achat, l'adversaire doit piocher jusqu’à tomber sur une Malédiction ou une Victoire (embête les autres)
- Bibliothèque coûte 5 Cuivres : piocher jusqu’à avoir 7 cartes en main (soit garder la carte Action en main, soit la défausser : `skip_card_reception_in_hand`)
- Magnat coûte 5 Cuivres : piocher autant de cartes qu’on a de cartes Trésor en main
- Carte Atelier coûte 3 Cuivres : recevoir une carte coûtant jusqu’à 4 Cuivres (possible combinaison avec Jardins : `choose_card_to_receive_in_discard`)

## Réponses & Échanges

### Bilan Tournoi & Positionnement

- **2ᵉ place au classement général :** Le bot s'est hissé à la 2ᵉ position ce matin, tandis que plusieurs équipes concurrentes rencontrent des difficultés techniques et reculent.
- **Opportunité stratégique :** L'équipe est informée en premier de l'activation des nouvelles cartes, offrant un avantage décisif pour prendre de l'avance.

### Correctif d'Arbitrage

- **Correction de la réserve :** Le bug qui allouait **12 cartes par pile** au lieu de **8** dans les configurations à 2 joueurs a été corrigé par l'arbitre.
- **Impact sur le rythme de jeu :** Les piles (notamment les Provinces) s'épuisant plus vite, les parties à 2 joueurs se terminent plus rapidement. L'heuristique de bascule vers les points de victoire doit en tenir compte.

### Nouvelles Cartes Actives & Endpoints API Associés

| Carte | Coût (cuivre) | Fonction | Effet & Mécaniques |
| :--- | :--- | :--- | :--- |
| Aventurier *(Adventurer)* | 6 | Géré par le serveur | Dévoile des cartes du deck jusqu'à obtenir **2 cartes Trésor** (ajoutées à la main) ; le reste est défaussé. *Règle de mélange :* Si le deck s'épuise, la défausse est remélangée **une seule fois** pour tenter de compléter les 2 Trésors (l'effet s'arrête si cela ne suffit toujours pas). |
| Cave *(Cellar)* | 2 | `/confirm_discard_card_from_hand` | **+1 Action**. Permet de défausser autant de cartes que souhaité de sa main pour en repiocher le même nombre. *Intérêt :* Idéal pour recycler les mains encombrées (Malédictions, Domaines). |
| Festin *(Feast)* | 4 | `/choose_card_to_receive_in_discard` | La carte est **écartée (Rebut)** après utilisation pour recevoir directement dans sa défausse une carte coûtant **jusqu'à 5 pièces**. |
| Diseuse de bonne aventure *(Fortune Teller)* | 3 | Automatique (adversaire) | **+2 Pièces d'achat**. **Attaque :** Les adversaires dévoilent des cartes de leur deck jusqu'à tomber sur une carte **Victoire** ou **Malédiction**, qu'ils replacent sur le dessus de leur pioche (le reste est défaussé). |
| Bibliothèque *(Library)* | 5 | `/skip_card_reception_in_hand` | Pioche des cartes jusqu'à atteindre **7 cartes en main**. Pour chaque carte **Action** piochée durant cet effet, le joueur peut choisir de la conserver en main ou de l'écarter/défausser immédiatement. |
| Magnat *(Magnate)* | 5 | Géré par le serveur | Permet de piocher **autant de cartes que l'on possède de cartes Trésor en main**. *Synergie :* Très puissant couplé à des cartes octroyant `+X Achat` pour rentabiliser l'afflux de monnaie. |
| Atelier *(Workshop)* | 3 | `/choose_card_to_receive_in_discard` | Permet de recevoir directement dans sa défausse une carte coûtant **jusqu'à 4 pièces**. *Synergie :* Accélère le volume du deck (idéal en combinaison avec **Jardins**). |

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Implémenter / vérifier la gestion des 7 nouvelles cartes sur les endpoints existants (`/confirm_discard_card_from_hand`, `/choose_card_to_receive_in_discard`, `/skip_card_reception_in_hand`) | Adam Alves | Fin de matinée |
| Coder la logique de décision pour **Cave** (défausser uniquement les cartes mortes : Malédictions, Domaines, Cuivres en fin de partie) et **Bibliothèque** | Guillaume Befre | Fin de matinée |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |