import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from dopynion.cards import Card, CardContainer
from dopynion.data_model import CardName, Cards
from dopynion.game import Game
from dopynion.player import Player, State

from action import EFFETS_ACTION, action, confirmer_fin_action, effets_action


class ActionTests(unittest.TestCase):
    def test_carte_action_presente_en_main(self):
        main = Cards(quantities={CardName.VILLAGE: 1})
        self.assertEqual(action(main, CardName.VILLAGE).decision, "ACTION village")

    def test_carte_absente_ou_quantite_nulle(self):
        for quantites in ({}, {CardName.VILLAGE: 0}, {CardName.SMITHY: 1}):
            with self.subTest(main=quantites):
                self.assertIs(
                    action(Cards(quantities=quantites), CardName.VILLAGE),
                    False,
                )

    def test_carte_tresor_ou_victoire_refusee(self):
        for carte in (CardName.COPPER, CardName.SILVER, CardName.ESTATE, CardName.GARDENS):
            with self.subTest(carte=carte):
                main = Cards(quantities={carte: 1})
                self.assertIs(action(main, carte), False)

    def test_actions_epuisees(self):
        main = Cards(quantities={CardName.VILLAGE: 1})
        self.assertIs(action(main, CardName.VILLAGE, actions_restantes=0), False)

    def test_respect_de_la_carte_choisie_et_main_inchangee(self):
        main = Cards(quantities={CardName.VILLAGE: 1, CardName.SMITHY: 1})
        main_avant = main.model_dump()
        self.assertEqual(action(main, CardName.SMITHY).decision, "ACTION smithy")
        self.assertEqual(main.model_dump(), main_avant)

    def test_carte_nommee_mais_non_implementee(self):
        carte = next(
            nom for nom in CardName if nom not in Card.types and nom != CardName.NONE
        )
        self.assertIs(action(Cards(quantities={carte: 1}), carte), False)

    def creer_joueur(self):
        dossier = self.enterContext(TemporaryDirectory())
        self.enterContext(patch("dopynion.record.records_dir", Path(dossier)))
        jeu = Game()
        joueur = Player("Toulousain")
        jeu.add_player(joueur)
        joueur.hand = CardContainer()
        joueur.hand.append(CardName.VILLAGE)
        joueur.hand.append(CardName.SMITHY)
        joueur.deck = CardContainer()
        joueur.discard = CardContainer()
        return joueur

    def test_enchainement_et_bonus_avec_le_moteur(self):
        joueur = self.creer_joueur()
        joueur.deck.append_several(4, CardName.COPPER)
        joueur.start_turn()

        for carte in (CardName.VILLAGE, CardName.SMITHY):
            with self.subTest(carte=carte):
                resultat = action(
                    joueur.hand.state,
                    carte,
                    actions_restantes=joueur.actions_left,
                )
                self.assertEqual(resultat.decision, f"ACTION {carte.value}")
                self.assertFalse(resultat.end_action)
                commande, nom_carte = resultat.decision.split()
                self.assertEqual(commande, "ACTION")
                joueur.action(CardName(nom_carte))
                resultat_termine = confirmer_fin_action(resultat)
                self.assertTrue(resultat_termine.end_action)
                self.assertNotIn(carte, joueur.hand)
                self.assertIn(carte, joueur.played_cards)
                if carte == CardName.VILLAGE:
                    # Une action dépensée, puis deux gagnées : 1 - 1 + 2 = 2.
                    self.assertEqual(joueur.actions_left, 2)
                    self.assertEqual(joueur.hand.copper_qty, 1)

        self.assertEqual(joueur.hand.copper_qty, 4)
        self.assertEqual(joueur.state_machine, State.BUY)
        self.assertEqual(joueur.actions_left, 0)

    def test_effet_pioche_impossible_ne_bloque_pas_la_carte(self):
        joueur = self.creer_joueur()
        joueur.start_turn()
        resultat = action(joueur.hand.state, CardName.VILLAGE)
        self.assertEqual(resultat.decision, "ACTION village")
        joueur.action(CardName(resultat.decision.split()[1]))
        # La pioche vide empêche +1 carte, mais pas le bonus +2 actions.
        self.assertEqual(joueur.actions_left, 2)
        self.assertEqual(joueur.hand.state.quantities, {CardName.SMITHY: 1})

    def test_retours_des_cartes_action(self):
        for carte, actions, buys, bonus_money in (
            (CardName.VILLAGE, 2, 0, 0),
            (CardName.WOODCUTTER, 0, 1, 2),
            (CardName.SMITHY, 0, 0, 0),
            (CardName.FESTIVAL, 2, 1, 2),
            (CardName.LABORATORY, 1, 0, 0),
            (CardName.MARKET, 1, 1, 1),
            (CardName.COUNCILROOM, 0, 1 ,0),
            (CardName.WITCH, 0, 0, 0),
            (CardName.FARMINGVILLAGE, 2 ,0 ,0),
            (CardName.DISTANTSHORE, 1, 0, 0),
            (CardName.HIRELING, 0, 0, 0),
            (CardName.BANDIT, 0, 0, 0), 
            (CardName.BUREAUCRAT, 0, 0, 0),
            (CardName.CHANCELLOR, 0, 0, 2),
            (CardName.MILITIA, 0, 0, 2),
            (CardName.ADVENTURER, 0, 0, 0),
            (CardName.CELLAR, 1, 0, 0),
            (CardName.FORTUNETELLER, 0, 0, 2),
            (CardName.LIBRARY, 0, 0, 0),
            (CardName.MAGNATE, 0, 0, 0),
            (CardName.WORKSHOP, 0, 0, 0),
            (CardName.CHAPEL, 0, 0, 0),
            (CardName.MINE, 0, 0, 0),
            (CardName.MONEYLENDER, 0, 0, 0),
            (CardName.REMODEL, 0, 0, 0),
            (CardName.SWAP, 1, 0, 0),
        ):
            with self.subTest(carte=carte):
                resultat = action(Cards(quantities={carte: 1}), carte)
                self.assertEqual(resultat.decision, f"ACTION {carte.value}")
                self.assertEqual(resultat.actions, actions)
                self.assertEqual(resultat.buys, buys)
                self.assertEqual(resultat.bonus_money, bonus_money)
                self.assertFalse(resultat.end_action)

    def test_bonus_independants_des_compteurs_et_sans_cumul(self):
        main = Cards(quantities={CardName.FESTIVAL: 1})
        premier = action(main, CardName.FESTIVAL, actions_restantes=1)
        deuxieme = action(main, CardName.FESTIVAL, actions_restantes=5)
        self.assertEqual(premier, deuxieme)
        self.assertEqual((deuxieme.actions, deuxieme.buys, deuxieme.bonus_money), (2, 1, 2))

    def test_confirmation_fin_action_sans_modifier_les_bonus(self):
        resultat = action(Cards(quantities={CardName.MARKET: 1}), CardName.MARKET)
        termine = confirmer_fin_action(resultat)
        self.assertFalse(resultat.end_action)
        self.assertTrue(termine.end_action)
        self.assertEqual(termine.decision, resultat.decision)
        self.assertEqual(
            (termine.actions, termine.buys, termine.bonus_money),
            (resultat.actions, resultat.buys, resultat.bonus_money),
        )

    def test_carte_action_hors_catalogue_refusee(self):
        self.assertIs(action(Cards(quantities={CardName.FEAST: 1}), CardName.FEAST), False)

    def test_preteur_bonus_uniquement_si_un_cuivre_est_ecarte(self):
        for nb_cuivres, accepte, bonus_attendu in (
            (0, True, 0),
            (1, False, 0),
            (2, True, 3),
        ):
            with self.subTest(nb_cuivres=nb_cuivres, accepte=accepte):
                joueur = self.creer_joueur()
                joueur.hand.append(CardName.MONEYLENDER)
                joueur.hand.append_several(nb_cuivres, CardName.COPPER)
                joueur.start_turn()

                resultat = action(joueur.hand.state, CardName.MONEYLENDER)
                self.assertEqual(resultat.bonus_money, 0)
                with patch.object(
                    joueur.hooks,
                    "confirm_trash_card_from_hand",
                    autospec=True,
                    return_value=accepte,
                ) as confirmation:
                    joueur.action(CardName.MONEYLENDER)

                self.assertEqual(confirmation.call_count, int(nb_cuivres > 0))
                self.assertEqual(joueur.money, bonus_attendu)
                self.assertEqual(joueur.hand.copper_qty, nb_cuivres - int(bonus_attendu > 0))


