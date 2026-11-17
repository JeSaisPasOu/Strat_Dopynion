import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

BASE_URL = "https://dopynion.lecalamar.fr/"
BOT_NAME = "Toulousain test"

def recuperer_statistiques():
    print(f"🔍 Récupération de la page principale : {BASE_URL}")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Erreur de connexion au site : {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. Cibler spécifiquement la section "Last games"
    titre_last_games = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3'] and 'Last games' in tag.get_text())
    
    if not titre_last_games:
        print("❌ Section 'Last games' introuvable sur la page d'accueil.")
        return

    liste_globale = titre_last_games.find_next('ul')
    
    liens_parties = []
    for li in liste_globale.find_all('li'):
        a_tag = li.find('a')
        if a_tag and BOT_NAME in li.text:
            lien_relatif = a_tag['href']
            lien_absolu = urljoin(BASE_URL, lien_relatif)
            liens_parties.append(lien_absolu)

    # 2. Limiter aux 10 dernières parties
    liens_parties = liens_parties[:10]

    print(f"✅ {len(liens_parties)} parties récentes trouvées pour '{BOT_NAME}'. Analyse en cours...\n")

    stats = {
        "jouees": 0,
        "victoires": 0,
        "second": 0,
        "defaites": 0,
        "total_points": 0
    }

    # 3. Analyser chaque partie
    for url_partie in liens_parties:
        try:
            req = requests.get(url_partie)
            game_soup = BeautifulSoup(req.text, 'html.parser')
            
            # Utiliser un dictionnaire pour écraser les scores intermédiaires et garder le score final
            scores_finaux_dict = {}
            
            # On scanne directement TOUS les éléments <li> de la page
            for li in game_soup.find_all('li'):
                # Nettoyage vital : on remplace les espaces HTML invisibles (\xa0) par des espaces standards
                texte = li.get_text(strip=True).replace('\xa0', ' ')
                
                # On ignore les annonces de score en cours de jeu
                if "pour l'instant" in texte:
                    continue
                    
                # Recherche du pattern du score final
                match = re.search(r'(.*?)\s+a un score de\s+(-?\d+)', texte, re.IGNORECASE)
                if match:
                    joueur = match.group(1).strip()
                    score = int(match.group(2))
                    scores_finaux_dict[joueur] = score

            if not scores_finaux_dict:
                print(f"⚠️ Impossible d'extraire les scores dans {url_partie}")
                continue

            # Convertir le dictionnaire final en liste et le trier du meilleur au pire score
            scores_partie = [{'joueur': j, 'score': s} for j, s in scores_finaux_dict.items()]
            scores_partie.sort(key=lambda x: x['score'], reverse=True)

            # S'assurer que le nom du bot correspond bien (parfois il y a des espaces en trop)
            bot_exact_name = None
            for d in scores_partie:
                if BOT_NAME in d['joueur']:
                    bot_exact_name = d['joueur']
                    break

            if not bot_exact_name:
                print(f"⚠️ Le bot '{BOT_NAME}' n'a pas été trouvé dans le classement final de {url_partie}")
                continue

            # 4. Enregistrer la performance
            for rang, data in enumerate(scores_partie):
                if data['joueur'] == bot_exact_name:
                    stats["jouees"] += 1
                    stats["total_points"] += data['score']
                    
                    if rang == 0:
                        stats["victoires"] += 1
                    elif rang == 1:
                        stats["second"] += 1
                    else:
                        stats["defaites"] += 1

        except Exception as e:
            print(f"⚠️ Erreur technique lors de l'analyse de {url_partie} : {e}")

    # 5. Affichage du bilan
    if stats["jouees"] > 0:
        win_rate = (stats["victoires"] / stats["jouees"]) * 100
        avg_score = stats["total_points"] / stats["jouees"]
        
        print("========================================")
        print(f"📊 BILAN DES {stats['jouees']} DERNIÈRES PARTIES : {BOT_NAME}")
        print("========================================")
        print(f"🏆 Victoires       : {stats['victoires']} ({win_rate:.1f}%)")
        print(f"🥈 Secondes places : {stats['second']}")
        print(f"💀 Défaites (3e+)  : {stats['defaites']}")
        print(f"🎯 Score moyen     : {avg_score:.1f} points par partie")
        print("========================================")
    else:
        print("\n❌ Aucune statistique n'a pu être extraite.")

if __name__ == "__main__":
    recuperer_statistiques()