"""Décisions de réaction, d'épuration et de transformation des cartes."""

from dopynion.cards import Card
from dopynion.data_model import CardName


def _optional_card(*names: str):
    for name in names:
        value = getattr(CardName, name, None)
        if value is not None:
            return value
    return None


CHAPEL = _optional_card("CHAPEL", "CHAPELLE")
MINE = _optional_card("MINE")
MONEYLENDER = _optional_card("MONEYLENDER", "MONEY_LENDER", "PRETEUR_SUR_GAGES")
REMODEL = _optional_card("REMODEL", "RENOVATION", "REMODELATION")
SWAP = _optional_card("SWAP", "TROC")
COLONY = _optional_card("COLONY", "COLONIE")


def _count(mapping, card) -> int:
    if mapping is None or card is None:
        return 0
    try:
        return max(0, int(mapping.get(card, 0)))
    except (AttributeError, TypeError, ValueError):
        return 0


def confirmer_defausse(carte: CardName | None) -> bool:
    """Accepte de défausser les cartes mortes avant les cartes de valeur."""
    return carte in {
        CardName.CURSE,
        CardName.ESTATE,
        CardName.COPPER,
        CardName.GARDENS,
        CardName.CHANCELLOR,
        CardName.WOODCUTTER,
    }


def choisir_defausse(main: list[CardName]) -> CardName:
    """En cas de défausse imposée, conserve les meilleures cartes."""
    ordre = [
        CardName.CURSE,
        CardName.ESTATE,
        CardName.COPPER,
        CardName.GARDENS,
        CardName.CHANCELLOR,
        CardName.WOODCUTTER,
        CardName.BUREAUCRAT,
        CardName.WORKSHOP,
        CardName.ADVENTURER,
        CardName.MAGNATE,
        CardName.FORTUNETELLER,
        CardName.CELLAR,
        CardName.VILLAGE,
        CardName.FARMINGVILLAGE,
        CardName.SMITHY,
        CardName.LIBRARY,
        CardName.COUNCILROOM,
        CardName.MILITIA,
        CardName.BANDIT,
        CardName.WITCH,
        CardName.LABORATORY,
        CardName.FESTIVAL,
        CardName.MARKET,
        CardName.HIRELING,
        CardName.SILVER,
        CardName.GOLD,
    ]
    for card in ordre:
        if card in main:
            return card
    return main[0] if main else CardName.COPPER


def confirmer_destruction(carte: CardName | None) -> bool:
    """Autorise Chapel à épurer Curse/Estate/Copper et Moneylender à ôter Copper.

    Le moteur limite lui-même les cartes proposées à Moneylender : dans ce cas,
    seul Copper est normalement présenté. Pour Chapel, plusieurs appels peuvent
    être faits, jusqu'à quatre cartes.
    """
    return carte in {CardName.CURSE, CardName.ESTATE, CardName.COPPER}


def _remodel_trash_priority(card: CardName, turn: int) -> tuple[int, int]:
    """Rang de sacrifice pour Remodel : plus petit = meilleure cible à détruire."""
    # Estate coûte 2 : le détruire ouvre une cible jusqu'à 4, souvent
    # nettement plus intéressante. À coût égal (0), Curse passe avant Copper.
    if card == CardName.ESTATE:
        return (0, 0)
    if card == CardName.CURSE:
        return (1, 0)
    if card == CardName.COPPER:
        return (2, 0)
    # Si les déchets ont déjà disparu, on ne sacrifie que des cartes
    # généralement faibles, et jamais les gros moteurs/points.
    weak_order = [
        CardName.CHANCELLOR,
        CardName.WOODCUTTER,
        CardName.BUREAUCRAT,
        CardName.GARDENS,
        CardName.CELLAR,
        CardName.WORKSHOP,
        CardName.ADVENTURER,
    ]
    if card in weak_order:
        return (3, weak_order.index(card))
    if card == CardName.DUCHY and turn <= 8:
        return (4, 0)
    # Argent n'est sacrifié qu'en toute dernière option, plutôt tard.
    if card == CardName.SILVER and turn >= 15:
        return (5, 0)
    return (100, 0)


def choisir_destruction(main: list[CardName], *, tour: int = 1) -> CardName:
    """Choisit la carte la moins utile à transformer avec Remodel."""
    if not main:
        return CardName.COPPER
    eligible = [card for card in main if _remodel_trash_priority(card, tour)[0] < 100]
    if eligible:
        return min(eligible, key=lambda card: _remodel_trash_priority(card, tour))
    # Si aucune carte clairement sacrifiable n'est présente, choisir la carte
    # d'action la moins intéressante plutôt que toucher à Gold/Province.
    safe_fallback = [
        card for card in main
        if card not in {CardName.PROVINCE, CardName.GOLD, CardName.HIRELING,
                        CardName.LABORATORY, CardName.WITCH, CardName.FESTIVAL,
                        CardName.MARKET, CardName.BANDIT}
    ]
    return safe_fallback[0] if safe_fallback else main[0]


