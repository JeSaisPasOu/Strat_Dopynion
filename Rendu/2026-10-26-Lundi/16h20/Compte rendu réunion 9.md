# Compte rendu de réunion - 9

## Récap fin de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 26 octobre 2026
- **Heure réunion :** 16h20
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Bilan de la journée et mesure de la progression par rapport à la dernière session.
- Retours sur les performances en compétition (classement et corrections de bugs).
- Intégration des nouvelles cartes et des routes POST interactives dans la stratégie globale et analyse des points de blocage liés au passage en multi-parties simultanées pour demain.
- Possibilité de mettre en place un système de logs structurés pour l'optimisation décisionnelle assistée par IA.

## Notes brutes

- Amélioration comparée à la semaine dernière
- Nouvelle stratégie qui nous a permis de monter dans le classement et réglage des problèmes dans le code
- Réfléchir à une nouvelle stratégie en incorporant les nouvelles cartes Action vues aujourd'hui
- Première réunion : voir pour le multi-game et les potentiels points de blocage
- Fichier texte par partie pour mieux l’analyser par une IA et donc avoir une meilleure stratégie

## Résumé de la journée : Synthèse des acquis & Résultats

### Performances & Progression

- **Montée au classement :** L'ajustement de la stratégie de base et la résolution de plusieurs bugs bloquants dans le code ont permis un bond notable dans le classement général face aux autres équipes.
- **Stabilité accrue :** Le comportement du bot est nettement plus robuste et fiable comparativement aux sessions de la semaine passée.

### Architecture Technique & Concurrence (Multi-parties)

Prévention sur :

- **Validation du mode simultané :** Exécution concurrente de plusieurs parties lancées par l'arbitre.
- **Points de vigilance :** Risques de blocage (écrasement de variables globales, gestion des timeouts sur les nouvelles requêtes POST interactives). L'isolation stricte des contextes par `game_id` reste impérative.

### Évolution Stratégique & Nouvelles Cartes

- **Adaptation tactique :** Nécessité de faire évoluer le moteur de décision pour exploiter le catalogue étendu (Sorcière, Chambre du conseil, Recrue, Rivage lointain, Village agricole).
- **Gestion des choix interactifs :** Prise en compte active des nouvelles routes POST (`trash`, `discard`, sélection d'acquisitions) pour épurer le deck et se défendre contre la distribution de Malédictions.

### Outillage & Analyse par IA (Data Logging)

- **Génération de logs dédiés :** Possibilité de mettre en place un export au format texte/log dédié par partie (1 fichier par `game_id`).
- **Objectif :** Disposer d'un historique complet du déroulé de chaque match pour permettre une analyse fine post-partie (identification des choix sous-optimaux, benchmarking des adversaires) et accélérer l'amélioration de la stratégie via IA.

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Mettre en place les 7 nouveaux endpoints POST sur le serveur HTTP du bot | Adam Alves / Guillaume Befre | Prochaine séance |
| Ajouter un validateur de sécurité vérifiant que la carte renvoyée appartient bien au payload reçu | Adam Alves / Guillaume Befre | Prochaine séance |
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