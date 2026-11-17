# Bilan stratégique Dopynion — Toulousain test

**Étiquette de collecte :** V6  
**Versions dans l'historique :** V6  
**Rapport généré :** 2026-11-17T15:52:49+01:00  
**Objectif :** 300 parties de ce bot ; **collectées :** 56  

## Qualité de l'échantillon

- Parties validées via `dop-game-data.players` : **56** (aucune partie d'un homonyme).
- Le champ `revision` est celui fourni au collecteur ; il ne prouve pas quelle version tournait lors d'un ancien match importé.
- Résultats exploitables : **56**.
- Premières places (y compris éventuelles égalités) : **29/56 = 51.8 %**.
- Victoires sans égalité : **26/56**.
- Intervalle indicatif 95 % de la proportion de premières places (Wilson) : **39.0 % à 64.3 %**.
- Cet intervalle ne corrige pas les différences de nombre d'adversaires, de qualité des adversaires ou de version du bot.
- Score moyen final : **37.86** ; rang moyen : **1.61**.
- Tours moyens du bot : **22.32**.
- Tours sans achat (moyenne/partie) : **1.62**.
- Tour moyen du premier Or : **9.04** (uniquement si acheté).
- Tour moyen de la première Province : **11.05** (uniquement si achetée).
- Écart moyen avec la première Province des adversaires : **1.35 tours** (positif = notre bot démarre plus tard).

## Par taille de partie

| Joueurs | Parties | Premières places | Taux | Score moyen | Rang moyen |
|---:|---:|---:|---:|---:|---:|
| 2 | 12 | 6 | 50.0 % | 34.33 | 1.5 |
| 3 | 25 | 11 | 44.0 % | 40.36 | 1.72 |
| 4 | 19 | 12 | 63.2 % | 36.79 | 1.53 |

## Achats et actions observés

| Carte achetée | Total | Par partie |
|---|---:|---:|
| province | 294 | 5.25 |
| gold | 224 | 4.00 |
| silver | 219 | 3.91 |
| duchy | 93 | 1.66 |
| witch | 52 | 0.93 |
| laboratory | 40 | 0.71 |
| hireling | 34 | 0.61 |
| estate | 29 | 0.52 |
| fortuneteller | 23 | 0.41 |
| festival | 22 | 0.39 |
| farmingvillage | 20 | 0.36 |
| militia | 19 | 0.34 |
| village | 19 | 0.34 |
| market | 18 | 0.32 |
| chapel | 18 | 0.32 |
| smithy | 17 | 0.30 |
| cellar | 14 | 0.25 |
| magnate | 12 | 0.21 |
| bandit | 11 | 0.20 |
| library | 6 | 0.11 |
| moneylender | 4 | 0.07 |
| councilroom | 3 | 0.05 |
| workshop | 2 | 0.04 |
| woodcutter | 1 | 0.02 |
| bureaucrat | 1 | 0.02 |
| gardens | 1 | 0.02 |

| Carte Action jouée | Total |
|---|---:|
| witch | 237 |
| laboratory | 157 |
| chapel | 78 |
| festival | 66 |
| militia | 64 |
| market | 61 |
| fortuneteller | 57 |
| smithy | 56 |
| bandit | 44 |
| farmingvillage | 43 |
| cellar | 41 |
| village | 38 |
| hireling | 34 |
| library | 18 |
| magnate | 11 |
| councilroom | 10 |
| moneylender | 3 |
| bureaucrat | 2 |
| woodcutter | 1 |
| workshop | 1 |

## Signaux de faiblesse à examiner

- **Au moins 6 Argent achetés** : 3/56 parties ; 0 premières places (0.0 %).
- **Aucun Or acheté** : 3/56 parties ; 0 premières places (0.0 %).
- **Aucune Province achetée** : 0/56 parties ; 0 premières places (n/d).
- **Au moins 4 tours sans achat** : 6/56 parties ; 3 premières places (50.0 %).
- **Première Province après le tour 12** : 13/56 parties ; 7 premières places (53.8 %).
- **Plus lent que le premier adversaire sur les Provinces** : 30/56 parties ; 15 premières places (50.0 %).

## Destructions et interactions

| Carte détruite (réponses de hook confirmées) | Total |
|---|---:|
| copper | 108 |
| estate | 46 |
| curse | 25 |

### Hooks reçus par le bot

| Hook Dopynion | Nombre d'appels |
|---|---:|
| `confirm_trash_card_from_hand` | 339 |
| `discard_card_from_hand` | 203 |
| `confirm_discard_card_from_hand` | 174 |
| `skip_card_reception_in_hand` | 12 |
| `choose_card_to_receive_in_discard` | 1 |

- Erreurs explicitement attribuées au bot : **0**.
- Les gains automatiques ne sont pas toujours traçables ; `cartes_recues_choisies` concerne seulement les gains décidés via un hook.

## Comparaison descriptive : achat d'une carte et première place

Attention : **corrélation, pas causalité**. Acheter une carte peut être la conséquence d'une bonne main, et non sa cause.
Afficher une association seulement si au moins 15 parties contiennent cette carte ET 15 n'en contiennent pas.

| Carte | Parties avec | 1res places avec | Parties sans | 1res places sans |
|---|---:|---:|---:|---:|
| duchy | 39 | 53.8 % | 17 | 47.1 % |
| witch | 25 | 56.0 % | 31 | 48.4 % |
| hireling | 23 | 60.9 % | 33 | 45.5 % |
| laboratory | 22 | 54.5 % | 34 | 50.0 % |
| estate | 21 | 57.1 % | 35 | 48.6 % |
| chapel | 18 | 50.0 % | 38 | 52.6 % |
| smithy | 17 | 47.1 % | 39 | 53.8 % |
| fortuneteller | 17 | 64.7 % | 39 | 46.2 % |
| market | 15 | 40.0 % | 41 | 56.1 % |
| militia | 15 | 60.0 % | 41 | 48.8 % |

## Matchs où le bot termine dernier / sans Province

| Date | Joueurs | Rang | Score | Tours sans achat | Argent achetés | Province achetées | Lien |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026-11-17T15:51:27.032857+01:00 | 4 | 4 | 16 | 3 | 4 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_51_27_032857.html) |
| 2026-11-17T15:51:17.141490+01:00 | 3 | 3 | 27 | 1 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_51_17_141490.html) |
| 2026-11-17T15:50:57.381640+01:00 | 2 | 2 | 31 | 3 | 3 | 5 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_50_57_381640.html) |
| 2026-11-17T15:50:27.037144+01:00 | 3 | 3 | 27 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_50_27_037144.html) |
| 2026-11-17T15:49:44.366082+01:00 | 2 | 2 | 30 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_49_44_366082.html) |
| 2026-11-17T15:47:40.502601+01:00 | 2 | 2 | 27 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_47_40_502601.html) |
| 2026-11-17T15:47:12.528930+01:00 | 3 | 3 | 24 | 2 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_47_12_528930.html) |
| 2026-11-17T15:47:11.375655+01:00 | 2 | 2 | 27 | 1 | 3 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_47_11_375655.html) |
| 2026-11-17T15:46:59.023180+01:00 | 3 | 3 | 19 | 3 | 5 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_46_59_023180.html) |
| 2026-11-17T15:46:34.236224+01:00 | 2 | 2 | 32 | 4 | 5 | 5 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_46_34_236224.html) |
| 2026-11-17T15:45:13.325425+01:00 | 2 | 2 | 31 | 1 | 5 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_45_13_325425.html) |

## Points à investiguer

- Si beaucoup de tours sans achat : examiner les actions, les ressources et l'épuration du deck.
- Si zéro Province achetée : comparer l'économie, la durée du match et la pression adverse.
- Si trop d'Argent en fin de partie : réduire les achats économiques après le milieu de partie.
- Si un type de partie perd souvent (2, 3 ou 4 joueurs) : régler l'agressivité et le moment de la course aux points.
- Si les hooks renvoient des erreurs : corriger l'API avant de retoucher les scores.

## Limites

- Les matchs collectés sont observationnels et ne contrôlent pas les différences de configuration ni d'adversaires.
- La collecte ne reconstruit pas parfaitement le deck ; les entrées `h` du journal ne sont que des instantanés de main.
- Une version du bot peut changer pendant la collecte : renseigner `--revision` et utiliser un dossier distinct.
- L'historique public accessible peut être limité. Utiliser `--suivi` pour accumuler les nouveaux matchs, sans promettre une récupération instantanée de 300 parties.
- Les achats enregistrés ne comprennent pas tous les gains automatiques de cartes.
