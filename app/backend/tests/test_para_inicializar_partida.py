import asyncio
import pytest

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from unittest.mock import MagicMock, patch
from game.game_status.endpoints import start_game
from game.game_status.schemas import StartGame


def mock_player_get(id):
#     # Retorna un objeto MockPlayer con el ID apropiado
    return MockPlayer(id)


def mock_select(*args, **kwargs):
    class MockedSelect:
        @staticmethod
        def first():
            return MockPlayer(1)
    
    return MockedSelect

class MockCardsList:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def __contains__(self, card):
        return card in self.cards

class MockPlayer:
    def __init__(self, player_id , name="mocked_name" , cards=[]):
        self.id = player_id
        self.name = name
        self.cards = MockCardsList()  # Usa el objeto MockCardsList
        

def mock_game_get(id=None):
    mock_game = MagicMock()
    mock_game.players = [MockPlayer(i) for i in [1, 2, 3, 4, 5]]
    mock_game.id = 1
    mock_game.Min_players = 5
    mock_game.Max_players = 7
    return mock_game


@patch('game.game_status.endpoints.select', side_effect=mock_select)
@patch('game.game_status.endpoints.change_player_status_to_TheThing', return_value=None)
@patch('game.game_status.endpoints.sit_the_players', return_value=None)
@patch('game.game_status.endpoints.deal_cards_to_players')    
@patch('game.game_status.endpoints.associate_deck_with_game_status')
@patch('game.game_status.endpoints.change_all_status')
@patch('game.game.endpoints.Game.get', side_effect=mock_game_get)
@patch('game.card.endpoints.Player.get', side_effect=mock_player_get)
@patch('game.card.endpoints.Card.get')
@patch('game.game_status.endpoints.is_player_admin')
@patch('game.game_status.endpoints.verify_game_state_exists')
@patch('game.game_status.endpoints.cantidad_players_para_iniciar')
@patch('game.game_status.endpoints.verify_game_exists')
@patch('pony.orm.db_session')
@pytest.mark.asyncio
async def test_start_game(mocked_db_session, mocked_verify_game_exists, mocked_cantidad_players_para_iniciar,
                    mocked_verify_game_state_exists, mocked_is_player_admin,
                    mocked_card_get, mocked_player_get, mocked_game_get, mocked_change_all_status, 
                    mocked_associate_deck_with_game_status, mocked_deal_cards_to_players, mocked_change_player_status_to_TheThing, mocked_select,  mocked_sit_the_players):

    # Aquí creamos una lista de objetos MockPlayer en lugar de una lista de enteros
    mock_game = MagicMock()
    mock_game.players = [MockPlayer(i) for i in [1, 2, 3, 4, 5]]
    mock_game.id = 1
    mock_game.Min_players = 5
    mock_game.Max_players = 7

    mocked_verify_game_exists.return_value = mock_game
    mocked_cantidad_players_para_iniciar.return_value = None
    mocked_is_player_admin.return_value = True  

    mock_estado_de_juego = MagicMock()
    mock_estado_de_juego.IdGame = 1
    mock_estado_de_juego.jugador_de_turno = 1
    mock_estado_de_juego.Fase_de_turno = 1
    mock_estado_de_juego.Sentido = True

    mocked_verify_game_state_exists.return_value = mock_estado_de_juego
    
#     # Simulamos que existe una carta con id 1
    mocked_card_get.return_value = MagicMock(id=1)
    
#     # Simulamos que existe un jugador con id 1
    mocked_player_get.return_value = MagicMock(id=1)

    mocked_change_all_status.return_value = None

    mocked_associate_deck_with_game_status.return_value = None

    mocked_deal_cards_to_players.return_value = None

    test_data = StartGame(id_game=1, id_player=1)
    response = await start_game(test_data)

    expected_response = {
         "id": 1,
         "cantidad de jugadores": 5,
         "jugador de turno": 1,
         "fase de turno": 1,
         "sentido": True
    }
    assert response == expected_response
