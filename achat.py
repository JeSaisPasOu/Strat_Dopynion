"""Achats de Toulousain v4 : priorité à une économie qui ne peut pas s'écrouler.

Les seuils sont des heuristiques, pas des probabilités de victoire. On garde
les mêmes signatures que l'API existante pour faciliter le déploiement.
"""
from typing import Mapping
from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


def option(*names):
    for name in names:
        card = getattr(CardName, name, None)
        if card is not None:
            return card
    return None


CHAPEL = option('CHAPEL', 'CHAPELLE')
MONEYLENDER = option('MONEYLENDER', 'MONEY_LENDER')
MINE = option('MINE')
REMODEL = option('REMODEL')
SWAP = option('SWAP')
FEAST = option('FEAST')
COLONY = option('COLONY')


def unique(cards):
    return tuple(dict.fromkeys(c for c in cards if c is not None))


CARTES_STRATEGIE = unique((
    COLONY, CardName.PROVINCE, CardName.GOLD, CardName.SILVER,
    CardName.HIRELING, CardName.WITCH, CardName.BANDIT,
    CardName.LABORATORY, CardName.FESTIVAL, CardName.MARKET,
    CardName.LIBRARY, CardName.MILITIA, CardName.COUNCILROOM,
    CardName.SMITHY, CardName.MAGNATE, CardName.FORTUNETELLER,
    CardName.ADVENTURER, CardName.WORKSHOP, CardName.CELLAR,
    CardName.DISTANTSHORE, CardName.VILLAGE, CardName.FARMINGVILLAGE,
    CardName.WOODCUTTER, CardName.BUREAUCRAT, CardName.CHANCELLOR,
    CardName.GARDENS, CardName.DUCHY, CardName.ESTATE,
    CHAPEL, MONEYLENDER, MINE, REMODEL, SWAP, FEAST,
))

TERMINALES = unique((
    CardName.WITCH, CardName.BANDIT, CardName.HIRELING, CardName.LIBRARY,
    CardName.COUNCILROOM, CardName.SMITHY, CardName.MILITIA,
    CardName.MAGNATE, CardName.FORTUNETELLER, CardName.ADVENTURER,
    CardName.WORKSHOP, CardName.BUREAUCRAT, CardName.CHANCELLOR,
    CardName.WOODCUTTER, CHAPEL, MONEYLENDER, MINE, REMODEL, FEAST,
))
VILLAGES = unique((CardName.VILLAGE, CardName.FARMINGVILLAGE, CardName.FESTIVAL))


def nombre(mapping, carte):
    if carte is None or mapping is None:
        return 0
    try:
        return max(0, int(mapping.get(carte, 0)))
    except (AttributeError, ValueError, TypeError):
        return 0


def type_carte(carte):
    try:
        return Card.class_(carte)
    except (AttributeError, TypeError, ValueError, KeyError):
        return Card


def cout_carte(carte):
    cls = type_carte(carte)
    if cls is Card:
        return 10**6
    try:
        return int(cls.cost)
    except (AttributeError, TypeError, ValueError):
        return 10**6


def monnaie_en_main(main: Cards):
    total = 0
    for carte, q in (getattr(main, 'quantities', {}) or {}).items():
        try:
            total += int(getattr(type_carte(carte), 'money', 0)) * int(q)
        except (ValueError, TypeError, AttributeError):
            pass
    return total


def economie_estimee(achats, trashed):
    """Conservateur : on ne présume jamais qu'un cuivre détruit existe encore."""
    cuivre = max(0, 7 + nombre(achats, CardName.COPPER) - nombre(trashed, CardName.COPPER))
    argent = max(0, nombre(achats, CardName.SILVER) - nombre(trashed, CardName.SILVER))
    or_ = max(0, nombre(achats, CardName.GOLD) - nombre(trashed, CardName.GOLD))
    return cuivre, argent, or_


def seuil_cuivre(achats, trashed):
    """Plancher de Cuivre tant que l'économie n'est pas reconstruite."""
    _, argent, or_ = economie_estimee(achats, trashed)
    if or_ >= 2 or (or_ >= 1 and argent >= 2) or argent >= 4:
        return 0
    if or_ >= 1 or argent >= 2:
        return 3
    if argent >= 1:
        return 4
    return 5