def _cost(card: CardName) -> int:
    try:
        card_type = Card.class_(card)
        return int(card_type.cost) if card_type is not Card else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def choisir_carte_recue(
    possibles: list[CardName],
    destination: str = "discard",
    *,
    tour: int = 1,
    achats=None,
    trashed=None,
) -> CardName:
    """Choisit la meilleure carte légale parmi les options fournies par le moteur."""
    if not possibles:
        return CardName.COPPER

    # Le socle initial est estimé à 7 Cuivres + 3 Domaines ; les Malédictions
    # sont des déchets supplémentaires et ne réduisent pas cette estimation.
    junk_left = max(0, 10 - _count(trashed, CardName.ESTATE) - _count(trashed, CardName.COPPER))
    bought = achats or {}

    valeurs = {
        CardName.PROVINCE: 155,
        CardName.GOLD: 111,
        CardName.HIRELING: 108,
        CardName.LABORATORY: 103,
        CardName.WITCH: 100,
        CardName.BANDIT: 94,
        CardName.FESTIVAL: 96,
        CardName.MILITIA: 86,
        CardName.COUNCILROOM: 82,
        CardName.MARKET: 84,
        CardName.LIBRARY: 91,
        CardName.SMITHY: 76,
        CardName.DISTANTSHORE: 69,
        CardName.FORTUNETELLER: 80,
        CardName.FARMINGVILLAGE: 67,
        CardName.BUREAUCRAT: 57,
        CardName.WORKSHOP: 55,
        CardName.CELLAR: 54,
        CardName.MAGNATE: 76,
        CardName.ADVENTURER: 65,
        CardName.SILVER: 70,
        CardName.CHANCELLOR: 36,
        CardName.VILLAGE: 59,
        CardName.WOODCUTTER: 32,
        CardName.GARDENS: 25,
        CardName.DUCHY: 38 if tour >= 13 else 8,
        CardName.ESTATE: 12,
        CardName.COPPER: 0,
        CardName.CURSE: -100,
    }
    if COLONY is not None:
        valeurs[COLONY] = 170
    if CHAPEL is not None:
        valeurs[CHAPEL] = 101 if tour <= 7 and junk_left >= 3 else 50 if tour <= 12 else 25
        if _count(bought, CHAPEL) > 0:
            valeurs[CHAPEL] -= 18
    if MINE is not None:
        valeurs[MINE] = 86 if tour <= 12 else 60
        if _count(bought, MINE) > 0:
            valeurs[MINE] -= 22
    if MONEYLENDER is not None:
        valeurs[MONEYLENDER] = 82 if tour <= 10 and junk_left >= 3 else 45
        if _count(bought, MONEYLENDER) > 0:
            valeurs[MONEYLENDER] -= 20
    if REMODEL is not None:
        valeurs[REMODEL] = 88 if tour <= 12 else 58
        if _count(bought, REMODEL) > 0:
            valeurs[REMODEL] -= 15
    if SWAP is not None:
        valeurs[SWAP] = 68 if tour <= 12 else 45

    def score(card: CardName) -> float:
        value = float(valeurs.get(card, 20 + 2 * _cost(card)))
        if destination == "deck":
            if card in (CardName.PROVINCE, CardName.DUCHY, CardName.ESTATE, CardName.GARDENS):
                value -= 35
            if card in (
                CardName.LABORATORY, CardName.FESTIVAL, CardName.MARKET,
                CardName.HIRELING, CardName.GOLD, CardName.WITCH,
                CardName.BANDIT, CardName.LIBRARY, CardName.COUNCILROOM,
                CardName.SMITHY,
            ):
                value += 6
        return value

    return max(possibles, key=score)


def sauter_reception_en_main() -> bool:
    """False signifie qu'on accepte la réception de la carte en main."""
    return False


def _money(card: CardName) -> int:
    try:
        card_type = Card.class_(card)
        return int(getattr(card_type, "money", 0)) if card_type is not Card else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def choisir_monnaie_a_detruire(monnaies: list[CardName], *, tour: int = 1) -> CardName:
    """Pour Mine, upgrade prioritairement le trésor de plus grande valeur.

    Silver -> Gold apporte un gain supérieur à Copper -> Silver. Si aucune
    carte Silver n'est disponible, on détruit Copper.
    """
    if not monnaies:
        return CardName.COPPER
    # D'après les évolutions confirmées : Silver -> Gold est prioritaire,
    # sinon Copper -> Silver. Ne pas supposer une évolution Gold -> autre chose
    # tant que le moteur n'a pas confirmé cette possibilité.
    if CardName.SILVER in monnaies:
        return CardName.SILVER
    if CardName.COPPER in monnaies:
        return CardName.COPPER
    return monnaies[0]
