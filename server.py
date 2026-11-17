"""API FastAPI de Toulousain test, avec stratégie séparée en modules.

Cette version adapte les achats et les réactions aux cartes Chapelle, Mine,
Prêteur sur gages et Rénovation. La logique de jeu des actions reste dans
'action.py' et n'est volontairement pas modifiée ici.
"""

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

from action import ACTION_PRIORITY, action
from achat import CHAPEL, MONEYLENDER, MINE, REMODEL, seuil_cuivre, economie_estimee
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
        # Budget restant après les achats afin de ne pas dépenser deux fois
        # les mêmes trésors lorsque /play est rappelé.
        "money_remaining": None,
        "purchased": Counter(),
        "gained": Counter(),
        # Cartes réellement épurées : utilisé pour estimer si Chapel reste utile.
        "trashed": Counter(),
        "known_piles": set(),
        "joueurs_actifs": 2,
        "last_stock": {},
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
        cout = int(cout_carte(carte))
        return cout if cout < 10**6 else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        try:
            classe = Card.class_(carte)
            return int(classe.cost) if classe is not Card else 0
        except (AttributeError, TypeError, ValueError, KeyError):
            return 0


def _cartes_connues(state: dict[str, Any]) -> Counter:
    """Fusionne les achats et les cartes obtenues via les effets du jeu."""
    result = Counter(state.get("purchased", Counter()))
    result.update(state.get("gained", Counter()))
    return result


def _enregistrer_carte_gagnee(game_id: str, carte: CardName) -> None:
    state = turn_state.setdefault(game_id, _new_state())
    state.setdefault("gained", Counter())[carte] += 1


def _enregistrer_carte_epuree(game_id: str, carte: CardName | None) -> None:
    if carte is None:
        return
    state = turn_state.setdefault(game_id, _new_state())
    state.setdefault("trashed", Counter())[carte] += 1
    logger.info(
        "game=%s carte_epuree=%s total_epure=%s",
        game_id,
        carte.value,
        sum(state["trashed"].values()),
    )


def _maj_piles_vides(state: dict[str, Any], stock: Any) -> int:
    """Compte les piles à zéro, y compris celles qui disparaissent du snapshot.

    Hypothèse à confirmer avec le modèle Dopynion : une pile épuisée peut être
    omise de stock.quantities. Si le moteur conserve les piles à zéro, elles
    sont également comptées.
    """
    quantities = getattr(stock, "quantities", {}) or {}
    known = state.setdefault("known_piles", set())
    previous = state.setdefault("last_stock", {})
    current_names = set(quantities.keys())
    known.update(current_names)

    for name, quantity in quantities.items():
        try:
            previous[name] = max(0, int(quantity))
        except (TypeError, ValueError):
            continue

    empty = 0
    for name in known:
        if name not in current_names or previous.get(name, 1) == 0:
            empty += 1
    state["piles_vides"] = empty
    return empty


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
    state["money_remaining"] = None
    return DopynionResponseStr(game_id=game_id, decision="OK")


def _action_utile(carte: CardName, main: Any, state: dict[str, Any]) -> bool:
    """Évite les actions qui ne produiraient rien ou détruisent l'économie."""
    q = getattr(main, "quantities", {}) or {}
    n = lambda c: int(q.get(c, 0)) if c is not None else 0
    achats = _cartes_connues(state)
    trashed = state.get("trashed", Counter())
    cuivre, _, _ = economie_estimee(achats, trashed)
    minimum = seuil_cuivre(achats, trashed)
    if carte == MONEYLENDER and MONEYLENDER is not None:
        # Le +3 pièces est compté uniquement si le moteur pourra détruire un Cuivre.
        return n(CardName.COPPER) > 0 and cuivre > minimum
    if carte == CHAPEL and CHAPEL is not None:
        # Chapelle n'a plus d'intérêt sans Domaine, Malédiction ni Cuivre sacrifiable.
        return (n(CardName.CURSE) + n(CardName.ESTATE) > 0
                or (n(CardName.COPPER) > 0 and cuivre > minimum))
    if carte == MINE and MINE is not None:
        return n(CardName.COPPER) + n(CardName.SILVER) > 0
    if carte == REMODEL and REMODEL is not None:
        return any(n(c) > 0 for c in (CardName.ESTATE, CardName.CURSE,
                CardName.COPPER, CardName.CHANCELLOR, CardName.WOODCUTTER))
    return True


def _joueurs_en_jeu(game: Any) -> int:
    """Nombre de participants actifs quand le moteur fournit l'information."""
    players = getattr(game, 'players', None) or []
    actifs = []
    for p in players:
        if any(getattr(p, attr, False) is True for attr in ('eliminated', 'is_eliminated', 'out')):
            continue
        actifs.append(p)
    return max(2, len(actifs))


