"""Évaluation et validation des achats pour Toulousain test."""

from typing import Iterable, Mapping

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


# Cartes gérées explicitement par la stratégie fournie. Silver est gardé comme
# solution de repli économique quand aucune carte plus rentable n'est disponible.
CARTES_STRATEGIE: tuple[CardName, ...] = (
    CardName.PROVINCE,
    CardName.GOLD,
    CardName.HIRELING,
    CardName.WITCH,
    CardName.BANDIT,
    CardName.LABORATORY,
    CardName.FESTIVAL,
    CardName.MILITIA,
    CardName.COUNCILROOM,
    CardName.MARKET,
    CardName.SMITHY,
    CardName.DISTANTSHORE,
    CardName.SILVER,
    CardName.WOODCUTTER,
    CardName.FARMINGVILLAGE,
    CardName.VILLAGE,
    CardName.BUREAUCRAT,
    CardName.CHANCELLOR,
    CardName.GARDENS,
    CardName.DUCHY,
    CardName.ESTATE,
)


def type_carte(carte: CardName):
    try:
        return Card.class_(carte)
    except (AttributeError, TypeError, ValueError, KeyError):
        return Card


def cout_carte(carte: CardName) -> int:
    """Coût entier de la carte, ou un coût impossible si elle est inconnue."""
    classe = type_carte(carte)
    if classe is Card:
        return 10**6
    try:
        return int(classe.cost)
    except (AttributeError, TypeError, ValueError):
        return 10**6


def monnaie_en_main(main: Cards) -> int:
    """Valeur des trésors en main, indépendamment des bonus d'actions."""
    total = 0
    quantites = getattr(main, "quantities", {}) or {}
    for nom, quantite in quantites.items():
        classe = type_carte(nom)
        try:
            total += int(getattr(classe, "money", 0)) * int(quantite)
        except (AttributeError, TypeError, ValueError):
            continue
    return total


def _n_achete(achats: Mapping[CardName, int] | None, carte: CardName) -> int:
    if not achats:
        return 0
    try:
        return int(achats.get(carte, 0))
    except (TypeError, ValueError):
        return 0


