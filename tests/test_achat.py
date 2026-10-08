import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from dopynion.cards import CardContainer
from dopynion.data_model import CardName, Cards
from dopynion.game import Game
from dopynion.player import Player

from achat import achat


class AchatTests(unittest.TestCase):
    def test_budget_et_valeur_des_tresors(self):
        stock = Cards(quantities={CardName.SILVER: 1})
        cas = [
            ("insuffisant", {CardName.COPPER: 2}, False),
            ("exact", {CardName.COPPER: 3}, "BUY silver"),
            ("superieur", {CardName.COPPER: 4}, "BUY silver"),
            ("argent et cuivre", {CardName.SILVER: 1, CardName.COPPER: 1}, "BUY silver"),
            ("or", {CardName.GOLD: 1}, "BUY silver"),
            ("victoire sans monnaie", {CardName.ESTATE: 5}, False),
            ("main vide", {}, False),
        ]
        for nom, cartes, attendu in cas:
            with self.subTest(nom=nom):
                self.assertEqual(
                    achat(Cards(quantities=cartes), CardName.SILVER, stock),
                    attendu,
                )

    def test_stock_absent_ou_epuise(self):
        main = Cards(quantities={CardName.GOLD: 3})
        for quantites in ({}, {CardName.PROVINCE: 0}):
            with self.subTest(stock=quantites):
                self.assertIs(
                    achat(main, CardName.PROVINCE, Cards(quantities=quantites)),
                    False,
                )

    def test_carte_gratuite_et_limite_achats(self):
        main = Cards()
        stock = Cards(quantities={CardName.COPPER: 1})
        self.assertEqual(achat(main, CardName.COPPER, stock), "BUY copper")
        self.assertIs(
            achat(main, CardName.COPPER, stock, achats_restants=0), False
        )

    def test_bonus_de_monnaie(self):
        self.assertEqual(
            achat(
                Cards(),
                CardName.SILVER,
                Cards(quantities={CardName.SILVER: 1}),
                monnaie_disponible=3,
            ),
            "BUY silver",
        )

    def test_respect_du_choix_du_programme_strategie(self):
        stock = Cards(
            quantities={CardName.PROVINCE: 12, CardName.ESTATE: 12}
        )
        main = Cards(quantities={CardName.COPPER: 8})
        # Domaine reste la cible, même si Province est aussi abordable.
        self.assertEqual(achat(main, CardName.ESTATE, stock), "BUY estate")

    def test_achat_avec_le_moteur_et_monnaie_restante(self):
        dossier = self.enterContext(TemporaryDirectory())
        self.enterContext(patch("dopynion.record.records_dir", Path(dossier)))
        jeu = Game()
        joueur = Player("Toulousain")
        jeu.add_player(joueur)
        joueur.hand = CardContainer()
        joueur.hand.append(CardName.GOLD)
        joueur.hand.append(CardName.SILVER)
        joueur.start_turn()
        joueur.purchases_left = 2

        for carte in (CardName.SILVER, CardName.ESTATE):
            with self.subTest(carte=carte):
                main = joueur.hand.state
                stock = jeu.stock.state
                main_avant = main.model_dump()
                stock_avant = stock.model_dump()
                decision = achat(
                    main,
                    carte,
                    stock,
                    monnaie_disponible=joueur.money,
                    achats_restants=joueur.purchases_left,
                )
                self.assertEqual(decision, f"BUY {carte.value}")
                self.assertEqual(main.model_dump(), main_avant)
                self.assertEqual(stock.model_dump(), stock_avant)

                commande, nom_carte = decision.split()
                self.assertEqual(commande, "BUY")
                joueur.buy(CardName(nom_carte))
                self.assertIn(carte, joueur.discard)
                self.assertEqual(
                    jeu.stock.state.quantities[carte],
                    stock.quantities[carte] - 1,
                )

        self.assertEqual(joueur.money, 0)
        self.assertEqual(joueur.purchases_left, 0)


if __name__ == "__main__":
    unittest.main()