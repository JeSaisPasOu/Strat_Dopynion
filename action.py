"""Vérification d'une carte action choisie par le programme stratégie."""

from dataclasses import dataclass, replace
from typing import Literal

from dopynion.cards import Card
from dopynion.data_model import CardName, Cards

from communication import transmettre_commande


@dataclass(frozen=True)
class EffetsAction:
    """Bonus fixes d'une carte, tels qu'annoncés au compte rendu 5.

    ``actions`` et ``buys`` sont des bonus à ajouter aux compteurs.
    Jouer la carte consomme d'abord une action, indépendamment du bonus.
    ``bonus_money`` représente des crédits pour le tour en cours.
    La pioche est gérée par l'arbitre ; la stratégie consulte la main
    mise à jour et aucun nombre de cartes piochées n'est retourné ici.
    """

    actions: int = 0
    buys: int = 0
    bonus_money: int = 0


EFFETS_ACTION: dict[CardName, EffetsAction] = {
    CardName.VILLAGE: EffetsAction(actions=2),
    CardName.WOODCUTTER: EffetsAction(buys=1, bonus_money=2),
    CardName.SMITHY: EffetsAction(),
    CardName.FESTIVAL: EffetsAction(actions=2, buys=1, bonus_money=2),
    CardName.LABORATORY: EffetsAction(actions=1),
    CardName.MARKET: EffetsAction(actions=1, buys=1, bonus_money=1),
}


def effets_action(carte: CardName) -> EffetsAction:
    """Décrit les bonus fixes d'une des six cartes du compte rendu 5.

    Aucune carte n'est jouée par cette fonction. Une carte hors du
    catalogue doit être définie avant que ses effets soient annoncés.
    """
    try:
        return EFFETS_ACTION[carte]
    except KeyError:
        raise ValueError(f"Effets non définis pour la carte {carte}.") from None


@dataclass(frozen=True)
class ResultatAction:
    """Commande et bonus de la seule carte demandée, sans cumul.

    ``end_action`` confirme la fin réelle des effets chez l'arbitre.
    Il vaut False à la préparation de la commande : revenir de cette
    fonction ne signifie pas que l'arbitre a déjà joué la carte.
    """

    decision: str
    end_action: bool
    actions: int
    buys: int
    bonus_money: int


def confirmer_fin_action(resultat: ResultatAction) -> ResultatAction:
    """Marque une action comme résolue, sur confirmation du programme.

    À appeler après la résolution par l'arbitre, par exemple lorsque
    la stratégie reprend au prochain /play de la même partie après
    la commande ACTION et toutes les éventuelles demandes de choix.
    Ne pas appeler immédiatement après la préparation de la commande.

    Le résultat initial reste inchangé et les bonus ne sont pas cumulés.
    Cette fonction n'interroge pas l'arbitre et ne joue aucune carte.
    """
    return replace(resultat, end_action=True)


def action(
    main: Cards,
    carte: CardName,
    *,
    actions_restantes: int = 1,
) -> ResultatAction | Literal[False]:
    """Transmet la commande via /play et retourne les bonus, ou False.

    La stratégie choisit la carte, fournit la main courante du joueur
    et appelle cette fonction au bon moment du tour. Il faut avoir au
    moins une action disponible et posséder un exemplaire d'une carte
    de type action dans la main.

    Par défaut, le joueur dispose d'une action. Avant chaque appel
    suivant, le programme doit fournir le nombre d'actions restantes,
    en tenant compte des actions dépensées et des bonus +X Action.

    Les six cartes du compte rendu 5 sont prises en charge. Une autre
    carte doit avoir ses effets définis dans EFFETS_ACTION avant usage.

    Les champs ``actions``, ``buys`` et ``bonus_money`` sont les bonus
    annoncés par cette carte, pas des totaux restants. Jouer la carte
    consomme une action : le compteur devient ancien - 1 + bonus actions.
    Tous ces bonus concernent uniquement le tour en cours.

    Pendant /play, la commande est automatiquement placée dans la
    réponse HTTP courante ; la stratégie n'a pas à la transmettre.
    Le serveur envoie cette réponse avec le game_id après le retour
    de la stratégie. Hors de /play (par exemple dans un test local),
    seule la préparation est effectuée, sans envoi à un arbitre.
    Le programme peut ensuite appeler confirmer_fin_action, quand
    la résolution chez l'arbitre est confirmée.
    Un effet de pioche irréalisable ne rend pas la carte injouable.

    Cette fonction ne modifie ni la main ni le compteur d'actions.
    ``False`` signale au programme stratégie une action impossible ;
    ce n'est pas une commande à transmettre à /play.
    """
    if actions_restantes <= 0:
        return False

    if main.quantities.get(carte, 0) <= 0:
        return False

    if not Card.class_(carte).is_action:
        return False

    if carte not in EFFETS_ACTION:
        return False

    effets = effets_action(carte)
    resultat = ResultatAction(
        decision=f"ACTION {carte.value}",
        end_action=False,
        actions=effets.actions,
        buys=effets.buys,
        bonus_money=effets.bonus_money,
    )
    transmettre_commande(resultat.decision)
    return resultat
