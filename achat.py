"""Scoring dynamique des achats pour le bot Toulousain test.

La stratégie tient compte du tour, des cartes déjà acquises, des cartes
épurées et de la composition de la main reçue par /play.
"""

from typing import Mapping

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


def _optional_card(*names: str):
    """Récupère une carte sans faire échouer l'import si l'enum diffère."""
    for name in names:
        value = getattr(CardName, name, None)
        if value is not None:
            return value
    return None


COLONY = _optional_card("COLONY", "COLONIE")
CHAPEL = _optional_card("CHAPEL", "CHAPELLE")
MINE = _optional_card("MINE")
MONEYLENDER = _optional_card("MONEYLENDER", "MONEY_LENDER", "PRETEUR_SUR_GAGES")
REMODEL = _optional_card("REMODEL", "RENOVATION", "REMODELATION")
SWAP = _optional_card("SWAP", "TROC")


def _unique_cards(cards):
    result = []
    for card in cards:
        if card is not None and card not in result:
            result.append(card)
    return tuple(result)


# Troc est inclus à l'achat, mais sa valeur reste modérée tant que son effet
# d'échange n'est pas confirmé dans action.py et par l'API du moteur.
CARTES_STRATEGIE: tuple[CardName, ...] = _unique_cards((
    CardName.PROVINCE,
    COLONY,
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
    MINE,
    MONEYLENDER,
    REMODEL,
    CHAPEL,
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
))


CARTES_TERMINALES: tuple[CardName, ...] = _unique_cards((
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
    CHAPEL,
    MINE,
    MONEYLENDER,
    REMODEL,
))


CARTES_DECHETS = _unique_cards((CardName.CURSE, CardName.ESTATE, CardName.COPPER))


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


def _quantite(mapping, carte) -> int:
    if mapping is None or carte is None:
        return 0
    try:
        return max(0, int(mapping.get(carte, 0)))
    except (AttributeError, TypeError, ValueError):
        return 0


def _n_achete(achats: Mapping[CardName, int] | None, carte: CardName) -> int:
    return _quantite(achats, carte)


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


def _nombre_dans_main(main: Cards | None, carte: CardName | None) -> int:
    if main is None or carte is None:
        return 0
    return _quantite(getattr(main, "quantities", {}) or {}, carte)


def _dechets_dans_main(main: Cards | None) -> int:
    return sum(_nombre_dans_main(main, card) for card in CARTES_DECHETS)


def _dechets_epures(trashed: Mapping[CardName, int] | None) -> int:
    return sum(_quantite(trashed, card) for card in CARTES_DECHETS)


