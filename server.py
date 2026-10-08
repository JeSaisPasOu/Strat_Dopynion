from typing import Annotated

from dopynion.data_model import (
    CardName,
    CardNameAndHand,
    Game,
    Hand,
    MoneyCardsInHand,
    PossibleCards,
)
from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Import de ta fonction d'achat
from achat import achat

app = FastAPI()

#####################################################
# Variables globales pour la mémoire du Bot
#####################################################
# turn_state : retient l'état du tour en cours (actions, achats, monnaie bonus)
turn_state = {}

#####################################################
# Data model for responses
#####################################################

class DopynionResponseBool(BaseModel):
    game_id: str
    decision: bool

class DopynionResponseCardName(BaseModel):
    game_id: str
    decision: CardName

class DopynionResponseStr(BaseModel):
    game_id: str
    decision: str

#####################################################
# Getter for the game identifier
#####################################################

def get_game_id(x_game_id: str = Header(description="ID of the game")) -> str:
    return x_game_id

GameIdDependency = Annotated[str, Depends(get_game_id)]

#####################################################
# Error management
#####################################################

@app.exception_handler(Exception)
def unknown_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    print(exc.__class__.__name__, str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "message": "Oops!",
            "detail": str(exc),
            "name": exc.__class__.__name__,
        },
    )

#####################################################
# The code of the strategy
#####################################################

@app.get("/name")
def name() -> str:
    return "Toulousain"

@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    # Nettoyage initial
    turn_state.pop(game_id, None)
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    # À chaque début de tour, on a 1 Action, 1 Achat, et 0 monnaie bonus
    turn_state[game_id] = {"actions": 1, "buys": 1, "bonus_money": 0}
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.post("/play")
def play(_game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    print(_game)
    state = turn_state.setdefault(game_id, {"actions": 1, "buys": 1, "bonus_money": 0})
    
    # Recherche de la main de notre bot
    mon_joueur = next((p for p in _game.players if p.hand is not None), _game.players[0])
    ma_main = mon_joueur.hand
    stock = _game.stock

    # ==========================================
    # 1. PHASE D'ACTION
    # ==========================================
    if state["actions"] > 0:
        # Liste de nos actions en main
        actions_en_main = [carte for carte, qte in ma_main.quantities.items() if qte > 0 and carte in [
            "village", "woodcutter", "smithy", "festival", "laboratory", "market"
        ]]
        
        if actions_en_main:
            # ORDRE DE PRIORITÉ DES ACTIONS (priorité haute à basse -> cartes qui ajoute des actions en premier)
            priorite_actions = ["village", "festival", "laboratory", "market", "smithy", "woodcutter"]
            
            action_a_jouer = None
            for action in priorite_actions:
                if action in actions_en_main:
                    action_a_jouer = action
                    break
            
            if action_a_jouer:
                state["actions"] -= 1
                
                # --- PRÉ-SIMULATION DES EFFETS (en attendant action.py) ---
                if action_a_jouer == "village":
                    state["actions"] += 2  # +2 Actions
                elif action_a_jouer == "festival":
                    state["actions"] += 2  # +2 Actions
                    state["buys"] += 1     # +1 Achat
                    state["bonus_money"] += 2 # +2 Cuivres (Monnaie)
                elif action_a_jouer == "laboratory":
                    state["actions"] += 1  # +1 Action
                elif action_a_jouer == "market":
                    state["actions"] += 1  # +1 Action
                    state["buys"] += 1     # +1 Achat
                    state["bonus_money"] += 1 # +1 Pièce
                elif action_a_jouer == "woodcutter":
                    state["buys"] += 1     # +1 Achat
                    state["bonus_money"] += 2 # +2 Cuivres
                # Note: Le Forgeron (smithy) fait piocher, c'est géré par l'arbitre, pas de stats à changer ici.

                return DopynionResponseStr(game_id=game_id, decision=f"ACTION {action_a_jouer}")

    # ==========================================
    # 2. PHASE D'ACHAT
    # ==========================================
    if state["buys"] > 0:
        # LISTE DYNAMIQUE DE PRIORITÉS D'ACHAT (du plus cher au moins cher)
        priorites_achat = [
            CardName("province"),   # Coût 8 (Priorité absolue pour gagner)
            CardName("laboratory"), # Coût 5 (Super piocheur qui ne bloque pas le tour)
            CardName("smithy"),     # Coût 4 (Bon piocheur)
            CardName("festival"),   # Coût 5 (Générateur d'actions et de sous)
            CardName("market"),     # Coût 5 (Carte polyvalente)
            CardName("silver"),     # Coût 3 (Sécurité économique)
            CardName("village"),    # Coût 3 (Nécessaire si on a trop d'actions terminales)
            CardName("woodcutter"), # Coût 3 (Si on manque d'achats)
            CardName("estate")      # Coût 2 (En dernier recours)
        ]
        
        for carte_cible in priorites_achat:
            decision_achat = achat(
                main=ma_main, 
                carte=carte_cible, 
                stock=stock, 
                monnaie_disponible=state["bonus_money"], 
                achats_restants=state["buys"]
            )
            
            if decision_achat:
                # Achat validé ! On consomme 1 achat et on renvoie la décision
                state["buys"] -= 1
                # (Bonus : on remet l'argent bonus à zéro ou on le déduit si on voulait être ultra précis, 
                # mais dans ton achat.py actuel, le budget est recalculé globalement, ce qui est suffisant pour le moment)
                return DopynionResponseStr(game_id=game_id, decision=decision_achat)

    # ==========================================
    # 3. FIN DE TOUR
    # ==========================================
    return DopynionResponseStr(game_id=game_id, decision="END_TURN")

@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state.pop(game_id, None)
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.post("/confirm_discard_card_from_hand")
async def confirm_discard_card_from_hand(game_id: GameIdDependency, _decision_input: CardNameAndHand) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)

@app.post("/discard_card_from_hand")
async def discard_card_from_hand(game_id: GameIdDependency, decision_input: Hand) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.hand[0])

@app.post("/confirm_trash_card_from_hand")
async def confirm_trash_card_from_hand(game_id: GameIdDependency, _decision_input: CardNameAndHand) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)

@app.post("/trash_card_from_hand")
async def trash_card_from_hand(game_id: GameIdDependency, decision_input: Hand) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.hand[0])

@app.post("/confirm_discard_deck")
async def confirm_discard_deck(game_id: GameIdDependency) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)

@app.post("/choose_card_to_receive_in_discard")
async def choose_card_to_receive_in_discard(game_id: GameIdDependency, decision_input: PossibleCards) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.possible_cards[0])

@app.post("/choose_card_to_receive_in_deck")
async def choose_card_to_receive_in_deck(game_id: GameIdDependency, decision_input: PossibleCards) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.possible_cards[0])

@app.post("/skip_card_reception_in_hand")
async def skip_card_reception_in_hand(game_id: GameIdDependency, _decision_input: CardNameAndHand) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)

@app.post("/trash_money_card_for_better_money_card")
async def trash_money_card_for_better_money_card(game_id: GameIdDependency, decision_input: MoneyCardsInHand) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.money_in_hand[0])