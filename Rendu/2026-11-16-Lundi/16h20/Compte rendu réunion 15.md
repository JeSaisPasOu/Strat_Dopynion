# Compte rendu de réunion - 15

## Fin de journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 16 novembre 2026
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

- Bilan de la journée et point sur le classement général du tournoi.
- Retour sur l'architecture technique, les correctifs d'arbitrage et l'organisation de l'équipe.
- Définition de la stratégie et du plan d'action pour la dernière journée (points doublés).

## Réponses & Échanges

### Bilan Tournoi & Positionnement

- **Classement actuel :** Notre équipe occupe la **4e place** au classement général. Malgré une perte d'environ 200 points constatée sur l'un des comptes, le compte principal reste globalement stable, ce qui est encourageant pour la suite.
- **Dynamique de la concurrence :** De gros scores réalisés aujourd'hui par les adversaires ont entraîné d'importants mouvements dans le classement

### Points Techniques & Organisation

- **Modularité du code :** L'architecture actuelle (fichier `action` dédié et fonctions modulaires) permet d'intégrer facilement les nouvelles cartes sans casser l'existant. Le principal enjeu reste l'adaptation rapide de la stratégie.
- **Organisation de l'équipe :** La répartition des rôles est jugée efficace et est maintenue :
  - **Adam Alves & Pierre Dejean :** Conception et ajustement des stratégies.
  - **Guillaume Befre & Erwan Menard :** Implémentation technique et gestion des actions.
  - *Points collectifs :* Organisés dès qu'un ajustement stratégique majeur est nécessaire.

### Objectifs & Axes Stratégiques (Dernière Journée)

- **Enjeu majeur (Points doublés) :** Demain marque la fin des 3 jours de compétition avec un barème où **les points comptent double**. L'objectif est de tout donner pour remonter sur le podium.
- **Anticipation des nouveautés :** Une nouvelle carte jugée très efficace sera introduite demain, nécessitant une intégration et une adaptation rapides.
- **Refonte stratégique :** Abandon de la stratégie expérimentale testée aujourd'hui (non concluante) pour repartir sur la base saine existante, en l'optimisant afin de prioriser les nouvelles cartes les plus rentables.
- **Automatisation de l'analyse des logs :** Mise en place d'un système (ou script dédié) pour sauvegarder et analyser plus rapidement les logs de parties afin d'en tirer des conclusions efficaces et d'observer les stratégies adverses.

## Questions restantes à clarifier avec le client

- Aucune question en suspens à l'issue de cette réunion.

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Abandonner le test stratégique non concluant et restaurer/améliorer la stratégie de base (priorisation des nouvelles cartes rentables) | Pierre Dejean / Adam Alves | Demain matin |
| Mettre en place un outil d'automatisation pour la sauvegarde et l'analyse rapide des logs de parties (observation des stratégies adverses) | Adam Alves / Guillaume Befre | Demain matin |
| Préparer l'intégration rapide de la nouvelle carte annoncée pour la dernière journée | Guillaume Befre / Erwan Menard | Demain matin |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |