"""Réactions v4 : ne JAMAIS détruire sa dernière économie pour épurer le deck."""
from dopynion.cards import Card
from dopynion.data_model import CardName
from achat import (CHAPEL, MONEYLENDER, MINE, REMODEL, SWAP, FEAST,
                   nombre, cout_carte, seuil_cuivre, economie_estimee)


def _money(carte):
    try:
        classe = Card.class_(carte)
        return int(getattr(classe, 'money', 0))
    except (AttributeError, TypeError, ValueError, KeyError):
        return 0


def _action(carte):
    try:
        return bool(getattr(Card.class_(carte), 'is_action', False))
    except (AttributeError, TypeError, ValueError, KeyError):
        return False


def confirmer_defausse(carte, main=None):
    if carte in (CardName.CURSE, CardName.ESTATE, CardName.DUCHY,
                 CardName.PROVINCE, CardName.GARDENS):
        return True
    if carte == CardName.COPPER:
        # Cellar : ne pas vider un jeu qui ne contient que du Cuivre.
        autres_tresors = sum(_money(x) for x in (main or []) if x != CardName.COPPER)
        return autres_tresors > 0
    return False


def choisir_defausse(main):
    if not main:
        return CardName.COPPER
    priority = [CardName.CURSE, CardName.ESTATE, CardName.GARDENS,
                CardName.DUCHY, CardName.PROVINCE]
    for c in priority:
        if c in main:
            return c
    # En cas de défausse forcée, préserver l'argent autant que possible.
    weak = [CardName.CHANCELLOR, CardName.WOODCUTTER, CardName.BUREAUCRAT,
            CardName.WORKSHOP, CardName.ADVENTURER, CardName.CELLAR,
            CardName.MAGNATE, CardName.SMITHY, CardName.VILLAGE, CardName.COPPER]
    for c in weak:
        if c in main:
            return c
    return main[0]


def confirmer_destruction(carte, *, achats=None, trashed=None, tour=1, main=None):
    """Pour Chapelle/Prêteur : le plancher dépend des trésors déjà construits."""
    achats, trashed = achats or {}, trashed or {}
    if carte is None:
        return False
    if carte == CardName.CURSE:
        return True
    if carte == CardName.ESTATE:
        return True
    if carte == CardName.COPPER:
        cuivre, _, _ = economie_estimee(achats, trashed)
        return cuivre > seuil_cuivre(achats, trashed)
    return False


def choisir_destruction(main, *, tour=1, achats=None, trashed=None):
    """Choix demandé par Remodel/effet de transformation : cible légale fournie."""
    if not main:
        return CardName.COPPER
    for c in (CardName.CURSE, CardName.ESTATE):
        if c in main:
            return c
    if CardName.COPPER in main and confirmer_destruction(
        CardName.COPPER, achats=achats, trashed=trashed, tour=tour
    ):
        return CardName.COPPER
    for c in (CardName.CHANCELLOR, CardName.WOODCUTTER, CardName.WORKSHOP,
              CardName.BUREAUCRAT, CardName.ADVENTURER, CardName.CELLAR):
        if c in main:
            return c
    # Toujours répondre avec un choix légal, même si aucun n'est souhaitable.
    return min(main, key=lambda c: (c in (CardName.PROVINCE, CardName.GOLD), cout_carte(c)))


def choisir_carte_recue(possibles, destination='discard', *, tour=1,
                         achats=None, trashed=None):
    """Workshop/Remodel/Mine/Feast : ne prendre que les choix proposés par l'arbitre."""
    if not possibles:
        return CardName.COPPER
    achats, trashed = achats or {}, trashed or {}
    _, argent, or_ = economie_estimee(achats, trashed)
    priority = {
        CardName.PROVINCE: 165, CardName.GOLD: 117,
        CardName.HIRELING: 112, CardName.WITCH: 111,
        CardName.LABORATORY: 108, CardName.BANDIT: 93,
        CardName.FESTIVAL: 91, CardName.MARKET: 90,
        CardName.MILITIA: 85, CardName.LIBRARY: 84,
        CardName.COUNCILROOM: 81, CardName.SMITHY: 80,
        CardName.FORTUNETELLER: 78, CardName.SILVER: 76,
        CardName.FARMINGVILLAGE: 69, CardName.VILLAGE: 67,
        CardName.MAGNATE: 64, CardName.DISTANTSHORE: 65,
        CardName.CELLAR: 55, CardName.ADVENTURER: 48,
        CardName.WOODCUTTER: 30, CardName.WORKSHOP: 43,
        CardName.BUREAUCRAT: 48, CardName.CHANCELLOR: 25,
        CardName.GARDENS: 25, CardName.DUCHY: 24,
        CardName.ESTATE: 1, CardName.COPPER: -5,
        CardName.CURSE: -100,
    }
    if CHAPEL is not None:
        priority[CHAPEL] = 78 if nombre(achats, CHAPEL) == 0 and tour <= 8 else 10
    if MONEYLENDER is not None:
        priority[MONEYLENDER] = 42 if nombre(achats, CHAPEL) == 0 else 10
    if REMODEL is not None:
        priority[REMODEL] = 55
    if MINE is not None:
        priority[MINE] = 63
    if FEAST is not None:
        priority[FEAST] = 39
    if SWAP is not None:
        priority[SWAP] = 42

    def score(c):
        s = priority.get(c, 20 + 2 * min(10, cout_carte(c)))
        if c == CardName.SILVER and argent + or_ == 0:
            s = 125
        if c == CardName.SILVER and argent == 1 and or_ == 0:
            s = 101
        if c == CardName.GOLD and or_ == 0:
            s += 5
        if c in (CardName.PROVINCE, CardName.DUCHY, CardName.ESTATE,
                 CardName.GARDENS) and tour < 13:
            s -= 28
        if destination == 'deck' and c in (CardName.PROVINCE, CardName.DUCHY,
                                            CardName.ESTATE, CardName.GARDENS):
            s -= 30
        return s - 15 * nombre(achats, c)
    return max(possibles, key=score)


def sauter_reception_en_main(carte=None, *, actions_restantes=0, main=None):
    """Bibliothèque : écarter une Action qui ne pourrait plus être jouée."""
    return bool(carte is not None and _action(carte) and actions_restantes <= 0)


def choisir_monnaie_a_detruire(monnaies, *, tour=1):
    if not monnaies:
        return CardName.COPPER
    # Mine : Silver -> Gold avant Copper -> Silver, si l'arbitre autorise la cible.
    for c in (CardName.SILVER, CardName.COPPER):
        if c in monnaies:
            return c
    return monnaies[0]