@app.post("/play")
def play(game: Game, game_id: GameIdDependency) -> DopynionResponseStr:
    state = turn_state.setdefault(game_id, _new_state())
    players = getattr(game, "players", None) or []
    player = next((p for p in players if getattr(p, "hand", None) is not None), None)
    if player is None:
        return DopynionResponseStr(game_id=game_id, decision="END_TURN")

    main = player.hand
    stock = game.stock
    state["joueurs_actifs"] = _joueurs_en_jeu(game)

    # Les nouvelles actions sont jouées par action.py : on ne duplique pas ici
    # leur résolution. action.py doit renvoyer les bons bonus/compteurs.
    if int(state.get("actions", 0)) > 0:
        for carte_action in ACTION_PRIORITY:
            if not _action_utile(carte_action, main, state):
                continue
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

    stock_quantities = getattr(stock, "quantities", {}) or {}
    provinces_restantes = int(stock_quantities.get(CardName.PROVINCE, 8))
    piles_vides = _maj_piles_vides(state, stock)
    if state.get("money_remaining") is None:
        state["money_remaining"] = int(state.get("bonus_money", 0)) + monnaie_en_main(main)
    budget = int(state.get("money_remaining", 0))

    if int(state.get("buys", 0)) > 0:
        priorites = priorites_achat(
            stock,
            achats=_cartes_connues(state),
            trashed=state.get("trashed", Counter()),
            tour=int(state.get("turn", 1)),
            provinces_restantes=provinces_restantes,
            piles_vides=piles_vides,
            budget=budget,
            main=main,
            joueurs_actifs=int(state.get("joueurs_actifs", 2)),
        )
        for carte_cible in priorites:
            decision_achat = achat(
                main=main,
                carte=carte_cible,
                stock=stock,
                # Le budget restant comprend déjà les bonus et achats précédents.
                monnaie_disponible=budget - monnaie_en_main(main),
                achats_restants=int(state.get("buys", 0)),
            )
            if decision_achat:
                state["buys"] = int(state.get("buys", 0)) - 1
                state["money_remaining"] = max(0, budget - _safe_card_cost(carte_cible))
                state.setdefault("purchased", Counter())[carte_cible] += 1
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
    main = list(getattr(decision_input, "hand", None) or [])
    return DopynionResponseBool(game_id=game_id, decision=confirmer_defausse(card, main=main))


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
    state = turn_state.setdefault(game_id, _new_state())
    decision = confirmer_destruction(
        card, achats=_cartes_connues(state), trashed=state.get("trashed", Counter()),
        tour=int(state.get("turn", 1)), main=list(getattr(decision_input, 'hand', []) or [])
    )
    if decision:
        _enregistrer_carte_epuree(game_id, card)
    return DopynionResponseBool(game_id=game_id, decision=decision)


@app.post("/trash_card_from_hand")
def trash_card_from_hand(
    game_id: GameIdDependency, decision_input: Hand
) -> DopynionResponseCardName:
    state = turn_state.setdefault(game_id, _new_state())
    cards = list(decision_input.hand)
    chosen = choisir_destruction(
        cards, tour=int(state.get("turn", 1)), achats=_cartes_connues(state),
        trashed=state.get("trashed", Counter())
    )
    if cards:
        _enregistrer_carte_epuree(game_id, chosen)
    return DopynionResponseCardName(game_id=game_id, decision=chosen)


@app.post("/confirm_discard_deck")
def confirm_discard_deck(game_id: GameIdDependency) -> DopynionResponseBool:
    # Ne pas sacrifier le deck entier sans connaître sa composition.
    return DopynionResponseBool(game_id=game_id, decision=False)


@app.post("/choose_card_to_receive_in_discard")
def choose_card_to_receive_in_discard(
    game_id: GameIdDependency, decision_input: PossibleCards
) -> DopynionResponseCardName:
    state = turn_state.setdefault(game_id, _new_state())
    possibles = list(decision_input.possible_cards)
    chosen = choisir_carte_recue(
        possibles,
        destination="discard",
        tour=int(state.get("turn", 1)),
        achats=_cartes_connues(state),
        trashed=state.get("trashed", Counter()),
    )
    if possibles:
        _enregistrer_carte_gagnee(game_id, chosen)
    return DopynionResponseCardName(game_id=game_id, decision=chosen)


@app.post("/choose_card_to_receive_in_deck")
def choose_card_to_receive_in_deck(
    game_id: GameIdDependency, decision_input: PossibleCards
) -> DopynionResponseCardName:
    state = turn_state.setdefault(game_id, _new_state())
    possibles = list(decision_input.possible_cards)
    chosen = choisir_carte_recue(
        possibles,
        destination="deck",
        tour=int(state.get("turn", 1)),
        achats=_cartes_connues(state),
        trashed=state.get("trashed", Counter()),
    )
    if possibles:
        _enregistrer_carte_gagnee(game_id, chosen)
    return DopynionResponseCardName(game_id=game_id, decision=chosen)


@app.post("/skip_card_reception_in_hand")
def skip_card_reception_in_hand(
    game_id: GameIdDependency, decision_input: CardNameAndHand
) -> DopynionResponseBool:
    state = turn_state.setdefault(game_id, _new_state())
    card = _extract_card_name(decision_input)
    decision = sauter_reception_en_main(
        card, actions_restantes=int(state.get('actions', 0)),
        main=list(getattr(decision_input, 'hand', []) or [])
    )
    return DopynionResponseBool(game_id=game_id, decision=decision)


@app.post("/trash_money_card_for_better_money_card")
def trash_money_card_for_better_money_card(
    game_id: GameIdDependency, decision_input: MoneyCardsInHand
) -> DopynionResponseCardName:
    state = turn_state.setdefault(game_id, _new_state())
    monies = list(decision_input.money_in_hand)
    chosen = choisir_monnaie_a_detruire(monies, tour=int(state.get("turn", 1)))
    if monies:
        _enregistrer_carte_epuree(game_id, chosen)
    return DopynionResponseCardName(game_id=game_id, decision=chosen)
