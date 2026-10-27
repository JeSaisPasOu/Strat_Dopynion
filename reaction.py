from dopynion.data_model import CardName

def confirmer_defausse(carte: CardName) -> bool:
    cartes_inutiles_en_main = [
        CardName.CURSE,
        CardName.PROVINCE,
        CardName.DUCHY,
        CardName.ESTATE
    ]
    return carte in cartes_inutiles_en_main

def choisir_defausse(main: list[CardName]) -> CardName:
    """
    Cas de la Milice : l'adversaire nous force à défausser.
    On jette en priorité les points de victoire (qui encombrent la main) et les malédictions.
    """
    ordre_defausse = [
        CardName.CURSE,
        CardName.PROVINCE,
        CardName.DUCHY,
        CardName.ESTATE,
        CardName.COPPER,
        CardName.SILVER
    ]
    for carte_cible in ordre_defausse:
        if carte_cible in main:
            return carte_cible
    # Sécurité : on défausse la première carte si on n'a que des bonnes cartes
    return main[0] 

def confirmer_destruction(carte: CardName) -> bool:
    """
    L'arbitre demande si on veut détruire (trash) cette carte.
    ATTENTION : Détruire est définitif ! On ne détruit jamais de gros points de victoire.
    """
    cartes_a_detruire = [
        CardName.CURSE,
        CardName.ESTATE,
        CardName.COPPER
    ]
    return carte in cartes_a_detruire

def choisir_destruction(main: list[CardName]) -> CardName:
    """
    L'arbitre nous force à détruire (trash) une carte.
    On cible en priorité la Malédiction (-1 PV), puis les petites cartes.
    """
    ordre_poubelle = [
        CardName.CURSE,
        CardName.ESTATE,
        CardName.COPPER
    ]
    for carte_cible in ordre_poubelle:
        if carte_cible in main:
            return carte_cible
    return main[0]