# **Compte rendu de réunion \- 11**

# **Mi-journée**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 27 octobre 2026  
* **Heure réunion** : 14h20  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour & Objectif de la séance**  

* Spécification du nouvel endpoint d'arbitrage dédié à l'amélioration de trésors.  
* Analyse de la mécanique de transformation (effet classique type *Mine* de Dominion : écarter un trésor pour en acquérir un supérieur).  
* Règles de formatage du payload et contraintes de réponse.


## **2\. Notes brutes** 

- trash\_money\_card\_for\_better\_money\_card \=\> quel carte tresore enlever de sa main pour avoir des cartes argent declanché par des cartes actions  
- money\_hand (voir enregistrement)   
- 

## 

## **3\. Réponses & Échanges**  

**3.1. Nouvel Endpoint POST**   

Cet endpoint est déclenché par l'arbitre lors de l'activation d'une carte Action spécifique permettant d'améliorer directement la qualité de ses trésors.

* **Mécanique de la carte :**  
  * Le joueur écarte (envoie au Rebut) une carte Trésor présente dans sa main.  
  * En contrepartie, il gagne une carte Trésor supérieure coûtant jusqu'à 3 pièces de plus que la carte écartée.  
  * *Rappel des coûts des Trésors :*  
    * Écarter un Cuivre (coût 0\) $\rightarrow$ permet de récupérer un Argent (coût 3).  
    * Écarter un Argent (coût 3\) $\rightarrow$ permet de récupérer un Or (coût 6).  
* **Payload reçu de l'arbitre :**  
  * Un objet JSON transmettant notamment la liste des cartes trésors disponibles dans la main du joueur via la propriété money\_in\_hand (ou money\_hand).  
* **Format de réponse attendu du bot :**  
  * Un JSON contenant la clé decision (ou le nom de la carte trésor ciblée) :  
    * Exemple : {"decision": "\<nom\_carte\_tresor\>"} *(ex. "Copper" ou "Silver")*.  
  * Sécurité : La carte désignée doit impérativement faire partie de la liste reçue dans money\_in\_hand pour éviter toute pénalité ou élimination pour coup invalide.


**3.2. Intérêt Stratégique & Priorisation**  

**Double avantage (Épuration \+ Richesse) :** Cette mécanique accélère considérablement le deck en supprimant les *Cuivres* (dépollution) tout en injectant des *Argents* ou des *Ors* sans consommer d'achat de tour.  
**Heuristique recommandée :**

1. Si un **Argent** est en main et qu'il reste de l'Or en réserve $\rightarrow$ Écarter *Argent* pour récupérer *Gold*.  
2. Sinon, si un **Cuivre** est en main et qu'il reste de l'Argent en réserve $\rightarrow$ Écarter *Copper* pour récupérer *Silver*.  
3. Ne pas cibler l'*Or* (sauf si une carte Trésor supérieure existe dans les règles, ce qui n'est pas le cas ici).

## **4\. Questions restantes à clarifier avec le client** 

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?  
4. Est ce que c’est à nous de compter les points de victoire des jardins à la fin de la partie? Ou si c’est l’arbitre? Réponse : l’arbitre compte les points en fin de partie. Mais ca peut être intéressant de compter quand même le nombre de carte pour la stratégie.

## **5\. Décisions & Plan d'action** 

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Implémenter l'endpoint POST `/skip_card_reception_in_hand` avec réponse booléenne stricte  Adapter la boucle de réponse sur `/discard_card_from_hand` pour gérer les attaques répétées de la Milice  Implémenter la route POST `/trash_money_card_for_better_money_card`  | Adam Alves  | Ce soir |
| Ajouter un contrôle de sécurité vérifiant la présence effective de la carte dans `money_in_hand`  | Adam Alves  | Ce soir |
| Intégrer l'évaluation de la carte Jardins dans la stratégie d'achat (détection des decks massifs)  Écrire la logique d'arbitrage de sélection (Silver $\rightarrow$ Gold prioritaire, sinon Copper $\rightarrow$ Silver)  | Guillaume Befre | Ce soir |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre/Erwan Menard | Au fur et à mesure |

## **6\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

note reunion : jour 4 fin aprem 

- amélioration de la stratégie   
- achat des cartes avec des scores pour acheter les meilleurs cartes possibles et donc les meilleurs decisions  
- points de victoire bas au debut car pas trop besoin  
- penser à mettre en place un systeme de statistique pour ameliorer notre strategie  
- bucheron et jardin peu utilisé  
- sorcière, recrue, village bcp utilisé  
- detection nb de joueur pour fin de partie (adapter la start en fonction du nb de joueur qu’il reste)  
- 