def _score_achat(
    carte: CardName,
    *,
    achats: Mapping[CardName, int] | None,
    trashed: Mapping[CardName, int] | None,
    tour: int,
    provinces_restantes: int,
    piles_vides: int,
    budget: int,
    stock: Cards,
    main: Cards | None,
) -> float:
    """Score heuristique de carte, ajusté au moment de la partie."""
    copies = _n_achete(achats, carte)
    quantites_stock = getattr(stock, "quantities", {}) or {}
    fin_proche = provinces_restantes <= 3 or piles_vides >= 2
    total_cartes_ajoutees = _total_connues(achats)
    taille_deck_estimee = 10 + total_cartes_ajoutees - _dechets_epures(trashed)
    terminales = sum(_n_achete(achats, nom) for nom in CARTES_TERMINALES)
    villages = sum(
        _n_achete(achats, nom)
        for nom in (CardName.VILLAGE, CardName.FARMINGVILLAGE, CardName.FESTIVAL)
    )
    tresors_achetes = sum(
        _n_achete(achats, nom)
        for nom in (CardName.SILVER, CardName.GOLD, CardName.COPPER)
    )
    # Estimation des 7 Cuivres + 3 Domaines initiaux. Les Malédictions
    # épurées sont suivies séparément et ne doivent pas fausser ce socle.
    junk_left_estimate = max(0, 10 - _quantite(trashed, CardName.COPPER) - _quantite(trashed, CardName.ESTATE))
    junk_in_hand = _dechets_dans_main(main)
    copper_left_estimate = max(0, 7 - _quantite(trashed, CardName.COPPER))
    estate_left_estimate = max(0, 3 - _quantite(trashed, CardName.ESTATE))

    # Les points prennent le dessus quand ils sont disponibles et que la
    # partie se termine réellement.
    if carte == CardName.PROVINCE:
        return 160.0
    if COLONY is not None and carte == COLONY:
        return 170.0
    if carte == CardName.DUCHY:
        return 126.0 if fin_proche else 8.0
    if carte == CardName.ESTATE:
        return 91.0 if provinces_restantes <= 1 or piles_vides >= 2 else 0.0
    if carte == CardName.GARDENS:
        points_estimes = max(0, taille_deck_estimee // 10)
        if fin_proche and points_estimes >= 4:
            return min(72.0, 25.0 + 9.0 * points_estimes)
        return 10.0 + 3.0 * points_estimes

    # Épuration : Chapelle est un achat d'ouverture prioritaire si le deck
    # contient encore ses Domaines/Cuivres/Malédictions.
    if CHAPEL is not None and carte == CHAPEL:
        if junk_left_estimate <= 2:
            base = 28.0
        elif tour <= 5:
            base = 103.0
        elif tour <= 8:
            base = 94.0
        elif tour <= 11:
            base = 74.0
        elif tour <= 14:
            base = 49.0
        else:
            base = 24.0
        if junk_in_hand >= 2:
            base += 6.0
        if copies == 1:
            base -= 25.0
        elif copies >= 2:
            base -= 48.0
        return max(5.0, base)

    # Mine transforme Copper -> Silver et surtout Silver -> Gold. Une seule
    # copie suffit généralement ; on l'achète plus tôt si des trésors restent.
    if MINE is not None and carte == MINE:
        if tour <= 10:
            base = 86.0
        elif tour <= 15:
            base = 76.0
        elif tour <= 19:
            base = 58.0
        else:
            base = 34.0
        if _nombre_dans_main(main, CardName.SILVER) > 0 or tresors_achetes >= 2:
            base += 5.0
        if copies >= 1:
            base -= 30.0
        return max(8.0, base)

    # Prêteur sur gages est intéressant tant qu'il reste des Cuivres à convertir
    # en +3 pièces. Chapelle garde la priorité car elle épure jusqu'à quatre cartes.
    if MONEYLENDER is not None and carte == MONEYLENDER:
        if copper_left_estimate <= 1:
            base = 25.0
        elif tour <= 7:
            base = 88.0
        elif tour <= 11:
            base = 78.0
        elif tour <= 15:
            base = 57.0
        else:
            base = 28.0
        if _nombre_dans_main(main, CardName.COPPER) > 0:
            base += 4.0
        if copies >= 1:
            base -= 35.0
        return max(5.0, base)

    # Rénovation transforme un Domaine en action de coût 4 ou une carte faible
    # en une carte plus chère. Sa valeur baisse lorsque l'épuration est terminée.
    if REMODEL is not None and carte == REMODEL:
        if tour <= 8 and (estate_left_estimate > 0 or junk_in_hand > 0):
            base = 91.0
        elif tour <= 13:
            base = 78.0
        elif tour <= 17:
            base = 63.0
        else:
            base = 38.0
        if copies == 1:
            base -= 24.0
        elif copies >= 2:
            base -= 42.0
        return max(5.0, base)

    # Troc : carte potentiellement puissante, mais on limite son score tant que
    # son endpoint d'échange et son exécution ne sont pas validés en jeu.
    if SWAP is not None and carte == SWAP:
        if tour <= 13:
            base = 72.0 if copies == 0 else 48.0
        else:
            base = 50.0 if copies == 0 else 30.0
        return base

    # Cartes de moteur et d'économie.
    if carte == CardName.HIRELING:
        return 112.0 if copies == 0 else 96.0 if copies == 1 else 72.0 if copies == 2 else 44.0
    if carte == CardName.GOLD:
        return 106.0 if copies < 3 else 94.0 if copies < 5 else 76.0
    if carte == CardName.WITCH:
        maledictions = _quantite(quantites_stock, CardName.CURSE)
        if maledictions > 0 and tour <= 18:
            return 100.0 if copies == 0 else 88.0 if copies == 1 else 65.0 if copies == 2 else 42.0
        return 65.0 if copies == 0 else 42.0
    if carte == CardName.BANDIT:
        return 92.0 if copies < 2 and tour <= 18 else 73.0 if copies < 3 else 45.0
    if carte == CardName.LABORATORY:
        return 101.0 if copies < 2 else 88.0 if copies < 3 else 65.0 if copies < 4 else 42.0
    if carte == CardName.LIBRARY:
        return 91.0 if copies == 0 else 80.0 if copies == 1 else 63.0 if copies == 2 else 43.0
    if carte == CardName.COUNCILROOM:
        return 80.0 if copies < 2 else 65.0 if copies < 3 else 42.0
    if carte == CardName.SMITHY:
        return 77.0 if copies < 2 else 62.0 if copies < 3 else 40.0
    if carte == CardName.MAGNATE:
        return 80.0 if tresors_achetes >= 3 and copies == 0 else 66.0 if copies == 0 else 49.0
    if carte == CardName.FORTUNETELLER:
        return 82.0 if copies == 0 and tour <= 13 else 68.0 if copies < 2 else 48.0
    if carte == CardName.MILITIA:
        return 84.0 if copies < 2 else 68.0 if copies < 3 else 44.0
    if carte == CardName.FESTIVAL:
        return 94.0 if copies < 2 else 82.0 if copies < 3 else 61.0 if copies < 4 else 42.0
    if carte == CardName.MARKET:
        return 84.0 if copies < 3 else 68.0 if copies < 4 else 44.0
    if carte == CardName.DISTANTSHORE:
        return 71.0 if copies < 2 else 54.0

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
            _quantite(quantites_stock, nom) > 0 and cout_carte(nom) <= 4
            for nom in bonnes_cibles
        )
        if cible_disponible and tour <= 12:
            return 78.0 if copies == 0 else 60.0
        return 46.0 if copies == 0 else 30.0
    if carte == CardName.CELLAR:
        return 57.0 if copies == 0 and tour <= 10 else 43.0 if copies == 0 else 28.0
    if carte == CardName.ADVENTURER:
        return 66.0 if copies == 0 and tour <= 14 and tresors_achetes < 3 else 46.0
    if carte == CardName.SILVER:
        return 72.0 if tour <= 10 else 59.0 if tour <= 16 else 39.0
    if carte == CardName.WOODCUTTER:
        return 35.0 if copies == 0 else 22.0
    if carte == CardName.VILLAGE:
        if terminales >= 2 and villages < terminales:
            return 73.0 if copies < 2 else 53.0
        return 43.0 if copies < 2 else 28.0
    if carte == CardName.FARMINGVILLAGE:
        if terminales >= 2 and villages < terminales:
            return 70.0 if copies == 0 else 50.0
        return 42.0 if copies == 0 else 27.0
    if carte == CardName.BUREAUCRAT:
        return 59.0 if copies == 0 and tour < 12 else 39.0
    if carte == CardName.CHANCELLOR:
        return 42.0 if copies == 0 else 27.0

    return 0.0


def priorites_achat(
    stock: Cards,
    *,
    achats: Mapping[CardName, int] | None = None,
    trashed: Mapping[CardName, int] | None = None,
    tour: int = 1,
    provinces_restantes: int = 8,
    piles_vides: int = 0,
    budget: int = 0,
    main: Cards | None = None,
) -> list[CardName]:
    """Classe les cartes disponibles selon le contexte courant de la partie."""
    quantites = getattr(stock, "quantities", {}) or {}
    fin_proche = provinces_restantes <= 3 or piles_vides >= 2
    candidates: list[CardName] = []

    for carte in CARTES_STRATEGIE:
        if _quantite(quantites, carte) <= 0 or cout_carte(carte) >= 10**6:
            continue
        if carte == CardName.DUCHY and not fin_proche:
            continue
        if carte == CardName.ESTATE and not (provinces_restantes <= 1 or piles_vides >= 2):
            continue
        if carte == CardName.GARDENS and tour < 11 and not fin_proche:
            continue
        candidates.append(carte)

    scored = [
        (nom, _score_achat(
            nom,
            achats=achats,
            trashed=trashed,
            tour=tour,
            provinces_restantes=provinces_restantes,
            piles_vides=piles_vides,
            budget=budget,
            stock=stock,
            main=main,
        ))
        for nom in candidates
    ]
    # Ne pas acheter une carte médiocre uniquement parce qu'elle est abordable.
    # En fin de partie, les cartes à points sont déjà remontées par leurs scores.
    score_minimum = 40.0
    return [nom for nom, score in sorted(scored, key=lambda item: item[1], reverse=True)
            if score >= score_minimum]


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
    if _quantite(quantites_stock, carte) <= 0:
        return False
    cout = cout_carte(carte)
    if cout >= 10**6:
        return False
    try:
        budget_total = monnaie_en_main(main) + int(monnaie_disponible)
    except (TypeError, ValueError):
        return False
    if budget_total < cout:
        return False
    return f"BUY {carte.value}"
