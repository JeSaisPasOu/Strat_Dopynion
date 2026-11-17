"""Achats de Toulousain V5, classés par le moteur central strategie.py."""
from dataclasses import replace
from dopynion.data_model import CardName
from strategie import (CARTES_STRATEGIE, Contexte, cout as cout_carte,
                       nombre, quantites, argent, valeur_achat)


def monnaie_en_main(main) -> int:
    return sum(nombre(quantites(main), c)*argent(c) for c in CARTES_STRATEGIE)


def priorites_achat(stock, *, achats=None, gains=None, trashed=None,
                    tour=1, provinces_restantes=8, piles_vides=0, budget=0,
                    main=None, joueurs_actifs=2, achats_restants=1,
                    observation=None, contexte=None):
    """Compare toutes les cartes gérées, avec un second achat en regard si possible."""
    ctx = contexte or Contexte(
        tour=tour, stock=quantites(stock), main=quantites(main),
        achats=achats or {}, gains=gains or {}, detruits=trashed or {},
        observation=observation or {}, provinces=provinces_restantes,
        piles_vides=piles_vides, budget=budget,
        joueurs_actifs=joueurs_actifs, achats_restants=achats_restants,
    )
    candidates = [c for c in CARTES_STRATEGIE if nombre(ctx.stock,c)>0 and cout_carte(c)<=ctx.budget]

    def valeur_totale(c):
        value = valeur_achat(c,ctx)
        if achats_restants < 2 or value==float('-inf'):
            return value
        restant = ctx.budget-cout_carte(c)
        # Exploration limitée : un second achat, sans simulation coûteuse.
        achats_suivants=dict(ctx.achats)
        achats_suivants[c] = achats_suivants.get(c,0)+1
        stock_suivant=dict(ctx.stock)
        stock_suivant[c] -= 1
        ctx2 = replace(ctx, achats=achats_suivants, stock=stock_suivant,
                       budget=restant, achats_restants=achats_restants-1)
        suivantes = [x for x in CARTES_STRATEGIE if nombre(stock_suivant,x)>0 and cout_carte(x)<=restant]
        meilleur_second=max((valeur_achat(x,ctx2) for x in suivantes),default=0)
        return value + 0.45 * max(0,meilleur_second)

    return [c for c in sorted(candidates,key=valeur_totale,reverse=True)
            if valeur_achat(c,ctx) >= 20]


def achat(main, carte, stock, *, monnaie_disponible=0, achats_restants=1):
    if achats_restants<=0 or nombre(quantites(stock),carte)<=0:
        return False
    if cout_carte(carte)>monnaie_en_main(main)+int(monnaie_disponible):
        return False
    return f'BUY {carte.value}'
