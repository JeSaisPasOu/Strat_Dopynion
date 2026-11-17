# Bilan stratégique Dopynion — Toulousain test

**Étiquette de collecte :** V6  
**Versions dans l'historique :** V6  
**Rapport généré :** 2026-11-17T16:24:19+01:00  
**Objectif :** 300 parties de ce bot ; **collectées :** 313  

## Qualité de l'échantillon

- Parties validées via `dop-game-data.players` : **313** (aucune partie d'un homonyme).
- Le champ `revision` est celui fourni au collecteur ; il ne prouve pas quelle version tournait lors d'un ancien match importé.
- Résultats exploitables : **313**.
- Premières places (y compris éventuelles égalités) : **154/313 = 49.2 %**.
- Victoires sans égalité : **136/313**.
- Intervalle indicatif 95 % de la proportion de premières places (Wilson) : **43.7 % à 54.7 %**.
- Cet intervalle ne corrige pas les différences de nombre d'adversaires, de qualité des adversaires ou de version du bot.
- Score moyen final : **3.82** ; rang moyen : **1.7**.
- Tours moyens du bot : **21.6**.
- Tours sans achat (moyenne/partie) : **1.86**.
- Tour moyen du premier Or : **9.0** (uniquement si acheté).
- Tour moyen de la première Province : **10.57** (uniquement si achetée).
- Écart moyen avec la première Province des adversaires : **0.69 tours** (positif = notre bot démarre plus tard).

## Par taille de partie

| Joueurs | Parties | Premières places | Taux | Score moyen | Rang moyen |
|---:|---:|---:|---:|---:|---:|
| 2 | 66 | 46 | 69.7 % | 36.64 | 1.3 |
| 3 | 112 | 61 | 54.5 % | 40.2 | 1.57 |
| 4 | 135 | 47 | 34.8 % | -42.39 | 2 |

## Achats et actions observés

| Carte achetée | Total | Par partie |
|---|---:|---:|
| province | 1525 | 4.87 |
| silver | 1275 | 4.07 |
| gold | 1026 | 3.28 |
| duchy | 511 | 1.63 |
| witch | 246 | 0.79 |
| laboratory | 188 | 0.60 |
| estate | 160 | 0.51 |
| hireling | 151 | 0.48 |
| village | 133 | 0.42 |
| festival | 132 | 0.42 |
| fortuneteller | 130 | 0.42 |
| chapel | 121 | 0.39 |
| militia | 119 | 0.38 |
| cellar | 104 | 0.33 |
| smithy | 99 | 0.32 |
| market | 78 | 0.25 |
| bandit | 74 | 0.24 |
| farmingvillage | 74 | 0.24 |
| library | 62 | 0.20 |
| magnate | 53 | 0.17 |
| councilroom | 23 | 0.07 |
| gardens | 15 | 0.05 |
| workshop | 13 | 0.04 |
| moneylender | 12 | 0.04 |
| remodel | 12 | 0.04 |
| swap | 7 | 0.02 |
| mine | 3 | 0.01 |
| bureaucrat | 3 | 0.01 |
| woodcutter | 2 | 0.01 |
| chancellor | 2 | 0.01 |
| feast | 1 | 0.00 |

| Carte Action jouée | Total |
|---|---:|
| witch | 1094 |
| laboratory | 674 |
| chapel | 435 |
| fortuneteller | 372 |
| militia | 370 |
| festival | 370 |
| cellar | 351 |
| smithy | 332 |
| village | 304 |
| bandit | 260 |
| market | 219 |
| library | 178 |
| farmingvillage | 169 |
| hireling | 149 |
| magnate | 90 |
| councilroom | 60 |
| workshop | 24 |
| swap | 9 |
| remodel | 8 |
| moneylender | 8 |
| bureaucrat | 6 |
| woodcutter | 2 |
| feast | 1 |
| chancellor | 1 |

## Signaux de faiblesse à examiner

- **Au moins 6 Argent achetés** : 22/313 parties ; 2 premières places (9.1 %).
- **Aucun Or acheté** : 16/313 parties ; 6 premières places (37.5 %).
- **Aucune Province achetée** : 1/313 parties ; 0 premières places (0.0 %).
- **Au moins 4 tours sans achat** : 51/313 parties ; 21 premières places (41.2 %).
- **Première Province après le tour 12** : 68/313 parties ; 27 premières places (39.7 %).
- **Plus lent que le premier adversaire sur les Provinces** : 161/313 parties ; 63 premières places (39.1 %).

## Destructions et interactions

| Carte détruite (réponses de hook confirmées) | Total |
|---|---:|
| copper | 661 |
| estate | 270 |
| curse | 86 |
| witch | 1 |

### Hooks reçus par le bot

| Hook Dopynion | Nombre d'appels |
|---|---:|
| `confirm_trash_card_from_hand` | 1812 |
| `confirm_discard_card_from_hand` | 1449 |
| `discard_card_from_hand` | 1077 |
| `skip_card_reception_in_hand` | 101 |
| `choose_card_to_receive_in_discard` | 34 |
| `trash_card_from_hand` | 8 |
| `confirm_discard_deck` | 1 |

- Erreurs explicitement attribuées au bot : **4**.
- Les gains automatiques ne sont pas toujours traçables ; `cartes_recues_choisies` concerne seulement les gains décidés via un hook.

## Comparaison descriptive : achat d'une carte et première place

Attention : **corrélation, pas causalité**. Acheter une carte peut être la conséquence d'une bonne main, et non sa cause.
Afficher une association seulement si au moins 15 parties contiennent cette carte ET 15 n'en contiennent pas.

| Carte | Parties avec | 1res places avec | Parties sans | 1res places sans |
|---|---:|---:|---:|---:|
| gold | 297 | 49.8 % | 16 | 37.5 % |
| duchy | 214 | 50.9 % | 99 | 45.5 % |
| chapel | 121 | 44.6 % | 192 | 52.1 % |
| witch | 118 | 48.3 % | 195 | 49.7 % |
| laboratory | 113 | 46.0 % | 200 | 51.0 % |
| hireling | 104 | 59.6 % | 209 | 44.0 % |
| estate | 100 | 54.0 % | 213 | 46.9 % |
| fortuneteller | 98 | 48.0 % | 215 | 49.8 % |
| smithy | 86 | 40.7 % | 227 | 52.4 % |
| militia | 85 | 45.9 % | 228 | 50.4 % |
| festival | 84 | 46.4 % | 229 | 50.2 % |
| village | 78 | 47.4 % | 235 | 49.8 % |
| bandit | 70 | 54.3 % | 243 | 47.7 % |
| market | 68 | 55.9 % | 245 | 47.3 % |
| cellar | 67 | 46.3 % | 246 | 50.0 % |
| library | 59 | 40.7 % | 254 | 51.2 % |
| farmingvillage | 50 | 42.0 % | 263 | 50.6 % |
| magnate | 45 | 48.9 % | 268 | 49.3 % |
| councilroom | 23 | 52.2 % | 290 | 49.0 % |

## Matchs où le bot termine dernier / sans Province

| Date | Joueurs | Rang | Score | Tours sans achat | Argent achetés | Province achetées | Lien |
|---|---:|---:|---:|---:|---:|---:|---|
| 2026-11-17T16:22:21.657082+01:00 | 2 | 2 | 30 | 0 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_22_21_657082.html) |
| 2026-11-17T16:21:31.269871+01:00 | 2 | 2 | 32 | 5 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_21_31_269871.html) |
| 2026-11-17T16:20:25.233922+01:00 | 3 | 3 | 23 | 1 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_20_25_233922.html) |
| 2026-11-17T16:19:35.640270+01:00 | 3 | 3 | 21 | 1 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_19_35_640270.html) |
| 2026-11-17T16:18:38.992230+01:00 | 4 | 4 | 24 | 0 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_18_38_992230.html) |
| 2026-11-17T16:17:33.412671+01:00 | 4 | 4 | 21 | 1 | 4 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_17_33_412671.html) |
| 2026-11-17T16:16:32.838473+01:00 | 2 | 2 | 24 | 2 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_16_32_838473.html) |
| 2026-11-17T16:15:52.837006+01:00 | 2 | 2 | 24 | 3 | 4 | 4 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_15_52_837006.html) |
| 2026-11-17T16:15:42.292061+01:00 | 4 | 4 | 21 | 0 | 5 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_15_42_292061.html) |
| 2026-11-17T16:14:26.421647+01:00 | 2 | 2 | 23 | 0 | 2 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_14_26_421647.html) |
| 2026-11-17T16:14:02.029852+01:00 | 4 | 4 | 18 | 1 | 4 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_14_02_029852.html) |
| 2026-11-17T16:13:42.704698+01:00 | 2 | 2 | 21 | 3 | 5 | 3 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_13_42_704698.html) |
| 2026-11-17T16:11:52.084035+01:00 | 4 | 4 | 16 | 1 | 4 | 2 | [match](https://dopynion.lecalamar.fr/games/game__2026_11_17__16_11_52_084035.html) |
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
