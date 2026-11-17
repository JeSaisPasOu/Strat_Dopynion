
# -*- coding: utf-8 -*-
"""
ANALYSEUR DOPYNION - TOULOUSAIN TEST
Récupère les dernières parties, les pages HTML, les textes
et les réponses JSON chargées par JavaScript.

Installation :
pip install requests beautifulsoup4 playwright
playwright install chromium

Lancement :
python analyser_dopynion.py

Options :
python analyser_dopynion.py --nombre 20
python analyser_dopynion.py --joueur "Toulousain test"
"""

import argparse
import json
import re
import time
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://dopynion.lecalamar.fr/"
BOT_URL = "https://alves.alwaysdata.net/"

NOM_BOT = "Toulousain test"
NOMBRE_PARTIES = 50

DOSSIER = Path("analyse_dopynion")
DOSSIER_BRUT = DOSSIER / "pages_brutes"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/130 Safari/537.36"
)

# ============================================================
# OUTILS
# ============================================================

def nettoyer(texte):
    return re.sub(r"\s+", " ", str(texte or "")).strip()


def sauvegarder_json(chemin, donnees):
    chemin.write_text(
        json.dumps(donnees, indent=4, ensure_ascii=False, default=str),
        encoding="utf-8"
    )


def nom_fichier(url):
    nom = url.split("/")[-1]
    nom = re.sub(r"[^a-zA-Z0-9_.-]", "_", nom)
    return nom[:120] or "partie"


def est_lien_partie(url):
    return bool(re.search(r"game__.*\.html", url, re.IGNORECASE))


# ============================================================
# COLLECTE DE LA PAGE D'ACCUEIL
# ============================================================

def recuperer_parties(page, nom_bot, nombre):

    print("\n[1/3] Chargement du classement et de l'historique...")

    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)

    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except Exception:
        pass

    page.wait_for_timeout(2000)

    texte_page = page.locator("body").inner_text()
    html = page.content()

    # Sauvegarde du contenu de la page pour diagnostic
    (DOSSIER / "page_accueil.html").write_text(html, encoding="utf-8")
    (DOSSIER / "page_accueil.txt").write_text(texte_page, encoding="utf-8")

    liens = page.locator("a[href]").evaluate_all(
        """elements => elements.map(a => ({
            href: a.href,
            texte: a.innerText || '',
            parent: a.parentElement?.parentElement?.innerText || ''
        }))"""
    )

    parties = []
    deja_vues = set()

    for lien in liens:

        url = lien.get("href", "")

        if not est_lien_partie(url):
            continue

        contexte = nettoyer(
            lien.get("texte", "") + " " + lien.get("parent", "")
        )

        # On vérifie que le joueur recherché apparaît dans le bloc
        # associé au lien de partie.
        if nom_bot.casefold() not in contexte.casefold():
            continue

        if url in deja_vues:
            continue

        deja_vues.add(url)

        parties.append({
            "url": url,
            "texte_lien": nettoyer(lien.get("texte")),
            "contexte": contexte,
            "accessible": False,
            "erreur": None,
            "texte_partie": "",
            "json": [],
            "joueurs_detectes": [],
            "indices": {}
        })

        if len(parties) >= nombre:
            break

    print(f"    {len(parties)} partie(s) trouvée(s).")

    return parties, texte_page


# ============================================================
# CAPTURE DES DONNEES JSON
# ============================================================

def installer_capture_json(page, stockage):

    def intercepter(response):

        try:
            content_type = response.headers.get(
                "content-type", ""
            ).lower()

            if "json" not in content_type:
                return

            if response.status >= 400:
                return

            contenu = response.json()

            stockage.append({
                "url": response.url,
                "status": response.status,
                "json": contenu
            })

        except Exception:
            pass

    page.on("response", intercepter)


# ============================================================
# ANALYSE DES PAGES DE PARTIES
# ============================================================

