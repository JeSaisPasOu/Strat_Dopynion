"""API FastAPI de Toulousain test, avec stratégie séparée en modules."""

import logging
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

from action import action
from achat import achat, cout_carte, monnaie_en_main, priorites_achat
from reaction import (
    confirmer_defausse,
    choisir_defausse,
    confirmer_destruction,
    choisir_destruction,
    choisir_carte_recue,
    sauter_reception_en_main,
    choisir_monnaie_a_detruire,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("toulousain")
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
                continue
    return None


def _safe_card_cost(carte: CardName) -> int:
    try:
        return int(cout_carte(carte))
    except (AttributeError, TypeError, ValueError, KeyError):
        try:
            classe = Card.class_(carte)
            return int(classe.cost) if classe is not Card else 0
        except (AttributeError, TypeError, ValueError, KeyError):
            return 0


def _piles_vides(stock: Any) -> int:
    quantities = getattr(stock, "quantities", {}) or {}
    return sum(1 for quantity in quantities.values() if int(quantity) == 0)


@app.exception_handler(Exception)
def unknown_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Erreur non gérée dans l'API Dopynion")
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
    players = getattr(game, "players", None) or []
    player = next((p for p in players if getattr(p, "hand", None) is not None), None)
    if player is None:
        return DopynionResponseStr(game_id=game_id, decision="END_TURN")

    main = player.hand
    stock = game.stock
    quantities_main = getattr(main, "quantities", {}) or {}

    # Les cartes qui ajoutent des actions passent avant les actions terminales.
    # L'ordre est réévalué à chaque appel de /play avec la main réellement reçue.
    priorites_actions = [
        CardName.FARMINGVILLAGE,
        CardName.VILLAGE,
        CardName.FESTIVAL,
        CardName.LABORATORY,
        CardName.DISTANTSHORE,
        CardName.MARKET,
        CardName.COUNCILROOM,
        CardName.WITCH,
        CardName.BANDIT,
        CardName.HIRELING,
        CardName.MILITIA,
        CardName.BUREAUCRAT,
        CardName.SMITHY,
        CardName.CHANCELLOR,
        CardName.WOODCUTTER,
    ]

    if int(state.get("actions", 0)) > 0:
        for carte_action in priorites_actions:
            resultat_action = action(
                main=main,
                carte=carte_action,
                actions_restantes=int(state["actions"]),
            )
            if resultat_action:
                state["actions"] = max(
                    0,
                    int(state.get("actions", 0)) - 1 + int(resultat_action.actions),
                )
                state["buys"] = int(state.get("buys", 0)) + int(resultat_action.buys)
                state["bonus_money"] = int(state.get("bonus_money", 0)) + int(
                    resultat_action.bonus_money
                )
                logger.info(
                    "game=%s turn=%s action=%s actions_restantes=%s bonus=%s",
                    game_id,
                    state.get("turn", 0),
                    carte_action.value,
                    state["actions"],
                    state["bonus_money"],
                )
                return DopynionResponseStr(game_id=game_id, decision=resultat_action.decision)

    # Fin de partie : standard Dominion = Province vide OU trois piles vides.
    provinces_restantes = int(getattr(stock, "quantities", {}).get(CardName.PROVINCE, 8))
    piles_vides = _piles_vides(stock)
    budget = int(state.get("bonus_money", 0)) + monnaie_en_main(main)

    if int(state.get("buys", 0)) > 0:
        priorites = priorites_achat(
            stock,
            achats=state.get("purchased", Counter()),
            tour=int(state.get("turn", 1)),
            provinces_restantes=provinces_restantes,
            piles_vides=piles_vides,
            budget=budget,
        )
        for carte_cible in priorites:
            decision_achat = achat(
                main=main,
                carte=carte_cible,
                stock=stock,
                monnaie_disponible=int(state.get("bonus_money", 0)),
                achats_restants=int(state.get("buys", 0)),
            )
            if decision_achat:
                state["buys"] = int(state.get("buys", 0)) - 1
                state["bonus_money"] = int(state.get("bonus_money", 0)) - _safe_card_cost(
                    carte_cible
                )
                state["purchased"][carte_cible] += 1
                logger.info(
                    "game=%s turn=%s achat=%s budget_avant=%s achats_restants=%s",
                    game_id,
                    state.get("turn", 0),
                    carte_cible.value,
                    budget,
                    state["buys"],
                )
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
    # Choix prudent : ne vide pas le deck sans connaître sa composition.
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
