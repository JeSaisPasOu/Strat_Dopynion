import requests
import random
import time

API_URL = "http://127.0.0.1:8000"
GAME_ID = "simu-test-001"
HEADERS = {"x-game-id": GAME_ID, "Content-Type": "application/json"}

<<<<<<< HEAD
# Base de données des cartes avec les valeurs en points de victoire (val_pv)
CARTES = {
=======
# Base de données des cartes avec les effets d'actions
CARTES = {
    # Trésors et Victoires
>>>>>>> simulateur
    "copper": {"cost": 0, "val_money": 1, "val_pv": 0, "type": "treasure"},
    "silver": {"cost": 3, "val_money": 2, "val_pv": 0, "type": "treasure"},
    "gold":   {"cost": 6, "val_money": 3, "val_pv": 0, "type": "treasure"},
    "estate": {"cost": 2, "val_money": 0, "val_pv": 1, "type": "victory"},
    "duchy":  {"cost": 5, "val_money": 0, "val_pv": 3, "type": "victory"},
    "province":{"cost": 8, "val_money": 0, "val_pv": 6, "type": "victory"},
<<<<<<< HEAD
    "laboratory": {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action"},
    "market": {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action"},
    "village": {"cost": 3, "val_money": 0, "val_pv": 0, "type": "action"},
    "woodcutter": {"cost": 3, "val_money": 0, "val_pv": 0, "type": "action"},
    "smithy": {"cost": 4, "val_money": 0, "val_pv": 0, "type": "action"},
    "festival": {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action"},
=======
    
    # Cartes Actions avec leurs bonus (cards, actions, buys, money)
    "village":    {"cost": 3, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 1, "plus_actions": 2, "plus_buys": 0, "plus_money": 0},
    "woodcutter": {"cost": 3, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 0, "plus_actions": 0, "plus_buys": 1, "plus_money": 2},
    "smithy":     {"cost": 4, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 3, "plus_actions": 0, "plus_buys": 0, "plus_money": 0},
    "festival":   {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 0, "plus_actions": 2, "plus_buys": 1, "plus_money": 2},
    "laboratory": {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 2, "plus_actions": 1, "plus_buys": 0, "plus_money": 0},
    "market":     {"cost": 5, "val_money": 0, "val_pv": 0, "type": "action", "plus_cards": 1, "plus_actions": 1, "plus_buys": 1, "plus_money": 1},
>>>>>>> simulateur
}

class ArbitreDominion:
    def __init__(self):
<<<<<<< HEAD
        # Stock avec les clés en minuscules
=======
>>>>>>> simulateur
        self.stock = {
            "gold": 30, "silver": 40, "copper": 60, 
            "estate": 12, "duchy": 12, "province": 12, 
            "laboratory": 10, "market": 10, "village": 10, 
            "woodcutter": 10, "smithy": 10, "festival": 10
        }
<<<<<<< HEAD
        # Deck de départ : 7 cuivres, 3 domaines (score initial de 3)
=======
>>>>>>> simulateur
        self.deck = ["copper"] * 7 + ["estate"] * 3
        random.shuffle(self.deck)
        self.hand = []
        self.discard = []
        self.score = 3
        
    def draw_cards(self, n):
        for _ in range(n):
            if not self.deck:
                if not self.discard:
                    break
                self.deck = self.discard.copy()
                random.shuffle(self.deck)
                self.discard = []
            self.hand.append(self.deck.pop())

    def get_money_in_hand(self):
        return sum(CARTES[c]["val_money"] for c in self.hand if CARTES[c]["type"] == "treasure")

    def run_game(self):
        print("=== DÉBUT DE LA PARTIE ===")
        requests.get(f"{API_URL}/start_game", headers=HEADERS)
        self.draw_cards(5)
        
        tour = 1
<<<<<<< HEAD
        # On limite toujours à 5 tours pour éviter une boucle infinie pendant les tests
        while self.stock["province"] > 0 and tour <= 5:
=======
        # La limite passe à 20 tours pour te laisser le temps de tester un moteur de pioche
        while self.stock["province"] > 0 and tour <= 20:
>>>>>>> simulateur
            print(f"\n--- TOUR {tour} ---")
            print(f"Main : {self.hand} | Défausse : {len(self.discard)} | Deck : {len(self.deck)}")
            requests.get(f"{API_URL}/start_turn", headers=HEADERS)
            
            # Initialisation des variables du tour
            tour_en_cours = True
            actions_left = 1
            buys_left = 1
            bonus_money = 0
            spent_money = 0
            played_cards = []  # Cartes jouées pendant le tour, retirées de la main
            
            while tour_en_cours:
                # 1. On compte les cartes dans la main
                hand_quantities = {}
                for card in self.hand:
                    hand_quantities[card] = hand_quantities.get(card, 0) + 1
                
                # 2. Le payload mis à jour dynamiquement
                payload = {
                    "finished": False,
                    "players": [
                        {
                            "name": "Toulousain",
                            "hand": {"quantities": hand_quantities},
                            "score": self.score
                        },
<<<<<<< HEAD
                        {
                            "name": "Adversaire 1",
                            "hand": None,
                            "score": 3
                        },
                        {
                            "name": "Adversaire 2",
                            "hand": None,
                            "score": 3
                        }
                    ],
                    "stock": {
                        "quantities": self.stock
                    }
=======
                        {"name": "Adversaire 1", "hand": None, "score": 3},
                        {"name": "Adversaire 2", "hand": None, "score": 3}
                    ],
                    "stock": {"quantities": self.stock}
>>>>>>> simulateur
                }
                
                try:
                    rep = requests.post(f"{API_URL}/play", headers=HEADERS, json=payload)
                    rep.raise_for_status()
                    decision = rep.json().get("decision", "END_TURN")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur API : {e}")
                    if hasattr(e.response, 'text'):
                        print("Détail de l'erreur :", e.response.text)
                    decision = "END_TURN"

                print(f">> L'API décide : {decision}")
                
<<<<<<< HEAD
                if decision == "END_TURN":
                    tour_en_cours = False
                elif decision.startswith("BUY "):
                    carte_achetee = decision.split(" ")[1].lower()
                    money_dispo = self.get_money_in_hand()
                    
                    if carte_achetee not in self.stock or self.stock[carte_achetee] <= 0:
                        print(f"  [!] Achat annulé : {carte_achetee} indisponible.")
                        tour_en_cours = False
                    elif CARTES[carte_achetee]["cost"] > money_dispo:
                        print(f"  [!] Achat annulé : Pas assez d'argent ({money_dispo} vs {CARTES[carte_achetee]['cost']}).")
                        tour_en_cours = False
                    else:
                        # Validation de l'achat et mise à jour du stock
                        self.stock[carte_achetee] -= 1
                        self.discard.append(carte_achetee)
                        
                        # --- MISE À JOUR DU SCORE ---
                        points_gagnes = CARTES[carte_achetee]["val_pv"]
                        if points_gagnes > 0:
                            self.score += points_gagnes
                            print(f"  [+] Achat réussi : {carte_achetee} (+{points_gagnes} PV). Nouveau score : {self.score}")
                        else:
                            print(f"  [+] Achat réussi : {carte_achetee}")
                            
                        tour_en_cours = False
                elif decision.startswith("ACTION "):
                    print(f"  [+] Action jouée : {decision}")
                    tour_en_cours = False
                
                time.sleep(0.5)

=======
                # TRAITEMENT DE LA DÉCISION
                if decision == "END_TURN":
                    tour_en_cours = False
                    
                elif decision.startswith("ACTION "):
                    carte_jouee = decision.split(" ")[1].lower()
                    
                    if actions_left <= 0:
                        print("  [!] Action annulée : Plus d'actions disponibles.")
                        tour_en_cours = False
                    elif carte_jouee not in self.hand:
                        print(f"  [!] Action annulée : {carte_jouee} n'est pas dans la main.")
                        tour_en_cours = False
                    elif CARTES[carte_jouee]["type"] != "action":
                        print(f"  [!] Action annulée : {carte_jouee} n'est pas une carte action.")
                        tour_en_cours = False
                    else:
                        # 1. Transfert de la carte de la main vers la zone de jeu
                        self.hand.remove(carte_jouee)
                        played_cards.append(carte_jouee)
                        actions_left -= 1
                        
                        # 2. Application des effets
                        effets = CARTES[carte_jouee]
                        cartes_a_piocher = effets.get("plus_cards", 0)
                        actions_bonus = effets.get("plus_actions", 0)
                        achats_bonus = effets.get("plus_buys", 0)
                        money_bonus = effets.get("plus_money", 0)
                        
                        if cartes_a_piocher > 0:
                            self.draw_cards(cartes_a_piocher)
                        actions_left += actions_bonus
                        buys_left += achats_bonus
                        bonus_money += money_bonus
                        
                        print(f"  [+] Action jouée : {carte_jouee} (+{cartes_a_piocher} C, +{actions_bonus} A, +{achats_bonus} Buy, +{money_bonus} Pièces)")
                        # Pas de tour_en_cours = False : la boucle continue

                elif decision.startswith("BUY "):
                    carte_achetee = decision.split(" ")[1].lower()
                    total_money = self.get_money_in_hand() + bonus_money - spent_money
                    
                    if buys_left <= 0:
                        print("  [!] Achat annulé : Plus d'achats disponibles.")
                        tour_en_cours = False
                    elif carte_achetee not in self.stock or self.stock[carte_achetee] <= 0:
                        print(f"  [!] Achat annulé : {carte_achetee} indisponible.")
                        tour_en_cours = False
                    elif CARTES[carte_achetee]["cost"] > total_money:
                        print(f"  [!] Achat annulé : Pas assez d'argent ({total_money} vs {CARTES[carte_achetee]['cost']}).")
                        tour_en_cours = False
                    else:
                        # Validation de l'achat et mise à jour du budget
                        self.stock[carte_achetee] -= 1
                        self.discard.append(carte_achetee)
                        spent_money += CARTES[carte_achetee]["cost"]
                        buys_left -= 1
                        
                        points_gagnes = CARTES[carte_achetee]["val_pv"]
                        if points_gagnes > 0:
                            self.score += points_gagnes
                            print(f"  [+] Achat réussi : {carte_achetee} (+{points_gagnes} PV). Score : {self.score}")
                        else:
                            print(f"  [+] Achat réussi : {carte_achetee}")
                            
                        # Pas de tour_en_cours = False : la boucle continue pour un second achat éventuel
                
                time.sleep(0.5)

            # Fin du tour : nettoyage de la main et des cartes jouées
>>>>>>> simulateur
            self.discard.extend(self.hand)
            self.discard.extend(played_cards)
            self.hand = []
            self.draw_cards(5)
            tour += 1

        print("\n=== FIN DE PARTIE ===")
        requests.get(f"{API_URL}/end_game", headers=HEADERS)

if __name__ == "__main__":
    simu = ArbitreDominion()
    simu.run_game()