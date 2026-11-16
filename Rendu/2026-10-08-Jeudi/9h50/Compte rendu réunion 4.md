# Compte rendu de réunion - 4

## Début de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 8 octobre 2026
- **Heure réunion :** 9h50
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour

- Spécification détaillée du protocole de communication HTTP avec l'arbitre (endpoints et formats JSON).
- Définition des coûts et valeurs des cartes Monnaie et Victoire.
- Règles de fonctionnement du marché (réserve).
- Recommandations et axes stratégiques pour le bot.

## Notes brutes

**Protocole de communication :**

- Carte Argent vaut 3 Cuivres à l'achat mais dans la main ne vaut que 2 Cuivres
- Route `/name` en HTTP (renvoie le nom de l’équipe)
- Méthode `start_game` appelée en début de partie
- Méthode `start_turn`
- Méthode `/play` appelée à chaque fois qu’on doit faire une action
- `end_turn` marque la fin du tour
- Entrée : gros objet JavaScript du jeu
- Recevoir 2 propriétés : `stock` et `players`
- Info joueur contient propriétés `name`, `score` et `hand`
- Joueur adverse pas accessible (les cartes dans les mains)
- Propriété carte : voir vocabulaire, ça c’est `/play`
- `/end_game` pour finir la partie et libérer de la mémoire
- Phase achat : l’arbitre te dit ce qu’il y a dans la réserve, l’état du magasin varie (stock de départ et ça diminue au fur et à mesure)
- 1er achat / pouvoir d'achat : Cuivre coûte 0 et dépensé vaut 1 Cuivre
- Silver : 3 Cuivres à acquérir et 2 Cuivres à dépenser
- Gold coûte 6 Cuivres à acquérir et 3 Cuivres à dépenser
- Pire tour : 3 Domaines et 2 Cuivres
- Carte Domaine (`Estate`) coûte 2 Cuivres et vaut 1 point de victoire
- Carte Duché (`Duchy`) coûte 5 Cuivres et compte pour 3 points de victoire
- On ne peut pas vendre des cartes au marché
- Carte Province coûte 8 Cuivres et rapporte 6 points de victoire
- Acheter plein de points de victoire

## Réponses & Échanges

### Protocole de communication (API HTTP de l'Arbitre)

Toutes les routes exposées par le bot sont appelées via la méthode **GET** par l'arbitre :

- **`/name` :** Retourne une simple chaîne de caractères contenant le nom de l'équipe (utilisé pour les logs et l'affichage).
- **`/start_game` :** Signale l'initialisation d'une partie et transmet l'identifiant de celle-ci (`game_id`).
  - *Réponse attendue :* `{"decision": "OK"}`
- **`/start_round` :** Indique le démarrage d'un nouveau round.
  - *Réponse attendue :* `{"decision": "OK"}`
- **`/play` (Route principale) :** Appelée en boucle par l'arbitre tant que le tour du joueur n'est pas terminé.
  - **Payload reçu (état de jeu) :**
    - `isFinished` *(booléen)* : État de la partie (`false` en cours).
    - `players` *(liste)* : Contient le nom (`name`), le score (`score`) et les cartes en main (`hand`). *Remarque : la main des adversaires est masquée.*
    - `stock` *(objet)* : Piles et quantités restantes au marché.
  - **Format de réponse du bot :** Un JSON contenant obligatoirement l'identifiant de partie et la clé `decision` :
    - `{"game_id": "...", "decision": "END_TURN"}` : Met fin au tour en cours.
    - `{"game_id": "...", "decision": "ACTION <nom_carte>"}` : Déclenche l'effet d'une carte Action.
    - `{"game_id": "...", "decision": "BUY <nom_carte>"}` : Achète la carte spécifiée.
- **`/end_game` :** Marque la fin officielle de la partie (libération de la mémoire / reset des sessions).
  - *Réponse attendue :* `{"decision": "OK"}`

### Fonctionnement du marché (Réserve)

- **Pas de réapprovisionnement :** Les stocks ne se renouvellent pas ; ils s'épuisent au fil des achats des joueurs.
- **Disponibilité :** Un achat n'est valide que si la pile correspondante dans le `stock` est strictement supérieure à 0.
- **Pas de revente :** Aucune carte ne peut être revendue au marché.

### Nomenclature, Coûts et Valeurs des Cartes

| Catégorie | Nom en jeu | Coût d'achat | Valeur en jeu / Effet |
| :--- | :--- | :--- | :--- |
| Monnaie | Copper | Gratuit (0) | Génère **1** cuivre pour les achats |
| Monnaie | Silver | 3 | Génère **2** cuivres pour les achats |
| Monnaie | Gold | 6 | Génère **3** cuivres pour les achats |
| Point de victoire | Estate | 2 | Vaut **1** Point de victoire |
| Point de victoire | Duchy | 5 | Vaut **3** Point de victoire |
| Point de victoire | Province | 8 | Vaut **6** Point de victoire *(l'épuisement de cette pile clôt la partie)* |

### Principes & Conseils Stratégiques

- **Gestion du deck initial :** Le deck de départ contient 10 cartes (7 Cuivres et 3 Domaines). La main de départ pioche 5 cartes dans ce paquet.
- **L'encombrement des points de victoire :** Les cartes de victoire n'apportent aucun pouvoir ni ressource pendant le tour. Un tirage défavorable (ex. 3 Domaines et 2 Cuivres) ralentit l'économie.
- **Recommandation :** Éviter d'acheter des cartes de faible victoire (`Estate`) en début de partie. Privilégier d'abord le développement économique (`Silver`, puis `Gold`) avant de basculer vers les achats massifs de `Province`.

## Questions restantes à clarifier avec le client

1. **Malus environnementaux :** Y a-t-il des malus imprévus (intempéries, maladies, événements aléatoires) qui pénalisent un royaume ?
2. **Attaques & Interactivité :** Existe-t-il des cartes Action de type « Attaque » ciblant les adversaires ? Si oui, y a-t-il des cartes « Réaction » pour s'en défendre ?
3. **Alliances & Diplomatie :** Les alliances, échanges de ressources ou pactes entre royaumes sont-ils autorisés ou la partie est-elle strictement en « chacun pour soi » ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Fonction d’achat | Guillaume Befre | Fin de journée |
| Simulateur local | Adam Alves | Fin de matinée |
| Stratégie | Pierre Dejean | Fin de journée |
| Fonction carte action | Erwan Menard / Guillaume Befre | Fin de journée |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |