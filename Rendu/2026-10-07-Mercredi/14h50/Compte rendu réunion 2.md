# **Compte rendu de réunion \- 2**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 7 octobre 2026  
* **Heure réunion** : 14h40  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour** 

* Clarification sur la mécanique des **cartes Action** et la gestion des tours.  
* Spécificités des royaumes et équilibrage de départ.  
* Mécaniques d’achat et gestion des effets de cartes.  
* Spécifications sur le protocole de communication avec l’arbitre (multi-parties).


## **2\. Notes brutes** 

Questions qu’il reste à poser : 

- Est ce qu’il faut des cartes obligatoires pour tout les royaumes du jeu ? A t on des cartes personnalisé selon le royaume ? Si oui à tes cartes en têtes qu’il souhaite. Si oui a t il commencer à réfléchir à une ligne directionnel de la stratégie.  
- Quelles sont les limites du nombre de carte jouable par tour ?  
- Y a t il des malus à travers des intempéries, maladie qui pénalise notre royaume ?  
- Peut on attaquer les autres royaume ?  
- Possibilité de faire des alliances entre les royaumes?

Réponse de la reunion:

- dans le magazin, il y a 10 piles de 10 cartes actions choisit par l’arbitre  
- pour utiliser une carte action, que dans la main  
- sur une carte action, peut y avoir des effets infaisable (ex, effet cuivre alors qur ya plus de cuivre)  
- pas obligation de jouer une carte action  
- si carte action joué, on est obligé de finir l’action  
- une carte action par tour si sur carte action il y a \+x on peut faire plusieurs action  
- tous les royaumes ont le meme depart  
- pas de specificité aux royaumes  
- on trouve souvent des \+x achat (ex : cuivre) valable juste sur le tour en cours  
- un achat par tour par defaut (pas obligatoire)  
- effet qu’on peut retrouver sur les cartes : defausser, ecarter (jeter une carte au rebus),recevoir (je prends une carte de la reserve et je la mets dans ma défausse)  
- conversion de retour, automatique  
- carte acheté on l’a met dans la defausse   
- repartir les cuivre dans differents achats

- protocole de comm avec l’arbitre  
- plusieurs api : numero de partie parce que on peut avoir des parties en instantané

## **3\. Réponses & Échanges**

#### **3.1. Structure du tour de jeu & Actions** 

* **Limite par défaut :** Chaque joueur dispose par défaut de **1 action** et **1 achat** par tour.  
* **Cumul d’actions (+X Action) :** Si une carte action octroie \+X Action, le joueur peut enchaîner d’autres actions durant le tour en cours.  
* **Condition d’activation :** Une carte action ne peut être jouée que depuis la main.  
* **Résolution obligatoire :** Il n'est pas obligatoire de jouer une carte action. En revanche, **dès qu'une carte action est jouée, elle doit être résolue jusqu'au bout**.  
* **Effets impossibles :** Si un effet devient irréalisable (ex. la carte demande d'obtenir un Cuivre mais la pile de Cuivre est vide, l’effet est simplement ignoré, mais le reste de la carte s’applique normalement.

#### **3.2. Mécanique des Achats & Économie**

* **Limite d’achat :** 1 achat par tour par défaut (non obligatoire). Des effets de cartes peuvent accorder \+X Achat (valables uniquement pour le tour en cours).  
* **Destination d’une carte achetée :** Toute carte achetée part **immédiatement dans la défausse** et elles ne rejoignent le deck qu'après le mélange.  
* **Conversions :** La conversion des ressources et le calcul du montant disponible pour l'achat sont automatiques.

#### **3.3. Composition de la Réserve (Magasin) & Mots-clés**

* **Piles d’actions :** La réserve contient **10 piles de 10 cartes Action** (soit 100 cartes action au total), choisies, configurées et distribuées aléatoirement par l’arbitre.  
* **Effets / Vocabulaire standardisé :**  
  * **Défausser :** Mettre une carte de sa main dans sa défausse personnelle.  
  * **Écarter :** Envoyer une carte au Rebut (poubelle commune), la retirant définitivement de la partie.  
  * **Recevoir :** Prendre une carte directement depuis la réserve pour la placer dans sa défausse personnelle.

#### **3.4. Équilibrage des Royaumes**

* **Aucune asymétrie :** Tous les royaumes démarrent avec la même configuration (7 Cuivres, 3 Domaines).  
* **Pas de personnalisation :** Aucun royaume ne possède de cartes exclusives ou de spécificités propres.

#### **3.5. Spécifications Techniques & API Arbitre**

* **Gestion multi-parties :** L’API gère plusieurs instances en parallèle. Chaque échange intègre obligatoirement un **numéro de partie** (Game ID) pour distinguer les parties jouées en simultané. Elle doit être également envoyée pour chaques réponses.  
* **Protocole HTTP :** Respect strict des schémas d’entrées/sorties attendus par l’arbitre pour éviter toute disqualification.

## **4\. Questions restantes à clarifier avec le client** 

Parmi les questions initiales, certaines restent encore en suspens pour les futurs échanges :

1. **Continuer l’explication sur l’API et l’arbitre (lié à la réunion précédente)**   
2. **Malus environnementaux :** Y a-t-il des malus imprévus (intempéries, maladies, événements aléatoires) qui pénalisent un royaume ?  
3. **Attaques & Interactivité :** Existe-t-il des cartes Action de type « Attaque » ciblant les adversaires ? Si oui, y a-t-il des cartes « Réaction » pour s'en défendre ?  
4. **Alliances & Diplomatie :** Les alliances, échanges de ressources ou pactes entre royaumes sont-ils autorisés ou la partie est-elle strictement en « chacun pour soi » ?

## **5\. Décisions & Plan d'action** 

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

## **6\. Signatures**

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :---- | :---- | :---- | :---- | :---- |
| —------------- | —------------- | —------------- | —------------- | —------------- |

## 