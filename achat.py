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
    """Retourne ``BUY <carte>`` si l'achat est possible, ``False`` sinon.

    La stratégie fournit la carte souhaitée. Son prix et la valeur des
    trésors en main proviennent de la bibliothèque Dopynion : un cuivre
    vaut 1, un argent 2 et un or 3. Les cartes de victoire ne rapportent
    aucune monnaie.

    ``monnaie_disponible`` représente la monnaie déjà obtenue hors de la
    main (bonus d'action ou monnaie restante après un précédent achat).
    ``achats_restants`` vaut 1 pour un tour ordinaire ; la stratégie doit
    fournir sa valeur courante en cas d'achats successifs.

    La commande doit être placée dans le champ ``decision`` de la réponse
    à /play. L'arbitre effectue alors l'achat et met à jour le jeu.
    ``False`` est un résultat interne, pas une commande à envoyer à /play.
    """
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
