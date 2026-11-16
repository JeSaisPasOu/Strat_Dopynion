# **Compte rendu de réunion \- 12**

# **Fin-journée**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 27 octobre 2026  
* **Heure réunion** : 16h30  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour & Objectif de la séance**  

* Bilan de la journée et refonte de l'algorithme de décision d'achat (système de scoring).  
* Analyse des retours d'expérience sur l'utilisation réelle des cartes en match.  
* Adaptation dynamique de la stratégie selon le nombre de joueurs actifs en cours de partie.  
* Conception d'un outil de statistiques post-partie pour piloter l'optimisation du bot.


## **2\. Notes brutes** 

## **3\. Réponses & Échanges**  

**3.1. Refonte de la Stratégie : Système de Scoring des Cartes**    

* **Scoring dynamique :** Remplacement des règles d'achat rigides par une attribution de scores (poids) pour chaque carte disponible au marché, permettant au bot d'évaluer et de sélectionner la meilleure opportunité à chaque tour.

* **Pondération temporelle des Points de Victoire :** Attribution d'un score volontairement **faible en début de partie** aux cartes Victoire (*Domaine*, *Duché*) afin de ne pas polluer la main et de privilégier la montée en puissance économique et les moteurs d'actions.

**3.2. Retour d'expérience sur les Cartes (Méta-analyse)**  
    
**Cartes à forte valeur ajoutée (très utilisées et performantes) :**

* **Sorcière** : très efficace pour ralentir simultanément les decks adverses via les *Malédictions*.  
* **Recrue** : avantage décisif sur la durée grâce au gain passif de `+1 carte` à chaque début de tour.  
* **Village** : pilier indispensable pour fluidifier l'enchaînement des actions.

**Cartes sous-exploitées (faible rentabilité constatée) :**

* **Bûcheron** et **Jardins** : peu achetés et peu rentables dans la configuration actuelle du moteur de jeu du bot ; leur poids dans le scoring d'achat est donc revu à la baisse.

**3.3. Retour d'expérience sur les Cartes (Méta-analyse)**

* **Détection en temps réel :** Prise en compte dynamique du nombre de joueurs actifs dans la partie (notamment en cas d'élimination d'un adversaire en cours de match).

* **Ajustement de fin de partie :** L'anticipation de l'épuisement des piles (Provinces ou 3 piles vides) et le déclenchement du « rush final » vers les points de victoire s'adaptent automatiquement au nombre de participants restants.

**3.4. Retour d'expérience sur les Cartes (Méta-analyse)**

* **Mise en place d'un module de statistiques :** Décision de développer un outil d'agrégation de données à partir des logs de parties (taux d'achat par carte, fréquence de victoire, durée moyenne des matchs, causes d'élimination adverses).  
* **Objectif :** Objectiver les choix d'équilibrage du scoring et affiner les seuils de décision entre chaque session de tournoi.

## **4\. Questions restantes à clarifier avec le client** 

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## **5\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

