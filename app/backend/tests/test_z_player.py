import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest
from fastapi import HTTPException
from pony.orm import db_session, select

from game.game.models import *
from game.player.endpoints import *
from game.player.schemas import PlayerJoin


# test for player join game


# test for player join game, when game not exist
@pytest.mark.integration_test
@pytest.mark.asyncio
async def test_join_game_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for player join game, when game not exist")

    input_data = PlayerJoin(name="test", gameId=100)
    try:
        response = await join_game(input_data)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Game 100 not exists"


# test for player join game, when game is full
@pytest.mark.integration_test
@pytest.mark.asyncio
async def test_join_game_full(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for player join game, when game is full")

    input_data = PlayerJoin(name="test", gameId=1)
    try:
        response = await join_game(input_data)
    except HTTPException as e:
        assert e.status_code == 400
        assert e.detail == "Game 1 is full"

# test for player join game, when name is already taken
@pytest.mark.integration_test
@pytest.mark.asyncio
async def test_join_game_name_taken(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for player join game, when name is already taken")

    input_data = PlayerJoin(name="test", gameId=2)
    try:
        response = await join_game(input_data)
    except HTTPException as e:
        assert e.status_code == 406
        assert e.detail == "Name test is already taken"

# test for player join game, when is the first player, and test if Estado_Partida is changed
@pytest.mark.integration_test
@pytest.mark.asyncio
async def test_join_game_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for player join game, when is the first player, and test if Estado_Partida is changed")

    input_data = PlayerJoin(name="test", gameId=3)
    response = await join_game(input_data)
    with db_session:
        game = select(g for g in Game if g.id == 3 and "test" in g.players.name).first()
        player = select(p for p in Player if p.name == "test" and p.game.id == 3).first()
        id = player.id
        assert game is not None
        assert game.admin == id
        assert game.Estado_Partida == GameStatus.NOTREADY
    assert response.playerId == id
    assert response.admin == True

# test for player join game, when is not the first player, and test if Estado_Partida is changed
@pytest.mark.integration_test
@pytest.mark.asyncio
async def test_join_game_not_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for player join game, when is not the first player, and test if Estado_Partida is changed")

    input_data = PlayerJoin(name="test1", gameId=3)
    response = await join_game(input_data)
    with db_session:
        game = select(g for g in Game if g.id == 3 and "test1" in g.players.name).first()
        player = select(p for p in Player if p.name == "test1" and p.game.id == 3).first()
        id = player.id
        player_ad = select(p for p in Player if p.name == "test" and p.game.id == 3).first()
        player_ad_id = player_ad.id
        assert game is not None
        assert game.admin == player_ad_id
        assert game.Estado_Partida == GameStatus.READY
    assert response.playerId == id
    assert response.admin == False

## tests for get players in a game

# test for get players in a game, when game not exist
@pytest.mark.integration_test
def test_get_players_not_exist(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players in a game, when game not exist")

    try:
        response = get_players(10)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "Game 10 not exists"

# test for get players in a game, but no players
@pytest.mark.integration_test
def test_get_players_no_players(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players in a game, but no players")

    response = get_players(game_id=4)
    assert response == []

# test for get players in a game, with players
@pytest.mark.integration_test
@db_session
def test_get_players(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players in a game, with players")

    response = get_players(game_id=3)
    player1 = select(p for p in Player if p.name == "test" and p.game.id == 3).first()
    player2 = select(p for p in Player if p.name == "test1" and p.game.id == 3).first()
    assert len(response) == 2
    assert response[0].playerId == player1.id
    assert response[0].name == "test"
    assert response[0].admin == True
    assert response[1].playerId == player2.id
    assert response[1].name == "test1"
    assert response[1].admin == False
