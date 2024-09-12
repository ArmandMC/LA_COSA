import asyncio
import pytest

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from game.game.schemas import PartidaCreate
from game.game.endpoints import crear_partida

@patch('game.game.endpoints.Estado_de_juego')  # Mockeamos también Estado_de_juego
@patch('game.game.endpoints.validate_players')
@patch('game.game.endpoints.check_game_name_exists')
@patch('game.game.endpoints.Game')
@patch('pony.orm.db_session')
def test_crear_partida(mocked_db_session, mocked_Game, mocked_check_game_name_exists, mocked_validate_players, mocked_Estado_de_juego):  # Agregamos el nuevo mock al final
    
    # Definir comportamientos simulados
    mocked_validate_players.return_value = None
    mocked_check_game_name_exists.return_value = False
    
    mocked_game_instance = MagicMock()
    mocked_game_instance.id = 1  
    mocked_game_instance.Max_players = 7  
    mocked_game_instance.Min_players = 5
    
    mocked_Game.return_value = mocked_game_instance

    # Mockeamos una instancia para Estado_de_juego
    mock_estado_de_juego = MagicMock()
    mock_estado_de_juego.IdGame = 1
    mock_estado_de_juego.jugador_de_turno = 1
    mock_estado_de_juego.Fase_de_turno = 1
    mock_estado_de_juego.Sentido = True

    mocked_Estado_de_juego.return_value = mock_estado_de_juego
    
    # Datos de entrada
    test_data = PartidaCreate(name="test_game", min_players=5, max_players=7, has_password=False)
    
    response = asyncio.run(crear_partida(test_data))
    
    assert response == {"id": 1}