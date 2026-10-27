"""Gestion prudente de la phase d'action pour le bot Dopynion."""

from dataclasses import dataclass, replace
from typing import Literal

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


@dataclass(frozen=True)
class EffetsAction:
    """Nombre d'effets bonus déclarés par la carte, avant consommation de l'action."""

    actions: int = 0
    buys: int = 0
    bonus_money: int = 0


# Ces valeurs servent uniquement à maintenir le compteur local du bot.
# Les effets complets des cartes sont exécutés par l'arbitre Dopynion.
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
    CardName.CHANCELLOR: EffetsAction(bonus_money=2),
    CardName.GARDENS: EffetsAction(),
    CardName.MILITIA: EffetsAction(bonus_money=2),
}


@dataclass(frozen=True)
class ResultatAction:
    decision: str
    end_action: bool
    actions: int
    buys: int
    bonus_money: int


def effets_action(carte: CardName) -> EffetsAction:
    try:
        return EFFETS_ACTION[carte]
    except KeyError:
        raise ValueError(f"Effets non définis pour la carte {carte}.") from None


def confirmer_fin_action(resultat: ResultatAction) -> ResultatAction:
    return replace(resultat, end_action=True)


def _card_type(carte: CardName):
    """Retourne le type de carte si connu, sans faire planter une décision API."""
    try:
        return Card.class_(carte)
    except (AttributeError, TypeError, ValueError, KeyError):
        return Card


def action(
    main: Cards,
    carte: CardName,
    *,
    actions_restantes: int = 1,
) -> ResultatAction | Literal[False]:
    """Propose une action seulement si elle est réellement présente et jouable."""
    if actions_restantes <= 0:
        return False

    quantites = getattr(main, "quantities", {}) or {}
    if int(quantites.get(carte, 0)) <= 0:
        return False

    carte_type = _card_type(carte)
    if carte_type is Card or not bool(getattr(carte_type, "is_action", False)):
        return False
    if carte not in EFFETS_ACTION:
        return False

    effets = effets_action(carte)
    return ResultatAction(
        decision=f"ACTION {carte.value}",
        end_action=False,
        actions=effets.actions,
        buys=effets.buys,
        bonus_money=effets.bonus_money,
    )
