# Bilan stratégique Dopynion — Toulousain test

**Étiquette de collecte :** V6  
**Versions dans l'historique :** V6  
**Rapport généré :** 2026-11-17T15:54:51+01:00  
**Objectif :** 300 parties de ce bot ; **collectées :** 65  

## Qualité de l'échantillon

- Parties validées via `dop-game-data.players` : **65** (aucune partie d'un homonyme).
- Le champ `revision` est celui fourni au collecteur ; il ne prouve pas quelle version tournait lors d'un ancien match importé.
- Résultats exploitables : **65**.
- Premières places (y compris éventuelles égalités) : **35/65 = 53.8 %**.
- Victoires sans égalité : **32/65**.
- Intervalle indicatif 95 % de la proportion de premières places (Wilson) : **41.9 % à 65.4 %**.
- Cet intervalle ne corrige pas les différences de nombre d'adversaires, de qualité des adversaires ou de version du bot.
- Score moyen final : **38.11** ; rang moyen : **1.58**.
- Tours moyens du bot : **22.6**.
- Tours sans achat (moyenne/partie) : **1.82**.
- Tour moyen du premier Or : **9.19** (uniquement si acheté).
- Tour moyen de la première Province : **11.15** (uniquement si achetée).
- Écart moyen avec la première Province des adversaires : **1.37 tours** (positif = notre bot démarre plus tard).

## Par taille de partie

| Joueurs | Parties | Premières places | Taux | Score moyen | Rang moyen |
|---:|---:|---:|---:|---:|---:|
| 2 | 16 | 10 | 62.5 % | 36.06 | 1.38 |
| 3 | 28 | 13 | 46.4 % | 40.54 | 1.71 |
| 4 | 21 | 12 | 57.1 % | 36.43 | 1.57 |

## Achats et actions observés

| Carte achetée | Total | Par partie |
|---|---:|---:|
| province | 338 | 5.20 |
| silver | 259 | 3.98 |
| gold | 251 | 3.86 |
| duchy | 118 | 1.82 |
| witch | 58 | 0.89 |
| laboratory | 48 | 0.74 |
| hireling | 37 | 0.57 |
| estate | 34 | 0.52 |
| fortuneteller | 29 | 0.45 |
| festival | 26 | 0.40 |
| militia | 26 | 0.40 |
| chapel | 22 | 0.34 |
| village | 22 | 0.34 |
| farmingvillage | 21 | 0.32 |
| cellar | 20 | 0.31 |
| smithy | 18 | 0.28 |
| market | 18 | 0.28 |
| bandit | 12 | 0.18 |
| magnate | 12 | 0.18 |
| library | 8 | 0.12 |
| moneylender | 4 | 0.06 |
| councilroom | 3 | 0.05 |
| bureaucrat | 2 | 0.03 |
| gardens | 2 | 0.03 |
| workshop | 2 | 0.03 |
| woodcutter | 1 | 0.02 |

| Carte Action jouée | Total |
|---|---:|
| witch | 277 |
| laboratory | 191 |
| chapel | 97 |
| militia | 90 |
| festival | 79 |
| fortuneteller | 73 |
| smithy | 61 |
| market | 61 |
| cellar | 59 |
| bandit | 49 |
| farmingvillage | 47 |
| village | 44 |
| hireling | 37 |
| library | 26 |
| magnate | 11 |
| councilroom | 10 |
| bureaucrat | 3 |
| moneylender | 3 |
| woodcutter | 1 |
| workshop | 1 |

## Signaux de faiblesse à examiner

- **Au moins 6 Argent achetés** : 5/65 parties ; 0 premières places (0.0 %).
- **Aucun Or acheté** : 3/65 parties ; 0 premières places (0.0 %).
- **Aucune Province achetée** : 0/65 parties ; 0 premières places (n/d).
- **Au moins 4 tours sans achat** : 9/65 parties ; 4 premières places (44.4 %).
- **Première Province après le tour 12** : 17/65 parties ; 8 premières places (47.1 %).
- **Plus lent que le premier adversaire sur les Provinces** : 35/65 parties ; 17 premières places (48.6 %).

## Destructions et interactions

| Carte détruite (réponses de hook confirmées) | Total |
|---|---:|
| copper | 131 |
| estate | 51 |
| curse | 33 |

### Hooks reçus par le bot

| Hook Dopynion | Nombre d'appels |
|---|---:|
| `confirm_trash_card_from_hand` | 407 |
| `discard_card_from_hand` | 269 |
| `confirm_discard_card_from_hand` | 241 |
| `skip_card_reception_in_hand` | 13 |
| `choose_card_to_receive_in_discard` | 1 |

- Erreurs explicitement attribuées au bot : **0**.
- Les gains automatiques ne sont pas toujours traçables ; `cartes_recues_choisies` concerne seulement les gains décidés via un hook.

## Comparaison descriptive : achat d'une carte et première place

Attention : **corrélation, pas causalité**. Acheter une carte peut être la conséquence d'une bonne main, et non sa cause.
Afficher une association seulement si au moins 15 parties contiennent cette carte ET 15 n'en contiennent pas.

| Carte | Parties avec | 1res places avec | Parties sans | 1res places sans |
|---|---:|---:|---:|---:|
| duchy | 47 | 55.3 % | 18 | 50.0 % |
| witch | 29 | 55.2 % | 36 | 52.8 % |
| laboratory | 27 | 59.3 % | 38 | 50.0 % |
| estate | 25 | 60.0 % | 40 | 50.0 % |
| hireling | 25 | 64.0 % | 40 | 47.5 % |
| chapel | 22 | 50.0 % | 43 | 55.8 % |
| fortuneteller | 21 | 61.9 % | 44 | 50.0 % |
| militia | 19 | 52.6 % | 46 | 54.3 % |
| smithy | 18 | 50.0 % | 47 | 55.3 % |
| festival | 16 | 68.8 % | 49 | 49.0 % |
| village | 15 | 46.7 % | 50 | 56.0 % |
| market | 15 | 40.0 % | 50 | 58.0 % |

## Matchs où le bot termine dernier / sans Province

| Date | Joueurs | Rang | Score | Tours sans achat | Argent achetés | Province achetées | Lien |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026-11-17T15:53:05.999817+01:00 | 3 | 3 | 32 | 7 | 6 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_53_05_999817.html) |
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
