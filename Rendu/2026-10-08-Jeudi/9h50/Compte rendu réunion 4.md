# **Compte rendu de réunion \- 4**

# **Projet Compétition de Royaume**

**Informations générales**

* **Date :** 8 octobre 2026  
* **Heure réunion** : 9h50  
* **Lieu :** Ynov campus bordeaux  
* **Absents et excusés :** /  
* **Participants :**  
* Pierre Dejean  
* Erwan Menard  
* Guillaume Befre  
* Adam Alves  
* Client

## **1\. Ordre du jour** 

* Spécification détaillée du protocole de communication HTTP avec l'arbitre (endpoints et formats JSON).  
* Définition des coûts et valeurs des cartes monnaies et Victoire.  
* Règles de fonctionnement du marché (réserve).  
* Recommandations et axes stratégiques pour le bot.

## **2\. Notes brutes** 

**Protocole de com :**

- carte argent vaut 3 cuivre mais dans la main ne vaut que 2 de cuivre  
- route /name en http (renvoie le nom de l’equipe)  
- methode start\_game appelé en debut de parti  
- methode start\_turn   
- methode /play appelé à chaque fois qu’on doit faire une action  
- end\_turn marque la fin du tour  
- entré gros objet java script du jeu  
- recevoir 2 propriété stuck et player  
- info playeur continent propriété name, score et hand   
- joueur adverse pas accessible (les carte dan sles mains)  
- propriété carte voir voc ca c’est /play  
- /end pour finir la partie et liberer de la memoire  
    
    
    
- phase achat : l’arbitre te dit ce qu’il y a dans la reserve l’etat varie du magazin (stock depard et ca diminue au fur et a mesure)  
- 1er acheté point de pouvoir acheé cuivre coute 0 et depensé coute 1 cuivre  
- silever 3 cuivre à acquerir et 2 cuivres à depensé  
- gold coute 6 cuivres à acquerir et 3 cuivres à depensé  
- pire tour 3 domaines et 2 cuivre  
- carte domaine estate coute 2 cuivre et un point de victoire  
- carte dushy coute 5 cuivres et compte pour 3 points de victoire  
- peut pas vendre des carte au marché  
- carte province coute 8 cuivres et rapport 6   
- acheté plein de points de victoire

## **3\. Réponses & Échanges**

#### **3.1. Protocole de communication (API HTTP de l'Arbitre)** 

Toutes les routes exposées par le bot sont appelées via la méthode **GET** par l'arbitre :

* **`/name`** : Retourne une simple chaîne de caractères contenant le nom de l'équipe (utilisé pour les logs et l'affichage).  
* **`/start_game`** : Signale l'initialisation d'une partie et transmet l'identifiant de celle-ci (`game_id`).  
  * *Réponse attendue :* `{"decision": "OK"}`  
* **`/start_round`** : Indique le démarrage d'un nouveau round.  
  * *Réponse attendue :* `{"decision": "OK"}`  
* **`/play` (Route principale)** : Appelée en boucle par l'arbitre tant que le tour du joueur n'est pas terminé.  
  * **Payload reçu (état de jeu) :**  
    * `isFinished` *(booléen)* : État de la partie (`false` en cours).  
    * `players` *(liste)* : Contient le nom (`name`), le score (`score`) et les cartes en main (`hand`). *Remarque : la main des adversaires est masquée.*  
    * `stock` *(objet)* : Piles et quantités restantes au marché.  
  * **Format de réponse du bot :** Un JSON contenant obligatoirement l'identifiant de partie et la clé `decision` :  
    * `{"game_id": "...", "decision": "END_TURN"}` : Met fin au tour en cours.  
    * `{"game_id": "...", "decision": "ACTION <nom_carte>"}` : Déclenche l'effet d'une carte action.  
    * `{"game_id": "...", "decision": "BUY <nom_carte>"}` : Achète la carte spécifiée.  
* **`/end_game`** : Marque la fin officielle de la partie (libération de la mémoire / reset des sessions).  
  * *Réponse attendue :* `{"decision": "OK"}`

#### **3.2. Fonctionnement du marché (Réserve)**

* **Pas de réapprovisionnement :** Les stocks ne se renouvellent pas ; ils s'épuisent au fil des achats des joueurs.  
* **Disponibilité :** Un achat n'est valide que si la pile correspondante dans le `stock` est strictement supérieure à 0\.  
* **Pas de revente :** Aucune carte ne peut être revendue au marché.

#### 

#### **3.3. Nomenclature, Coûts et Valeurs des Cartes** 

| Catégorie  | Nom en jeu  | Coût d'achat  | Valeur en jeu / Effet  |
| :---- | :---- | :---- | :---- |
| Monnaie | Copper  | free | Génère **1** cuivre pour les achats  |
| Monnaie | Silver  | 3 | Génère **2** cuivres pour les achats  |
| Monnaie | Gold  | 6 | Génère **3** cuivres pour les achats  |
| Point de victoire | Estate  | 2 | Vaut **1** Point de victoire |
| Point de victoire | Duchy  | 5 | Vaut **3** Point de victoire |
| Point de victoire | Province  | 8 | Vaut **6** Point de victoire *(l'épuisement de cette pile clôt la partie)*  |

#### **3.4. Principes & Conseils Stratégiques** 

* **Gestion du deck initial :** Le deck de départ contient 10 cartes (7 Cuivres et 3 Domaines). La main de départ pioche 5 cartes dans ce paquet.  
* **L'encombrement des points de victoire :** Les cartes de victoire n'apportent aucun pouvoir ni ressource pendant le tour. Un tirage défavorable (ex. 3 Domaines et 2 Cuivres) ralentit l'économie.  
* **Recommandation :** Éviter d'acheter des cartes de faible victoire (`Estate`) en début de partie. Privilégier d'abord le développement économique (`Silver`, puis `Gold`) avant de basculer vers les achats massifs de `Province`.

## **4\. Questions restantes à clarifier avec le client** 

1. **Malus environnementaux :** Y a-t-il des malus imprévus (intempéries, maladies, événements aléatoires) qui pénalisent un royaume ?  
2. **Attaques & Interactivité :** Existe-t-il des cartes Action de type « Attaque » ciblant les adversaires ? Si oui, y a-t-il des cartes « Réaction » pour s'en défendre ?  
3. **Alliances & Diplomatie :** Les alliances, échanges de ressources ou pactes entre royaumes sont-ils autorisés ou la partie est-elle strictement en « chacun pour soi » ?  
   

## **5\. Décisions & Plan d'action** 

| Action  | Responsable | Echéance |
| :---- | :---- | :---- |
| Fonction d’achat | Guillaume Befre | Fin de journée |
| Simulateur local | Adam Alves | Fin de matinée |
| Stratégie | Pierre Dejean | Fin de journée |
| Fonction carte action | Erwan Menard/Guillaume Befre | Fin de journée |
| Compte rendu avant et après reunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure |

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