class EffetsActionTests(unittest.TestCase):
    def test_catalogue_des_cartes_action_du_client(self):
        self.assertEqual(
            set(EFFETS_ACTION),
            {
                CardName.VILLAGE,
                CardName.WOODCUTTER,
                CardName.SMITHY,
                CardName.FESTIVAL,
                CardName.LABORATORY,
                CardName.MARKET,
                CardName.COUNCILROOM,
                CardName.WITCH,
                CardName.FARMINGVILLAGE,
                CardName.DISTANTSHORE,
                CardName.HIRELING,
                CardName.BANDIT,
                CardName.BUREAUCRAT,
                CardName.CHANCELLOR,
                CardName.MILITIA,
                CardName.ADVENTURER,
                CardName.CELLAR,
                CardName.FORTUNETELLER,
                CardName.LIBRARY,
                CardName.MAGNATE,
                CardName.WORKSHOP,
                CardName.CHAPEL,
                CardName.MINE,
                CardName.MONEYLENDER,
                CardName.REMODEL,
                CardName.SWAP,
            }
        )

    def test_bonus_conformes_a_la_bibliotheque_dopynion(self):
        for carte in EFFETS_ACTION:
            with self.subTest(carte=carte):
                effets = effets_action(carte)
                type_carte = Card.class_(carte)
                self.assertEqual(effets.actions, type_carte.more_actions)
                self.assertEqual(effets.buys, type_carte.more_purchases)
                self.assertEqual(effets.bonus_money, type_carte.more_money)

    def test_carte_hors_catalogue_non_devinee(self):
        with self.assertRaises(ValueError):
            effets_action(CardName.FEAST)

    def test_bonus_contre_execution_reelle_des_cartes_action(self):
        dossier = self.enterContext(TemporaryDirectory())
        self.enterContext(patch("dopynion.record.records_dir", Path(dossier)))
        for carte in EFFETS_ACTION:
            with self.subTest(carte=carte):
                jeu = Game()
                joueur = Player("Toulousain")
                jeu.add_player(joueur)
                joueur.hand = CardContainer()
                joueur.hand.append(carte)
                # Une autre action reste en main après la résolution.
                joueur.hand.append(CardName.VILLAGE)
                if carte == CardName.REMODEL:
                    joueur.hand.append(CardName.ESTATE)
                joueur.deck = CardContainer()
                joueur.deck.append_several(5, CardName.COPPER)
                joueur.discard = CardContainer()
                joueur.start_turn()
                joueur.actions_left = 3
                effets = effets_action(carte)

                if carte == CardName.REMODEL:
                    with patch.object(
                        joueur.hooks,
                        "trash_card_from_hand",
                        autospec=True,
                        return_value=CardName.ESTATE,
                    ):
                        joueur.action(carte)
                    self.assertNotIn(CardName.ESTATE, joueur.hand)
                    self.assertIn(CardName.VILLAGE, joueur.hand)
                else:
                    joueur.action(carte)

                self.assertEqual(joueur.actions_left, 3 - 1 + effets.actions)
                self.assertEqual(joueur.purchases_left, 1 + effets.buys)
                self.assertEqual(joueur.money, effets.bonus_money)


if __name__ == "__main__":
    unittest.main()
