"""Adaptateur Action. Le classement dépend de strategie.valeur_action, pas d'une liste fixe."""
from dataclasses import dataclass
from dopynion.data_model import CardName
from strategie import (ACTIONS_CONNUES, CONTINUATIONS, Contexte, est_action,
                       nombre, valeur_action, carte)

@dataclass(frozen=True)
class EffetsAction:
    actions: int = 0
    buys: int = 0
    bonus_money: int = 0

@dataclass(frozen=True)
class ResultatAction:
    decision: str
    end_action: bool = False
    actions: int = 0
    buys: int = 0
    bonus_money: int = 0

EFFETS_ACTION = {}

def enregistrer(nom, *, actions=0, buys=0, bonus_money=0):
    c = carte(nom)
    if c is not None:
        EFFETS_ACTION[c] = EffetsAction(actions, buys, bonus_money)

for c in ACTIONS_CONNUES:
    EFFETS_ACTION[c] = EffetsAction()
for c in (carte('VILLAGE'), carte('FARMINGVILLAGE'), carte('FESTIVAL')):
    if c is not None: EFFETS_ACTION[c] = EffetsAction(actions=2)
for c in (carte('LABORATORY'), carte('MARKET'), carte('DISTANTSHORE'),
          carte('CELLAR'), carte('SWAP')):
    if c is not None: EFFETS_ACTION[c] = EffetsAction(actions=1)
for nom, effets in {
    'FESTIVAL': (2,1,2), 'MARKET': (1,1,1), 'WOODCUTTER': (0,1,2),
    'COUNCILROOM': (0,1,0), 'CHANCELLOR': (0,0,2), 'MILITIA': (0,0,2),
    'FORTUNETELLER': (0,0,2), 'MONEYLENDER': (0,0,3),
}.items():
    enregistrer(nom, actions=effets[0], buys=effets[1], bonus_money=effets[2])

# Compatibilité avec les scripts qui importent encore ACTION_PRIORITY.
# server.py V5 n'utilise plus cette liste pour décider.
ACTION_PRIORITY = ACTIONS_CONNUES


def effets_action(c):
    return EFFETS_ACTION[c]


def action(main, carte, *, actions_restantes=1):
    """Signature conservée de la V4, validation individuelle de la carte."""
    if actions_restantes<=0 or not est_action(carte) or nombre(getattr(main,'quantities',{}),carte)==0:
        return False
    e = EFFETS_ACTION.get(carte)
    if e is None: return False
    return ResultatAction(f'ACTION {carte.value}', False, e.actions,e.buys,e.bonus_money)


def choisir_action(main, ctx: Contexte):
    """Compare les actions présentes au lieu d'appliquer un ordre constant."""
    possibilites = [c for c in ACTIONS_CONNUES if nombre(ctx.main,c)>0 and est_action(c)]
    if not possibilites or ctx.actions<=0:
        return None
    meilleure = max(possibilites,key=lambda c: valeur_action(c,ctx))
    if valeur_action(meilleure,ctx)==float('-inf'):
        return None
    return action(main,meilleure,actions_restantes=ctx.actions)
