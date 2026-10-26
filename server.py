from typing import Annotated

from dopynion.cards import Card
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

from achat import achat
from action import action

app = FastAPI()

turn_state = {}

class DopynionResponseBool(BaseModel):
    game_id: str
    decision: bool

class DopynionResponseCardName(BaseModel):
    game_id: str
    decision: CardName

class DopynionResponseStr(BaseModel):
    game_id: str
    decision: str

def get_game_id(x_game_id: str = Header(description="ID of the game")) -> str:
    return x_game_id

GameIdDependency = Annotated[str, Depends(get_game_id)]

@app.exception_handler(Exception)
def unknown_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    print(exc.__class__.__name__, str(exc))
    return JSONResponse(status_code=500, content={"message": "Oops!", "detail": str(exc), "name": exc.__class__.__name__})

@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return "<html><head><title>Dopynion Bot API</title></head><body><h1>Dopynion API</h1><p><a href='/docs'>Documentation</a></p></body></html>"

@app.get("/name")
def name() -> str:
    return "Toulousain"

@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state.pop(game_id, None)
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state[game_id] = {"actions": 1, "buys": 1, "bonus_money": 0}
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.post("/play")
def play(_game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    state = turn_state.setdefault(game_id, {"actions": 1, "buys": 1, "bonus_money": 0})
    mon_joueur = next((p for p in _game.players if p.hand is not None), _game.players[0])
    ma_main = mon_joueur.hand
    stock = _game.stock

    # ==========================================
    # 1. PHASE D'ACTION (Moteurs d'abord, Terminaux ensuite)
    # ==========================================
    if state["actions"] > 0:
        priorites_actions = [
            CardName.FARMINGVILLAGE,
            CardName.VILLAGE,
            CardName.FESTIVAL,
            CardName.DISTANTSHORE,
            CardName.LABORATORY,
            CardName.MARKET,
            CardName.HIRELING,
            CardName.WITCH,
            CardName.COUNCILROOM,
            CardName.SMITHY,
            CardName.WOODCUTTER
        ]
        
        for carte_action in priorites_actions:
            resultat_action = action(main=ma_main, carte=carte_action, actions_restantes=state["actions"])
            if resultat_action:
                state["actions"] = state["actions"] - 1 + resultat_action.actions
                state["buys"] += resultat_action.buys
                state["bonus_money"] += resultat_action.bonus_money
                return DopynionResponseStr(game_id=game_id, decision=resultat_action.decision)

    # ==========================================
    # 2. PHASE D'ACHAT
    # ==========================================
    if state["buys"] > 0:
        priorites_achat = [
            CardName.PROVINCE,         # 8 (Victoire)
            CardName.HIRELING,         # 6 (Pioche permanente, incroyable)
            CardName.DISTANTSHORE,     # 6 (Victoire + Moteur)
            CardName.GOLD,             # 6 (Économie)
            CardName.WITCH,            # 5 (Attaque dévastatrice)
            CardName.COUNCILROOM,      # 5 (Forte pioche + Achat)
            CardName.LABORATORY,       # 5 
            CardName.FESTIVAL,         # 5 
            CardName.MARKET,           # 5 
            CardName.DUCHY,            # 5 (Victoire)
            CardName.FARMINGVILLAGE,   # 4 (Meilleur que le Village standard)
            CardName.SMITHY,           # 4 
            CardName.SILVER,           # 3 
            CardName.VILLAGE           # 3 
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
                state["buys"] -= 1
                cout_carte = Card.class_(carte_cible).cost
                state["bonus_money"] -= cout_carte
                return DopynionResponseStr(game_id=game_id, decision=decision_achat)

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