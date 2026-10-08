# Dopynion Bot API

API FastApi servant de joueur / bot pour le jeu **Dopynion** (implémentation Python de *Dominion*).

Documentation interactive de référence : [https://dopynion-template.lecalamar.fr/docs](https://dopynion-template.lecalamar.fr/docs)

---

## 1. Prérequis

* **Python 3.14**
* Gestionnaire de paquets **pip**

---

## 2. Modules et Dépendances

Faire la commande 'pip install -r requirements.txt'


## 3. Modifier l'api

Pour modifier l'api et le mettre en ligne faire ces commande :

1) ssh befre@ssh-befre.alwaysdata.net
2) mot de passe : voir discord
3) cd ~/Strat_Dopynion
4) git pull

Après ça aller sur le site alwaysdata et relancer l'api avec le logo des fleche qui tourne (ps: pour sortir du terminal ssh fair "exit")

## 4. Retour de la fonction action

La stratégie choisit la carte et appelle `action` au bon moment du tour.
Pendant une requête `/play`, cet appel place automatiquement la commande
dans la réponse destinée à l'arbitre. La stratégie récupère les bonus ;
elle n'a pas à envoyer ni à retourner la commande pour qu'elle soit transmise.
La fonction retourne `False` si la carte ne peut pas être jouée ou si
ses effets ne sont pas encore définis dans le catalogue. Sinon, elle
retourne un `ResultatAction` avec les champs suivants :

| Champ | Signification |
|---|---|
| `decision` | Commande `ACTION <nom_carte>`, placée automatiquement dans la réponse à `/play`. |
| `end_action` | Confirmation de fin réelle des effets ; `False` à la préparation. |
| `actions` | Bonus d'actions de cette carte uniquement. |
| `buys` | Bonus d'achats de cette carte uniquement. |
| `bonus_money` | Bonus de crédits de cette carte uniquement, pour ce tour. |

Aucun cumul ni état entre les requêtes n'est mémorisé par la fonction. Une carte
consomme une action avant son bonus : le compteur devient
`actions_restantes - 1 + resultat.actions`. Un bonus nul vaut toujours `0`.

Les six cartes du [compte rendu réunion 5](https://docs.google.com/document/d/1tSDUKYQxZG90aoxY5dKmFEJY5ZVaT0kAA_7aPzr12ws/edit)
sont définies :

| Carte | `actions` | `buys` | `bonus_money` |
|---|---:|---:|---:|
| Village | 2 | 0 | 0 |
| Bûcheron | 0 | 1 | 2 |
| Forgeron | 0 | 0 | 0 |
| Festival | 2 | 1 | 2 |
| Laboratoire | 1 | 0 | 0 |
| Marché | 1 | 1 | 1 |

Exemple de préparation locale d'une action (sans requête `/play`, aucun envoi) :

```python
from dopynion.data_model import CardName, Cards
from action import action

main = Cards(quantities={CardName.FESTIVAL: 1})
resultat = action(main, CardName.FESTIVAL, actions_restantes=1)
if resultat is not False:
    print(resultat.decision)     # ACTION festival
    print(resultat.end_action)   # False : commande pas encore exécutée
    print(resultat.actions)      # 2
    print(resultat.buys)         # 1
    print(resultat.bonus_money)  # 2
```

L'arbitre appelle `POST /play` avec l'état du jeu et l'en-tête `x-game-id`.
Le serveur appelle la stratégie, puis transmet la commande enregistrée
par `action` dans sa réponse HTTP, avec le `game_id`, par exemple :

```json
{"game_id": "partie-1", "decision": "ACTION village"}
```

L'envoi a lieu lorsque `/play` renvoie sa réponse, après le retour de la
stratégie. Il n'y a pas de requête sortante vers une URL de l'arbitre.
Chaque `/play` peut transmettre une seule commande ; une autre action
doit attendre l'appel suivant de l'arbitre, avec la main mise à jour.
Les commandes sont isolées entre les requêtes et les parties.

Le programme stratégie n'est pas présent dans cette branche. Pour le
raccorder, affecter sa fonction à `app.state.strategie` dans `server.py`
après son import. Le point d'entrée prévu est `strategie(jeu, game_id)`.
Cette fonction appelle `action` pour jouer la carte choisie. Pour les
autres décisions, elle peut retourner une chaîne, notamment `END_TURN`.
`action` ne produit jamais `END_TURN` ; une action impossible retourne
`False` sans placer de commande dans la réponse.

Sans stratégie raccordée, `/play` répond HTTP 503. Si la stratégie ne
fournit aucune commande, le serveur signale une erreur ; il ne termine
pas automatiquement le tour.

Une fois la résolution confirmée (par exemple au prochain `/play` de
la même partie après toutes les demandes de choix), la stratégie peut
appeler `confirmer_fin_action(resultat)` : le nouveau résultat aura
`end_action=True`, avec les mêmes bonus. Cette confirmation reste à
raccorder au programme stratégie ; elle ne se produit pas automatiquement
dans le serveur actuel. `end_action` n'est pas la fin de la phase action.

La fonction ne retourne aucune information sur la pioche. L'arbitre
résout cet effet et la stratégie consulte elle-même la main mise à jour.

Pour lancer les tests :

```powershell
python -B -m unittest discover -s test_action -v
```

Les tests couvrent aussi la réponse HTTP de `/play`, avec une stratégie
de test : transmission automatique de `ACTION`, séparation des parties,
action impossible, et `END_TURN` décidé uniquement par la stratégie.
