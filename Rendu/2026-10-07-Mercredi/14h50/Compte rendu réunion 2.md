# Compte rendu de réunion - 2

## Mi-journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 7 octobre 2026
- **Heure réunion :** 14h40
- **Lieu :** Ynov Campus Bordeaux
- **Absents et excusés :** /
- **Participants :**
  - Pierre Dejean
  - Erwan Menard
  - Guillaume Befre
  - Adam Alves
  - Client

## Ordre du jour

- Clarification sur la mécanique des **cartes Action** et la gestion des tours.
- Spécificités des royaumes et équilibrage de départ.
- Mécaniques d’achat et gestion des effets de cartes.
- Spécifications sur le protocole de communication avec l’arbitre (multi-parties).

## Notes brutes

**Questions qu’il reste à poser :**

- Est-ce qu’il faut des cartes obligatoires pour tous les royaumes du jeu ? A-t-on des cartes personnalisées selon le royaume ? Si oui, a-t-il des cartes en tête qu’il souhaite ? Si oui, a-t-il commencé à réfléchir à une ligne directionnelle de la stratégie ?
- Quelles sont les limites du nombre de cartes jouables par tour ?
- Y a-t-il des malus à travers des intempéries ou des maladies qui pénalisent notre royaume ?
- Peut-on attaquer les autres royaumes ?
- Possibilité de faire des alliances entre les royaumes ?

**Réponses de la réunion :**

- Dans le magasin, il y a 10 piles de 10 cartes Action choisies par l’arbitre
- Pour utiliser une carte Action, uniquement depuis la main
- Sur une carte Action, il peut y avoir des effets infaisables (ex. : effet Cuivre alors qu'il n'y a plus de Cuivre)
- Pas d'obligation de jouer une carte Action
- Si une carte Action est jouée, on est obligé de finir l’action
- Une carte Action par tour, sauf si sur la carte Action il y a `+X`, auquel cas on peut faire plusieurs actions
- Tous les royaumes ont le même départ
- Pas de spécificité aux royaumes
- On trouve souvent des `+X Achat` (ex. : Cuivre) valables juste sur le tour en cours
- Un achat par tour par défaut (pas obligatoire)
- Effets qu’on peut retrouver sur les cartes : défausser, écarter (jeter une carte au rebut), recevoir (je prends une carte de la réserve et je la mets dans ma défausse)
- Conversion de retour automatique
- Carte achetée : on la met dans la défausse
- Répartir les Cuivres dans différents achats
- Protocole de communication avec l’arbitre
- Plusieurs API : numéro de partie parce qu'on peut avoir des parties en instantané

## Réponses & Échanges

### Structure du tour de jeu & Actions

- **Limite par défaut :** Chaque joueur dispose par défaut de **1 action** et **1 achat** par tour.
- **Cumul d’actions (+X Action) :** Si une carte Action octroie `+X Action`, le joueur peut enchaîner d’autres actions durant le tour en cours.
- **Condition d’activation :** Une carte Action ne peut être jouée que depuis la main.
- **Résolution obligatoire :** Il n'est pas obligatoire de jouer une carte Action. En revanche, **dès qu'une carte Action est jouée, elle doit être résolue jusqu'au bout**.
- **Effets impossibles :** Si un effet devient irréalisable (ex. la carte demande d'obtenir un Cuivre mais la pile de Cuivre est vide), l’effet est simplement ignoré, mais le reste de la carte s’applique normalement.

### Mécanique des Achats & Économie

- **Limite d’achat :** 1 achat par tour par défaut (non obligatoire). Des effets de cartes peuvent accorder `+X Achat` (valables uniquement pour le tour en cours).
- **Destination d’une carte achetée :** Toute carte achetée part **immédiatement dans la défausse** et elle ne rejoint le deck qu'après le mélange.
- **Conversions :** La conversion des ressources et le calcul du montant disponible pour l'achat sont automatiques.

### Composition de la Réserve (Magasin) & Mots-clés

- **Piles d’actions :** La réserve contient **10 piles de 10 cartes Action** (soit 100 cartes Action au total), choisies, configurées et distribuées aléatoirement par l’arbitre.
- **Effets / Vocabulaire standardisé :**
  - **Défausser :** Mettre une carte de sa main dans sa défausse personnelle.
  - **Écarter :** Envoyer une carte au Rebut (poubelle commune), la retirant définitivement de la partie.
  - **Recevoir :** Prendre une carte directement depuis la réserve pour la placer dans sa défausse personnelle.

### Équilibrage des Royaumes

- **Aucune asymétrie :** Tous les royaumes démarrent avec la même configuration (7 Cuivres, 3 Domaines).
- **Pas de personnalisation :** Aucun royaume ne possède de cartes exclusives ou de spécificités propres.

### Spécifications Techniques & API Arbitre

- **Gestion multi-parties :** L’API gère plusieurs instances en parallèle. Chaque échange intègre obligatoirement un **numéro de partie** (Game ID) pour distinguer les parties jouées en simultané. Il doit également être renvoyé pour chaque réponse.
- **Protocole HTTP :** Respect strict des schémas d’entrées/sorties attendus par l’arbitre pour éviter toute disqualification.

## Questions restantes à clarifier avec le client

Parmi les questions initiales, certaines restent encore en suspens pour les futurs échanges :

1. **Continuer l’explication sur l’API et l’arbitre (lié à la réunion précédente)**
2. **Malus environnementaux :** Y a-t-il des malus imprévus (intempéries, maladies, événements aléatoires) qui pénalisent un royaume ?
3. **Attaques & Interactivité :** Existe-t-il des cartes Action de type « Attaque » ciblant les adversaires ? Si oui, y a-t-il des cartes « Réaction » pour s'en défendre ?
4. **Alliances & Diplomatie :** Les alliances, échanges de ressources ou pactes entre royaumes sont-ils autorisés ou la partie est-elle strictement en « chacun pour soi » ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Configuration hébergeur web | Guillaume Befre | Fin de journée |
| Mise en place de l’API | Adam Alves | Fin de journée |
| Création du repository GitHub | Pierre Dejean | Immédiat |
| Déployer le serveur HTTP avec le template de base (*passer son tour*) | Adam Alves | Fin de journée |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |