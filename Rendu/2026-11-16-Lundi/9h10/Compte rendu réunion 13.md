# **Compte rendu de réunion \- 13**

# **Début de journée**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 16 novembre 2026  
* **Heure réunion** : 9h10  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour & Objectif de la séance**  

* Point sur le classement général du tournoi et l'évolution des performances.  
* Correction d'un bug d'arbitrage impactant la durée des parties à 2 joueurs.  
* Présentation en avant-première de 7 nouvelles cartes (déjà actives sur le serveur) et de leurs endpoints API associés.  
* Plan d'action immédiat pour creuser l'écart au classement.

## **2\. Notes brutes** 

- Bug, 8 cartes au lieu de 12 corrigé (parti qui finit plus tot)  
- Carte aventurier coute 6 cuivres. Prendre carte du deck jusqu’a 2 cartes tresore  
- carte cave coute 2 cuivres. \+ 1 action defausser autant de carte de notre main et piocher le meme nombre de carte discard\_comfirm\_from\_hand  
- festin coutre 4 cuivre. Doit jeter cette carte a la poubelle (a voir avec la note) choose carte to recive in the carte  
- Fortuner 3 cuivres, 2 cuivres en bon achat. Adversaire doit piocher jusqu’a tomber sur une malediction ou une victoire. embete les autres  
- Bibliotheque coute 5 cuivres, piocher jusqu’a avoir 5 cartes en main (soit la garder dans notre main soit defausser la carte. skiped carte recepcion in hand  
- mania coute 5 cuivres piocher autant de carte qu’on a de carte tresore  
- carte atelier coute 3 cuivre recevoir une carte jusqu’a 4 cuivres. (possible combinaison avec jardin) choose card to receved in this card   
- 

**3\. Réponses & Échanges**  

**3.1. Bilan Tournoi & Positionnement**

* **2ᵉ place au classement général :** Le bot s'est hissé à la 2ᵉ position ce matin, tandis que plusieurs équipes concurrentes rencontrent des difficultés techniques et reculent.  
* **Opportunité stratégique :** L'équipe est informée en premier de l'activation des nouvelles cartes, offrant un avantage décisif pour prendre de l'avance.

**3.2. Correctif d'Arbitrage**

* **Correction de la réserve :** Le bug qui allouait **12 cartes par pile** au lieu de **8** dans les configurations à 2 joueurs a été corrigé par l'arbitre.  
* **Impact sur le rythme de jeu :** Les piles (notamment les Provinces) s'épuisant plus vite, les parties à 2 joueurs se terminent plus rapidement. L'heuristique de bascule vers les points de victoire doit en tenir compte.

**3.3. Nouvelles Cartes Actives & Endpoints API Associés**   

| Carte | Coût (cuivre) | Fonction | Effet & Mécaniques |
| :---: | :---: | :---: | :---: |
| Aventurier *(Adventurer)*  | 6 | Géré par le serveur | Dévoile des cartes du deck jusqu'à obtenir **2 cartes Trésor** (ajoutées à la main) ; le reste est défaussé. *Règle de mélange :* Si le deck s'épuise, la défausse est remélangée **une seule fois** pour tenter de compléter les 2 Trésors (l'effet s'arrête si cela ne suffit toujours pas).  |
| Cave *(Cellar)*  | 2 | /confirm\_discard\_card\_from\_hand  | **\+1 Action**. Permet de défausser autant de cartes que souhaité de sa main pour en repiocher le même nombre. *Intérêt :* Idéal pour recycler les mains encombrées (Malédictions, Domaines).  |
| Festin *(Feast)*  | 4 | /choose\_card\_to\_receive\_in\_discard  | La carte est **écartée (Rebut)** après utilisation pour recevoir directement dans sa défausse une carte coûtant **jusqu'à 5 pièces**.  |
| Diseuse de bonne aventure *(Fortune Teller)*   | 3 | Automatique (adversaire) | • \+2 Pièces d'achat. • **Attaque :** Les adversaires dévoilent des cartes de leur deck jusqu'à tomber sur une carte **Victoire** ou **Malédiction**, qu'ils replacent sur le dessus de leur pioche (le reste est défaussé). |
| Bibliothèque *(Library)*   | 5  | /skip\_card\_reception\_in\_hand  | Pioche des cartes jusqu'à atteindre **7 cartes en main**. Pour chaque carte **Action** piochée durant cet effet, le joueur peut choisir de la conserver en main ou de l'écarter/défausser immédiatement  |
| Magnat *(Magnate)*  | 5 | Géré par le serveur | Permet de piocher **autant de cartes que l'on possède de cartes Trésor en main**. *Synergie :* Très puissant couplé à des cartes octroyant \+X Achat pour rentabiliser l'afflux de monnaie |
| Atelier *(Workshop)*  | 3 | /choose\_card\_to\_receive\_in\_discard  | Permet de recevoir directement dans sa défausse une carte coûtant **jusqu'à 4 pièces**. *Synergie :* Accélère le volume du deck (idéal en combinaison avec **Jardins**). |

## 

## **4\. Questions restantes à clarifier avec le client** 

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## **5\. Décisions & Plan d'action** 

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Implémenter / vérifier la gestion des 7 nouvelles cartes sur les endpoints existants (`confirm_discard_card_from_hand`, `choose_card_to_receive_in_discard`, `skip_card_reception_in_hand`)  | Adam Alves  | Fin de matinée |
| Coder la logique de décision pour **Cave** (défausser uniquement les cartes mortes : Malédictions, Domaines, Cuivres en fin de partie) et **Bibliothèque**  | Guillaume Befre | Fin de matinée |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre/Erwan Menard | Au fur et à mesure |

## **6\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

