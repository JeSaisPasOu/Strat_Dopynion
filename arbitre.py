import requests
import random
import time

# Configuration de l'API
API_URL = "http://127.0.0.1:8000"
GAME_ID = "simu-test-001"
HEADERS = {"x-game-id": GAME_ID, "Content-Type": "application/json"}

# Définition des cartes et de leur coût/valeur
CARTES = {
    "Copper": {"cost": 0, "val_money": 1, "val_pv": 0, "type": "treasure"},
    "Silver": {"cost": 3, "val_money": 2, "val_pv": 0, "type": "treasure"},
    "Gold":   {"cost": 6, "val_money": 3, "val_pv": 0, "type": "treasure"},
    "Estate": {"cost": 2, "val_money": 0, "val_pv": 1, "type": "victory"},
    "Duchy":  {"cost": 5, "val_money": 0, "val_pv": 3, "type": "victory"},
    "Province":{"cost": 8, "val_money": 0, "val_pv": 6, "type": "victory"},
}

class ArbitreDominion:
    def __init__(self):
        # 1. Initialisation du marché (Stock)
        self.stock = {
            "Copper": 60, "Silver": 40, "Gold": 30,
            "Estate": 8, "Duchy": 8, "Province": 8
        }
        
        # 2. Initialisation du deck du joueur (7 Cuivres, 3 Domaines)
        self.deck = ["Copper"] * 7 + ["Estate"] * 3
        random.shuffle(self.deck)
        self.hand = []
        self.discard = []
        self.score = 3  # 3 Domaines au départ = 3 PV
        
    def draw_cards(self, n):
        """Pioche n cartes. Mélange la défausse si le deck est vide."""
        for _ in range(n):
            if not self.deck:
                if not self.discard:
                    break
                self.deck = self.discard.copy()
                random.shuffle(self.deck)
                self.discard = []
            self.hand.append(self.deck.pop())

    def get_money_in_hand(self):
        """Calcule l'argent total généré par les cartes trésor de la main."""
        return sum(CARTES[c]["val_money"] for c in self.hand if CARTES[c]["type"] == "treasure")

    def run_game(self):
        print("=== DÉBUT DE LA PARTIE ===")
        # Appel GET /start_game
        requests.get(f"{API_URL}/start_game", headers=HEADERS)
        
        # Piocher la main de départ (5 cartes)
        self.draw_cards(5)
        
        tour = 1
        # Au lieu de : while self.stock["Province"] > 0:
        while self.stock["Province"] > 0 and tour <= 5:
            print(f"\n--- TOUR {tour} ---")
            print(f"Main : {self.hand} | Défausse : {len(self.discard)} | Deck : {len(self.deck)}")
            
            # Appel GET /start_round (ou /start_turn selon votre API)
            requests.get(f"{API_URL}/start_turn", headers=HEADERS)
            
            tour_en_cours = True
            while tour_en_cours:
                payload = {
                    "is_finished": False,
                    "players": [
                        {
                            "name": "BotToulousain",
                            "score": self.score,
                            "hand": self.hand,
                            "discard_pile": self.discard, # Souvent requis
                            "deck_size": len(self.deck)   # Souvent requis
                        }
                    ],
                    "stock": self.stock
                }
                
                # Appel POST /play
                try:
                    rep = requests.post(f"{API_URL}/play", headers=HEADERS, json=payload)
                    rep.raise_for_status()
                    decision = rep.json().get("decision", "END_TURN")
                except Exception as e:
                    print(f"Erreur API : {e}")
                    decision = "END_TURN"

                print(f">> L'API décide : {decision}")
                
                # Traitement de la décision
                if decision == "END_TURN":
                    tour_en_cours = False
                    
                elif decision.startswith("BUY "):
                    carte_achetee = decision.split(" ")[1]
                    money_dispo = self.get_money_in_hand()
                    
                    if carte_achetee not in self.stock:
                        print(f"  [!] Achat refusé : {carte_achetee} n'existe pas.")
                        tour_en_cours = False
                    elif self.stock[carte_achetee] <= 0:
                        print(f"  [!] Achat refusé : Rupture de stock pour {carte_achetee}.")
                        tour_en_cours = False
                    elif CARTES[carte_achetee]["cost"] > money_dispo:
                        print(f"  [!] Achat refusé : Fonds insuffisants ({money_dispo} dispo, coûte {CARTES[carte_achetee]['cost']}).")
                        tour_en_cours = False
                    else:
                        # Validation de l'achat
                        self.stock[carte_achetee] -= 1
                        self.discard.append(carte_achetee)
                        print(f"  [+] Achat réussi : {carte_achetee}")
                        tour_en_cours = False # On suppose 1 seul achat par tour par défaut
                        
                elif decision.startswith("ACTION "):
                    print("  [i] Carte action jouée (Logique à implémenter)")
                    # À compléter si vous ajoutez des cartes Action (Village, Forgeron...)
                    
                time.sleep(0.5) # Pause pour lire les logs

            # Fin du tour : nettoyage de la main et nouvelle pioche
            self.discard.extend(self.hand)
            self.hand = []
            self.draw_cards(5)
            tour += 1

        # Fin de partie
        print("\n=== FIN DE PARTIE (Plus de Provinces) ===")
        requests.get(f"{API_URL}/end_game", headers=HEADERS)

if __name__ == "__main__":
    simu = ArbitreDominion()
    simu.run_game()