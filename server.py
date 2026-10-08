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
# turn_tracker : retient à quel tour se trouve chaque partie
turn_tracker = {}
# buy_tracker : retient combien d'achats ont été faits dans le tour actuel
buy_tracker = {}


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
# Home page
#####################################################

@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <html>
        <head><title>Dopynion Bot API</title></head>
        <body>
            <h1>Dopynion API</h1>
            <p><a href="/docs">Consulter la documentation interactive de l'API (/docs)</a></p>
        </body>
    </html>
    """


#####################################################
# The code of the strategy
#####################################################

@app.get("/name")
def name() -> str:
    return "Toulousain"

@app.get("/start_game")
def start_game(game_id: GameIdDependency) -> DopynionResponseStr:
    # Initialisation de la mémoire pour une nouvelle partie
    turn_tracker[game_id] = 0
    return DopynionResponseStr(game_id=game_id, decision="OK")

@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    # On incrémente le tour et on remet le compteur d'achats à 0
    turn_tracker[game_id] = turn_tracker.get(game_id, 0) + 1
    buy_tracker[game_id] = 0
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/play")
def play(_game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    tour_actuel = turn_tracker.get(game_id, 1)
    achats_faits = buy_tracker.get(game_id, 0)
    print(_game)
    
    # Sécurité anti-boucle : 1 seul achat par tour par défaut
    if achats_faits >= 1:
        return DopynionResponseStr(game_id=game_id, decision="END_TURN")

    # Recherche de la main de notre bot (c'est le joueur dont la main n'est pas masquée)
    mon_joueur = next((p for p in _game.players if p.hand is not None), _game.players[0])
    ma_main = mon_joueur.hand
    stock = _game.stock

    decision = False

    # --- STRATÉGIE D'OUVERTURE ---
    if tour_actuel == 1:
        # Acheter un domaine au tour 1 (coût 2)
        decision = achat(ma_main, CardName("estate"), stock)
    elif tour_actuel == 2:
        # Acheter un Argent au tour 2 (coût 3)
        decision = achat(ma_main, CardName("silver"), stock)
        
        # Si on n'a pas les 3 cuivres nécessaires pour l'Argent, on se rabat sur un Domaine
        if not decision:
            decision = achat(ma_main, CardName("estate"), stock)
    
    # Application de la décision d'achat
    if decision:
        buy_tracker[game_id] = achats_faits + 1
        return DopynionResponseStr(game_id=game_id, decision=decision)

    # Fin de tour par défaut
    return DopynionResponseStr(game_id=game_id, decision="END_TURN")


@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_tracker.pop(game_id, None)
    buy_tracker.pop(game_id, None)
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