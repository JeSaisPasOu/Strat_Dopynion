"""Évaluation, classement et validation des achats du bot Toulousain test."""

from typing import Mapping

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


# Les nouvelles cartes sont incluses explicitement. Leur coût réel est toujours
# lu dans dopynion.cards : aucun coût n'est codé en dur dans la stratégie.
CARTES_STRATEGIE: tuple[CardName, ...] = (
    CardName.PROVINCE,
    CardName.GOLD,
    CardName.HIRELING,
    CardName.WITCH,
    CardName.BANDIT,
    CardName.LABORATORY,
    CardName.FESTIVAL,
    CardName.LIBRARY,
    CardName.MILITIA,
    CardName.COUNCILROOM,
    CardName.MARKET,
    CardName.MAGNATE,
    CardName.SMITHY,
    CardName.DISTANTSHORE,
    CardName.FORTUNETELLER,
    CardName.ADVENTURER,
    CardName.SILVER,
    CardName.WORKSHOP,
    CardName.WOODCUTTER,
    CardName.FARMINGVILLAGE,
    CardName.VILLAGE,
    CardName.CELLAR,
    CardName.BUREAUCRAT,
    CardName.CHANCELLOR,
    CardName.GARDENS,
    CardName.DUCHY,
    CardName.ESTATE,
)


