import asyncio
import pytest
import sys
import os
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from game.game_status.utils import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

# Mocking db_session, change_status_game_to_finish y Game
@patch('game.game_status.utils.db_session')
@patch('game.game_status.utils.change_status_game_to_finish', return_value=None)
@patch('game.game_status.utils.Game')
def test_is_game_over(mocked_Game, _mocked_change_status, _mocked_db_session):
    """
    Comprobar si el juego ha terminado según diferentes escenarios.
    Escenarios:
    1. El estado del juego ya está en FINISH.
    2. Solo hay jugadores humanos.
    3. Hay jugadores humanos y "theThing".
    """

    
    # Configurar el juego ficticio y sus jugadores
    mocked_game = MagicMock()

    # Escenario donde el estado del juego es FINISH
    mocked_game.Estado_Partida = GameStatus.FINISH
    mocked_game.players = []  # Una lista vacía porque no necesitamos jugadores para este escenario
    mocked_Game.get.return_value = mocked_game

    game_id = 1  # Esto es un valor arbitrario ya que estamos mockeando la llamada a la base de datos
    assert is_game_over(game_id) == True  # Se espera que devuelva True ya que el estado es FINISH
    
    # Escenario donde hay solo jugadores humanos (o solo jugadores "theThing")
    mocked_game.Estado_Partida = GameStatus.INIT
    player_human = MagicMock()
    player_human.status = PlayerStatus.human
    mocked_game.players = [player_human, player_human]  #asdasdasd Dos jugadores humanos
    mocked_Game.get.return_value = mocked_game
    
    assert is_game_over(game_id) == True  # Se espera que devuelva True ya que no hay jugadores "theThing"
    
    # Escenario donde hay jugadores humanos y "theThing"
    player_the_thing = MagicMock()
    player_the_thing.status = PlayerStatus.theThing
    mocked_game.players = [player_human, player_the_thing]  # Un jugador humano y un jugador "theThing"
    mocked_Game.get.return_value = mocked_game
    
    assert is_game_over(game_id) == False  # Se espera que devuelva False ya que hay jugadores de ambos tipos
