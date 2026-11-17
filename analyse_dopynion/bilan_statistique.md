# Bilan stratégique Dopynion — Toulousain test

**Étiquette de collecte :** V6  
**Versions dans l'historique :** V6  
**Rapport généré :** 2026-11-17T16:13:07+01:00  
**Objectif :** 300 parties de ce bot ; **collectées :** 204  

## Qualité de l'échantillon

- Parties validées via `dop-game-data.players` : **204** (aucune partie d'un homonyme).
- Le champ `revision` est celui fourni au collecteur ; il ne prouve pas quelle version tournait lors d'un ancien match importé.
- Résultats exploitables : **204**.
- Premières places (y compris éventuelles égalités) : **99/204 = 48.5 %**.
- Victoires sans égalité : **89/204**.
- Intervalle indicatif 95 % de la proportion de premières places (Wilson) : **41.8 % à 55.4 %**.
- Cet intervalle ne corrige pas les différences de nombre d'adversaires, de qualité des adversaires ou de version du bot.
- Score moyen final : **-12.88** ; rang moyen : **1.71**.
- Tours moyens du bot : **21.81**.
- Tours sans achat (moyenne/partie) : **1.9**.
- Tour moyen du premier Or : **9.19** (uniquement si acheté).
- Tour moyen de la première Province : **10.85** (uniquement si achetée).
- Écart moyen avec la première Province des adversaires : **0.97 tours** (positif = notre bot démarre plus tard).

## Par taille de partie

| Joueurs | Parties | Premières places | Taux | Score moyen | Rang moyen |
|---:|---:|---:|---:|---:|---:|
| 2 | 46 | 32 | 69.6 % | 36.96 | 1.3 |
| 3 | 70 | 34 | 48.6 % | 40.64 | 1.67 |
| 4 | 88 | 33 | 37.5 % | -81.51 | 1.94 |

## Achats et actions observés

| Carte achetée | Total | Par partie |
|---|---:|---:|
| province | 993 | 4.87 |
| silver | 830 | 4.07 |
| gold | 656 | 3.22 |
| duchy | 361 | 1.77 |
| witch | 167 | 0.82 |
| laboratory | 145 | 0.71 |
| estate | 106 | 0.52 |
| hireling | 103 | 0.50 |
| village | 87 | 0.43 |
| festival | 84 | 0.41 |
| chapel | 82 | 0.40 |
| militia | 82 | 0.40 |
| fortuneteller | 82 | 0.40 |
| cellar | 73 | 0.36 |
| smithy | 57 | 0.28 |
| farmingvillage | 49 | 0.24 |
| market | 47 | 0.23 |
| bandit | 41 | 0.20 |
| library | 36 | 0.18 |
| magnate | 35 | 0.17 |
| councilroom | 13 | 0.06 |
| gardens | 12 | 0.06 |
| workshop | 11 | 0.05 |
| remodel | 8 | 0.04 |
| moneylender | 8 | 0.04 |
| bureaucrat | 3 | 0.01 |
| mine | 2 | 0.01 |
| chancellor | 2 | 0.01 |
| swap | 1 | 0.00 |
| feast | 1 | 0.00 |
| woodcutter | 1 | 0.00 |

| Carte Action jouée | Total |
|---|---:|
| witch | 756 |
| laboratory | 524 |
| chapel | 311 |
| cellar | 276 |
| militia | 259 |
| festival | 248 |
| fortuneteller | 238 |
| village | 209 |
| smithy | 188 |
| bandit | 147 |
| market | 141 |
| farmingvillage | 119 |
| library | 110 |
| hireling | 102 |
| magnate | 65 |
| councilroom | 35 |
| workshop | 19 |
| bureaucrat | 6 |
| remodel | 5 |
| moneylender | 4 |
| woodcutter | 2 |
| swap | 1 |
| feast | 1 |
| chancellor | 1 |

## Signaux de faiblesse à examiner

- **Au moins 6 Argent achetés** : 17/204 parties ; 2 premières places (11.8 %).
- **Aucun Or acheté** : 12/204 parties ; 4 premières places (33.3 %).
- **Aucune Province achetée** : 1/204 parties ; 0 premières places (0.0 %).
- **Au moins 4 tours sans achat** : 38/204 parties ; 15 premières places (39.5 %).
- **Première Province après le tour 12** : 48/204 parties ; 20 premières places (41.7 %).
- **Plus lent que le premier adversaire sur les Provinces** : 109/204 parties ; 46 premières places (42.2 %).

## Destructions et interactions

| Carte détruite (réponses de hook confirmées) | Total |
|---|---:|
| copper | 464 |
| estate | 186 |
| curse | 66 |

### Hooks reçus par le bot

| Hook Dopynion | Nombre d'appels |
|---|---:|
| `confirm_trash_card_from_hand` | 1296 |
| `confirm_discard_card_from_hand` | 1139 |
| `discard_card_from_hand` | 729 |
| `skip_card_reception_in_hand` | 59 |
| `choose_card_to_receive_in_discard` | 25 |
| `trash_card_from_hand` | 5 |
| `confirm_discard_deck` | 1 |

- Erreurs explicitement attribuées au bot : **4**.
- Les gains automatiques ne sont pas toujours traçables ; `cartes_recues_choisies` concerne seulement les gains décidés via un hook.

## Comparaison descriptive : achat d'une carte et première place

Attention : **corrélation, pas causalité**. Acheter une carte peut être la conséquence d'une bonne main, et non sa cause.
Afficher une association seulement si au moins 15 parties contiennent cette carte ET 15 n'en contiennent pas.

| Carte | Parties avec | 1res places avec | Parties sans | 1res places sans |
|---|---:|---:|---:|---:|
| duchy | 145 | 51.0 % | 59 | 42.4 % |
| laboratory | 84 | 42.9 % | 120 | 52.5 % |
| chapel | 82 | 50.0 % | 122 | 47.5 % |
| witch | 81 | 48.1 % | 123 | 48.8 % |
| hireling | 71 | 57.7 % | 133 | 43.6 % |
| estate | 68 | 51.5 % | 136 | 47.1 % |
| fortuneteller | 59 | 54.2 % | 145 | 46.2 % |
| militia | 58 | 46.6 % | 146 | 49.3 % |
| festival | 54 | 50.0 % | 150 | 48.0 % |
| smithy | 52 | 40.4 % | 152 | 51.3 % |
| village | 51 | 43.1 % | 153 | 50.3 % |
| cellar | 45 | 46.7 % | 159 | 49.1 % |
| market | 42 | 54.8 % | 162 | 46.9 % |
| bandit | 40 | 50.0 % | 164 | 48.2 % |
| library | 35 | 42.9 % | 169 | 49.7 % |
| farmingvillage | 31 | 45.2 % | 173 | 49.1 % |
| magnate | 28 | 50.0 % | 176 | 48.3 % |

## Matchs où le bot termine dernier / sans Province

| Date | Joueurs | Rang | Score | Tours sans achat | Argent achetés | Province achetées | Lien |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026-11-17T16:10:36.954349+01:00 | 3 | 3 | 26 | 2 | 2 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_10_36_954349.html) |
| 2026-11-17T16:09:58.171469+01:00 | 4 | 4 | 21 | 0 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_09_58_171469.html) |
| 2026-11-17T16:09:54.118189+01:00 | 2 | 2 | 27 | 2 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_09_54_118189.html) |
| 2026-11-17T16:07:33.647641+01:00 | 3 | 3 | 25 | 5 | 5 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_07_33_647641.html) |
| 2026-11-17T16:06:50.167414+01:00 | 4 | 4 | 13 | 1 | 6 | 1 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_06_50_167414.html) |
| 2026-11-17T16:04:24.158691+01:00 | 2 | 2 | 21 | 1 | 5 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_04_24_158691.html) |
| 2026-11-17T16:04:03.518943+01:00 | 3 | 3 | 27 | 1 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_04_03_518943.html) |
| 2026-11-17T16:02:51.374720+01:00 | 3 | 3 | 32 | 7 | 6 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_02_51_374720.html) |
| 2026-11-17T16:02:48.841346+01:00 | 3 | 3 | 30 | 0 | 5 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_02_48_841346.html) |
| 2026-11-17T16:02:43.596113+01:00 | 4 | 4 | -10000 | 2 | 3 | 0 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_02_43_596113.html) |
| 2026-11-17T16:02:22.915788+01:00 | 2 | 2 | 28 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_02_22_915788.html) |
| 2026-11-17T16:00:42.852986+01:00 | 2 | 2 | 33 | 2 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_00_42_852986.html) |
| 2026-11-17T16:00:27.261594+01:00 | 3 | 3 | 26 | 0 | 6 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_00_27_261594.html) |
| 2026-11-17T15:57:12.450787+01:00 | 2 | 2 | 30 | 3 | 6 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_57_12_450787.html) |
| 2026-11-17T15:57:01.230838+01:00 | 4 | 4 | 24 | 0 | 5 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_57_01_230838.html) |
| 2026-11-17T15:56:56.777898+01:00 | 4 | 4 | 6 | 5 | 6 | 1 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_56_56_777898.html) |
| 2026-11-17T15:56:34.186336+01:00 | 2 | 2 | 36 | 0 | 5 | 5 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_56_34_186336.html) |
| 2026-11-17T15:54:30.992779+01:00 | 2 | 2 | 27 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_54_30_992779.html) |
| 2026-11-17T15:54:28.742150+01:00 | 2 | 2 | 27 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__15_54_28_742150.html) |
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
