"""Gestion de la phase d'action pour le bot Toulousain test.

Le moteur Dopynion applique les effets complets des cartes. Ce module indique
uniquement la décision ACTION et les bonus qui doivent être suivis localement
par server.py (actions, achats et argent supplémentaire).
"""

from dataclasses import dataclass, replace
from typing import Literal

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


@dataclass(frozen=True)
class EffetsAction:
    """Bonus à ajouter aux compteurs locaux après avoir joué une carte."""

    actions: int = 0
    buys: int = 0
    bonus_money: int = 0


# Important : les valeurs représentent les bonus de la carte, pas le coût
# d'une action pour la jouer. server.py calcule le solde avec :
# actions_restantes - 1 + effets.actions.
EFFETS_ACTION: dict[CardName, EffetsAction] = {
    # Actions qui permettent de continuer à jouer d'autres actions.
    CardName.VILLAGE: EffetsAction(actions=2),
    CardName.FARMINGVILLAGE: EffetsAction(actions=2),
    CardName.FESTIVAL: EffetsAction(actions=2, buys=1, bonus_money=2),
    CardName.LABORATORY: EffetsAction(actions=1),
    CardName.MARKET: EffetsAction(actions=1, buys=1, bonus_money=1),
    CardName.DISTANTSHORE: EffetsAction(actions=1),
    CardName.CELLAR: EffetsAction(actions=1),
    # Troc : +1 action compense l'action dépensée pour le jouer.
    CardName.SWAP: EffetsAction(actions=1),
    **({CardName.FEAST: EffetsAction()} if hasattr(CardName, "FEAST") else {}),

    # Actions terminales : elles ne rendent pas d'action.
    CardName.CHAPEL: EffetsAction(),
    CardName.MINE: EffetsAction(),
    CardName.MONEYLENDER: EffetsAction(bonus_money=3),
    CardName.REMODEL: EffetsAction(),
    CardName.WITCH: EffetsAction(),
    CardName.BANDIT: EffetsAction(),
    CardName.HIRELING: EffetsAction(),
    CardName.COUNCILROOM: EffetsAction(buys=1),
    CardName.LIBRARY: EffetsAction(),
    CardName.SMITHY: EffetsAction(),
    CardName.MILITIA: EffetsAction(bonus_money=2),
    CardName.FORTUNETELLER: EffetsAction(bonus_money=2),
    CardName.MAGNATE: EffetsAction(),
    CardName.ADVENTURER: EffetsAction(),
    CardName.BUREAUCRAT: EffetsAction(),
    CardName.WORKSHOP: EffetsAction(),
    CardName.CHANCELLOR: EffetsAction(bonus_money=2),
    CardName.WOODCUTTER: EffetsAction(buys=1, bonus_money=2),
}


# L'ordre est important : server.py joue la première carte de cette liste
# présente en main, puis rappelle /play après résolution de son effet.
# 1. Libérer des actions avant de jouer les cartes terminales.
# 2. Utiliser les améliorations/bonus de trésor avant que Chapelle ne retire
#    les Cuivres qui pourraient leur servir.
# 3. Épurer avec Chapelle avant les autres actions terminales moins urgentes.
# 4. Jouer ensuite pioche, attaques et cartes économiques.
ACTION_PRIORITY: tuple[CardName, ...] = (
    # Actions supplémentaires
    CardName.FARMINGVILLAGE,
    CardName.VILLAGE,
    CardName.FESTIVAL,
    CardName.LABORATORY,
    CardName.MARKET,
    CardName.DISTANTSHORE,
    CardName.CELLAR,
    CardName.SWAP,

    # Actions terminales à fort impact avant l’épuration secondaire.
    CardName.WITCH,
    CardName.BANDIT,
    CardName.HIRELING,
    CardName.COUNCILROOM,
    CardName.LIBRARY,
    CardName.SMITHY,
    CardName.MILITIA,
    CardName.FORTUNETELLER,
    CardName.MAGNATE,
    CardName.ADVENTURER,
    CardName.BUREAUCRAT,
    CardName.WORKSHOP,
    CardName.CHANCELLOR,
    CardName.WOODCUTTER,
    # La Chapelle ne doit pas occuper l’action unique face à une Sorcière.
    CardName.CHAPEL,
    CardName.MONEYLENDER,
    CardName.MINE,
    CardName.REMODEL,
    *((CardName.FEAST,) if hasattr(CardName, "FEAST") else ()),
)


@dataclass(frozen=True)
class ResultatAction:
    decision: str
    end_action: bool
    actions: int
    buys: int
    bonus_money: int


def effets_action(carte: CardName) -> EffetsAction:
    """Retourne les bonus connus pour une carte Action."""
    try:
        return EFFETS_ACTION[carte]
    except KeyError:
        raise ValueError(f"Effets non définis pour la carte {carte}.") from None


def confirmer_fin_action(resultat: ResultatAction) -> ResultatAction:
    """Marque un résultat comme fin de phase d'action."""
    return replace(resultat, end_action=True)


def _card_type(carte: CardName):
    """Retourne la classe de carte, ou Card si elle n'est pas reconnue."""
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
    """Renvoie ACTION uniquement si la carte est en main et est jouable."""
    if actions_restantes <= 0:
        return False

    quantites = getattr(main, "quantities", {}) or {}
    try:
        if int(quantites.get(carte, 0)) <= 0:
            return False
    except (TypeError, ValueError):
        return False

    carte_type = _card_type(carte)
    if carte_type is Card or not bool(getattr(carte_type, "is_action", False)):
        return False

    effets = EFFETS_ACTION.get(carte)
    if effets is None:
        return False

    return ResultatAction(
        decision=f"ACTION {carte.value}",
        end_action=False,
        actions=effets.actions,
        buys=effets.buys,
        bonus_money=effets.bonus_money,
    )
