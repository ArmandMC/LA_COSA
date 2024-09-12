import asyncio
import pytest

import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from unittest.mock import MagicMock, patch
from fastapi import HTTPException


#importamos las funciones que vamos a testear, es decir las que estan en el archivo utils.py de cambio de fase de turno
from game.game_status.utils import *


@patch('game.game_status.utils.next_turn_player')
@patch('game.game_status.utils.Estado_de_juego')
@patch('game.game_status.utils.db_session')
def test_next_turn_phase_phase_1(mocked_db_session, mocked_Estado_de_juego, mocked_Next_turn_player):
    mocked_game_status = MagicMock()
    mocked_game_status.Fase_de_turno = 1
    mocked_game_status.jugador_de_turno = 1
    mocked_game_status.Sentido = True

    mocked_db_session.__enter__.return_value = mocked_game_status
    mocked_Estado_de_juego.get.return_value = mocked_game_status

    id_game = 1
    response = next_turn_phase(id_game)
    
    assert response == "game status updated"
    assert mocked_game_status.Fase_de_turno == 2  # Verificación adicional



@patch('game.game_status.utils.update_next_player')
@patch('game.game_status.utils.next_turn_player')
@patch('game.game_status.utils.Estado_de_juego')
@patch('game.game_status.utils.db_session')
def test_next_turn_phase_phase_2(mocked_db_session, mocked_Estado_de_juego, mocked_Next_turn_player, mocked_update_next_player):
    mocked_game_status = MagicMock()
    mocked_game_status.Fase_de_turno = 2
    mocked_game_status.jugador_de_turno = 1
    mocked_game_status.Sentido = True

    mocked_db_session.__enter__.return_value = mocked_game_status
    mocked_Estado_de_juego.get.return_value = mocked_game_status
    mocked_update_next_player.return_value = None

    id_game = 1
    response = next_turn_phase(id_game)
    
    assert response == "game status updated"
    assert mocked_game_status.Fase_de_turno == 3  # Verificación adicional





# @patch('game.game_status.utils.next_turn_player')
# @patch('game.game_status.utils.Estado_de_juego')
# @patch('game.game_status.utils.db_session')
# def test_next_turn_phase_phase_3(mocked_db_session, mocked_Estado_de_juego, mocked_Next_turn_player):
#     mocked_game_status = MagicMock()
#     mocked_game_status.Fase_de_turno = 3
#     mocked_game_status.jugador_de_turno = 1
#     mocked_game_status.Sentido = True

#     mocked_db_session.__enter__.return_value = mocked_game_status
#     mocked_Estado_de_juego.get.return_value = mocked_game_status

#     id_game = 1
#     response = next_turn_phase(id_game)
    
#     assert response == "game status updated"
#     assert mocked_game_status.Fase_de_turno == 1  # Verificación adicional
#     mocked_Next_turn_player.assert_called_once_with(id_game)