def analyser_indices(texte, donnees_json):

    contenu = texte.lower()

    for element in donnees_json:
        contenu += " " + json.dumps(
            element.get("json", {}),
            ensure_ascii=False,
            default=str
        ).lower()

    indices = {
        "score": bool(re.search(
            r"\b(score|points?|victory points|vp)\b", contenu
        )),
        "gagnant": bool(re.search(
            r"\b(winner|victor|gagnant|victoire|won)\b", contenu
        )),
        "tours": bool(re.search(
            r"\b(turn|tour|round)\b", contenu
        )),
        "achats": bool(re.search(
            r"\b(bought|purchase|buy|achat|acheté)\b", contenu
        )),
        "destructions": bool(re.search(
            r"\b(trash|trashed|destroy|détruit|détruire)\b", contenu
        )),
        "defausses": bool(re.search(
            r"\b(discard|discarded|défausse|défaussé)\b", contenu
        )),
        "cartes": bool(re.search(
            r"\b(card|carte|deck|hand)\b", contenu
        ))
    }

    return indices


def collecter_partie(page, partie, numero):

    url = partie["url"]

    print(f"\n    Partie {numero} : {url}")

    stockage_json = []
    installer_capture_json(page, stockage_json)

    try:

        reponse = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        try:
            page.wait_for_load_state("networkidle", timeout=12000)
        except Exception:
            pass

        page.wait_for_timeout(2000)

        partie["http_status"] = (
            reponse.status if reponse else None
        )

        partie["accessible"] = bool(
            reponse and reponse.ok
        )

        partie["titre"] = page.title()

        partie["texte_partie"] = page.locator(
            "body"
        ).inner_text()[:100000]

        partie["html"] = page.content()

        partie["json"] = stockage_json

        partie["joueurs_detectes"] = [
            ligne.strip()
            for ligne in partie["texte_partie"].splitlines()
            if partie.get("contexte", "").casefold() in ligne.casefold()
        ]

        partie["indices"] = analyser_indices(
            partie["texte_partie"],
            stockage_json
        )

        # Sauvegarde individuelle des données brutes
        prefixe = f"{numero:02d}_{nom_fichier(url)}"

        (DOSSIER_BRUT / f"{prefixe}.txt").write_text(
            partie["texte_partie"],
            encoding="utf-8"
        )

        (DOSSIER_BRUT / f"{prefixe}.html").write_text(
            partie["html"],
            encoding="utf-8"
        )

        sauvegarder_json(
            DOSSIER_BRUT / f"{prefixe}.json",
            stockage_json
        )

        print(
            "       Accessible :", partie["accessible"],
            "| Réponses JSON :", len(stockage_json)
        )

    except Exception as erreur:

        partie["accessible"] = False
        partie["erreur"] = str(erreur)

        print("       ERREUR :", erreur)

    return partie


# ============================================================
# EXTRACTION DES VALEURS JSON
# ============================================================

def extraire_valeurs_cartes(objet, chemin="$", resultat=None):

    if resultat is None:
        resultat = []

    if isinstance(objet, dict):

        for cle, valeur in objet.items():

            nouveau_chemin = f"{chemin}.{cle}"

            if isinstance(valeur, (str, int, float)):
                resultat.append({
                    "chemin": nouveau_chemin,
                    "valeur": valeur
                })

            extraire_valeurs_cartes(
                valeur,
                nouveau_chemin,
                resultat
            )

    elif isinstance(objet, list):

        for index, valeur in enumerate(objet[:5000]):

            extraire_valeurs_cartes(
                valeur,
                f"{chemin}[{index}]",
                resultat
            )

    return resultat


# ============================================================
# GENERATION DU RAPPORT
# ============================================================

