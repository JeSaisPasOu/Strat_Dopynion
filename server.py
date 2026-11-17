"""API Dopynion Toulousain V5 : mêmes routes, décisions contextuelles, état SQLite.

Le moteur n'expose pas forcément le deck intégral ; les comptes sont estimés.
Définir TOULOUSAIN_STATE_DB pour placer la base sur un disque persistant Alwaysdata.
"""
import json
import logging
import os
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dopynion.data_model import (
    CardName, CardNameAndHand, Game, Hand, MoneyCardsInHand, PossibleCards,
)

from action import choisir_action
from achat import achat, cout_carte, monnaie_en_main, priorites_achat
from reaction import (
    confirmer_defausse, choisir_defausse, confirmer_destruction,
    choisir_destruction, choisir_carte_recue,
    sauter_reception_en_main, choisir_monnaie_a_detruire,
)
from strategie import Contexte, carte, nombre, quantites

logger = logging.getLogger('toulousain')
logging.basicConfig(level=logging.INFO)
app = FastAPI(title='Toulousain - Dopynion V5')
DATABASE = Path(os.environ.get('TOULOUSAIN_STATE_DB',
    str(Path(__file__).with_name('toulousain_etat.sqlite3'))))
DECISIONS_LOG = os.environ.get('TOULOUSAIN_DECISIONS_LOG')


class DopynionResponseBool(BaseModel):
    game_id: str
    decision: bool


class DopynionResponseCardName(BaseModel):
    game_id: str
    decision: CardName


class DopynionResponseStr(BaseModel):
    game_id: str
    decision: str


def get_game_id(x_game_id: str = Header(description='ID of the game')) -> str:
    return x_game_id


GameIdDependency = Annotated[str, Depends(get_game_id)]


def _new_state():
    return {
        'turn': 0, 'actions': 1, 'buys': 1, 'bonus_money': 0,
        'money_remaining': None, 'purchased': {}, 'gained': {},
        'trashed': {}, 'observed': {}, 'piles': {}, 'joueurs_actifs': 2,
        'events': [], 'hirelings_jouees': 0,
    }


def _log_decision(game_id: str, event: dict):
    if not DECISIONS_LOG:
        return
    try:
        path = Path(DECISIONS_LOG)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps({'time':datetime.now(timezone.utc).isoformat(),
                    'game_id':game_id, **event}, ensure_ascii=False) + '\n')
    except OSError:
        logger.warning('Impossible d\'écrire les statistiques',exc_info=True)


def _transition(game_id, func, *, fresh=False, remove=False):
    """Transaction par partie, persistante et sérialisée même entre workers.

    SQLite garantit que chaque lecture/modification/écriture est atomique.
    Conserver le fichier sur un disque local (pas un répertoire temporaire).
    """
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE, timeout=5, isolation_level=None) as db:
        db.execute('CREATE TABLE IF NOT EXISTS parties (id TEXT PRIMARY KEY, etat TEXT NOT NULL)')
        db.execute('BEGIN IMMEDIATE')
        row = db.execute('SELECT etat FROM parties WHERE id=?', (game_id,)).fetchone()
        state = _new_state() if fresh or row is None else json.loads(row[0])
        result = func(state)
        if remove:
            db.execute('DELETE FROM parties WHERE id=?', (game_id,))
        else:
            db.execute('INSERT INTO parties(id,etat) VALUES(?,?) '
                       'ON CONFLICT(id) DO UPDATE SET etat=excluded.etat',
                       (game_id,json.dumps(state,ensure_ascii=False)))
        db.commit()
    return result


def _nom(c) -> str:
    return getattr(c,'name',str(c).upper())


def _decodage(mapping) -> dict:
    resultat = {}
    for k, value in (mapping or {}).items():
        c = getattr(CardName,str(k), None)
        if c is not None:
            resultat[c]=max(0,int(value))
    return resultat


def _compter(state, champ, c, incr=1):
    if c is None: return
    mapping = state.setdefault(champ,{})
    k = _nom(c)
    mapping[k] = max(0,int(mapping.get(k,0))+incr)


def _contexte(state, *, main=None, stock=None, player_count=None) -> Contexte:
    supply = quantites(stock) if stock is not None else _decodage(state.get('piles'))
    hand = quantites(main) if main is not None else {}
    return Contexte(
        tour=max(1,int(state.get('turn',1))),
        stock=supply,
        main=hand,
        achats=_decodage(state.get('purchased')),
        gains=_decodage(state.get('gained')),
        detruits=_decodage(state.get('trashed')),
        observation=_decodage(state.get('observed')),
        provinces=nombre(supply,carte('PROVINCE')) if supply else 8,
        piles_vides=sum(1 for v in supply.values() if int(v)==0),
        joueurs_actifs=int(player_count or state.get('joueurs_actifs',2)),
        actions=int(state.get('actions',1)),
        achats_restants=int(state.get('buys',1)),
        hirelings_jouees=int(state.get('hirelings_jouees',0)),
        budget=int(state.get('money_remaining') if state.get('money_remaining') is not None
                   else (monnaie_en_main(main) if main is not None else 0)
                       +int(state.get('bonus_money',0))),
    )


