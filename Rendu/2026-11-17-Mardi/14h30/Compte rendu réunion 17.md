# Compte rendu de réunion - 17

## Mi-journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 17 novembre 2026
- **Heure réunion :** 14h30
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Mise en place de l'outil d'extraction et d'analyse des logs de parties (JSON).
- Bilan d'efficacité des cartes (priorisation de la Chapelle) et ajustement du scoring dynamique.
- Définition des prochaines étapes d'observation et d'optimisation.

## Notes brutes

- bot qui regarde les 10 dernieres parties dans un json et analyser pour ameliorer la strategie
- Pk 10, tester sur un code nouveau donc plus representatif
- Voir à augmenter le nb de partie analysé
- meilleur carte : chapelle (prof demandé à chat)

## Réponses & Échanges

### Bilan Tournoi & Positionnement

- **Classement actuel :** L'équipe occupe la **4e place** du classement général, avec un écart important derrière les 3 premiers groupes qui ont pris une forte avance. Le score du bot se situait aux alentours de **900 points** ce matin.

### Mise en place de l'Analyse de Données (Logs)

- **Outil d'extraction automatisée :** Nous avons mis en place un script/bot afin de récupérer automatiquement les données des **10 à 20 dernières parties** jouées. Il génère deux fichiers : un export structuré au format **JSON** et un **log complet** des coups joués par tous les participants.
- **Objectif :** Analyser les stratégies adverses (notamment la fréquence des malus subis), nos anciennes parties et évaluer l'impact d'un nouveau code sur un échantillon récent et représentatif.

### Ajustements Stratégiques & Gestion des Cartes

- **Système de scoring dynamique :** Maintien de l'approche adaptative où chaque carte reçoit un score calculé en temps réel selon l'état de la partie, les coups précédents et les attaques subies, évitant ainsi une stratégie trop rigide.
- **Bilan d'utilisation des cartes :**
  - **Chapelle *(Chapel)* :** Confirmée comme carte prioritaire et identifiée comme l'une des meilleures cartes du jeu. *Recommandation :* bien affiner les critères d'écartement (*trash*) pour optimiser l'épuration du deck dès l'ouverture.
  - **Cave *(Cellar)* :** Bien intégrée et performante dans la stratégie actuelle.
  - **Festin *(Feast)* :** Jugé peu rentable dans la configuration actuelle et mis de côté.
  - **Autres cartes :** Utilisées avec modération selon le contexte de chaque partie.

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Laisser tourner le bot afin d'accumuler un volume représentatif de parties | Adam Alves / Guillaume Befre | En continu |
| Élargir progressivement la fenêtre d'analyse de l'outil de logs (passer de 10-20 à 100 parties une fois le code stabilisé) | Adam Alves / Guillaume Befre | Prochaine séance |
| Affiner les règles d'écartement (*trash*) pour la **Chapelle** et ajuster les pondérations du scoring dynamique d'après les statistiques récoltées | Pierre Dejean / Erwan Menard | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |