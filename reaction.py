"""Décisions de réaction : défausse, destruction et cartes reçues."""

from typing import Iterable

from dopynion.data_model import CardName


def confirmer_defausse(carte: CardName | None) -> bool:
    """Accepte surtout de défausser les cartes peu utiles pour les pièces du tour."""
    return carte in {
        CardName.CURSE,
        CardName.ESTATE,
        CardName.DUCHY,
        CardName.PROVINCE,
        CardName.GARDENS,
        CardName.COPPER,
    }


def choisir_defausse(main: list[CardName]) -> CardName:
    """Défausse d'abord les cartes mortes, en préservant les trésors forts."""
    ordre = [
        CardName.CURSE,
        CardName.ESTATE,
        CardName.DUCHY,
        CardName.PROVINCE,
        CardName.GARDENS,
        CardName.COPPER,
        CardName.CHANCELLOR,
        CardName.WOODCUTTER,
        CardName.BUREAUCRAT,
        CardName.VILLAGE,
        CardName.FARMINGVILLAGE,
        CardName.SMITHY,
        CardName.SILVER,
        CardName.GOLD,
    ]
    for card in ordre:
        if card in main:
            return card
    return main[0] if main else CardName.COPPER


def confirmer_destruction(carte: CardName | None) -> bool:
    """Ne détruit volontairement que les cartes généralement nuisibles."""
    return carte in {CardName.CURSE, CardName.ESTATE, CardName.COPPER}


def choisir_destruction(main: list[CardName]) -> CardName:
    """Choisit les cartes à détruire dans l'ordre le moins coûteux."""
    ordre = [CardName.CURSE, CardName.ESTATE, CardName.COPPER]
    for card in ordre:
        if card in main:
            return card
    # Pas de carte que l'on souhaite détruire : renvoie une carte disponible.
    # confirmer_destruction() refusera ensuite une destruction coûteuse.
    return main[0] if main else CardName.COPPER


def _cost(card: CardName) -> int:
    try:
        from dopynion.cards import Card
        card_type = Card.class_(card)
        return int(card_type.cost) if card_type is not Card else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def choisir_carte_recue(possibles: list[CardName], destination: str = "discard") -> CardName:
    """Préfère les cartes utiles, et évite les points de victoire au-dessus du deck."""
    if not possibles:
        return CardName.COPPER

    valeurs = {
        CardName.PROVINCE: 82,
        CardName.GOLD: 80,
        CardName.HIRELING: 79,
        CardName.LABORATORY: 77,
        CardName.FESTIVAL: 74,
        CardName.WITCH: 73,
        CardName.BANDIT: 72,
        CardName.MARKET: 70,
        CardName.COUNCILROOM: 69,
        CardName.MILITIA: 68,
        CardName.DISTANTSHORE: 64,
        CardName.SMITHY: 63,
        CardName.DUCHY: 45,
        CardName.FARMINGVILLAGE: 45,
        CardName.BUREAUCRAT: 43,
        CardName.SILVER: 42,
        CardName.CHANCELLOR: 38,
        CardName.VILLAGE: 38,
        CardName.WOODCUTTER: 36,
        CardName.GARDENS: 30,
        CardName.ESTATE: 18,
        CardName.COPPER: 5,
        CardName.CURSE: -100,
    }

    def score(card: CardName) -> float:
        value = float(valeurs.get(card, 20 + 2 * _cost(card)))
        if destination == "deck":
            if card in (CardName.PROVINCE, CardName.DUCHY, CardName.ESTATE, CardName.GARDENS):
                value -= 35
            if card in (
                CardName.LABORATORY,
                CardName.FESTIVAL,
                CardName.MARKET,
                CardName.HIRELING,
                CardName.GOLD,
                CardName.WITCH,
                CardName.BANDIT,
            ):
                value += 7
        return value

    return max(possibles, key=score)


def sauter_reception_en_main() -> bool:
    """False : accepte par défaut de recevoir la carte dans la main."""
    return False


def choisir_monnaie_a_detruire(monnaies: list[CardName]) -> CardName:
    """Détruit en priorité le cuivre pour obtenir une meilleure carte de monnaie."""
    for card in (CardName.COPPER, CardName.SILVER):
        if card in monnaies:
            return card
    return monnaies[0] if monnaies else CardName.COPPER
