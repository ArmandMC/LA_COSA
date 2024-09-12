import asyncio
import pytest

import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from unittest.mock import MagicMock, patch
from fastapi import HTTPException

#importamos las funciones que vamos a testear, es decir las que estan en el archivo utils.py de cambio de turno
from game.game_status.utils import *

@patch('game.game_status.utils.db_session')
@patch('game.game_status.utils.select')
@patch('game.game_status.utils.Player.get')
@patch('game.game_status.utils.Game.get')
@patch('game.game_status.utils.Estado_de_juego.get')
def test_next_turn_player(mocked_Estado_de_juego_get, mocked_Game_get, mocked_Player_get, mocked_select, _mocked_db_session):
    mocked_game_status = MagicMock()
    mocked_game_status.jugador_de_turno = 1
    mocked_game_status.Sentido = True
    mocked_game_status.next_player = 2

    # Mockeamos un objeto ficticio para el juego y su lista de jugadores
    mocked_game = MagicMock()
    mocked_game.players = [MagicMock() for _ in range(3)]  # Suponiendo que hay 3 jugadores

    _mocked_db_session.__enter__.return_value = mocked_game_status
    mocked_Estado_de_juego_get.return_value = mocked_game_status
    mocked_Game_get.return_value = mocked_game
    mocked_Player_get.return_value = MagicMock(position=1)
    mocked_select.return_value.first.return_value = MagicMock(id=2)

    id_game = 1
    response = next_turn_player(id_game)

    assert response == "game status updated"
    assert mocked_game_status.jugador_de_turno == 2
