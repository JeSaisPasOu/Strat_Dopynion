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

from reaction import (
    confirmer_defausse, 
    choisir_defausse, 
    confirmer_destruction, 
    choisir_destruction
)

app = FastAPI()

turn_state = {}

# ==========================================
# PRIORITÉ 4 : LISTE UNIVERSELLE DE VALEUR DES CARTES
# Utilisée pour choisir quelle carte recevoir via un effet (ex: Bureaucrate)
# ==========================================
ORDRE_DE_VALEUR_DES_CARTES = [
    CardName.PROVINCE, CardName.GOLD, CardName.HIRELING, CardName.WITCH, 
    CardName.BANDIT, CardName.DISTANTSHORE, CardName.LABORATORY, 
    CardName.FESTIVAL, CardName.MARKET, CardName.COUNCILROOM, 
    CardName.DUCHY, CardName.GARDENS, CardName.FARMINGVILLAGE, 
    CardName.MILITIA, CardName.BUREAUCRAT, CardName.SMITHY, 
    CardName.SILVER, CardName.CHANCELLOR, CardName.VILLAGE, 
    CardName.WOODCUTTER, CardName.ESTATE, CardName.COPPER
]

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
                state["actions"] = state["actions"] - 1 + resultat_action.actions
                state["buys"] += resultat_action.buys
                state["bonus_money"] += resultat_action.bonus_money
                return DopynionResponseStr(game_id=game_id, decision=resultat_action.decision)

    # ==========================================
    # 2. PHASE D'ACHAT DYNAMIQUE
    # ==========================================
    if state["buys"] > 0:
        # PRIORITÉ 5 : Détection des fins de parties alternatives
        provinces_restantes = stock.quantities.get(CardName.PROVINCE, 8)
        piles_vides = sum(1 for qte in stock.quantities.values() if qte == 0)
        
        # Si 4 Provinces ou moins, OU si au moins 2 piles sont vides (la 3ème vide termine la partie)
        if provinces_restantes <= 4 or piles_vides >= 2:
            # LATE GAME : Course aux points 
            priorites_achat = [
                CardName.PROVINCE, 
                CardName.DUCHY, 
                CardName.GARDENS, 
                CardName.ESTATE, 
                CardName.GOLD, 
                CardName.SILVER
            ]
        else:
            # EARLY / MID GAME : Construction du moteur et attaques
            priorites_achat = [
                CardName.PROVINCE,         
                CardName.GOLD,             
                CardName.BANDIT,           
                CardName.WITCH,            
                # PRIORITÉ 3 : Hireling abaissé après l'Or et la Sorcière
                CardName.HIRELING,         
                # PRIORITÉ 2 : Villages remontés pour fournir les actions des cartes terminales
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
                state["buys"] -= 1
                cout_carte = Card.class_(carte_cible).cost
                state["bonus_money"] -= cout_carte
                return DopynionResponseStr(game_id=game_id, decision=decision_achat)

    return DopynionResponseStr(game_id=game_id, decision="END_TURN")

@app.get("/end_game")
def end_game(game_id: GameIdDependency) -> DopynionResponseStr:
    turn_state.pop(game_id, None)
    return DopynionResponseStr(game_id=game_id, decision="OK")

# ==========================================
# GESTION INTELLIGENTE DES RÉACTIONS (reaction.py externe)
# ==========================================

@app.post("/confirm_discard_card_from_hand")
async def confirm_discard_card_from_hand(game_id: GameIdDependency, decision_input: CardNameAndHand) -> DopynionResponseBool:
    carte = getattr(decision_input, 'card_name', getattr(decision_input, 'card', None))
    decision = confirmer_defausse(carte)
    return DopynionResponseBool(game_id=game_id, decision=decision)

@app.post("/discard_card_from_hand")
async def discard_card_from_hand(game_id: GameIdDependency, decision_input: Hand) -> DopynionResponseCardName:
    carte_choisie = choisir_defausse(decision_input.hand)
    return DopynionResponseCardName(game_id=game_id, decision=carte_choisie)

@app.post("/confirm_trash_card_from_hand")
async def confirm_trash_card_from_hand(game_id: GameIdDependency, decision_input: CardNameAndHand) -> DopynionResponseBool:
    carte = getattr(decision_input, 'card_name', getattr(decision_input, 'card', None))
    decision = confirmer_destruction(carte)
    return DopynionResponseBool(game_id=game_id, decision=decision)

@app.post("/trash_card_from_hand")
async def trash_card_from_hand(game_id: GameIdDependency, decision_input: Hand) -> DopynionResponseCardName:
    carte_choisie = choisir_destruction(decision_input.hand)
    return DopynionResponseCardName(game_id=game_id, decision=carte_choisie)

@app.post("/confirm_discard_deck")
async def confirm_discard_deck(game_id: GameIdDependency) -> DopynionResponseBool:
    # PRIORITÉ 1 : On refuse systématiquement l'effet (ex: Chancelier) pour ne pas défausser une bonne pioche
    return DopynionResponseBool(game_id=game_id, decision=False)

@app.post("/choose_card_to_receive_in_discard")
async def choose_card_to_receive_in_discard(game_id: GameIdDependency, decision_input: PossibleCards) -> DopynionResponseCardName:
    # PRIORITÉ 4 : On utilise la liste de valeur universelle
    for carte_cible in ORDRE_DE_VALEUR_DES_CARTES:
        if carte_cible in decision_input.possible_cards:
            return DopynionResponseCardName(game_id=game_id, decision=carte_cible)
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.possible_cards[0])

@app.post("/choose_card_to_receive_in_deck")
async def choose_card_to_receive_in_deck(game_id: GameIdDependency, decision_input: PossibleCards) -> DopynionResponseCardName:
    # PRIORITÉ 4 : On utilise la liste de valeur universelle
    for carte_cible in ORDRE_DE_VALEUR_DES_CARTES:
        if carte_cible in decision_input.possible_cards:
            return DopynionResponseCardName(game_id=game_id, decision=carte_cible)
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.possible_cards[0])

@app.post("/skip_card_reception_in_hand")
async def skip_card_reception_in_hand(game_id: GameIdDependency, _decision_input: CardNameAndHand) -> DopynionResponseBool:
    return DopynionResponseBool(game_id=game_id, decision=True)

@app.post("/trash_money_card_for_better_money_card")
async def trash_money_card_for_better_money_card(game_id: GameIdDependency, decision_input: MoneyCardsInHand) -> DopynionResponseCardName:
    if CardName.COPPER in decision_input.money_in_hand:
        return DopynionResponseCardName(game_id=game_id, decision=CardName.COPPER)
    return DopynionResponseCardName(game_id=game_id, decision=decision_input.money_in_hand[0])