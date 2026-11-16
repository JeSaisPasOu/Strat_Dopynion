# **Compte rendu de réunion \- 1**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 7 octobre 2026  
* **Heure réunion** : 10h40  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour / Sujet réel**

Clarification des règles fondamentales et des spécifications techniques de la compétition :

* Critères de fin de partie et élimination.  
* Structure du deck, composition de départ et zones de jeu.  
* Composition de la réserve (magasin) et rôle de l'arbitre.  
* Livrables techniques immédiats.

Questions qu’il reste à poser : 

- Qu’est ce qui termine une partie: Objectifs ? Jeu cartes finis ? Nombre de tours ?  
- Est ce qu’il faut des cartes obligatoires pour tout les royaumes du jeu ? A t on des cartes personnalisé selon le royaume ? Si oui à tes cartes en têtes qu’il souhaite. Si oui a t il commencer à réfléchir à une ligne directionnel de la stratégie.  
- Quelles sont les limites du nombre de carte jouable par tour ?  
- Y a t il des malus à travers des intempéries, maladie qui pénalise notre royaume ?  
- Peut on attaquer les autres royaume ?  
- Possibilité de faire des alliances entre les royaumes?

## 

## **2\. Notes brutes** 

- la partie se termine quand (tous les joueurs fin de partie pour tous les joueurs)  
- possibilité d’acheté des cartes provinces dans la boutiques (critère 1 de fin de partie)  
- 3 piles du magazin (reserve) vide, ca met fin à la partie (critère 2\)  
- 150 tours de jeux (critère 3\)  
- si on fa	it un truc pas autorisé, on est eliminé de la partie 

- démarrage ressources : 7 cuivres, 3 domaines (carte point de victoire) (l’arbitre va les mélanger)   
- ratio de monnaie  
- deck, main et défausse (à moi) et le rebut (poubelle) et magasin (pile commun à tous les joueurs  
- a la fin du tour, on récupère 5 cartes  
- peut être carte spéciale (carte action)  
- fin de journée, mettre en place le serveur http pour rentrer dans la compétition (template par défaut passer son tour)  
- https\://dopynion-template.lecalamar.fr (voir photo adam)  
- compter les points : regarde l’ensemble des cartes   
- L'arbitre va décider des cartes présentes dans la réserve (60 cartes cuivres, 40 argents et 30 or), cartes point de victoire 12 carte points de victoire si ya 3 ou 4 royaume sinon 8 pour 2 joueurs.)

## **3\. Réponses & Échanges**

**3.1. Conditions de Fin de Partie & Pénalités**

Une partie prend fin immédiatement pour l'ensemble des joueurs dès qu'au moins l'un des trois critères suivants est validé :

1. **Épuisement des cartes victoires (provinces ou autre)** dans la boutique.  
2. **Épuisement de 3 piles quelconques** de la réserve (magasin).  
3. **Atteinte de la limite de 150 tours**.

> **Règle d'arbitrage / Disqualification :** Toute action non autorisée ou coup illégal entraîne l'élimination immédiate du joueur de la partie.

> 

### **3.2. Espaces de Jeu & Gestion du Tour**

* **Zones personnelles du joueur :**  
  * **Deck (Pioche) :** Pioche personnelle.  
  * **Main :** Cartes en main (complétée à **5 cartes** à la fin de chaque tour, peut varier en fonction du jeu).  
  * **Défausse :** Cartes jouées ou défaussées.  
  * Si plus de cartes dans le deck, l’arbitre mélange les cartes de la défausse et les replace dans le deck.  
* **Zones communes :**  
  * **Magasin (Réserve) :** Piles de cartes accessibles à l'achat par tous les joueurs.  
  * **Rebut (Poubelle) :** Zone commune pour les cartes retirées définitivement du jeu.  
* **Comptage des points :** Le décompte final prend en compte l'ensemble des cartes possédées (Deck \+ Main \+ Défausse).

### **3.3. Configuration Initiale & Composition de la Réserve**

* **Deck de départ d'un joueur (10 cartes mélangées par l'arbitre) :**  
  * $7\times$ Cuivres (Monnaie)  
  * $3\times$ Domaines (Points de victoire)  
* **Configuration de la Réserve (gérée par l'arbitre) :**  
  * **Cartes Trésor :**  
    * Cuivre : 60 cartes  
    * Argent : 40 cartes  
    * Or : 30 cartes

		Ratio entre les différents niveaux de trésors. (A définir avec le client)

**Cartes point de Victoire :**

* 2 joueurs : 8 cartes points de victoire  
  * 3 ou 4 royaum je es : 12 cartes points de victoire  
  * **Cartes Action :** à approfondir prochaine réunion, pas encore très clair  
    * Possibilité d'intégrer des cartes spéciales selon la configuration retenue par l'arbitre.

### **3.4. Aspect Technique & Infrastructure**

* **Serveur HTTPS du Bot :** Doit être opérationnel d'ici la fin de journée pour inscrire l'équipe à la compétition et gagner des points face aux autres équipes.  
* **Comportement initial :** Démarrer avec le comportement par défaut (passer son tour).  
* **Ressource technique :** Template disponible à l'adresse suivante : [https\://dopynion-template.lecalamar.fr](https://dopynion-template.lecalamar.fr).

## **4\. Décisions & Actions à Mener**

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Configuration hébergeur web  | Guillaume Befre | Fin de journée |
| Mise en place de l’api | Adam Alves | Fin de journée |
| Création du repository github | Pierre Dejean | Immédiat |
| Déployer le serveur HTTP avec le template de base (*passer son tour*) | Adam Alves | Fin de journée |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure |

## 

## 

## 

## 

## 

## 

## 

## 

## **5\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

## 