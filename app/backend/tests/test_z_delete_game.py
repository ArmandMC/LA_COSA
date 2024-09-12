import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest

from game.models.db import db

from pony.orm import db_session, commit
from fastapi import HTTPException
from game.game.utils import delete_game
from game.game.models import GameStatus
from game.player.utils import delete_player, dissasociate_player
from game.card.utils import delete_card
from game.game_status.utils import delete_game_status
from game.deckCards.utils import delete_deck

#test to delete a player, not exist
@pytest.mark.integration_test
def test_delete_player_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a player, not exist")

    try:
        delete_player(10)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Player 10 not exists"
    except Exception as e:
        assert False

#test to delete a player
@pytest.mark.integration_test
@db_session
def test_delete_player(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a player")

    player = db.Player(name="test", game=1)
    commit()
    delete_player(player.id)
    assert db.Player.get(id=player.id) is None

#test to delete a card, not exist
@pytest.mark.integration_test
def test_delete_card_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a card, not exist")

    try:
        delete_card(10)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Card 10 not exists"
    except Exception as e:
        assert False

#test to delete a card
@pytest.mark.integration_test
@db_session
def test_delete_card(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a card")

    card = db.Card(type="test", number=1, description="test")
    commit()
    delete_card(card.id)
    assert db.Card.get(id=card.id) is None

#test to delete a deck card, not exist
@pytest.mark.integration_test
def test_delete_deck_card_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a deck card, not exist")

    try:
        delete_deck(10)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Deck 10 not exists"
    except Exception as e:
        assert False

#test to delete a deck card
@pytest.mark.integration_test
@db_session
def test_delete_deck_card(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a deck card")

    game = db.Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = db.GameCards(id = game.id ,quantity_card=30, game_status=1)
    discard = db.DiscardCards(id = game.id ,quantity_card=0, game_status=1)
    commit()
    card1 = db.Card(type="test", number=1, description="test", game_deck=deck)
    card2 = db.Card(type="test", number=2, description="test", discard_deck=discard)

    delete_deck(deck.id)
    assert db.Card.get(id=card1.id) is None
    assert db.Card.get(id=card2.id) is None
    assert db.GameCards.get(id=game.id) is None
    assert db.DiscardCards.get(id=game.id) is None

#test to delete a game status
@pytest.mark.integration_test
@db_session
def test_delete_game_status(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a game status")

    game = db.Game(Max_players=4, Name="test5", Min_players=4, Estado_Partida=GameStatus.FINISH)
    commit()
    db.Estado_de_juego(IdGame=game.id, jugador_de_turno=1, Fase_de_turno=1, Sentido=True, players_alive=4)
    commit()
    deck = db.GameCards(id = game.id ,quantity_card=30, game_status=game.id)
    discard = db.DiscardCards(id = game.id ,quantity_card=0, game_status=game.id)
    commit()
    card1 = db.Card(type="test", number=1, description="test", game_deck=deck.id)
    card2 = db.Card(type="test", number=2, description="test", discard_deck=discard.id)
    commit()
    delete_game_status(game.id)
    assert db.Card.get(id=card1.id) is None
    assert db.Card.get(id=card2.id) is None
    assert db.GameCards.get(id=deck.id) is None
    assert db.DiscardCards.get(id=discard.id) is None
    assert db.Estado_de_juego.get(IdGame=game.id) is None


#test to delete a game, not exist
@pytest.mark.integration_test
def test_delete_game_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a game, not exist")

    try:
        delete_game(100)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Game 100 not exists"
    except Exception as e:
        assert False

#test to delete a game, game status not exist
@pytest.mark.integration_test
@db_session
def test_delete_game_status_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a game, game status not exist")

    game = db.Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    try:
        delete_game(game.id)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == f"Game status {game.id} not exists"
    except Exception as e:
        assert False
    game.delete()
    commit()


#test to delete a game
@pytest.mark.integration_test
@db_session
def test_delete_game(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to delete a game")

    game = db.Game(Max_players=4, Name="test5", Min_players=4, Estado_Partida=GameStatus.FINISH)
    commit()
    player1 = db.Player(name="test", game=game.id)
    player2 = db.Player(name="test", game=game.id)
    commit()
    estado = db.Estado_de_juego(IdGame=game.id, jugador_de_turno=1, Fase_de_turno=1, Sentido=True, players_alive=4)
    commit()
    deck = db.GameCards(id = game.id ,quantity_card=30, game_status=game.id)
    discard = db.DiscardCards(id = game.id ,quantity_card=0, game_status=game.id)
    commit()
    card1 = db.Card(type="test", number=1, description="test", game_deck=deck.id)
    card2 = db.Card(type="test", number=2, description="test", discard_deck=discard.id)
    commit()
    delete_game(game.id)
    assert db.Game.get(id=game.id) is None
    assert db.Player.get(id=player1.id) is None
    assert db.Player.get(id=player2.id) is None
    assert db.Estado_de_juego.get(IdGame=game.id) is None
    assert db.Card.get(id=card1.id) is None
    assert db.Card.get(id=card2.id) is None
    assert db.GameCards.get(id=deck.id) is None
    assert db.DiscardCards.get(id=discard.id) is None


#test to dissasociate a player from a game, not exist
@pytest.mark.integration_test
def test_dissasociate_player_from_game_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to dissasociate a player from a game, not exist")

    try:
        dissasociate_player(10)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Player 10 not exists"
    except Exception as e:
        assert False

#test to dissasociate a player from a game, game is ready
@pytest.mark.integration_test
@db_session
def test_dissasociate_player_from_game_ready(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to dissasociate a player from a game, game is ready")

    game = db.Game(Max_players=4, Name="test5", Min_players=4, Estado_Partida=GameStatus.READY)
    commit()
    player1 = db.Player(name="test", game=game.id)
    player2 = db.Player(name="test", game=game.id)
    commit()
    try:
        dissasociate_player(player1.id)
    except HTTPException as e:
        assert e.status_code == 406
        assert e.detail == f"Game {game.id} has already started"
    except Exception as e:
        assert False
    game.delete()
    player1.delete()
    player2.delete()
    commit()

#test to dissasociate a player from a game, player is not admin
@pytest.mark.integration_test
@db_session
def test_dissasociate_player_from_game_not_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to dissasociate a player from a game, player is not admin")

    game = db.Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = db.Player(name="test", game=game.id)
    player2 = db.Player(name="test", game=game.id)
    commit()
    response = dissasociate_player(player1.id)
    assert response == "Player deleted"
    assert db.Player.get(id=player1.id) is None
    assert db.Player.get(id=player2.id) is not None
    game.delete()
    player2.delete()
    commit()

#test to dissasociate a player from a game, player is admin
@pytest.mark.integration_test
@db_session
def test_dissasociate_player_from_game_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to dissasociate a player from a game, player is admin")

    game = db.Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = db.Player(name="test", game=game.id, admin=True)
    player2 = db.Player(name="test", game=game.id)
    commit()
    estado = db.Estado_de_juego(IdGame=game.id, jugador_de_turno=1, Fase_de_turno=1, Sentido=True, players_alive=4)
    commit()
    response = dissasociate_player(player1.id)
    assert response == "Game deleted"
    assert db.Player.get(id=player1.id) is None
    assert db.Player.get(id=player2.id) is None
    assert db.Game.get(id=game.id) is None