def generer_rapport(donnees):

    parties = donnees["parties"]

    lignes = []

    lignes.append("# ANALYSE DOPYNION")
    lignes.append("# TOULOUSAIN TEST")
    lignes.append("")

    lignes.append(
        f"Date de collecte : {donnees['date_collecte']}"
    )

    lignes.append(f"Bot : {NOM_BOT}")
    lignes.append(f"URL : {BOT_URL}")
    lignes.append("")

    lignes.append("## 1. Résumé")
    lignes.append("")

    accessibles = sum(
        1 for p in parties if p["accessible"]
    )

    lignes.append(f"- Parties trouvées : {len(parties)}")
    lignes.append(f"- Pages accessibles : {accessibles}")
    lignes.append(
        f"- Pages non accessibles : {len(parties) - accessibles}"
    )

    lignes.append("")
    lignes.append("## 2. Détail des parties")
    lignes.append("")

    for i, partie in enumerate(parties, 1):

        lignes.append(f"### Partie {i}")
        lignes.append("")

        lignes.append(f"- URL : {partie['url']}")
        lignes.append(f"- Contexte : {partie['contexte']}")
        lignes.append(f"- Accessible : {partie['accessible']}")

        if partie.get("erreur"):
            lignes.append(f"- Erreur : {partie['erreur']}")

        if partie.get("http_status"):
            lignes.append(
                f"- Statut HTTP : {partie['http_status']}"
            )

        lignes.append(
            f"- Réponses JSON : {len(partie['json'])}"
        )

        lignes.append("- Indices détectés :")

        for nom, valeur in partie["indices"].items():
            lignes.append(f"  - {nom} : {'oui' if valeur else 'non'}")

        lignes.append("")
        lignes.append("**Texte de la partie :**")
        lignes.append("")

        extrait = partie["texte_partie"][:3000]

        lignes.append(extrait or "Aucun texte récupéré.")
        lignes.append("")
        lignes.append("---")
        lignes.append("")

    lignes.append("## 3. Limites de l'analyse")
    lignes.append("")
    lignes.append(
        "Les indices détectés indiquent la présence de certains "
        "termes, pas nécessairement des actions réellement exécutées."
    )
    lignes.append(
        "Les statistiques d'achats, de destructions et de scores "
        "ne seront fiables qu'après identification du format réel "
        "des historiques JSON du site."
    )
    lignes.append(
        "Le script ne modifie aucun fichier de stratégie du bot."
    )

    return "\n".join(lignes)


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():

    global NOM_BOT, NOMBRE_PARTIES

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--nombre",
        type=int,
        default=NOMBRE_PARTIES
    )

    parser.add_argument(
        "--joueur",
        type=str,
        default=NOM_BOT
    )

    args = parser.parse_args()

    if not 1 <= args.nombre <= 100:
        parser.error("--nombre doit être entre 1 et 100")

    NOM_BOT = args.joueur
    NOMBRE_PARTIES = args.nombre

    DOSSIER.mkdir(exist_ok=True)
    DOSSIER_BRUT.mkdir(exist_ok=True)

    print("=" * 60)
    print(" ANALYSEUR DOPYNION - TOULOUSAIN TEST")
    print("=" * 60)

    with sync_playwright() as p:

        navigateur = p.chromium.launch(
            headless=True
        )

        contexte = navigateur.new_context(
            user_agent=USER_AGENT,
            viewport={"width": 1440, "height": 1000}
        )

        page = contexte.new_page()

        try:

            parties, texte_accueil = recuperer_parties(
                page,
                NOM_BOT,
                NOMBRE_PARTIES
            )

        except Exception as erreur:

            print("\nErreur lors du chargement de l'accueil :", erreur)
            navigateur.close()
            return

        for index, partie in enumerate(parties, 1):

            collecter_partie(
                page,
                partie,
                index
            )

            time.sleep(0.5)

        navigateur.close()

    donnees = {
        "date_collecte": datetime.now().astimezone().isoformat(),
        "joueur": NOM_BOT,
        "bot_url": BOT_URL,
        "page_accueil": texte_accueil[:30000],
        "parties": parties
    }

    # Fichier principal avec toutes les données récupérées
    sauvegarder_json(
        DOSSIER / "10_dernieres_parties.json",
        donnees
    )

    # Rapport lisible
    rapport = generer_rapport(donnees)

    (DOSSIER / "bilan_10_parties.md").write_text(
        rapport,
        encoding="utf-8"
    )

    print("\n" + "=" * 60)
    print(" COLLECTE TERMINEE")
    print("=" * 60)

    print("\nFichiers créés :")
    print(" - analyse_dopynion/10_dernieres_parties.json")
    print(" - analyse_dopynion/bilan_10_parties.md")
    print(" - analyse_dopynion/pages_brutes/")

    print("\nTu peux maintenant m'envoyer ces deux fichiers.")


if __name__ == "__main__":
    main()
