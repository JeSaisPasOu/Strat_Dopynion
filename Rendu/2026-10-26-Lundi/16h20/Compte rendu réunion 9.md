# **Compte rendu de réunion \- 9**

# **Recap fin de journée**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 26 octobre 2026  
* **Heure réunion** : 16h20  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour & Objectif de la séance**


* Bilan de la journée et mesure de la progression par rapport à la dernière session.  
* Retours sur les performances en compétition (classement et corrections de bugs).  
* Intégration des nouvelles cartes et des routes POST interactives dans la stratégie globale et analyse des points de blocage liés au passage en multi-parties simultanées pour demain.  
* Possibilité de mettre en place un système de logs structurés pour l'optimisation décisionnelle assistée par IA.

## **2\. Notes brutes** 

- amelioration comparé à la semaine derniere  
- nouvelle strategie qui nous a permit de monter dans le classement et reglage des problemes dans le code  
- reflechir nouvelle startegie en incorporant les nouvelles cartes actions vu aujourd'hui   
- premiere reunion, voir pour multi game et potentielle point de blocage  
- fichier texte par partie pour mieux l’analyser par une ia et donc avoir une meilleurs strategie 

## **3\. Résumé de la journée : Synthèse des acquis & Résultats** 

**3.1. Performances & Progression** 

* **Montée au classement :** L'ajustement de la stratégie de base et la résolution de plusieurs bugs bloquants dans le code ont permis un bond notable dans le classement général face aux autres équipes.  
* **Stabilité accrue :** Le comportement du bot est nettement plus robuste et fiable comparativement aux sessions de la semaine passée.

**3.2. Architecture Technique & Concurrence (Multi-parties)** 

Prévention sur :

* **Validation du mode simultané :** sur l'exécution concurrente de plusieurs parties lancées par l'arbitre.  
* **Points de vigilance :** des risques de blocage ( écrasement de variables globales, gestion des timeouts sur les nouvelles requêtes POST interactives). L'isolation stricte des contextes par `game_id` reste impérative.


**3.3. Évolution Stratégique & Nouvelles Cartes** 

* **Adaptation tactique :** Nécessité de faire évoluer le moteur de décision pour exploiter le catalogue étendu (Sorcière, Chambre du conseil, Recrue, Rivage lointain, Village agricole).  
* **Gestion des choix interactifs :** Prise en compte active des nouvelles routes POST (`trash`, `discard`, sélection d'acquisitions) pour épurer le deck et se défendre contre la distribution de Malédictions.


  
**3.4. Outillage & Analyse par IA (Data Logging)** 

* **Génération de logs dédiés :** Poossibilité de mettre en place d'un export au format texte/log dédié par partie (1 fichier par `game_id`).  
* **Objectif :** Disposer d'un historique complet du déroulé de chaque match pour permettre une analyse fine post-partie (identification des choix sous-optimaux, benchmarking des adversaires) et accélérer l'amélioration de la stratégie via IA.


## **4\. Questions restantes à clarifier avec le client** 

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## **5\. Décisions & Plan d'action** 

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Mettre en place les 7 nouveaux endpoints POST sur le serveur HTTP du bot  | Adam Alves / Guillaume Befre  | Prochaine séance  |
| Ajouter un validateur de sécurité vérifiant que la carte renvoyée appartient bien au payload reçu  | Adam Alves / Guillaume Befre  | Prochaine séance  |
| Valider le comportement du bot en conditions réelles contre l'arbitre officiel  | Guillaume Befre / Adam Alves  | Prochaine séance  |
| Simulateur local | Adam Alves | Fin de matinée (Finit) |
| Stratégie | Pierre Dejean | Fin de journée |
| Fonction carte action | Erwan Menard/Guillaume Befre/Adam Alves | Fin de journée |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre/Erwan Menard | Au fur et à mesure |

## 

## 

## 

## 

## 

## 

## 

## 

## **6\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

