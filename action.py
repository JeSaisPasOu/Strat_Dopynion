"""Vérification d'une carte action choisie par le programme stratégie."""

from dataclasses import dataclass, replace
from typing import Literal

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


@dataclass(frozen=True)
class EffetsAction:


    actions: int = 0
    buys: int = 0
    bonus_money: int = 0


EFFETS_ACTION: dict[CardName, EffetsAction] = {
    CardName.VILLAGE: EffetsAction(actions=2),
    CardName.WOODCUTTER: EffetsAction(buys=1, bonus_money=2),
    CardName.SMITHY: EffetsAction(),
    CardName.FESTIVAL: EffetsAction(actions=2, buys=1, bonus_money=2),
    CardName.LABORATORY: EffetsAction(actions=1),
    CardName.MARKET: EffetsAction(actions=1, buys=1, bonus_money=1),
    CardName.COUNCILROOM: EffetsAction(buys=1),
    CardName.WITCH: EffetsAction(),
    CardName.FARMINGVILLAGE: EffetsAction(actions=2),
    CardName.DISTANTSHORE: EffetsAction(actions=1),
    CardName.HIRELING: EffetsAction(),
    CardName.BANDIT: EffetsAction(),
    CardName.BUREAUCRAT: EffetsAction(),
    CardName.CHANCELLOR: EffetsAction(0, 0, 2),
    CardName.GARDENS: EffetsAction(),
    CardName.MILITIA: EffetsAction(0, 0, 2)
}


def effets_action(carte: CardName) -> EffetsAction:
    try:
        return EFFETS_ACTION[carte]
    except KeyError:
        raise ValueError(f"Effets non définis pour la carte {carte}.") from None


@dataclass(frozen=True)
class ResultatAction:
    decision: str
    end_action: bool
    actions: int
    buys: int
    bonus_money: int


def confirmer_fin_action(resultat: ResultatAction) -> ResultatAction:
    return replace(resultat, end_action=True)


def action(
    main: Cards,
    carte: CardName,
    *,
    actions_restantes: int = 1,
) -> ResultatAction | Literal[False]:
    if actions_restantes <= 0:
        return False

    if main.quantities.get(carte, 0) <= 0:
        return False

    if not Card.class_(carte).is_action:
        return False

    if carte not in EFFETS_ACTION:
        return False

    effets = effets_action(carte)
    resultat = ResultatAction(
        decision=f"ACTION {carte.value}",
        end_action=False,
        actions=effets.actions,
        buys=effets.buys,
        bonus_money=effets.bonus_money,
    )
    
    return resultat