from collections.abc import Callable
from typing import Annotated

from dopynion.data_model import (
    CardName,
    CardNameAndHand,
    Game,
    Hand,
    MoneyCardsInHand,
    PossibleCards,
)
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from communication import contexte_reponse_arbitre, transmettre_commande

app = FastAPI()

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


# La stratégie reçoit l'état du jeu et l'identifiant de la partie.
# Elle appelle action pour jouer une carte ou retourne une autre décision.
Strategie = Callable[[Game, str], object]


def get_strategie() -> Strategie:
    strategie = getattr(app.state, "strategie", None)
    if not callable(strategie):
        raise HTTPException(
            status_code=503,
            detail="Le programme stratégie n'est pas encore raccordé au serveur.",
        )
    return strategie


StrategieDependency = Annotated[Strategie, Depends(get_strategie)]


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
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.get("/start_turn")
def start_turn(game_id: GameIdDependency) -> DopynionResponseStr:
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/play")
def play(
    _game: Game,
    game_id: GameIdDependency,
    strategie: StrategieDependency,
) -> DopynionResponseStr:
    with contexte_reponse_arbitre(game_id) as reponse:
        decision_strategie = strategie(_game, game_id)
        if reponse.decision is None:
            if not isinstance(decision_strategie, str) or not decision_strategie:
                raise HTTPException(
                    status_code=500,
                    detail="La stratégie n'a fourni aucune commande pour ce /play.",
                )
            transmettre_commande(decision_strategie)
        elif (
            isinstance(decision_strategie, str)
            and decision_strategie != reponse.decision
        ):
            raise HTTPException(
                status_code=500,
                detail="La stratégie a fourni deux commandes différentes pour ce /play.",
            )
        return DopynionResponseStr(game_id=game_id, decision=reponse.decision)


@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    return DopynionResponseStr(game_id=game_id, decision="OK")


@app.post("/confirm_discard_card_from_hand")
async def confirm_discard_card_from_hand(
    game_id: GameIdDependency,
    _decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/discard_card_from_hand")
async def discard_card_from_hand(
    game_id: GameIdDependency,
    decision_input: Hand,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.hand[0])


@app.post("/confirm_trash_card_from_hand")
async def confirm_trash_card_from_hand(
    game_id: GameIdDependency,
    _decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/trash_card_from_hand")
async def trash_card_from_hand(
    game_id: GameIdDependency,
    decision_input: Hand,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.hand[0])


@app.post("/confirm_discard_deck")
async def confirm_discard_deck(
    game_id: GameIdDependency,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/choose_card_to_receive_in_discard")
async def choose_card_to_receive_in_discard(
    game_id: GameIdDependency,
    decision_input: PossibleCards,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.possible_cards[0],
    )


@app.post("/choose_card_to_receive_in_deck")
async def choose_card_to_receive_in_deck(
    game_id: GameIdDependency,
    decision_input: PossibleCards,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.possible_cards[0],
    )


@app.post("/skip_card_reception_in_hand")
async def skip_card_reception_in_hand(
    game_id: GameIdDependency,
    _decision_input: CardNameAndHand,
) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)


@app.post("/trash_money_card_for_better_money_card")
async def trash_money_card_for_better_money_card(
    game_id: GameIdDependency,
    decision_input: MoneyCardsInHand,
) -> DopynionResponseCardName:
    return DopynionResponseCardName(
        game_id=game_id,
        decision=decision_input.money_in_hand[0],
    )
