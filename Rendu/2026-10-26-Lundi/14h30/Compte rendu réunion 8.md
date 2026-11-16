# **Compte rendu de réunion \- 8**

# **Mi journée**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 26 octobre 2026  
* **Heure réunion** : 14h30  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour & Objectif de la séance**  

* Spécification des nouvelles interactions synchrones avec l'arbitre pendant le tour de jeu.  
* Implémentation des endpoints **POST** pour les cartes à choix interactifs (dépollution du deck, défausse ciblée et acquisition directe).  
* Gestion des contraintes de validité des réponses sous peine de disqualification immédiate.

## **2\. Notes brutes** 

- Carte qui vont declanché des com supplementaire à l’arbitre (tres conseillé de le faire)  
- nouvelle url  
- confirm\_trash\_card\_from\_hand methode http post quand certaine carte action vont etre joué. recevoir un json avec 2 propriétés card name et   
- reponse avec fichier json   
- trash\_card\_from\_hand methode post. obligé d’ecarter une carte de sa main entré json avec la liste de scartes dans sa main, reponse carte qui va etre ecarté parmi celle dans la liste (si invalide \=\> elimination) déclenchement de ce comportement avec une carte action  
- confirm\_discard\_card\_from\_hand  
- confirm\_discard\_deck methode post (carte action joué) si oui ou non on defausse le deck reponse : true pour defausser le deck, false ne rien faire  
- choose\_card\_receve\_in\_this\_card possible\_card liste des cartes qu’on peut choisir. La carte va dans la defausse  
- choose\_card\_to\_receve\_in\_this\_deck


## **3\. Réponses & Échanges**  

**3.1. Mécanique des Endpoints Interactifs (Méthode POST)** 

Certaines cartes Action déclenchent désormais des requêtes secondaires transmises par l'arbitre vers le bot. Contrairement aux routes du cycle principal (qui étaient en GET), ces requêtes arrivent en **POST** et exigent une réponse JSON stricte.

* **Important :** L'implémentation de ces routes est indispensable pour éviter les blocages de partie ou de recevoir des cartes non désirés.

**3.2. Spécification Détaillée des Routes POST**   

| Endpoint  | Déclencheur / Contexte  | Payload reçu (Arbitre)  | Réponse attendue (Bot)  | Risque d'élimination  |
| :---: | :---: | :---: | :---: | :---: |
| /confirm\_trash\_card\_from\_hand  | L'effet propose d'écarter (rebut) une carte précise de la main  | Objet JSON avec le nom de la carte (`card_name`)  | `{"decision": true}` ou `{"decision": false}`  | Non  |
| /confirm\_discard\_card\_from\_hand  | L'effet propose de défausser une carte spécifique de la main  | Objet JSON avec le nom de la carte ciblée  | `{"decision": true}` ou `{"decision": false}`  | Non  |
| /confirm\_discard\_deck  | L'effet propose de défausser l'intégralité de sa pioche (pour provoquer un remélange)  | Notification de déclenchement d'effet  | `{"decision": true}` *(pour défausser)* ou `{"decision": false}` *(pour conserver)*  | Non  |
| /trash\_card\_from\_hand  | L'effet oblige à écarter une carte au rebut  | Objet JSON contenant la liste des cartes en main  | `{"card_name": "<nom_carte>"}` *(doit figurer dans la main reçue)*  | **Oui** *(si carte invalide ou absente de la main)*  |
| /discard\_card\_from\_hand  | L'effet oblige à défausser une carte de la main  | Objet JSON contenant la liste des cartes en main  | `{"card_name": "<nom_carte>"}` *(doit figurer dans la main reçue)*  | **Oui** *(si carte invalide)*  |
| /choose\_card\_to\_receive\_in\_discard  | Gain direct d'une carte vers la défausse personnelle  | Objet JSON avec la liste des options possibles (`possible_cards`)  | `{"card_name": "<nom_carte>"}` *(strictement choisie dans la liste)*  | **Oui** *(si carte non autorisée)*  |
| /choose\_card\_to\_receive\_in\_deck  | Gain direct d'une carte placée sur le dessus de la pioche  | Objet JSON avec la liste des options possibles (`possible_cards`)  | `{"card_name": "<nom_carte>"}` *(strictement choisie dans la liste)*  | **Oui** *(si carte non autorisée)*  |

**3.3. Règles Stratégiques Associées** 

* **Épuration du Deck (`Trash`) :** Privilégier systématiquement l'épuration des cartes faibles (*Cuivre* et *Domaine*) dès le début/milieu de partie lorsqu'une confirmation ou un choix d'écartement est demandé.  
* **Sécurisation des réponses :** Tout choix renvoyé par le bot doit faire l'objet d'un contrôle d'existence préalable par rapport à la liste fournie par l'arbitre (`possible_cards` ou cartes en main) pour éliminer tout risque de disqualification.


## **4\. Questions restantes à clarifier avec le client** 

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?  
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).  
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## **5\. Décisions & Plan d'action** 

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Mettre en place les 7 nouveaux endpoints POST sur le serveur HTTP du bot  | Adam Alves / Guillaume Befre  | Demain |
| Ajouter un validateur de sécurité vérifiant que la carte renvoyée appartient bien au payload reçu  | Adam Alves / Guillaume Befre  | Demain |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre/Erwan Menard | Au fur et à mesure |

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