CARTES_TERMINALES: tuple[CardName, ...] = (
    CardName.WITCH,
    CardName.BANDIT,
    CardName.HIRELING,
    CardName.LIBRARY,
    CardName.COUNCILROOM,
    CardName.SMITHY,
    CardName.MAGNATE,
    CardName.FORTUNETELLER,
    CardName.MILITIA,
    CardName.ADVENTURER,
    CardName.BUREAUCRAT,
    CardName.WORKSHOP,
    CardName.CHANCELLOR,
    CardName.WOODCUTTER,
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
    """Somme la valeur des trésors actuellement présents dans la main."""
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
        return max(0, int(achats.get(carte, 0)))
    except (TypeError, ValueError):
        return 0


def _total_connues(achats: Mapping[CardName, int] | None) -> int:
    if not achats:
        return 0
    total = 0
    for quantite in achats.values():
        try:
            total += max(0, int(quantite))
        except (TypeError, ValueError):
            continue
    return total


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
    """Score heuristique, ajusté selon le tour, les cartes déjà acquises et le stock."""
    copies = _n_achete(achats, carte)
    quantites_stock = getattr(stock, "quantities", {}) or {}
    fin_proche = provinces_restantes <= 3 or piles_vides >= 2
    total_cartes_ajoutees = _total_connues(achats)
    taille_deck_estimee = 10 + total_cartes_ajoutees
    terminales = sum(_n_achete(achats, nom) for nom in CARTES_TERMINALES)
    villages = sum(
        _n_achete(achats, nom)
        for nom in (CardName.VILLAGE, CardName.FARMINGVILLAGE, CardName.FESTIVAL)
    )
    tresors_achetes = sum(
        _n_achete(achats, nom)
        for nom in (CardName.SILVER, CardName.GOLD, CardName.COPPER)
    )

    # Points : priorité absolue aux Provinces, puis aux points quand la partie
    # approche réellement de sa fin.
    if carte == CardName.PROVINCE:
        return 150.0
    if carte == CardName.DUCHY:
        return 124.0 if fin_proche else 12.0
    if carte == CardName.ESTATE:
        return 90.0 if provinces_restantes <= 1 or piles_vides >= 2 else 1.0
    if carte == CardName.GARDENS:
        points_estimes = taille_deck_estimee // 10
        if tour >= 11 or fin_proche:
            return min(92.0, 32.0 + 13.0 * points_estimes)
        return 18.0 + 5.0 * points_estimes

    # Économie et cartes très efficaces.
    if carte == CardName.HIRELING:
        return 108.0 if copies == 0 else 94.0 if copies == 1 else 66.0 if copies == 2 else 43.0
    if carte == CardName.GOLD:
        return 103.0 if copies < 3 else 92.0 if copies < 5 else 76.0
    if carte == CardName.WITCH:
        maledictions = int(quantites_stock.get(CardName.CURSE, 0))
        if maledictions > 0 and tour <= 18:
            return 98.0 if copies == 0 else 88.0 if copies == 1 else 67.0 if copies == 2 else 45.0
        return 68.0 if copies == 0 else 48.0
    if carte == CardName.BANDIT:
        return 93.0 if copies < 2 and tour <= 18 else 76.0 if copies < 3 else 48.0

    # Pioche : Library est très utile mais reste une action terminale ; on limite
    # les copies pour ne pas remplir le deck de cartes qui se concurrencent.
    if carte == CardName.LABORATORY:
        return 96.0 if copies < 2 else 86.0 if copies < 3 else 65.0 if copies < 4 else 44.0
    if carte == CardName.LIBRARY:
        return 91.0 if copies == 0 else 82.0 if copies == 1 else 68.0 if copies == 2 else 49.0
    if carte == CardName.COUNCILROOM:
        return 82.0 if copies < 2 else 68.0 if copies < 3 else 48.0
    if carte == CardName.SMITHY:
        return 78.0 if copies < 2 else 64.0 if copies < 3 else 45.0
    if carte == CardName.MAGNATE:
        # Magnate ne pioche qu'en fonction des trésors présents dans la main.
        # Les achats de Silver/Gold donnent une approximation de cette synergie.
        if tresors_achetes >= 3:
            return 82.0 if copies == 0 else 70.0 if copies == 1 else 49.0
        return 69.0 if copies == 0 else 55.0 if copies == 1 else 39.0

    # Actions qui ajoutent de l'argent et/ou attaquent. Fortune Teller est
    # meilleure tôt ; son +2 pièces reste utile même quand l'attaque baisse.
    if carte == CardName.FORTUNETELLER:
        return 83.0 if copies == 0 and tour <= 13 else 73.0 if copies < 2 else 57.0 if copies < 3 else 39.0
    if carte == CardName.MILITIA:
        return 86.0 if copies < 2 else 72.0 if copies < 3 else 48.0
    if carte == CardName.FESTIVAL:
        return 91.0 if copies < 2 else 79.0 if copies < 3 else 60.0 if copies < 4 else 42.0
    if carte == CardName.MARKET:
        return 83.0 if copies < 3 else 69.0 if copies < 4 else 48.0
    if carte == CardName.DISTANTSHORE:
        return 73.0 if copies < 2 else 58.0

    # Les nouvelles cartes à faible coût : Cellar recycle la main, Workshop
    # permet de gagner gratuitement une carte jusqu'à 4 pièces, Adventurer
    # apporte deux trésors mais coûte 6 et reste terminal.
    if carte == CardName.WORKSHOP:
        bonnes_cibles = (
            CardName.FESTIVAL,
            CardName.MILITIA,
            CardName.SMITHY,
            CardName.FARMINGVILLAGE,
            CardName.BUREAUCRAT,
            CardName.FORTUNETELLER,
        )
        cible_disponible = any(
            int(quantites_stock.get(nom, 0)) > 0 and cout_carte(nom) <= 4
            for nom in bonnes_cibles
        )
        if cible_disponible and tour <= 14:
            return 76.0 if copies == 0 else 64.0 if copies == 1 else 45.0
        return 57.0 if copies == 0 else 43.0
    if carte == CardName.CELLAR:
        dechets_estimes = sum(
            _n_achete(achats, nom)
            for nom in (CardName.ESTATE, CardName.CURSE, CardName.GARDENS)
        )
        if tour <= 10:
            return 63.0 if copies == 0 else 53.0 if copies == 1 else 37.0
        return 52.0 + min(10.0, 3.0 * dechets_estimes) if copies == 0 else 38.0
    if carte == CardName.ADVENTURER:
        # Gold est généralement un meilleur achat à 6 ; Adventurer est un
        # complément raisonnable si le deck manque encore de trésors.
        if tresors_achetes < 2 and tour <= 14:
            return 72.0 if copies == 0 else 58.0
        return 59.0 if copies == 0 else 43.0

    # Économie de base et actions de soutien.
    if carte == CardName.SILVER:
        return 68.0 if tour <= 12 else 58.0 if tour <= 18 else 44.0
    if carte == CardName.WOODCUTTER:
        return 57.0 if copies < 2 else 42.0
    if carte == CardName.VILLAGE:
        if terminales >= 2 and villages < terminales:
            return 69.0 if copies < 2 else 52.0
        return 48.0 if copies < 2 else 31.0
    if carte == CardName.FARMINGVILLAGE:
        if terminales >= 2 and villages < terminales:
            return 67.0 if copies == 0 else 51.0
        return 45.0 if copies == 0 else 30.0
    if carte == CardName.BUREAUCRAT:
        return 65.0 if copies == 0 and tour < 12 else 46.0 if copies < 2 else 32.0
    if carte == CardName.CHANCELLOR:
        return 50.0 if copies == 0 else 34.0

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
    """Classe les cartes encore en stock, de la plus intéressante à la moins bonne."""
    quantites = getattr(stock, "quantities", {}) or {}
    fin_proche = provinces_restantes <= 3 or piles_vides >= 2
    candidates: list[CardName] = []

    for carte in CARTES_STRATEGIE:
        try:
            disponible = int(quantites.get(carte, 0)) > 0
        except (TypeError, ValueError):
            disponible = False
        if not disponible or cout_carte(carte) >= 10**6:
            continue

        if carte == CardName.DUCHY and not fin_proche:
            continue
        if carte == CardName.ESTATE and not (provinces_restantes <= 1 or piles_vides >= 2):
            continue
        if carte == CardName.GARDENS and tour < 11 and not fin_proche:
            continue

        candidates.append(carte)

    return sorted(
        candidates,
        key=lambda nom: _score_achat(
            nom,
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
    """Valide un achat uniquement si le stock et le budget le permettent."""
    if achats_restants <= 0:
        return False

    quantites_stock = getattr(stock, "quantities", {}) or {}
    try:
        if int(quantites_stock.get(carte, 0)) <= 0:
            return False
    except (TypeError, ValueError):
        return False

    cout = cout_carte(carte)
    if cout >= 10**6:
        return False

    budget_total = monnaie_en_main(main) + int(monnaie_disponible)
    if budget_total < cout:
        return False

    return f"BUY {carte.value}"