def _mesurer_stock(state,stock):
    # Ne pas inventer une pile épuisée si elle disparaît d'un snapshot partiel.
    state['piles']={_nom(k):int(v) for k,v in quantites(stock).items()}


def _mesurer_main(state,main):
    # Les malédictions reçues ne sont pas toutes signalées par un callback.
    # On ne peut en retenir qu'une borne basse du maximum vu simultanément.
    q=quantites(main)
    for c in (carte('CURSE'),):
        if c is not None:
            k=_nom(c)
            state['observed'][k]=max(int(state['observed'].get(k,0)),nombre(q,c))


def _player(game):
    players=list(getattr(game,'players',None) or [])
    # La V4 prenait le premier joueur ayant une main non nulle, ce qui peut
    # désigner un adversaire si plusieurs mains sont présentes dans le modèle.
    for p in players:
        if getattr(p,'name',None)=='Toulousain' and getattr(p,'hand',None) is not None:
            return p
    hands=[p for p in players if getattr(p,'hand',None) is not None]
    return hands[0] if len(hands)==1 else None


def _joueurs(game):
    players=list(getattr(game,'players',None) or [])
    return max(2,sum(1 for p in players if not any(
        getattr(p,x,None) is True for x in ('eliminated','is_eliminated','out'))))


def _extraire_carte(payload):
    for key in ('card_name','card','card_to_discard','card_to_trash'):
        val=getattr(payload,key,None)
        if isinstance(val,CardName): return val
        if val is not None:
            try: return CardName(getattr(val,'value',val))
            except (ValueError,TypeError): pass
    return None


def _evenement(state,category,card=None):
    event={'tour':state.get('turn',0),'type':category}
    if card is not None: event['carte']=_nom(card)
    state.setdefault('events',[]).append(event)
    state['events']=state['events'][-150:]
    return event


@app.exception_handler(Exception)
def unknown_exception_handler(_request:Request,exc:Exception):
    logger.exception('Erreur du bot')
    return JSONResponse(status_code=500,content={'message':'Erreur de la strategie',
                              'detail':str(exc),'name':exc.__class__.__name__})


@app.get('/',response_class=HTMLResponse)
def root():
    return "<html><body><h1>Toulousain - Dopynion V5</h1><a href='/docs'>API</a></body></html>"


@app.get("/name")
def name() -> str:
    return "Toulousain"


@app.get('/start_game')
def start_game(game_id:GameIdDependency)->DopynionResponseStr:
    _transition(game_id,lambda s: None,fresh=True)
    return DopynionResponseStr(game_id=game_id,decision='OK')


@app.get('/start_turn')
def start_turn(game_id:GameIdDependency)->DopynionResponseStr:
    def change(s):
        s['turn']=int(s.get('turn',0))+1
        s.update(actions=1,buys=1,bonus_money=0,money_remaining=None)
    _transition(game_id,change)
    return DopynionResponseStr(game_id=game_id,decision='OK')


@app.post('/play')
def play(game:Game,game_id:GameIdDependency)->DopynionResponseStr:
    player=_player(game)
    if player is None:
        logger.warning('Impossible d\'identifier notre main pour la partie %s',game_id)
        return DopynionResponseStr(game_id=game_id,decision='END_TURN')
    main=player.hand
    stock=game.stock
    def change(s):
        s['joueurs_actifs']=_joueurs(game)
        _mesurer_stock(s,stock)
        _mesurer_main(s,main)
        ctx=_contexte(s,main=main,stock=stock)
        selection=choisir_action(main,ctx)
        if selection is not None and int(s['actions'])>0:
            s['actions']=max(0,int(s['actions'])-1+selection.actions)
            s['buys']+=selection.buys
            s['bonus_money']+=selection.bonus_money
            hireling = carte('HIRELING')
            if hireling is not None and selection.decision == f'ACTION {hireling.value}':
                s['hirelings_jouees'] = int(s.get('hirelings_jouees',0)) + 1
            # Encore en phase Actions : le budget n'a normalement pas été figé.
            s['money_remaining']=None
            event=_evenement(s,'ACTION',selection.decision.split()[-1])
            _log_decision(game_id,event)
            return selection.decision
        if s['money_remaining'] is None:
            s['money_remaining']=monnaie_en_main(main)+int(s['bonus_money'])
        ctx=_contexte(s,main=main,stock=stock)
        ranked=priorites_achat(stock,contexte=ctx,achats_restants=int(s['buys']))
        if int(s['buys'])>0:
            for target in ranked:
                budget=int(s['money_remaining'])
                cmd=achat(main,target,stock,
                    monnaie_disponible=budget-monnaie_en_main(main),
                    achats_restants=int(s['buys']))
                if cmd:
                    s['money_remaining']=max(0,budget-cout_carte(target))
                    s['buys']-=1
                    _compter(s,'purchased',target)
                    event=_evenement(s,'BUY',target)
                    _log_decision(game_id,event)
                    return cmd
        return 'END_TURN'
    decision=_transition(game_id,change)
    return DopynionResponseStr(game_id=game_id,decision=decision)


@app.get('/end_game')
def end_game(game_id:GameIdDependency)->DopynionResponseStr:
    _transition(game_id,lambda s: None,remove=True)
    return DopynionResponseStr(game_id=game_id,decision='OK')


@app.post('/confirm_discard_card_from_hand')
def confirm_discard_card_from_hand(game_id:GameIdDependency,
    decision_input:CardNameAndHand)->DopynionResponseBool:
    card=_extraire_carte(decision_input)
    hand=list(getattr(decision_input,'hand',None) or [])
    return DopynionResponseBool(game_id=game_id,decision=_transition(game_id,
       lambda s: confirmer_defausse(card,hand,contexte=_contexte(s,main=_cards(hand)))))


class _cards:
    def __init__(self,values):
        self.quantities=Counter(values)


@app.post('/discard_card_from_hand')
def discard_card_from_hand(game_id:GameIdDependency,
    decision_input:Hand)->DopynionResponseCardName:
    hand=list(decision_input.hand)
    def change(s):
        card=choisir_defausse(hand,contexte=_contexte(s,main=_cards(hand)))
        _evenement(s,'DISCARD',card)
        return card
    return DopynionResponseCardName(game_id=game_id,decision=_transition(game_id,change))


@app.post('/confirm_trash_card_from_hand')
def confirm_trash_card_from_hand(game_id:GameIdDependency,
    decision_input:CardNameAndHand)->DopynionResponseBool:
    card=_extraire_carte(decision_input)
    hand=list(getattr(decision_input,'hand',None) or [])
    def change(s):
        decision=confirmer_destruction(card,contexte=_contexte(s,main=_cards(hand)))
        if decision:
            _compter(s,'trashed',card)
            _evenement(s,'TRASH',card)
        return decision
    return DopynionResponseBool(game_id=game_id,decision=_transition(game_id,change))


@app.post('/trash_card_from_hand')
def trash_card_from_hand(game_id:GameIdDependency,
    decision_input:Hand)->DopynionResponseCardName:
    hand=list(decision_input.hand)
    def change(s):
        card=choisir_destruction(hand,contexte=_contexte(s,main=_cards(hand)))
        if hand:
            _compter(s,'trashed',card)
            _evenement(s,'TRASH',card)
        return card
    return DopynionResponseCardName(game_id=game_id,decision=_transition(game_id,change))


@app.post('/confirm_discard_deck')
def confirm_discard_deck(game_id:GameIdDependency)->DopynionResponseBool:
    # Sans connaître la composition actuelle de la pioche et de la défausse,
    # on ne peut pas estimer correctement le bénéfice du Chancellor.
    return DopynionResponseBool(game_id=game_id,decision=False)


@app.post('/choose_card_to_receive_in_discard')
def choose_card_to_receive_in_discard(game_id:GameIdDependency,
    decision_input:PossibleCards)->DopynionResponseCardName:
    return _receive(game_id,list(decision_input.possible_cards),'discard')


def _receive(game_id,possibles,destination):
    def change(s):
        ctx=_contexte(s)
        chosen=choisir_carte_recue(possibles,destination=destination,contexte=ctx)
        if possibles:
            _compter(s,'gained',chosen)
            _evenement(s,'GAIN_'+destination,chosen)
        return chosen
    return DopynionResponseCardName(game_id=game_id,decision=_transition(game_id,change))


@app.post('/choose_card_to_receive_in_deck')
def choose_card_to_receive_in_deck(game_id:GameIdDependency,
    decision_input:PossibleCards)->DopynionResponseCardName:
    return _receive(game_id,list(decision_input.possible_cards),'deck')


@app.post('/skip_card_reception_in_hand')
def skip_card_reception_in_hand(game_id:GameIdDependency,
    decision_input:CardNameAndHand)->DopynionResponseBool:
    card=_extraire_carte(decision_input)
    hand=list(getattr(decision_input,'hand',None) or [])
    decision=_transition(game_id,lambda s: sauter_reception_en_main(
        card,contexte=_contexte(s,main=_cards(hand))))
    return DopynionResponseBool(game_id=game_id,decision=decision)


@app.post('/trash_money_card_for_better_money_card')
def trash_money_card_for_better_money_card(game_id:GameIdDependency,
    decision_input:MoneyCardsInHand)->DopynionResponseCardName:
    monies=list(decision_input.money_in_hand)
    def change(s):
        chosen=choisir_monnaie_a_detruire(monies,contexte=_contexte(s))
        if monies:
            _compter(s,'trashed',chosen)
            _evenement(s,'TRASH',chosen)
        return chosen
    return DopynionResponseCardName(game_id=game_id,decision=_transition(game_id,change))
