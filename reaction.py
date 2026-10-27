"""Choix de réaction : défausse, destruction et cartes reçues."""
from typing import Iterable

from dopynion.data_model import CardName


def confirmer_defausse(carte: CardName | None) -> bool:
    """Accepte la défausse volontaire de cartes généralement peu utiles en main."""
    return carte in {
        CardName.CURSE,
        CardName.PROVINCE,
        CardName.DUCHY,
        CardName.ESTATE,
    }


def choisir_defausse(main: list[CardName]) -> CardName:
    """Lors d'une défausse forcée, jette d'abord les cartes mortes en main."""
    ordre = [
        CardName.CURSE, CardName.ESTATE, CardName.DUCHY, CardName.PROVINCE,
        CardName.COPPER, CardName.SILVER,
    ]
    for card in ordre:
        if card in main:
            return card
    return main[0] if main else CardName.COPPER


def confirmer_destruction(carte: CardName | None) -> bool:
    """Confirme la destruction d'une malédiction, d'un domaine ou d'un cuivre."""
    return carte in {CardName.CURSE, CardName.ESTATE, CardName.COPPER}


def choisir_destruction(main: list[CardName]) -> CardName:
    """Choisit une carte faible à détruire si l'arbitre impose un choix."""
    ordre = [CardName.CURSE, CardName.ESTATE, CardName.COPPER, CardName.SILVER]
    for card in ordre:
        if card in main:
            return card
    return main[0] if main else CardName.COPPER


def _cost(card: CardName) -> int:
    # Valeurs de repli : suffisantes pour départager les cartes si le SDK ne donne
    # pas un coût pour une carte dans l'ensemble fourni.
    try:
        from dopynion.cards import Card
        card_type = Card.class_(card)
        return int(card_type.cost) if card_type is not Card else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def choisir_carte_recue(possibles: list[CardName], destination: str = "discard") -> CardName:
    """Préfère une carte forte, en tenant compte du fait qu'elle va au-dessus du deck."""
    if not possibles:
        return CardName.COPPER
    valeurs = {
        CardName.PROVINCE: 80, CardName.GOLD: 76, CardName.HIRELING: 75,
        CardName.BANDIT: 68, CardName.WITCH: 67, CardName.LABORATORY: 66,
        CardName.FESTIVAL: 65, CardName.MARKET: 62, CardName.COUNCILROOM: 62,
        CardName.DISTANTSHORE: 60, CardName.DUCHY: 55, CardName.FARMINGVILLAGE: 55,
        CardName.MILITIA: 54, CardName.BUREAUCRAT: 51, CardName.SMITHY: 51,
        CardName.SILVER: 45, CardName.CHANCELLOR: 38, CardName.VILLAGE: 37,
        CardName.WOODCUTTER: 36, CardName.GARDENS: 34, CardName.ESTATE: 18,
        CardName.COPPER: 5, CardName.CURSE: -20,
    }

    def score(card: CardName) -> float:
        value = float(valeurs.get(card, 20 + 2 * _cost(card)))
        if destination == "deck":
            if card in (CardName.PROVINCE, CardName.DUCHY, CardName.ESTATE, CardName.GARDENS):
                value -= 25
            if card in (CardName.LABORATORY, CardName.FESTIVAL, CardName.MARKET, CardName.HIRELING):
                value += 8
        return value

    return max(possibles, key=score)


def sauter_reception_en_main() -> bool:
    """False signifie par défaut que le bot ne demande pas à sauter la réception."""
    return False


def choisir_monnaie_a_detruire(monnaies: list[CardName]) -> CardName:
    """Choisit la carte de monnaie la plus faible présente."""
    for card in (CardName.COPPER, CardName.SILVER):
        if card in monnaies:
            return card
    return monnaies[0] if monnaies else CardName.COPPER