def score_achat(carte, *, achats, trashed, tour, provinces_restantes,
                piles_vides, budget, stock, main=None, joueurs_actifs=2):
    n = lambda c: nombre(achats, c)
    stock_q = getattr(stock, 'quantities', {}) or {}
    cuivre, argent, or_ = economie_estimee(achats, trashed)
    terminales = sum(n(c) for c in TERMINALES)
    villages = sum(n(c) for c in VILLAGES)
    joueurs = max(2, int(joueurs_actifs or 2))
    course = (provinces_restantes <= (3 if joueurs <= 2 else 4 if joueurs == 3 else 5)
              or piles_vides >= 2)
    urgente = provinces_restantes <= 2 or piles_vides >= 2
    if carte == COLONY and COLONY is not None:
        return 190
    if carte == CardName.PROVINCE:
        return 175
    if carte == CardName.DUCHY:
        if urgente: return 125
        return 82 if course and tour >= 13 else -100
    if carte == CardName.ESTATE:
        return 89 if (provinces_restantes <= 1 or piles_vides >= 2) and tour >= 12 else -100
    if carte == CardName.GARDENS:
        # Le bot épure le deck : Jardins n'est donc pas sa stratégie par défaut.
        return 44 if urgente and tour >= 16 else -100

    # Économie : au moins un/deux Argent avant de commencer à épurer les Cuivres.
    if carte == CardName.SILVER:
        if argent == 0 and or_ == 0: return 105
        if argent == 1 and or_ == 0: return 91
        if argent < 3 and or_ == 0: return 79
        if argent < 4 and or_ <= 1: return 69
        return 53 if tour <= 13 else 39
    if carte == CardName.GOLD:
        return 113 if or_ < 2 else 105 if or_ < 4 else 89

    # Cas observé dans les logs : une deuxième Chapelle + Moneylender sans trésor
    # a produit un deck incapable d'acheter. Interdire le doublon.
    if CHAPEL is not None and carte == CHAPEL:
        if n(CHAPEL) >= 1 or tour > 10: return -100
        # N'acheter Chapelle qu'une fois le premier Argent sécurisé.
        if argent + or_ == 0: return 35
        return 99 if tour <= 6 else 73
    if MONEYLENDER is not None and carte == MONEYLENDER:
        if n(MONEYLENDER) >= 1 or n(CHAPEL) >= 1 or cuivre <= seuil_cuivre(achats, trashed):
            return -100
        return 71 if argent >= 1 and tour <= 8 else 42
    if MINE is not None and carte == MINE:
        if n(MINE) >= 1 or tour > 13: return -100
        return 72 if argent >= 2 else 51
    if REMODEL is not None and carte == REMODEL:
        if n(REMODEL) >= 1 or tour > 13: return -100
        return 57 if nombre(trashed, CardName.ESTATE) <= 1 else 41
    if FEAST is not None and carte == FEAST:
        return 52 if n(FEAST) == 0 and tour <= 10 else -100
    if SWAP is not None and carte == SWAP:
        return 54 if n(SWAP) == 0 and tour <= 11 else -100

    scores = {
        CardName.HIRELING: 114 if tour <= 11 else 90,
        CardName.WITCH: 110 if tour <= 12 else 83,
        CardName.LABORATORY: 104,
        CardName.BANDIT: 92,
        CardName.FESTIVAL: 88,
        CardName.MARKET: 87,
        CardName.LIBRARY: 82,
        CardName.MILITIA: 84,
        CardName.COUNCILROOM: 77,
        CardName.SMITHY: 75,
        CardName.MAGNATE: 63,
        CardName.FORTUNETELLER: 74,
        CardName.ADVENTURER: 48,
        CardName.WORKSHOP: 48,
        CardName.CELLAR: 51,
        CardName.DISTANTSHORE: 69,
        CardName.VILLAGE: 49,
        CardName.FARMINGVILLAGE: 48,
        CardName.WOODCUTTER: 29,
        CardName.BUREAUCRAT: 48,
        CardName.CHANCELLOR: 33,
    }
    score = float(scores.get(carte, -100))
    if carte == CardName.WITCH:
        if nombre(stock_q, CardName.CURSE) == 0: score -= 43
        if tour > 15: score -= 18
    if carte == CardName.HIRELING and tour > 15: score -= 24
    if carte == CardName.MAGNATE:
        score += min(19, 4 * argent + 7 * or_)
    if carte == CardName.ADVENTURER and argent + or_ >= 4:
        score -= 15
    if carte in VILLAGES:
        manque = terminales - villages
        score += min(35, max(0, manque - 1) * 17)
        if manque <= 1: score -= 22
    elif carte in TERMINALES:
        if terminales > villages + 1:
            score -= min(38, 12 * (terminales - villages - 1))
    if carte == CardName.WORKSHOP and tour > 10: score -= 18
    if carte == CardName.CELLAR and n(carte) >= 1: score -= 27
    if carte == CardName.LIBRARY and n(carte) >= 1: score -= 17
    # Règle générale : chaque exemplaire supplémentaire doit apporter plus
    # qu'un trésor ou un moteur déjà présent.
    if carte not in (CardName.GOLD, CardName.SILVER):
        score -= 17 * n(carte)
    if course and carte not in (CardName.GOLD, CardName.SILVER):
        score -= 12
    if urgente and carte not in (CardName.GOLD, CardName.SILVER):
        score -= 14
    return score


def priorites_achat(stock, *, achats=None, trashed=None, tour=1,
                    provinces_restantes=8, piles_vides=0, budget=0,
                    main=None, joueurs_actifs=2):
    achats, trashed = achats or {}, trashed or {}
    q = getattr(stock, 'quantities', {}) or {}
    propositions = []
    for carte in CARTES_STRATEGIE:
        if nombre(q, carte) <= 0 or cout_carte(carte) > budget:
            continue
        note = score_achat(carte, achats=achats, trashed=trashed,
                           tour=tour, provinces_restantes=provinces_restantes,
                           piles_vides=piles_vides, budget=budget, stock=stock,
                           main=main, joueurs_actifs=joueurs_actifs)
        if note >= 40:
            propositions.append((note, carte))
    return [carte for _, carte in sorted(propositions, key=lambda x: x[0], reverse=True)]


def achat(main, carte, stock, *, monnaie_disponible=0, achats_restants=1):
    if achats_restants <= 0 or nombre(getattr(stock, 'quantities', {}) or {}, carte) <= 0:
        return False
    cout = cout_carte(carte)
    if cout >= 10**6 or cout > monnaie_en_main(main) + int(monnaie_disponible):
        return False
    return f'BUY {carte.value}'
