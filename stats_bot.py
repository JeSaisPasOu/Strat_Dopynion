# -*- coding: utf-8 -*-
"""Collecteur statistique Dopynion pour « Toulousain test ».

Source de vérité : <script id="dop-game-data" type="application/json">.
Ne compte une partie que si le nom du bot figure EXACTEMENT dans players.

Installation :
    pip install playwright beautifulsoup4
    python -m playwright install chromium

Collecte ponctuelle :
    python stats_bot.py --nombre 300

Collecte jusqu'à atteindre 300 VRAIES parties du bot (à laisser tourner) :
    python stats_bot.py --nombre 300 --suivi --intervalle 60

Importer sans internet les anciennes captures :
    python stats_bot.py --importer 50_dernieres_parties.json 10_dernieres_parties.json

Pour comparer deux versions, utiliser un répertoire de résultats par version :
    python stats_bot.py --dossier stats_v6 --revision V6 --suivi
    python stats_bot.py --dossier stats_v7 --revision V7 --suivi
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime
import gzip
import json
import math
from pathlib import Path
import re
import statistics
import time
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

BASE_URL = "https://dopynion.lecalamar.fr/"
BOT_URL = "https://alves.alwaysdata.net/"
BOT_NOM = "Toulousain test"
NOMBRE_CIBLE = 300
DOSSIER_DEFAUT = "analyse_dopynion"
NOM_JSON = "statistiques_parties.json"
NOM_RAPPORT = "bilan_statistique.md"
GAME_LINK = re.compile(r"(?:^|/)games/game__[^/?#]+\.html$", re.I)
CARTES_VICTOIRE = {"province", "duchy", "estate", "gardens", "colony"}
CARTES_ARGENT = {"copper", "silver", "gold", "platinum"}


def ecrire_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def lire_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        x = json.loads(path.read_text(encoding="utf-8"))
        return x if isinstance(x, dict) else {}
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Données existantes illisibles ({path}): {exc}") from exc


def est_url_partie(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc == urlparse(BASE_URL).netloc and bool(
        GAME_LINK.search(parsed.path)
    )


def identifiant_partie(url: str) -> str:
    return urlparse(url).path.rsplit("/", 1)[-1].removesuffix(".html")


def jeu_depuis_html(html: str) -> dict | None:
    """Décodage du JSON interne réel, sans supposition sur les événements affichés."""
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", id="dop-game-data")
    if script is None:
        return None
    try:
        obj = json.loads(script.string or script.get_text() or "")
    except (TypeError, ValueError):
        return None
    if not isinstance(obj, dict):
        return None
    if not isinstance(obj.get("players"), list) or not isinstance(obj.get("scores"), list):
        return None
    if not isinstance(obj.get("turns"), list):
        return None
    if len(obj["players"]) != len(obj["scores"]):
        return None
    return obj


def _valeur_texte(v: object) -> str:
    return str(v).strip() if v is not None else ""


def _nombre(v: object) -> int | float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)) and math.isfinite(v):
        return int(v) if v == int(v) else float(v)
    return None


def _rang(scores: list, indice: int) -> int | None:
    if indice >= len(scores) or any(_nombre(s) is None for s in scores):
        return None
    return 1 + sum(s > scores[indice] for s in scores)


def statistiques_jeu(data: dict, url: str, nom_bot: str, revision: str) -> dict | None:
    """Extrait les décisions et scores observés, sans confondre les joueurs."""
    joueurs = data["players"]
    if nom_bot not in joueurs:  # Comparaison exacte : Toulousain != Toulousain test.
        return None
    idx = joueurs.index(nom_bot)
    scores = data["scores"]
    score = _nombre(scores[idx])
    rang = _rang(scores, idx)
    maximum = max(scores) if all(_nombre(s) is not None for s in scores) else None
    gagnes = score == maximum if score is not None and maximum is not None else None
    victoire_seule = bool(gagnes and scores.count(maximum) == 1)

    achats = Counter()
    achats_par_joueur = defaultdict(Counter)
    premieres_provinces = {}
    actions = Counter()
    destructions_confirmees = Counter()
    cartes_recues = Counter()
    appels_hook = Counter()
    reponses_hook = Counter()
    erreurs_bot = []
    avertissements_indefinis = []
    trace_tours = []
    compteur_tours = Counter()
    premier_achat_province = None
    premier_or = None
    score_par_tour = []
    achats_par_tour = defaultdict(list)
    tours_avec_achat = 0
    tours_sans_achat = 0
    total_tours = 0

    # L'indice p sur chaque entrée "turn" désigne le joueur actif.
    for tour in data.get("turns", []):
        if not isinstance(tour, dict):
            continue
        actif = tour.get("p")
        if not isinstance(actif, int) or not 0 <= actif < len(joueurs):
            continue
        compteur_tours[actif] += 1
        tour_du_joueur = compteur_tours[actif]
        propres = actif == idx
        if propres:
            total_tours += 1
            avant_achats = sum(achats.values())
            avant_score = None
        attente = None  # L'événement H est suivi d'une réponse R dans ce tour.
        for ev in tour.get("a", []):
            if not isinstance(ev, dict):
                continue
            typ = ev.get("t")
            card = _valeur_texte(ev.get("c")).lower()
            sujet = ev.get("p", actif)
            if typ == "B" and card:
                achats_par_joueur[actif][card] += 1
                if card == "province" and actif not in premieres_provinces:
                    premieres_provinces[actif] = tour_du_joueur
                if propres:
                    achats[card] += 1
                    achats_par_tour[tour_du_joueur].append(card)
                    if card == "province" and premier_achat_province is None:
                        premier_achat_province = tour_du_joueur
                    if card == "gold" and premier_or is None:
                        premier_or = tour_du_joueur
            elif typ == "A" and card and propres:
                actions[card] += 1
            elif typ == "H":
                attente = ev
                if sujet == idx:
                    appels_hook[_valeur_texte(ev.get("n"))] += 1
            elif typ == "R" and attente is not None:
                # Chaque hook est rattaché à SON joueur et non à l'actif.
                sujet_hook = attente.get("p", actif)
                if sujet_hook == idx:
                    nom = _valeur_texte(attente.get("n"))
                    retour = _valeur_texte(ev.get("r"))
                    reponses_hook[f"{nom}:{retour}"] += 1
                    if nom in {"trash_card_from_hand", "trash_money_card_for_better_money_card"} and retour:
                        destructions_confirmees[retour.lower()] += 1
                    elif nom == "confirm_trash_card_from_hand" and retour.casefold() == "true":
                        m = re.search(r"card_name\s*=\s*([\w]+)", _valeur_texte(attente.get("g")))
                        if m:
                            destructions_confirmees[m.group(1).lower()] += 1
                    if nom.startswith("choose_card_to_receive") and retour:
                        cartes_recues[retour.lower()] += 1
                attente = None
            elif typ == "X":
                erreur = _valeur_texte(ev.get("e"))
                if ev.get("p") == idx:
                    erreurs_bot.append(erreur[:300])
                elif "p" not in ev:
                    avertissements_indefinis.append(erreur[:300])
            if propres and typ in {"B", "E"}:
                s = _nombre(ev.get("s"))
                if s is not None:
                    avant_score = s
        if propres:
            a_achete = sum(achats.values()) > avant_achats
            tours_avec_achat += int(a_achete)
            tours_sans_achat += int(not a_achete)
            score_par_tour.append(avant_score)
            trace_tours.append({
                "tour_joueur": tour_du_joueur,
                "achats": achats_par_tour[tour_du_joueur],
                "score_apres_tour": avant_score,
            })

    distribution_achats = dict(achats.most_common())
    premiere_province_adverse = min(
        (t for joueur, t in premieres_provinces.items() if joueur != idx),
        default=None,
    )
    resultat = {
        "id": identifiant_partie(url),
        "url": url,
        "date": data.get("date"),
        "revision": revision,
        "joueur": nom_bot,
        "joueurs": joueurs,
        "nb_joueurs": len(joueurs),
        "scores": scores,
        "score_bot": score,
        "rang": rang,
        "premiere_place": gagnes,
        "victoire_seule": victoire_seule,
        "ecart_avec_meilleur_adversaire": (
            round(score - max(s for i, s in enumerate(scores) if i != idx), 2)
            if score is not None and len(scores) > 1 and all(_nombre(s) is not None for s in scores)
            else None
        ),
        "tours_bot": total_tours,
        "tours_avec_achat": tours_avec_achat,
        "tours_sans_achat": tours_sans_achat,
        "premiere_province_tour": premier_achat_province,
        "premiere_province_adverse_tour": premiere_province_adverse,
        "ecart_tour_premiere_province": (
            premier_achat_province - premiere_province_adverse
            if premier_achat_province is not None and premiere_province_adverse is not None
            else None
        ),
        "premier_or_tour": premier_or,
        "achats_adversaires": [
            {"nom": joueurs[p], "score": scores[p], "achats": dict(achats_par_joueur[p]),
             "premiere_province_tour": premieres_provinces.get(p)}
            for p in range(len(joueurs)) if p != idx
        ],
        "achats": distribution_achats,
        "actions_jouees": dict(actions.most_common()),
        "destructions_observees": dict(destructions_confirmees.most_common()),
        "cartes_recues_choisies": dict(cartes_recues.most_common()),
        "appels_hooks": dict(appels_hook.most_common()),
        "reponses_hooks": dict(reponses_hook.most_common()),
        "erreurs_du_bot": erreurs_bot[:30],
        "avertissements_non_attribues": avertissements_indefinis[:20],
        "tours": trace_tours,
    }
    return resultat


def charger_archive(chemin: Path, joueur: str) -> dict:
    old = lire_json(chemin)
    if not old:
        return {"format": 2, "joueur": joueur, "parties": {}, "non_bot": []}
    if old.get("joueur") != joueur:
        raise ValueError(
            f"Le fichier {chemin} concerne {old.get('joueur')!r}, pas {joueur!r}. "
            "Utilisez un dossier distinct pour chaque bot."
        )
    raw = old.get("parties", {})
    if isinstance(raw, list):
        # Compatibilité avec anciens collecteurs : ne les utilise pas aveuglément.
        raw = {p["id"]: p for p in raw if isinstance(p, dict) and p.get("id")}
    return {"format": 2, "joueur": joueur, "parties": raw, "non_bot": old.get("non_bot", [])}


def importer_captures(paths: list[Path], archive: dict, nom_bot: str, revision: str) -> tuple[int, int]:
    ajoutees = 0
    consultees = 0
    for chemin in paths:
        ancien = lire_json(chemin)
        if not isinstance(ancien.get("parties"), list):
            print(f"[IMPORT] {chemin}: pas un ancien export contenant une liste de parties")
            continue
        for p in ancien["parties"]:
            if not isinstance(p, dict):
                continue
            url = _valeur_texte(p.get("url"))
            if not est_url_partie(url):
                continue
            consultees += 1
            id_ = identifiant_partie(url)
            if id_ in archive["parties"]:
                continue
            data = jeu_depuis_html(p.get("html", ""))
            if data is None:
                continue
            stats = statistiques_jeu(data, url, nom_bot, revision)
            if stats is not None:
                archive["parties"][id_] = stats
                ajoutees += 1
    return ajoutees, consultees


def urls_accueil(page) -> tuple[list[dict], str]:
    """Parcourt les liens de l'index. La validation du joueur se fait dans les pages."""
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    liens = page.locator("a[href]").evaluate_all("""items => items.map(a => ({
       url: a.href,
       label: (a.innerText || '').trim(),
       contexte: ((a.closest('tr') || a.closest('li') || a.parentElement)?.innerText || '').trim().slice(0, 500)
    }))""")
    result = []
    seen = set()
    for lien in liens:
        url = lien.get("url", "")
        if est_url_partie(url) and url not in seen:
            result.append({"url": url, "contexte": lien.get("contexte", "")})
            seen.add(url)
    return result, page.locator("body").inner_text()[:30000]

