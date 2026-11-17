"""Moteur de décision commun de Toulousain V5.

Toutes les évaluations dépendent d'un contexte explicite. Le deck est ESTIMÉ à
partir du deck initial, des achats, des gains et des destructions observés ;
les cartes adverses et les événements sans callback ne sont pas inventés.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from math import prod
from typing import Any, Mapping

from dopynion.cards import Card
from dopynion.data_model import CardName


def carte(*noms: str):
    for nom in noms:
        valeur = getattr(CardName, nom, None)
        if valeur is not None:
            return valeur
    return None


def unique(*noms):
    return tuple(dict.fromkeys(x for x in noms if x is not None))


CHAPEL = carte('CHAPEL', 'CHAPELLE')
MINE = carte('MINE')
MONEYLENDER = carte('MONEYLENDER', 'MONEY_LENDER')
REMODEL = carte('REMODEL', 'REMODELATION')
SWAP = carte('SWAP')
FEAST = carte('FEAST')
COLONY = carte('COLONY')

# Ces noms figurent dans les fichiers de l'API envoyés. Les noms optionnels
# sont récupérés dynamiquement : pas d'AttributeError sur une ancienne version.
VILLAGES = unique(carte('VILLAGE'), carte('FARMINGVILLAGE'), carte('FESTIVAL'))
CONTINUATIONS = unique(*VILLAGES, carte('LABORATORY'), carte('MARKET'),
                       carte('DISTANTSHORE'), carte('CELLAR'), SWAP)
ACTIONS_CONNUES = unique(*CONTINUATIONS, CHAPEL, MINE, MONEYLENDER, REMODEL,
    carte('WITCH'), carte('BANDIT'), carte('HIRELING'), carte('COUNCILROOM'),
    carte('LIBRARY'), carte('SMITHY'), carte('MILITIA'), carte('FORTUNETELLER'),
    carte('MAGNATE'), carte('ADVENTURER'), carte('BUREAUCRAT'),
    carte('WORKSHOP'), carte('CHANCELLOR'), carte('WOODCUTTER'), FEAST)
TERMINALES = tuple(c for c in ACTIONS_CONNUES if c not in CONTINUATIONS)
VICTOIRES = unique(COLONY, carte('PROVINCE'), carte('DUCHY'),
                   carte('ESTATE'), carte('GARDENS'))
TRESORS = unique(carte('COPPER'), carte('SILVER'), carte('GOLD'))
CARTES_STRATEGIE = unique(*VICTOIRES, *TRESORS, *ACTIONS_CONNUES)


def _nom(c: Any) -> str:
    return getattr(c, 'name', str(c).upper())


def nombre(mapping: Mapping | None, c) -> int:
    if c is None or mapping is None:
        return 0
    try:
        return max(0, int(mapping.get(c, 0)))
    except (AttributeError, ValueError, TypeError):
        return 0


def proprietes(c):
    try:
        return Card.class_(c)
    except (AttributeError, TypeError, KeyError, ValueError):
        return Card


def cout(c) -> int:
    obj = proprietes(c)
    try:
        return int(obj.cost) if obj is not Card else 10**6
    except (AttributeError, TypeError, ValueError):
        return 10**6


def argent(c) -> int:
    try:
        return max(0, int(getattr(proprietes(c), 'money', 0)))
    except (AttributeError, TypeError, ValueError):
        return 0


def est_action(c) -> bool:
    return c in ACTIONS_CONNUES and bool(getattr(proprietes(c), 'is_action', False))


def quantites(obj) -> dict:
    return dict(getattr(obj, 'quantities', {}) or {})


@dataclass(frozen=True)
class Contexte:
    tour: int = 1
    stock: Mapping = field(default_factory=dict)
    main: Mapping = field(default_factory=dict)
    achats: Mapping = field(default_factory=dict)
    gains: Mapping = field(default_factory=dict)
    detruits: Mapping = field(default_factory=dict)
    observation: Mapping = field(default_factory=dict)
    provinces: int = 8
    piles_vides: int = 0
    joueurs_actifs: int = 2
    actions: int = 1
    achats_restants: int = 1
    budget: int = 0
    # Champ facultatif : valeurs visibles, et jamais points supposés.
    score_relatif_connu: float | None = None

    @property
    def fin_proche(self) -> bool:
        # Deux piles épuisées = une seule avant la fin, mais ce n'est PAS la fin.
        return self.piles_vides >= 2 or self.provinces <= (2 if self.joueurs_actifs <= 2 else 3)

    @property
    def tours_restants(self) -> float:
        # Horizon seulement approximatif (les adversaires restent inconnus).
        if self.piles_vides >= 2 or self.provinces <= 1:
            return 1.5
        if self.piles_vides == 1 or self.provinces <= 3:
            return 3.2
        return max(2.5, min(11.0, 18.0 - 0.65 * max(0, self.tour - 1)))

    @property
    def deck(self) -> Counter:
        cards = Counter()
        cards[carte('COPPER')] = 7
        cards[carte('ESTATE')] = 3
        cards.update({k: int(v) for k, v in self.achats.items() if int(v) > 0})
        cards.update({k: int(v) for k, v in self.gains.items() if int(v) > 0})
        cards.subtract({k: int(v) for k, v in self.detruits.items() if int(v) > 0})
        for k in list(cards):
            cards[k] = max(0, cards[k])
        # Les observations en main sont des bornes inférieures, pas une preuve
        # de possession totale ; surtout utile pour les Malédictions reçues.
        for k, v in self.observation.items():
            cards[k] = max(cards[k], int(v))
        for k, v in self.main.items():
            cards[k] = max(cards[k], int(v))
        return +cards

    def copies(self, c) -> int:
        return nombre(self.deck, c)

    @property
    def taille(self) -> int:
        return max(1, sum(self.deck.values()))

    @property
    def terminales(self) -> int:
        return sum(self.copies(c) for c in TERMINALES)

    @property
    def villages(self) -> int:
        return sum(self.copies(c) for c in VILLAGES)

    @property
    def pioches(self) -> int:
        return sum(self.copies(c) for c in unique(carte('LABORATORY'), carte('LIBRARY'),
                        carte('SMITHY'), carte('COUNCILROOM'), carte('MARKET'),
                        carte('MAGNATE'), carte('HIRELING')))

    @property
    def tresors(self) -> int:
        return sum(self.copies(c) for c in TRESORS)

    @property
    def monnaie_deck(self) -> float:
        return sum(self.copies(c) * argent(c) for c in TRESORS)

    @property
    def monnaie_main(self) -> float:
        return sum(nombre(self.main, c) * argent(c) for c in TRESORS)

    @property
    def puissance_main_moyenne(self) -> float:
        return 5 * self.monnaie_deck / self.taille

    @property
    def economies_ameliorees(self) -> int:
        return self.copies(carte('SILVER')) + self.copies(carte('GOLD'))

    def probabilite_pioche(self, c, main_taille: int = 5) -> float:
        """P(obtenir >=1 exemplaire en main initiale), approximation hypergéométrique."""
        n, k = self.taille, self.copies(c)
        if k <= 0:
            return 0.0
        tirages = min(n, max(0, int(main_taille)))
        return 1.0 - prod((n - k - i) / (n - i) for i in range(tirages)) if n > tirages and n-k>=tirages else 1.0


def seuil_cuivre(ctx: Contexte) -> int:
    """Empêche le piège observé dans l'historique : zéro trésor après Chapelle."""
    argent_, or_ = ctx.copies(carte('SILVER')), ctx.copies(carte('GOLD'))
    if or_ >= 2 or (or_ >= 1 and argent_ >= 2) or argent_ >= 4:
        return 0
    if or_ >= 1 or argent_ >= 2:
        return 3
    return 4 if argent_ >= 1 else 5


