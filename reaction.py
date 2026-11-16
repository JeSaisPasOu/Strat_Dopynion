"""Décisions de réaction et de choix de cartes pour Toulousain test."""

from dopynion.cards import Card
from dopynion.data_model import CardName


def confirmer_defausse(carte: CardName | None) -> bool:
    """Autorise la défausse des cartes mortes ou de faible valeur."""
    return carte in {
        CardName.CURSE,
        CardName.ESTATE,
        CardName.DUCHY,
        CardName.PROVINCE,
        CardName.GARDENS,
        CardName.COPPER,
    }


def choisir_defausse(main: list[CardName]) -> CardName:
    """Écarte d'abord les points morts et les cuivres, préserve les actions utiles."""
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
    """Ne détruit que les cartes qui encombrent généralement le deck."""
    return carte in {CardName.CURSE, CardName.ESTATE, CardName.COPPER}


def choisir_destruction(main: list[CardName]) -> CardName:
    """Détruit Curse puis Estate puis Copper, sans sacrifier une carte utile."""
    for card in (CardName.CURSE, CardName.ESTATE, CardName.COPPER):
        if card in main:
            return card
    return main[0] if main else CardName.COPPER


def _cost(card: CardName) -> int:
    try:
        card_type = Card.class_(card)
        return int(card_type.cost) if card_type is not Card else 0
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def choisir_carte_recue(possibles: list[CardName], destination: str = "discard") -> CardName:
    """Choisit la meilleure carte parmi les choix proposés par le moteur.

    Cette fonction sert notamment à sélectionner la carte gagnée par Workshop.
    Elle ne choisit jamais une carte absente de la liste des possibilités.
    """
    if not possibles:
        return CardName.COPPER

    valeurs = {
        CardName.PROVINCE: 100,
        CardName.GOLD: 92,
        CardName.HIRELING: 91,
        CardName.LABORATORY: 88,
        CardName.WITCH: 86,
        CardName.BANDIT: 84,
        CardName.FESTIVAL: 83,
        CardName.MILITIA: 78,
        CardName.COUNCILROOM: 77,
        CardName.MARKET: 76,
        CardName.LIBRARY: 75,
        CardName.SMITHY: 72,
        CardName.DISTANTSHORE: 68,
        CardName.FORTUNETELLER: 70,
        CardName.FARMINGVILLAGE: 66,
        CardName.BUREAUCRAT: 63,
        CardName.WORKSHOP: 59,
        CardName.CELLAR: 49,
        CardName.MAGNATE: 65,
        CardName.ADVENTURER: 57,
        CardName.SILVER: 61,
        CardName.CHANCELLOR: 45,
        CardName.VILLAGE: 57,
        CardName.WOODCUTTER: 54,
        CardName.GARDENS: 35,
        CardName.DUCHY: 28,
        CardName.ESTATE: 15,
        CardName.COPPER: 2,
        CardName.CURSE: -100,
    }

    def score(card: CardName) -> float:
        value = float(valeurs.get(card, 20 + 2 * _cost(card)))
        if destination == "deck":
            if card in (CardName.PROVINCE, CardName.DUCHY, CardName.ESTATE, CardName.GARDENS):
                value -= 42
            if card in (
                CardName.LABORATORY,
                CardName.FESTIVAL,
                CardName.MARKET,
                CardName.HIRELING,
                CardName.GOLD,
                CardName.WITCH,
                CardName.BANDIT,
                CardName.LIBRARY,
                CardName.COUNCILROOM,
                CardName.SMITHY,
            ):
                value += 7
        return value

    return max(possibles, key=score)


def sauter_reception_en_main() -> bool:
    """False signifie qu'on accepte la réception de la carte en main."""
    return False


def choisir_monnaie_a_detruire(monnaies: list[CardName]) -> CardName:
    """Détruit en priorité Copper, puis Silver si aucun Copper n'est disponible."""
    for card in (CardName.COPPER, CardName.SILVER):
        if card in monnaies:
            return card
    return monnaies[0] if monnaies else CardName.COPPER
