"""Achat pour l'arbitre de Dopynion."""

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards


def achat(
    main: Cards,
    carte: CardName,
    stock: Cards,
    *,
    monnaie_disponible: int = 0,
    achats_restants: int = 1,
) -> str | bool:
    
    if achats_restants <= 0 or stock.quantities.get(carte, 0) <= 0:
        return False
    
    type_carte = Card.class_(carte)
    if type_carte is Card:
        # Certaines cartes sont nommées dans le modèle mais pas implémentées.
        return False

    budget = monnaie_disponible + sum(
        Card.class_(nom_carte).money * quantite
        for nom_carte, quantite in main.quantities.items()
    )
    if budget < type_carte.cost:
        return False

    return f"BUY {carte.value}"
