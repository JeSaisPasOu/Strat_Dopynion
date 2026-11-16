# Compte rendu de réunion - 3

## Récap fin de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 7 octobre 2026
- **Heure réunion :** 16h50
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour & Objectif de la séance

- Bilan et synthèse globale du jeu dans la journée (règles, mécanique et stratégie).
- Validation des livrables techniques indispensables (dépôt, bot et communication HTTP).

## Résumé de la journée

### Règles fondamentales & Déroulement de partie

- **Conditions de fin :** La partie s’arrête dès qu’au moins un des 3 critères est rempli : épuisement des cartes Provinces/Victoires, épuisement de 3 piles de la réserve, ou limite atteinte à 150 tours.
- **Départ symétrique :** Tous les royaumes débutent avec les mêmes cartes (7 Cuivres et 3 Domaines), sans cartes exclusives ni asymétrie de départ.
- **Zones de jeu :** Gestion stricte des 3 zones individuelles (Deck, Main complétée à 5 cartes, Défausse) et des 2 zones communes (Magasin/Réserve et Rebut).
- **Décompte :** Score final calculé sur l'ensemble des cartes possédées (Deck + Main + Défausse).

### Mécanique des tours, Actions & Achats

- **Standard par tour :** Par défaut, un joueur a droit à 1 Action et 1 Achat (non obligatoires).
- **Cartes Action :** Jouables uniquement depuis la main. Tout effet d’action engagé doit obligatoirement être résolu jusqu’au bout (les effets impossibles sont ignorés). Des bonus cumulables (`+X Action`) permettent d’enchaîner.
- **Achats :** Possibilité de répartir la valeur des Trésors en plusieurs achats si des bonus (`+X Achat`) ont été débloqués. Toute carte achetée rejoint immédiatement la défausse.
- **Vocabulaire validé :** Distinction stricte entre *Défausser* (dans sa défausse), *Écarter* (au rebut définitif) et *Recevoir* (prise directe depuis la réserve vers la défausse).

### Livrables & Avancement technique

- **Dépôt Git :** Repository GitHub initialisé pour le projet.
- **Serveur du Bot :** Déploiement du serveur HTTP basé sur le template de base (`passer son tour`) pour assurer l'enregistrement immédiat du bot auprès de l'arbitre.
- **Gestion multi-parties :** Prise en compte du protocole de communication avec l'arbitre, obligeant le bot à renvoyer systématiquement le **Game ID** (`numero_partie`) pour traiter les parties simultanées sans disqualification.

## Questions restantes à clarifier avec le client

1. **Attaques & Interactivité :** Existe-t-il des cartes Action offensives pénalisant la main ou le deck des adversaires ? Si oui, existe-t-il des cartes de Réaction pour s'en prémunir ?
2. **Malus environnementaux :** Des aléas extérieurs (maladies, météo, malus automatiques) peuvent-ils frapper les royaumes ?
3. **Diplomatie & Alliances :** Des accords, échanges ou pactes sont-ils prévus, ou s'agit-il d'un format strictement individuel ?
4. **Détails de l'API Arbitre :** Finaliser les spécifications exactes de l'ensemble des payloads attendus lors des phases de choix complexes.

## Décisions & Plan d'action

| Action | Responsable | Échéance | État |
| :--- | :--- | :--- | :--- |
| Configuration hébergeur web | Guillaume Befre | Fin de journée | Fini |
| Mise en place de l’API | Adam Alves | Fin de journée | Fini |
| Création du repository GitHub | Pierre Dejean | Fin de journée | Créé |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure | En cours |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure | En cours |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |