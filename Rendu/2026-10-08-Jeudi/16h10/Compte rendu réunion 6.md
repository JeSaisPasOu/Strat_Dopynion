# Compte rendu de réunion - 6

## Récap fin de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 8 octobre 2026
- **Heure réunion :** 16h10
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Consolidation du protocole de communication avec l'arbitre, des mécaniques de cartes Action et des fonctions d’achat.
- État des lieux des livrables de développement (simulateur, achats, moteur d'actions, stratégie, cartes Action).
- Recensement des points restants et jalons pour la suite.

## Notes brutes

- Réunion fin de journée
- Prochain jour, dernier jour en simultané
- Trouver moyen de sauvegarder les données des parties

## Résumé de la journée : Synthèse des acquis

### Protocole API & Intégration HTTP de l'Arbitre

- **Méthode standard :** Toutes les routes d'écoute du bot sont interrogées en **GET** par l'arbitre.
- **Cycle d'une partie :**
  - `/name` : renvoie le nom d'équipe pour l'arbitrage.
  - `/start_game` : initialise la partie avec le `game_id` (réponse `{"decision": "OK"}`).
  - `/start_round` : notifie le début de manche (réponse `{"decision": "OK"}`).
  - `/play` : boucle principale fournissant l'état du jeu (`isFinished`, `players`, `stock`) et recevant l'action choisie (`END_TURN`, `ACTION <carte>`, `BUY <carte>`).
  - `/end_game` : clôture la session et purge la mémoire (réponse `{"decision": "OK"}`).

### Économie & Fonctionnement du Marché

- **Pas de réassort ni de revente :** Les cartes achetées diminuent le stock sans renouvellement ; aucune carte ne peut être revendue.
- **Monnaie & Victoires (coûts et valeurs confirmés) :**
  - **Monnaie :** *Copper* (coût 0 / +1 cuivre), *Silver* (coût 3 / +2 cuivres), *Gold* (coût 6 / +3 cuivres).
  - **Victoires :** *Estate* (coût 2 / 1 point de victoire), *Duchy* (coût 5 / 3 points de victoire), *Province* (coût 8 / 6 points de victoire).

### Cartes Action & Gestion du Tour

- **Catalogue d'actions intégré :** Spécification des cartes *Village* (+1 carte, +2 actions), *Bûcheron* (+1 achat, +2 cuivres), *Forgeron* (+3 cartes), *Festival* (+2 actions, +1 achat, +2 cuivres), *Laboratoire* (+2 cartes, +1 action) et *Marché* (+1 carte, +1 action, +1 achat, +1 cuivre).
- **Fin de tour :** Toutes les cartes jouées et restantes en main vont dans la défausse. Le joueur repioche systématiquement 5 cartes pour le tour d'après.
- **Gestion du Rebut :** Seul l'effet explicite d'une carte permet d'écarter au Rebut (rien n'y va par défaut).

### État des Livrables & Développements

- **Simulateur local :** Opérationnel pour tester les prises de décision du bot hors ligne.
- **Moteur d'achat & d'action :** Fonctions d'achat et d'exécution des cartes Action implémentées sur la route `/play` et vérification que les nouvelles fonctions ne retournent pas d’erreurs.
- **Logique stratégique :** Première version de l'arbitrage décisionnel (optimisation du ratio monnaies vs cartes Victoire pour éviter l'encombrement du deck).
- **Documentation :** Cahier des charges et comptes rendus mis à jour en continu.

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Valider le comportement du bot en conditions réelles contre l'arbitre officiel | Guillaume Befre / Adam Alves | Prochaine séance |
| Simulateur local | Adam Alves | Fin de matinée (Fini) |
| Stratégie | Pierre Dejean | Fin de journée |
| Fonction carte action | Erwan Menard / Guillaume Befre / Adam Alves | Fin de journée |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |