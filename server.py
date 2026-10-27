"""API FastAPI de Toulousain test. La stratégie est séparée en action.py,
achat.py et reaction.py.
"""
from collections import Counter
from typing import Annotated, Any

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

# Imports corrigés pour correspondre à tes fichiers réels
from action import action
from achat import achat

from reaction import (
    confirmer_defausse,
    choisir_defausse,
    confirmer_destruction,
    choisir_destruction,
    choisir_carte_recue,
    sauter_reception_en_main,
    choisir_monnaie_a_detruire,
)

app = FastAPI(title="Toulousain test - Dopynion")
turn_state: dict[str, dict[str, Any]] = {}


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


def _new_state() -> dict[str, Any]:
    return {
        "turn": 0,
        "actions": 1,
        "buys": 1,
        "bonus_money": 0,
        "purchased": Counter(),
    }


def _extract_card_name(payload: Any) -> CardName | None:
    """Lit le champ carte selon les variantes possibles du modèle API."""
    for field in ("card_name", "card", "card_to_discard", "card_to_trash"):
        raw = getattr(payload, field, None)
        if raw is None:
            continue
        if isinstance(raw, CardName):
            return raw
        raw = getattr(raw, "value", raw)
        try:
            return CardName(raw)
        except (TypeError, ValueError):
            try:
                return CardName(str(raw).lower())
            except (TypeError, ValueError):
                pass
    return None


@app.exception_handler(Exception)
def unknown_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    print(exc.__class__.__name__, str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": "Oops!", "detail": str(exc), "name": exc.__class__.__name__},
    )


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return (
        "<html><head><title>Toulousain test</title></head><body>"
        "<h1>Toulousain test - Dopynion</h1>"
        "<p><a href='/docs'>Documentation de l'API</a></p></body></html>"
    )


@app.get("/name")
def name() -> str:
    return "Toulousain test"


@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state[game_id] = _new_state()
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    state = turn_state.setdefault(game_id, _new_state())
    state["turn"] = int(state.get("turn", 0)) + 1
    state["actions"] = 1
    state["buys"] = 1
    state["bonus_money"] = 0
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/play")
def play(game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    state = turn_state.setdefault(game_id, _new_state())
    players = game.players or []
    player = next((p for p in players if p.hand is not None), players[0] if players else None)
    
    if player is None or player.hand is None:
        return DopynionResponseStr(game_id=game_id, decision="END_TURN")

    ma_main = player.hand
    stock = game.stock

    # ==========================================
    # 1. PHASE D'ACTION 
    # ==========================================
    if state["actions"] > 0:
        priorites_actions = [
            CardName.FARMINGVILLAGE,
            CardName.VILLAGE,
            CardName.FESTIVAL,
            CardName.LABORATORY,
            CardName.DISTANTSHORE,
            CardName.MARKET,
            CardName.BANDIT,       
            CardName.MILITIA,      
            CardName.WITCH,        
            CardName.BUREAUCRAT,   
            CardName.HIRELING,
            CardName.CHANCELLOR,   
            CardName.COUNCILROOM,
            CardName.SMITHY,
            CardName.WOODCUTTER
        ]
        
        for carte_action in priorites_actions:
            resultat_action = action(main=ma_main, carte=carte_action, actions_restantes=state["actions"])
            if resultat_action:
                state["actions"] = max(0, int(state.get("actions", 0)) - 1 + resultat_action.actions)
                state["buys"] = int(state.get("buys", 0)) + resultat_action.buys
                state["bonus_money"] = int(state.get("bonus_money", 0)) + resultat_action.bonus_money
                return DopynionResponseStr(game_id=game_id, decision=resultat_action.decision)

    # ==========================================
    # 2. PHASE D'ACHAT 
    # ==========================================
    if state["buys"] > 0:
        provinces_restantes = stock.quantities.get(CardName.PROVINCE, 8)
        piles_vides = sum(1 for qte in stock.quantities.values() if qte == 0)
        
        if provinces_restantes <= 4 or piles_vides >= 2:
            priorites_achat = [
                CardName.PROVINCE, 
                CardName.DUCHY, 
                CardName.GARDENS, 
                CardName.ESTATE, 
                CardName.GOLD, 
                CardName.SILVER
            ]
        else:
            priorites_achat = [
                CardName.PROVINCE,         
                CardName.GOLD,             
                CardName.BANDIT,           
                CardName.WITCH,            
                CardName.HIRELING,         
                CardName.FARMINGVILLAGE,   
                CardName.VILLAGE,          
                CardName.LABORATORY,       
                CardName.FESTIVAL,         
                CardName.MARKET,           
                CardName.COUNCILROOM,      
                CardName.MILITIA,          
                CardName.BUREAUCRAT,       
                CardName.DISTANTSHORE,     
                CardName.SMITHY,           
                CardName.SILVER,           
                CardName.CHANCELLOR        
            ]
        
        for carte_cible in priorites_achat:
            decision_achat = achat(main=ma_main, carte=carte_cible, stock=stock, monnaie_disponible=state["bonus_money"], achats_restants=state["buys"])
            if decision_achat:
                state["buys"] = int(state.get("buys", 0)) - 1
                cout_carte = Card.class_(carte_cible).cost
                state["bonus_money"] = int(state.get("bonus_money", 0)) - cout_carte
                return DopynionResponseStr(game_id=game_id, decision=decision_achat)

    return DopynionResponseStr(game_id=game_id, decision="END_TURN")


@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state.pop(game_id, None)
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/confirm_discard_card_from_hand")
def confirm_discard_card_from_hand(
    game_id: GameIdDependency, decision_input: CardNameAndHand
) -> DopynionResponseBool:
    card = _extract_card_name(decision_input)
    return DopynionResponseBool(game_id=game_id, decision=confirmer_defausse(card))


@app.post("/discard_card_from_hand")
def discard_card_from_hand(
    game_id: GameIdDependency, decision_input: Hand
) -> DopynionResponseCardName:
    cards = list(decision_input.hand)
    return DopynionResponseCardName(game_id=game_id, decision=choisir_defausse(cards))


@app.post("/confirm_trash_card_from_hand")
def confirm_trash_card_from_hand(
    game_id: GameIdDependency, decision_input: CardNameAndHand
) -> DopynionResponseBool:
    card = _extract_card_name(decision_input)
    return DopynionResponseBool(game_id=game_id, decision=confirmer_destruction(card))


@app.post("/trash_card_from_hand")
def trash_card_from_hand(
    game_id: GameIdDependency, decision_input: Hand
) -> DopynionResponseCardName:
    cards = list(decision_input.hand)
    return DopynionResponseCardName(game_id=game_id, decision=choisir_destruction(cards))


@app.post("/confirm_discard_deck")
def confirm_discard_deck(game_id: GameIdDependency) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=False)


@app.post("/choose_card_to_receive_in_discard")
def choose_card_to_receive_in_discard(
    game_id: GameIdDependency, decision_input: PossibleCards
) -> DopynionResponseCardName:
    chosen = choisir_carte_recue(list(decision_input.possible_cards), destination="discard")
    return DopynionResponseCardName(game_id=game_id, decision=chosen)


@app.post("/choose_card_to_receive_in_deck")
def choose_card_to_receive_in_deck(
    game_id: GameIdDependency, decision_input: PossibleCards
) -> DopynionResponseCardName:
    chosen = choisir_carte_recue(list(decision_input.possible_cards), destination="deck")
    return DopynionResponseCardName(game_id=game_id, decision=chosen)


@app.post("/skip_card_reception_in_hand")
def skip_card_reception_in_hand(
    game_id: GameIdDependency, _decision_input: CardNameAndHand
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=sauter_reception_en_main())


@app.post("/trash_money_card_for_better_money_card")
def trash_money_card_for_better_money_card(
    game_id: GameIdDependency, decision_input: MoneyCardsInHand
) -> DopynionResponseCardName:
    chosen = choisir_monnaie_a_detruire(list(decision_input.money_in_hand))
    return DopynionResponseCardName(game_id=game_id, decision=chosen)