def collecte_cycle(page, archive: dict, nom_bot: str, revision: str,
                   sauvegarder_brut: bool, dossier: Path,
                   delai_ms: int = 10000) -> tuple[int, int, int]:
    liens, accueil = urls_accueil(page)
    (dossier / "classement_et_historique.txt").write_text(accueil, encoding="utf-8")
    nouvelles = 0
    examinees = 0
    non_lisibles = 0
    exclus = set(archive.get("non_bot", []))
    
    for item in liens:
        url = item["url"]
        id_ = identifiant_partie(url)
        if id_ in archive["parties"] or id_ in exclus:
            continue
            
        # NOUVEAU FILTRE SOUPLE : On accepte le lien si le nom du bot est simplement PRÉSENT dans la ligne
        ctx = item.get("contexte", "").casefold()
        if nom_bot.casefold() not in ctx:
            continue
            
        examinees += 1
        try:
            r = page.context.request.get(url, timeout=delai_ms)
            if not r.ok:
                non_lisibles += 1
                continue
            html = r.text()
            data = jeu_depuis_html(html)
            if data is None:
                non_lisibles += 1
                continue
            
            stats = statistiques_jeu(data, url, nom_bot, revision)
            if stats is None:
                exclus.add(id_)
                continue
                
            archive["parties"][id_] = stats
            nouvelles += 1
            if sauvegarder_brut:
                rawdir = dossier / "donnees_brutes"
                rawdir.mkdir(exist_ok=True)
                with gzip.open(rawdir / f"{id_}.json.gz", "wt", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False)
        except Exception as exc:
            non_lisibles += 1
            print(f"  ! Lecture impossible {id_}: {type(exc).__name__}: {exc}")
            
    archive["non_bot"] = sorted(exclus)
    return nouvelles, examinees, non_lisibles