def _score_achat(
    carte: CardName,
    *,
    achats: Mapping[CardName, int] | None,
    tour: int,
    provinces_restantes: int,
    piles_vides: int,
    budget: int,
    stock: Cards,
) -> float:
    """Score heuristique : priorité économique tôt, points en fin de partie."""
    achetee = _n_achete(achats, carte)
    quantites_stock = getattr(stock, "quantities", {}) or {}

    if carte == CardName.PROVINCE:
        return 150.0
    if carte == CardName.DUCHY:
        return 118.0 if provinces_restantes <= 3 or piles_vides >= 2 else 18.0
    if carte == CardName.ESTATE:
        return 86.0 if provinces_restantes <= 1 or piles_vides >= 2 else 2.0
    if carte == CardName.GARDENS:
        # Sans accès au deck complet, on évite Gardens au début et on ne le
        # considère qu'en fin de partie, lorsque le nombre de cartes est plus élevé.
        return 72.0 if tour >= 13 and (provinces_restantes <= 4 or piles_vides >= 2) else 24.0

    # Hireling produit une carte supplémentaire à chaque tour : le premier est
    # très rentable, les suivants restent bons mais ne doivent pas monopoliser le deck.
    if carte == CardName.HIRELING:
        return 104.0 if achetee == 0 else 92.0 if achetee == 1 else 58.0
    if carte == CardName.GOLD:
        return 100.0
    if carte == CardName.WITCH:
        maledictions = int(quantites_stock.get(CardName.CURSE, 0))
        if maledictions > 0 and achetee < 2 and tour <= 18:
            return 94.0 if achetee == 0 else 87.0
        return 69.0 if achetee == 0 else 48.0
    if carte == CardName.BANDIT:
        return 91.0 if achetee < 2 and tour <= 18 else 68.0 if achetee < 3 else 45.0
    if carte == CardName.LABORATORY:
        return 93.0 if achetee < 3 else 72.0 if achetee < 4 else 45.0
    if carte == CardName.FESTIVAL:
        return 88.0 if achetee < 2 else 70.0 if achetee < 3 else 44.0
    if carte == CardName.MILITIA:
        return 84.0 if achetee < 2 else 65.0 if achetee < 3 else 42.0
    if carte == CardName.COUNCILROOM:
        return 79.0 if achetee < 2 else 60.0 if achetee < 3 else 40.0
    if carte == CardName.MARKET:
        return 78.0 if achetee < 3 else 60.0 if achetee < 4 else 40.0
    if carte == CardName.SMITHY:
        return 74.0 if achetee < 2 else 58.0 if achetee < 3 else 38.0
    if carte == CardName.DISTANTSHORE:
        return 70.0 if achetee < 2 else 52.0
    if carte == CardName.SILVER:
        # L'argent est la base économique : il passe avant les villages peu utiles.
        return 67.0 if tour <= 12 else 59.0
    if carte == CardName.WOODCUTTER:
        return 55.0 if achetee < 2 else 38.0
    if carte == CardName.VILLAGE:
        cartes_terminales = sum(
            _n_achete(achats, nom)
            for nom in (
                CardName.SMITHY,
                CardName.WITCH,
                CardName.BANDIT,
                CardName.MILITIA,
                CardName.COUNCILROOM,
                CardName.BUREAUCRAT,
                CardName.CHANCELLOR,
                CardName.WOODCUTTER,
            )
        )
        return 61.0 if cartes_terminales >= 2 and achetee < 2 else 43.0 if achetee < 3 else 28.0
    if carte == CardName.FARMINGVILLAGE:
        cartes_terminales = sum(
            _n_achete(achats, nom)
            for nom in (
                CardName.SMITHY,
                CardName.WITCH,
                CardName.BANDIT,
                CardName.MILITIA,
                CardName.COUNCILROOM,
                CardName.BUREAUCRAT,
                CardName.CHANCELLOR,
                CardName.WOODCUTTER,
            )
        )
        return 58.0 if cartes_terminales >= 2 and achetee == 0 else 39.0 if achetee < 2 else 25.0
    if carte == CardName.BUREAUCRAT:
        return 62.0 if achetee == 0 and tour < 12 else 43.0
    if carte == CardName.CHANCELLOR:
        return 49.0 if achetee == 0 else 32.0
    return 0.0


def priorites_achat(
    stock: Cards,
    *,
    achats: Mapping[CardName, int] | None = None,
    tour: int = 1,
    provinces_restantes: int = 8,
    piles_vides: int = 0,
    budget: int = 0,
) -> list[CardName]:
    """Classe les achats disponibles selon la situation de la partie."""
    quantites = getattr(stock, "quantities", {}) or {}
    fin_proche = provinces_restantes <= 3 or piles_vides >= 2
    candidates = []
    for carte in CARTES_STRATEGIE:
        if int(quantites.get(carte, 0)) <= 0 or cout_carte(carte) >= 10**6:
            continue
        # Ne pas acheter des cartes de points mortes au milieu de la partie.
        if carte == CardName.DUCHY and not fin_proche:
            continue
        if carte == CardName.ESTATE and not (provinces_restantes <= 1 or piles_vides >= 2):
            continue
        if carte == CardName.GARDENS and not (
            tour >= 13 and (provinces_restantes <= 4 or piles_vides >= 2)
        ):
            continue
        candidates.append(carte)
    return sorted(
        candidates,
        key=lambda carte: _score_achat(
            carte,
            achats=achats,
            tour=tour,
            provinces_restantes=provinces_restantes,
            piles_vides=piles_vides,
            budget=budget,
            stock=stock,
        ),
        reverse=True,
    )


def achat(
    main: Cards,
    carte: CardName,
    stock: Cards,
    *,
    monnaie_disponible: int = 0,
    achats_restants: int = 1,
) -> str | bool:
    """Vérifie que l'achat est disponible et que le budget restant suffit."""
    if achats_restants <= 0:
        return False

    quantites_stock = getattr(stock, "quantities", {}) or {}
    if int(quantites_stock.get(carte, 0)) <= 0:
        return False

    cout = cout_carte(carte)
    if cout >= 10**6:
        return False

    budget = monnaie_en_main(main) + int(monnaie_disponible)
    if budget < cout:
        return False

    return f"BUY {carte.value}"
