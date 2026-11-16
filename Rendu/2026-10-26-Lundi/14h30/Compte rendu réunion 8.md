# Compte rendu de réunion - 8

## Mi-journée

## Projet Compétition de Royaume

## Informations générales

- **Date :** 26 octobre 2026
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

- Spécification des nouvelles interactions synchrones avec l'arbitre pendant le tour de jeu.
- Implémentation des endpoints **POST** pour les cartes à choix interactifs (dépollution du deck, défausse ciblée et acquisition directe).
- Gestion des contraintes de validité des réponses sous peine de disqualification immédiate.

## Notes brutes

- Cartes qui vont déclencher des communications supplémentaires à l’arbitre (très conseillé de le faire)
- Nouvelles URL :
  - `confirm_trash_card_from_hand` : méthode HTTP POST quand certaines cartes Action vont être jouées. Recevoir un JSON avec 2 propriétés (`card_name` et...) ; réponse avec fichier JSON
  - `trash_card_from_hand` : méthode POST. Obligé d’écarter une carte de sa main. Entrée JSON avec la liste des cartes dans sa main, réponse : carte qui va être écartée parmi celles dans la liste (si invalide => élimination). Déclenchement de ce comportement avec une carte Action
  - `confirm_discard_card_from_hand`
  - `confirm_discard_deck` : méthode POST (carte Action jouée), si oui ou non on défausse le deck. Réponse : `true` pour défausser le deck, `false` pour ne rien faire
  - `choose_card_to_receive_in_discard` (`possible_cards` : liste des cartes qu’on peut choisir). La carte va dans la défausse
  - `choose_card_to_receive_in_deck`

## Réponses & Échanges

### Mécanique des Endpoints Interactifs (Méthode POST)

Certaines cartes Action déclenchent désormais des requêtes secondaires transmises par l'arbitre vers le bot. Contrairement aux routes du cycle principal (qui étaient en GET), ces requêtes arrivent en **POST** et exigent une réponse JSON stricte.

- **Important :** L'implémentation de ces routes est indispensable pour éviter les blocages de partie ou de recevoir des cartes non désirées.

### Spécification Détaillée des Routes POST

| Endpoint | Déclencheur / Contexte | Payload reçu (Arbitre) | Réponse attendue (Bot) | Risque d'élimination |
| :--- | :--- | :--- | :--- | :--- |
| `/confirm_trash_card_from_hand` | L'effet propose d'écarter (rebut) une carte précise de la main | Objet JSON avec le nom de la carte (`card_name`) | `{"decision": true}` ou `{"decision": false}` | Non |
| `/confirm_discard_card_from_hand` | L'effet propose de défausser une carte spécifique de la main | Objet JSON avec le nom de la carte ciblée | `{"decision": true}` ou `{"decision": false}` | Non |
| `/confirm_discard_deck` | L'effet propose de défausser l'intégralité de sa pioche (pour provoquer un remélange) | Notification de déclenchement d'effet | `{"decision": true}` *(pour défausser)* ou `{"decision": false}` *(pour conserver)* | Non |
| `/trash_card_from_hand` | L'effet oblige à écarter une carte au rebut | Objet JSON contenant la liste des cartes en main | `{"card_name": "<nom_carte>"}` *(doit figurer dans la main reçue)* | **Oui** *(si carte invalide ou absente de la main)* |
| `/discard_card_from_hand` | L'effet oblige à défausser une carte de la main | Objet JSON contenant la liste des cartes en main | `{"card_name": "<nom_carte>"}` *(doit figurer dans la main reçue)* | **Oui** *(si carte invalide)* |
| `/choose_card_to_receive_in_discard` | Gain direct d'une carte vers la défausse personnelle | Objet JSON avec la liste des options possibles (`possible_cards`) | `{"card_name": "<nom_carte>"}` *(strictement choisie dans la liste)* | **Oui** *(si carte non autorisée)* |
| `/choose_card_to_receive_in_deck` | Gain direct d'une carte placée sur le dessus de la pioche | Objet JSON avec la liste des options possibles (`possible_cards`) | `{"card_name": "<nom_carte>"}` *(strictement choisie dans la liste)* | **Oui** *(si carte non autorisée)* |

### Règles Stratégiques Associées

- **Épuration du Deck (`Trash`) :** Privilégier systématiquement l'épuration des cartes faibles (*Cuivre* et *Domaine*) dès le début et le milieu de partie lorsqu'une confirmation ou un choix d'écartement est demandé.
- **Sécurisation des réponses :** Tout choix renvoyé par le bot doit faire l'objet d'un contrôle d'existence préalable par rapport à la liste fournie par l'arbitre (`possible_cards` ou cartes en main) pour éliminer tout risque de disqualification.

## Questions restantes à clarifier avec le client

1. **Interactivité & Attaques :** Des cartes offensives ciblées (ex. vol, défausse forcée pour l'adversaire) ou défensives (cartes réaction) seront-elles introduites dans la réserve ?
2. **Malus environnementaux & Aléas :** Confirmation définitive de l'absence d'événements extérieurs pénalisants (météo, maladies).
3. **Diplomatie & Alliances :** Le jeu reste-t-il strictement en format chacun pour soi sans aucun accord multijoueur possible ?

## Décisions & Plan d'action

| Action | Responsable | Échéance |
| :--- | :--- | :--- |
| Mettre en place les 7 nouveaux endpoints POST sur le serveur HTTP du bot | Adam Alves / Guillaume Befre | Demain |
| Ajouter un validateur de sécurité vérifiant que la carte renvoyée appartient bien au payload reçu | Adam Alves / Guillaume Befre | Demain |
| Stratégie | Pierre Dejean | Au fur et à mesure |
| Compte rendu avant et après réunion | Erwan Menard | Au fur et à mesure |
| Avancement cahier des charges | Guillaume Befre / Erwan Menard | Au fur et à mesure |

## Signatures

| Pierre Dejean | Erwan Menard | Guillaume Befre | Adam Alves | Le Client |
| :--- | :--- | :--- | :--- | :--- |
| — | — | — | — | — |