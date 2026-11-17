"""Réactions V5 : même moteur de valeur que les achats et les actions."""
from dataclasses import replace
from strategie import (Contexte, TRESORS, VICTOIRES, ACTIONS_CONNUES, carte,
                       argent, valeur_action, valeur_achat, valeur_conservation,
                       valeur_destruction, valeur_gain, seuil_cuivre, nombre, cout)


def contexte_defaut(main=(), **kwargs):
    return Contexte(main={x:main.count(x) for x in set(main)}, **kwargs)


def confirmer_defausse(carte_choisie, main=None, *, contexte=None):
    ctx=contexte or contexte_defaut(main or [])
    if carte_choisie is None: return False
    if carte_choisie in VICTOIRES or carte_choisie==carte('CURSE'):
        return True
    if carte_choisie==carte('COPPER'):
        # Avec Cellar, échanger un cuivre faible est utile si d'autres trésors
        # suffisent déjà au tour ou si les cartes mortes dominent la main.
        autres = sum(nombre(ctx.main,c)*argent(c) for c in TRESORS if c!=carte_choisie)
        return autres >= 3
    return valeur_conservation(carte_choisie,ctx)<-20


def choisir_defausse(main, *, contexte=None):
    if not main: return carte('COPPER')
    ctx=contexte or contexte_defaut(main)
    return min(main, key=lambda c: valeur_conservation(c,ctx))


def confirmer_destruction(carte_choisie, *, achats=None, trashed=None, tour=1,
                           main=None, contexte=None):
    ctx=contexte or Contexte(tour=tour,achats=achats or {},detruits=trashed or {},
                            main={c: (main or []).count(c) for c in set(main or [])})
    return carte_choisie is not None and valeur_destruction(carte_choisie,ctx)>0


def choisir_destruction(main, *, tour=1, achats=None, trashed=None, contexte=None):
    if not main: return carte('COPPER')
    ctx=contexte or Contexte(tour=tour, achats=achats or {}, detruits=trashed or {},
                            main={c: main.count(c) for c in set(main)})
    # L'arbitre donne une liste légale. On minimise la perte si on est forcé.
    return max(main, key=lambda c: valeur_destruction(c,ctx))


def choisir_carte_recue(possibles, destination='discard', *, tour=1,
                         achats=None, trashed=None, contexte=None):
    if not possibles: return carte('COPPER')
    ctx=contexte or Contexte(tour=tour,achats=achats or {},detruits=trashed or {},
                            stock={c:1 for c in possibles})
    return max(possibles,key=lambda c: valeur_gain(c,ctx,destination))


def sauter_reception_en_main(carte_choisie=None, *, actions_restantes=0,
                              main=None, contexte=None):
    # Bibliothèque : mettre de côté une carte Action non jouable.
    ctx=contexte or Contexte(actions=actions_restantes,
          main={c:(main or []).count(c) for c in set(main or [])})
    if carte_choisie not in ACTIONS_CONNUES:
        return False
    if ctx.actions<=0:
        return True
    # Avec déjà plusieurs meilleures actions terminales à jouer, renouveler la pioche.
    n_actions=sum(nombre(ctx.main,c) for c in ACTIONS_CONNUES)
    return ctx.actions==1 and n_actions>=2 and valeur_action(carte_choisie,
        replace(ctx, main={**ctx.main,carte_choisie: max(1,nombre(ctx.main,carte_choisie))}))<55


def choisir_monnaie_a_detruire(monnaies, *, tour=1, contexte=None):
    if not monnaies: return carte('COPPER')
    ctx=contexte or Contexte(tour=tour)
    # Mine : privilégie Argent -> Or si la liste donnée par le moteur l'autorise.
    return max(monnaies, key=lambda c: (c==carte('SILVER'),
                                         valeur_destruction(c,ctx)))