def valeur_achat(c, ctx: Contexte) -> float:
    """Évaluation approximative d'un ajout au deck, recalculée à chaque choix.

    Pas de prétention à une espérance de victoire exacte : horizon, synergies,
    vitesse de pioche et saturation des actions sont évalués explicitement.
    """
    if c is None or nombre(ctx.stock, c) <= 0 or cout(c) > ctx.budget:
        return float('-inf')
    copies = ctx.copies(c)
    horizon = ctx.tours_restants
    fin = ctx.fin_proche
    n_joueurs = max(2, ctx.joueurs_actifs)
    # Fin de partie / points immédiats.
    if c == COLONY and c is not None:
        return 225 + (5 if fin else 0)
    if c == carte('PROVINCE'):
        return 205 + (12 if fin else 0)
    if c == carte('DUCHY'):
        return 117 if fin and (ctx.provinces <= 2 or ctx.piles_vides >= 2) else 15
    if c == carte('ESTATE'):
        return 87 if ctx.piles_vides >= 2 or ctx.provinces <= 1 else 0
    if c == carte('GARDENS'):
        return 18 + 12*(ctx.taille // 10) if fin else 5
    if c == carte('COPPER'):
        return -10
    # Économie : donne une raison mathématique de privilégier l'argent quand
    # le deck ne produit pas 6-8 pièces par tour.
    if c == carte('SILVER'):
        score = 67 + 39 * max(0.0, (5.1 - ctx.puissance_main_moyenne)/5.1)
        score += 12 if ctx.economies_ameliorees == 0 else 0
        score -= max(0, copies-3)*6
        score -= 18 if fin else 0
        return score
    if c == carte('GOLD'):
        score = 94 + 14 * max(0.0, (7.0 - ctx.puissance_main_moyenne)/7.0)
        score -= max(0, copies-4)*5
        score -= 12 if horizon <= 2 else 0
        return score

    base = {
        'HIRELING': 111, 'WITCH': 105, 'LABORATORY': 96,
        'BANDIT': 89, 'FESTIVAL': 89, 'MARKET': 84,
        'MILITIA': 81, 'LIBRARY': 83, 'COUNCILROOM': 77,
        'SMITHY': 77, 'MAGNATE': 66, 'FORTUNETELLER': 74,
        'DISTANTSHORE': 71, 'ADVENTURER': 53, 'WORKSHOP': 56,
        'CELLAR': 54, 'VILLAGE': 52, 'FARMINGVILLAGE': 50,
        'WOODCUTTER': 35, 'CHANCELLOR': 32, 'BUREAUCRAT': 47,
        'CHAPEL': 92, 'MONEYLENDER': 57, 'MINE': 62,
        'REMODEL': 55, 'SWAP': 48, 'FEAST': 40,
    }
    score = float(base.get(_nom(c), 0))
    if score <= 0 or c not in ACTIONS_CONNUES:
        return float('-inf')

    # Chaque action achetée est une carte morte si l'on ne peut la jouer.
    proportion_actions = sum(ctx.copies(x) for x in ACTIONS_CONNUES) / ctx.taille
    score -= max(0, copies)*17
    score -= 11*max(0, proportion_actions-0.26)*10
    # Une carte peu susceptible d'arriver en main avant la fin a moins de
    # valeur qu'une amélioration immédiatement rentable. Probabilité estimée
    # sur une main de 5 cartes après l'ajout de cette nouvelle copie.
    taille_apres = ctx.taille + 1
    copies_apres = copies + 1
    if taille_apres > 5 and taille_apres - copies_apres >= 5:
        chance = 1.0 - prod((taille_apres-copies_apres-i)/(taille_apres-i)
                            for i in range(5))
    else:
        chance = 1.0
    score += 9.0 * (chance-0.30)
    if c in TERMINALES:
        surcharge = max(0, ctx.terminales - ctx.villages - 1)
        score -= min(48, surcharge * 11)
    if c in VILLAGES:
        besoin = max(0, ctx.terminales - ctx.villages - 1)
        score += min(47, 19 * besoin)
        if besoin == 0:
            score -= 25
    if c == carte('LABORATORY'):
        score += min(14, 3 * max(0, ctx.terminales - ctx.villages))
    if c == carte('LIBRARY'):
        # Enrichit la main surtout si elle contient beaucoup de cartes mortes.
        pollution = ctx.copies(carte('CURSE')) + ctx.copies(carte('ESTATE'))
        score += min(13, pollution * 2)
    if c == carte('MAGNATE'):
        score += min(25, 4*ctx.copies(carte('SILVER')) + 7*ctx.copies(carte('GOLD')))
        if ctx.economies_ameliorees < 2: score -= 17
    if c == carte('WITCH'):
        maledictions = nombre(ctx.stock, carte('CURSE'))
        if maledictions == 0: score -= 40
        score += min(25, (n_joueurs-1)*9)
        if horizon < 5: score -= 20
    if c == carte('HIRELING'):
        score += min(18, max(0, horizon-5)*3)
        if horizon < 4: score -= 27
    if c == CHAPEL:
        dechets = ctx.copies(carte('CURSE')) + ctx.copies(carte('ESTATE'))
        dechets += max(0, ctx.copies(carte('COPPER'))-seuil_cuivre(ctx))
        if ctx.economies_ameliorees == 0 or dechets < 3 or ctx.tour > 10 or copies > 0:
            return -100.0
        score += min(12, dechets*2)
    if c == MONEYLENDER:
        if copies or ctx.copies(carte('COPPER')) <= seuil_cuivre(ctx) or ctx.copies(CHAPEL):
            return -100.0
    if c == MINE and (copies or ctx.economies_ameliorees == 0):
        score -= 35
    if c == REMODEL and copies:
        score -= 30
    if c == carte('WORKSHOP'):
        cibles = [x for x in CARTES_STRATEGIE if cout(x)<=4 and nombre(ctx.stock,x)>0 and x not in VICTOIRES]
        if not cibles: score -= 40
        if horizon<5: score -= 20
    if c == carte('ADVENTURER') and ctx.economies_ameliorees >= 4:
        score -= 20
    # Le jeu se termine trop tôt pour rentabiliser des moteurs coûteux.
    if horizon < 4:
        score -= (4-horizon) * 12
    return score


def valeur_action(c, ctx: Contexte) -> float:
    if c is None or not est_action(c) or nombre(ctx.main, c) <= 0 or ctx.actions <= 0:
        return float('-inf')
    n_actions = sum(nombre(ctx.main, k) for k in ACTIONS_CONNUES)
    n_terminales = sum(nombre(ctx.main, k) for k in TERMINALES)
    bonus_actions = 2 if c in VILLAGES else 1 if c in CONTINUATIONS else 0
    score = 35 + 6*bonus_actions
    if c in VILLAGES:
        score += 22 if n_terminales>0 else 3
        if ctx.actions>=n_actions: score -= 12
    if c == carte('LABORATORY'): score += 25
    if c == carte('MARKET'): score += 18
    if c == carte('FESTIVAL'): score += 23
    if c == carte('CELLAR'):
        score += 11 + 2*sum(nombre(ctx.main, x) for x in VICTOIRES)
    if c == carte('WITCH'):
        score += 36 if nombre(ctx.stock,carte('CURSE'))>0 else 8
        score += 4*(ctx.joueurs_actifs-2)
    if c == carte('HIRELING'): score += 30 if ctx.tours_restants>4 else 8
    if c == carte('BANDIT'): score += 25
    if c == carte('LIBRARY'): score += 21
    if c == carte('SMITHY'): score += 18
    if c == carte('MILITIA'): score += 17
    if c == carte('FORTUNETELLER'): score += 16
    if c == carte('COUNCILROOM'): score += 18
    if c == MONEYLENDER:
        if nombre(ctx.main,carte('COPPER')) == 0 or ctx.copies(carte('COPPER')) <= seuil_cuivre(ctx):
            return float('-inf')
        score += 14
    if c == CHAPEL:
        dechets = sum(nombre(ctx.main, x) for x in (carte('ESTATE'),carte('CURSE')))
        if ctx.copies(carte('COPPER'))>seuil_cuivre(ctx):
            dechets += nombre(ctx.main,carte('COPPER'))
        if dechets == 0: return float('-inf')
        score += min(14, 3*dechets)
    if c == MINE and sum(nombre(ctx.main,x) for x in
                         (carte('COPPER'),carte('SILVER')))==0:
        return float('-inf')
    if c == REMODEL:
        candidates=[x for x in ctx.main if x!=REMODEL and nombre(ctx.main,x)>0]
        if not candidates or max(valeur_destruction(x,ctx) for x in candidates)<-5:
            return float('-inf')
    if c == carte('MAGNATE'):
        score += 5*sum(nombre(ctx.main,x) for x in TRESORS)
    if c == carte('ADVENTURER') and ctx.puissance_main_moyenne<4.5: score += 10
    if c == carte('WORKSHOP') and ctx.tours_restants<4: score -= 10
    if c == carte('CHANCELLOR') or c == carte('WOODCUTTER'): score -= 4
    # Garder l'action pour une carte beaucoup plus forte si une seule action reste.
    if ctx.actions <= 1 and c in TERMINALES:
        score += 2
    return score


def valeur_destruction(c, ctx: Contexte) -> float:
    """Gain marginal à détruire c (positif = souhaitable), sans perdre l'économie."""
    if c == carte('CURSE'): return 100.0
    if c == carte('ESTATE'):
        return 64.0 if ctx.tours_restants>3 else -40.0
    if c == carte('COPPER'):
        if ctx.copies(c) <= seuil_cuivre(ctx): return -100.0
        return 28.0 + 5*ctx.economies_ameliorees
    if c in VICTOIRES: return -120.0
    if c == carte('SILVER'):
        return -85.0 if ctx.puissance_main_moyenne<6 else -35.0
    if c == carte('GOLD'): return -150.0
    if c in ACTIONS_CONNUES:
        # Une action terminale redondante peut être sacrifiée à Remodel.
        return 8.0 if c in TERMINALES and ctx.copies(c)>2 else -40.0
    return -30.0


def valeur_conservation(c, ctx: Contexte) -> float:
    """Valeur de conserver une carte en main face à une défausse forcée."""
    if c in VICTOIRES or c == carte('CURSE'): return -100.0
    if c in TRESORS: return 13.0 + 17*argent(c)
    if c in ACTIONS_CONNUES:
        if ctx.actions <= 0: return -15.0
        if ctx.actions == 1 and ctx.terminales>1 and c in TERMINALES:
            return 30 + valeur_action(c,ctx)/5
        return 40 + max(0,valeur_action(c,ctx))/6
    return 0.0


def valeur_gain(c, ctx: Contexte, destination='discard') -> float:
    # Même fonction que pour acheter, mais le gain ne dépense pas de monnaie.
    # Le moteur fournit une option de gain légale, même lorsqu'elle ne se
    # trouve pas dans le stock public (ou a été retirée au moment du choix).
    stock = dict(ctx.stock)
    stock[c] = max(1, nombre(stock,c))
    local = Contexte(**{**ctx.__dict__, 'stock': stock,
                         'budget': max(ctx.budget,cout(c))})
    score = valeur_achat(c,local)
    if destination == 'deck' and c in VICTOIRES:
        score -= 35
    if c == carte('SILVER') and ctx.economies_ameliorees==0:
        score += 15
    return score