def intervalle_wilson(succes: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    if n <= 0:
        return None
    p = succes / n
    den = 1 + z * z / n
    mid = (p + z*z/(2*n)) / den
    rad = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / den
    return max(0, mid-rad), min(1, mid+rad)


def moyenne(values: list[float | int | None]) -> float | None:
    numeric = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return round(statistics.mean(numeric), 2) if numeric else None


def pct(p: float | None) -> str:
    return f"{100*p:.1f} %" if p is not None else "n/d"


def fnum(x: float | int | None) -> str:
    return f"{x}" if x is not None else "n/d"


def bilan(archive: dict, cible: int, revision: str) -> str:
    jeux = sorted(archive["parties"].values(), key=lambda x: x.get("date") or "", reverse=True)
    n = len(jeux)
    revisions_presentes = sorted({x.get("revision", "inconnue") for x in jeux})
    complets = [x for x in jeux if x.get("premiere_place") is not None and x.get("rang") is not None]
    g = len(complets)
    premiers = sum(x["premiere_place"] for x in complets)
    seuls = sum(x["victoire_seule"] for x in complets)
    intervalle = intervalle_wilson(premiers, g)
    by_n = defaultdict(list)
    for x in complets: by_n[x["nb_joueurs"]].append(x)
    all_buys = Counter()
    all_actions = Counter()
    all_trash = Counter()
    all_hooks = Counter()
    total_warnings = 0
    for x in jeux:
        all_buys.update(x.get("achats", {}))
        all_actions.update(x.get("actions_jouees", {}))
        all_trash.update(x.get("destructions_observees", {}))
        all_hooks.update(x.get("appels_hooks", {}))
        total_warnings += len(x.get("erreurs_du_bot", []))

    lines = [
        "# Bilan stratégique Dopynion — Toulousain test", "",
        f"**Étiquette de collecte :** {revision}  ",
        f"**Versions dans l'historique :** {', '.join(revisions_presentes) or 'aucune'}  ",
        f"**Rapport généré :** {datetime.now().astimezone().isoformat(timespec='seconds')}  ",
        f"**Objectif :** {cible} parties de ce bot ; **collectées :** {n}  ",
        "", "## Qualité de l'échantillon", "",
        f"- Parties validées via `dop-game-data.players` : **{n}** (aucune partie d'un homonyme).",
        "- Le champ `revision` est celui fourni au collecteur ; il ne prouve pas quelle version tournait lors d'un ancien match importé.",
        f"- Résultats exploitables : **{g}**.",
        f"- Premières places (y compris éventuelles égalités) : **{premiers}/{g} = {pct(premiers/g if g else None)}**.",
        f"- Victoires sans égalité : **{seuls}/{g}**.",
        f"- Intervalle indicatif 95 % de la proportion de premières places (Wilson) : **{f'{pct(intervalle[0])} à {pct(intervalle[1])}' if intervalle else 'n/d'}**.",
        "- Cet intervalle ne corrige pas les différences de nombre d'adversaires, de qualité des adversaires ou de version du bot.",
        f"- Score moyen final : **{fnum(moyenne([x.get('score_bot') for x in jeux]))}** ; rang moyen : **{fnum(moyenne([x.get('rang') for x in jeux]))}**.",
        f"- Tours moyens du bot : **{fnum(moyenne([x.get('tours_bot') for x in jeux]))}**.",
        f"- Tours sans achat (moyenne/partie) : **{fnum(moyenne([x.get('tours_sans_achat') for x in jeux]))}**.",
        f"- Tour moyen du premier Or : **{fnum(moyenne([x.get('premier_or_tour') for x in jeux]))}** (uniquement si acheté).",
        f"- Tour moyen de la première Province : **{fnum(moyenne([x.get('premiere_province_tour') for x in jeux]))}** (uniquement si achetée).",
        f"- Écart moyen avec la première Province des adversaires : **{fnum(moyenne([x.get('ecart_tour_premiere_province') for x in jeux]))} tours** (positif = notre bot démarre plus tard).",
        "", "## Par taille de partie", "",
        "| Joueurs | Parties | Premières places | Taux | Score moyen | Rang moyen |", "|---:|---:|---:|---:|---:|---:|",
    ]
    for nb, games in sorted(by_n.items()):
        v = sum(x["premiere_place"] for x in games)
        lines.append(f"| {nb} | {len(games)} | {v} | {pct(v/len(games))} | {fnum(moyenne([x['score_bot'] for x in games]))} | {fnum(moyenne([x['rang'] for x in games]))} |")
    lines += ["", "## Achats et actions observés", "",
              "| Carte achetée | Total | Par partie |", "|---|---:|---:|"]
    for card, count in all_buys.most_common():
        lines.append(f"| {card} | {count} | {count/max(1,n):.2f} |")
    lines += ["", "| Carte Action jouée | Total |", "|---|---:|"]
    for card, count in all_actions.most_common():
        lines.append(f"| {card} | {count} |")
    lines += ["", "## Signaux de faiblesse à examiner", ""]
    alertes = [
        ("Au moins 6 Argent achetés", lambda x: x.get("achats", {}).get("silver", 0) >= 6),
        ("Aucun Or acheté", lambda x: x.get("achats", {}).get("gold", 0) == 0),
        ("Aucune Province achetée", lambda x: x.get("achats", {}).get("province", 0) == 0),
        ("Au moins 4 tours sans achat", lambda x: x.get("tours_sans_achat", 0) >= 4),
        ("Première Province après le tour 12", lambda x: x.get("premiere_province_tour") is not None and x["premiere_province_tour"] > 12),
        ("Plus lent que le premier adversaire sur les Provinces", lambda x: x.get("ecart_tour_premiere_province") is not None and x["ecart_tour_premiere_province"] > 0),
    ]
    for label, condition in alertes:
        subset = [x for x in complets if condition(x)]
        nb = len(subset)
        premieres_alertes = sum(x["premiere_place"] for x in subset)
        lines.append(f"- **{label}** : {nb}/{g} parties ; {premieres_alertes} premières places ({pct(premieres_alertes/nb if nb else None)}).")
    lines += ["", "## Destructions et interactions", "",
              "| Carte détruite (réponses de hook confirmées) | Total |", "|---|---:|"]
    for card, count in all_trash.most_common():
        lines.append(f"| {card} | {count} |")
    lines += ["", "### Hooks reçus par le bot", "", "| Hook Dopynion | Nombre d'appels |", "|---|---:|"]
    for h, count in all_hooks.most_common():
        lines.append(f"| `{h}` | {count} |")
    lines += ["", f"- Erreurs explicitement attribuées au bot : **{total_warnings}**.",
              "- Les gains automatiques ne sont pas toujours traçables ; `cartes_recues_choisies` concerne seulement les gains décidés via un hook.",
              "", "## Comparaison descriptive : achat d'une carte et première place", "",
              "Attention : **corrélation, pas causalité**. Acheter une carte peut être la conséquence d'une bonne main, et non sa cause.",
              "Afficher une association seulement si au moins 15 parties contiennent cette carte ET 15 n'en contiennent pas.",
              "", "| Carte | Parties avec | 1res places avec | Parties sans | 1res places sans |", "|---|---:|---:|---:|---:|"]
    cartes = Counter(k for x in complets for k, num in x.get("achats", {}).items() if num)
    for card, withcount in cartes.most_common():
        if withcount < 15 or g-withcount < 15:
            continue
        withs = [x for x in complets if x.get("achats", {}).get(card, 0) > 0]
        without = [x for x in complets if x.get("achats", {}).get(card, 0) == 0]
        w = sum(x["premiere_place"] for x in withs)
        wo = sum(x["premiere_place"] for x in without)
        lines.append(f"| {card} | {len(withs)} | {pct(w/len(withs))} | {len(without)} | {pct(wo/len(without))} |")
    lines += ["", "## Matchs où le bot termine dernier / sans Province", "",
              "| Date | Joueurs | Rang | Score | Tours sans achat | Argent achetés | Province achetées | Lien |",
              "|---|---:|---:|---:|---:|---:|---:|---|"]
    pires = [x for x in jeux if x.get("rang") == x.get("nb_joueurs") or x.get("achats", {}).get("province", 0) == 0]
    for x in pires[:40]:
        lines.append(f"| {x.get('date','')} | {x['nb_joueurs']} | {fnum(x.get('rang'))} | {fnum(x.get('score_bot'))} | {x.get('tours_sans_achat')} | {x.get('achats',{}).get('silver',0)} | {x.get('achats',{}).get('province',0)} | [match]({x['url']}) |")
    lines += ["", "## Points à investiguer", "",
              "- Si beaucoup de tours sans achat : examiner les actions, les ressources et l'épuration du deck.",
              "- Si zéro Province achetée : comparer l'économie, la durée du match et la pression adverse.",
              "- Si trop d'Argent en fin de partie : réduire les achats économiques après le milieu de partie.",
              "- Si un type de partie perd souvent (2, 3 ou 4 joueurs) : régler l'agressivité et le moment de la course aux points.",
              "- Si les hooks renvoient des erreurs : corriger l'API avant de retoucher les scores.",
              "", "## Limites", "",
              "- Les matchs collectés sont observationnels et ne contrôlent pas les différences de configuration ni d'adversaires.",
              "- La collecte ne reconstruit pas parfaitement le deck ; les entrées `h` du journal ne sont que des instantanés de main.",
              "- Une version du bot peut changer pendant la collecte : renseigner `--revision` et utiliser un dossier distinct.",
              "- L'historique public accessible peut être limité. Utiliser `--suivi` pour accumuler les nouveaux matchs, sans promettre une récupération instantanée de 300 parties.",
              "- Les achats enregistrés ne comprennent pas tous les gains automatiques de cartes.",
    ]
    return "\n".join(lines)+"\n"


def csv_export(archive: dict, dossier: Path) -> None:
    games = sorted(archive["parties"].values(), key=lambda x: x.get("date") or "", reverse=True)
    cols = ["date", "revision", "nb_joueurs", "rang", "score_bot", "premiere_place", "victoire_seule", "tours_bot", "tours_sans_achat", "premier_or_tour", "premiere_province_tour", "premiere_province_adverse_tour", "ecart_tour_premiere_province", "url"]
    with (dossier / "parties.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for x in games:
            w.writerow({c: x.get(c) for c in cols})
    with (dossier / "achats_par_partie.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "date", "revision", "rang", "nb_joueurs", "carte", "quantite", "tour_premiere_province"])
        for x in games:
            for card, count in x.get("achats", {}).items():
                w.writerow([x["id"], x.get("date"), x.get("revision"), x.get("rang"), x.get("nb_joueurs"), card, count, x.get("premiere_province_tour")])


def sauver_tout(archive: dict, dossier: Path, cible: int, revision: str) -> None:
    archive["maj"] = datetime.now().astimezone().isoformat(timespec="seconds")
    ecrire_json(dossier / NOM_JSON, archive)
    (dossier / NOM_RAPPORT).write_text(bilan(archive, cible, revision), encoding="utf-8")
    csv_export(archive, dossier)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Statistiques exactes des parties de Toulousain test")
    parser.add_argument("--nombre", type=int, default=NOMBRE_CIBLE, help="Objectif de parties propres (défaut : 300)")
    parser.add_argument("--joueur", default=BOT_NOM)
    parser.add_argument("--dossier", default=DOSSIER_DEFAUT)
    parser.add_argument("--revision", default="version_non_precisee", help="Version du bot actuellement déployée")
    parser.add_argument("--suivi", action="store_true", help="Revérifie régulièrement l'index jusqu'à atteindre l'objectif")
    parser.add_argument("--intervalle", type=int, default=60, help="Secondes entre deux scans en mode --suivi (minimum 30)")
    parser.add_argument("--importer", nargs="+", type=Path, help="Relit les anciennes captures JSON sans connexion internet")
    parser.add_argument("--brut", action="store_true", help="Enregistre également chaque dop-game-data en JSON.gz")
    args = parser.parse_args(argv)
    if not 1 <= args.nombre <= 10000:
        parser.error("--nombre doit être compris entre 1 et 10000")
    if args.suivi and args.intervalle < 30:
        parser.error("--intervalle doit être d'au moins 30 secondes")
    if args.importer and args.suivi:
        parser.error("--importer et --suivi ne peuvent pas être combinés")
    dossier = Path(args.dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    archive = charger_archive(dossier / NOM_JSON, args.joueur)
    archive["revision_collecte"] = args.revision

    if args.importer:
        ajoutees, vues = importer_captures(args.importer, archive, args.joueur, args.revision)
        sauver_tout(archive, dossier, args.nombre, args.revision)
        print(f"Anciennes pages examinées : {vues} ; nouvelles parties de {args.joueur} : {ajoutees}")
        print(f"Total conservé : {len(archive['parties'])}. Rapport : {dossier / NOM_RAPPORT}")
        return 0

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        parser.error("Playwright absent : pip install playwright beautifulsoup4")

    print(f"Objectif : {args.nombre} parties de {args.joueur} ; déjà conservées : {len(archive['parties'])}.")
    print("Le site n'affiche pas nécessairement autant de parties à la fois. --suivi permet de les accumuler.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(locale="fr-FR")
        page = context.new_page()
        cycle = 0
        try:
            while True:
                cycle += 1
                try:
                    nouvelles, examinees, erreurs = collecte_cycle(
                        page, archive, args.joueur, args.revision, args.brut, dossier
                    )
                except Exception as exc:
                    nouvelles, examinees, erreurs = 0, 0, 1
                    print(f"[Cycle {cycle}] Erreur sur la page d'accueil : {type(exc).__name__} : {exc}")
                sauver_tout(archive, dossier, args.nombre, args.revision)
                n = len(archive["parties"])
                print(f"[Cycle {cycle}] pages examinées={examinees}, nouvelles parties bot={nouvelles}, erreurs={erreurs}, total={n}/{args.nombre}")
                if n >= args.nombre:
                    print("Objectif atteint. Le rapport et les CSV sont prêts.")
                    break
                if not args.suivi:
                    print("Instantané terminé. Relancez plus tard ou utilisez --suivi pour cumuler les nouvelles parties.")
                    break
                time.sleep(args.intervalle)
        except KeyboardInterrupt:
            print("Arrêt demandé : les données déjà analysées sont conservées.")
        finally:
            sauver_tout(archive, dossier, args.nombre, args.revision)
            browser.close()
    print(f"Résultats : {dossier / NOM_RAPPORT}, {dossier / NOM_JSON}, {dossier / 'parties.csv'}, {dossier / 'achats_par_partie.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
