import requests
import pytest

SERVICE_URL = "http://127.0.0.1:8000"

# test to get game empty
@pytest.mark.end2end_test
def test_get_game_empty(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game empty")
    data = requests.get(f"{SERVICE_URL}/game/")
    assert data.status_code == 200
    assert data.json() == []

# test to create game with wrong data
@pytest.mark.end2end_test
def test_create_game_wrong(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for create game with wrong data")

    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game", "min_players": 3, "max_players": 8, "has_password": False})
    assert data.status_code == 400
    assert data.json() == {"detail": "Número de jugadores no válido."}
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game", "min_players": 4, "max_players": 13, "has_password": False})
    assert data.status_code == 400
    assert data.json() == {"detail": "Número de jugadores no válido."}
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game", "min_players": 5, "max_players": 4, "has_password": False})
    assert data.status_code == 400
    assert data.json() == {"detail": "El mínimo de jugadores no puede ser mayor que el máximo."}

# test to create game
@pytest.mark.end2end_test
def test_create_game(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for create game")

    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 1}

# test to create game, but name already exists
@pytest.mark.end2end_test
def test_create_game_name_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for create game, but name already exists")

    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game", "min_players": 4, "max_players": 8, "has_password": False})
    assert data.status_code == 400
    assert data.json() == {"detail": "El nombre de partida ya existe."}

# test to get game
@pytest.mark.end2end_test
def test_get_game(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game")

    data = requests.get(f"{SERVICE_URL}/game/")
    assert data.status_code == 200
    assert data.json() == [{"id": 1, "name": "test_game", "cantidad de jugadores": 0}]

# test join game
@pytest.mark.end2end_test
def test_join_game(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for join game, when is the first player")

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": 1})
    assert data.status_code == 200
    assert data.json() == {"playerId": 1, "admin": True}

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": 1})
    assert data.status_code == 200
    assert data.json() == {"playerId": 2, "admin": False}

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": 1})
    assert data.status_code == 200
    assert data.json() == {"playerId": 3, "admin": False}

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": 1})
    assert data.status_code == 200
    assert data.json() == {"playerId": 4, "admin": False}

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player5", "gameId": 1})
    assert data.status_code == 200
    assert data.json() == {"playerId": 5, "admin": False}

#test join game, but game not exists
@pytest.mark.end2end_test
def test_join_game_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for join game, but game not exists")

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player6", "gameId": 2})
    assert data.status_code == 404
    assert data.json() == {"detail": "Game 2 not exists"}

# test join game, but game is full
@pytest.mark.end2end_test
def test_join_game_full(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for join game, but game is full")

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player6", "gameId": 1})
    assert data.status_code == 400
    assert data.json() == {"detail": "Game 1 is full"}

# test join game, but name is already taken
@pytest.mark.end2end_test
def test_join_game_name_taken(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for join game, but name is already taken")

    requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game2", "min_players": 4, "max_players": 8, "has_password": False})
    requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player", "gameId": 2})
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player", "gameId": 2})
    assert data.status_code == 406
    assert data.json() == {"detail": "Name test_player is already taken"}

# test get players
@pytest.mark.end2end_test
def test_get_players(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players")

    data = requests.get(f"{SERVICE_URL}/player", params={"game_id": 1})
    assert data.status_code == 200
    assert data.json() == [{"playerId": 1, "name": "test_player1", "admin": True}, 
                           {"playerId": 2, "name": "test_player2", "admin": False}, 
                           {"playerId": 3, "name": "test_player3", "admin": False}, 
                           {"playerId": 4, "name": "test_player4", "admin": False}, 
                           {"playerId": 5, "name": "test_player5", "admin": False}]
    

# test get players, but game dont have players
@pytest.mark.end2end_test
def test_get_players_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players, but game dont have players")

    requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game3", "min_players": 4, "max_players": 8, "has_password": False})   
    data = requests.get(f"{SERVICE_URL}/player", params={"game_id": 3})
    assert data.status_code == 200
    assert data.json() == []

# test get players, but game not exists
@pytest.mark.end2end_test
def test_get_players_game_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get players, but game not exists")

    data = requests.get(f"{SERVICE_URL}/player", params={"game_id": 4})
    assert data.status_code == 404
    assert data.json() == {"detail": "Game 4 not exists"}

#test start game, but game not exists
@pytest.mark.end2end_test
def test_start_game_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for start game, but game not exists")

    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": 4, "id_player": 1})
    assert data.status_code == 404
    assert data.json() == {"detail": "La partida no existe."}

#test get game status, but game not exists
@pytest.mark.end2end_test
def test_get_game_status_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game status, but game not exists")

    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 50})
    assert data.status_code == 404
    assert data.json() == {"detail": "La partida no existe."}

#test get game status, but player not exists
@pytest.mark.end2end_test
def test_get_game_status_player_not_exists(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game status, but player not exists")

    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 3})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "NOTREADY",
                           "name": "test_game3",
                            "players": [],
                            "gameInfo": {"sentido": "derecha",
                                         "obstaculos": [], 
                                         "jugadorTurno": 1, 
                                         "faseDelTurno": 1,
                                         "siguienteJugador": None}}

#test get game status estatus ready
@pytest.mark.end2end_test
def test_get_game_status_ready(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game status, but game is ready")

    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "READY",
                           "name": "test_game",
                           "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 2, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 3, "name": "test_player3", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 4, "name": "test_player4", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 5, "name": "test_player5", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                            "gameInfo": {"sentido": "derecha",
                                        "obstaculos": [], 
                                        "jugadorTurno": 1, 
                                        "faseDelTurno": 1,
                                        "siguienteJugador": None}}

#test get game status estatus not ready
@pytest.mark.end2end_test
def test_get_game_status_not_ready(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game status, but game is not ready")

    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 2})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "NOTREADY", 
                           "name": "test_game2",
                           "players": [{'id': 6, 'name': 'test_player', 'position': 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha", 
                                        "obstaculos": [], 
                                        "jugadorTurno": 1, 
                                        "faseDelTurno": 1,
                                        "siguienteJugador": None}}

#test start game, but there are not enough players
@pytest.mark.end2end_test
def test_start_game_not_enough_players(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for start game, but there are not enough players")

    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": 2, "id_player": 6})
    assert data.status_code == 400
    assert data.json() == {"detail": "No hay suficientes jugadores para iniciar la partida."}

#test delete player, player not admin
@pytest.mark.end2end_test
def test_delete_player(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for delete player, player not admin")
    
    requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player7", "gameId": 2})
    data = requests.delete(f"{SERVICE_URL}/player/7")
    assert data.status_code == 200
    assert data.json() == 'Player deleted'
    #check with get status game
    response = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 2})
    assert response.status_code == 200
    assert response.json() == {"gameStatus": "NOTREADY",
                                "name": "test_game2",
                                "players": [{'id': 6, 'name': 'test_player', 'position': 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                                "gameInfo": {"sentido": "derecha",
                                            "obstaculos": [], 
                                            "jugadorTurno": 1,
                                            "faseDelTurno": 1,
                                            "siguienteJugador": None}}
    
#test delete player, player admin
@pytest.mark.end2end_test
def test_delete_player_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for delete player, player admin")
    
    requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player8", "gameId": 2})
    data = requests.delete(f"{SERVICE_URL}/player/6")
    assert data.status_code == 200
    assert data.json() == 'Game deleted'
    #check with get game
    response = requests.get(f"{SERVICE_URL}/game/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "test_game", "cantidad de jugadores": 5},
                                {"id": 3, "name": "test_game3", "cantidad de jugadores": 0}]

#test start game, but player is not admin
@pytest.mark.end2end_test
def test_start_game_not_admin(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for start game, but player is not admin")

    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": 1, "id_player": 2})
    assert data.status_code == 403
    assert data.json() == {"detail": "No eres el administrador de esta partida."}

#test start game
@pytest.mark.end2end_test
def test_start_game(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for start game")

    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": 1, "id_player": 1})
    assert data.status_code == 200
    assert data.json() == {"id": 1, "cantidad de jugadores": 5, "jugador de turno": 1, "fase de turno": 1, "sentido": True}

#test get game status estatus init
@pytest.mark.end2end_test
def test_get_game_status_init(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get game status, but game is init")
    
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game", 
                           "players": [{"id": 1, "name": "test_player1", "position": 0,  "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 2, "name": "test_player2", "position": 1,  "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": 3, "name": "test_player3", "position": 2,  "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": 4, "name": "test_player4", "position": 3,  "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}, 
                                       {"id": 5, "name": "test_player5", "position": 4,  "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                        "obstaculos": [],  
                                        "jugadorTurno": 1, 
                                        "faseDelTurno": 1,
                                        "siguienteJugador": 2}}
    
#test player status 1
@pytest.mark.end2end_test
def test_get_player_status_1(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get player status 1")

    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})

    assert data.status_code == 200
    assert data.json() == {'id': 1, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 'in_quarantine': False, 'quarantine_shifts': 0,
                             'cards': [{'type': 'Whisky', 'id': 133}, 
                                       {'type': 'Infeccion', 'id': 134}, 
                                       {'type': 'Lanzallamas', 'id': 135}, 
                                       {'type': 'LaCosa', 'id': 136}]}
    
#test player status 2
@pytest.mark.end2end_test
def test_get_player_status_2(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for get player status 2")

    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})

    assert data.status_code == 200
    assert data.json() == {'id': 2, 'name': 'test_player2', 'position': 1, 'status': 'human', 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'CambioDeLugar', 'id': 129}, 
                                     {'type': 'VigilaTusEspaldas', 'id': 130}, 
                                     {'type': 'MasValeQueCorras', 'id': 131}, 
                                     {'type': 'Analisis', 'id': 132}]}

#test hacer cosas fuera de turno
@pytest.mark.end2end_test
def test_hacer_cosas_fuera_de_turno(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for hacer cosas fuera de turno")

    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": 1, "id_player": 2, "id_player_to": 1, "id_card": 129})
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not your turn"}

    data = requests.post(f"{SERVICE_URL}/card/steal_card/2")
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not your turn"}

    data = requests.post(f"{SERVICE_URL}/card/discard_card/2/129")
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not your turn"}

    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": 2, "player_to_id": 1, "card_id": 129})
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not your turn"}


#test hacer cosas fuera de fase
@pytest.mark.end2end_test
def test_hacer_cosas_fuera_de_fase(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for hacer cosas fuera de fase")

    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": 1, "id_player": 1, "id_player_to": 2, "id_card": 133})
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not the phase of the turn"}

    data = requests.post(f"{SERVICE_URL}/card/discard_card/1/133")
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not the phase of the turn"}

    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": 1, "player_to_id": 2, "card_id": 133})
    assert data.status_code == 403
    assert data.json() == {"detail": "It is not the phase of the turn"}








# #test play card, lanzallamas
# @pytest.mark.end2end_test
# def test_play_card_lanzallamas(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for play card, lanzallamas")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/2")
#     assert data.status_code == 200
#     assert data.json() == {'id': 19, 'type': 'Lanzallamas', 'number': 19, 'description': 'Kill player'}

#     #play card
#     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 2, "id_player_to": 3, "id_card": 37})
#     assert data.status_code == 200
#     assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}

#     #check with get player status 1
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
#     assert data.status_code == 200
#     assert data.json() == {"id": 1, "name": "test_player1", "position": 0, "status": "theThing",
#                             'cards': [{'id': 33, 'type': 'MasValeQueCorras'},
#                                         {'id': 38, 'type': 'Empty'},
#                                         {'id': 39, 'type': 'Sospecha'},
#                                         {'id': 40, 'type': 'LaCosa'}]}
    
#     #check with get player status 2
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
#     assert data.status_code == 200
#     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
#                             'cards': [  {'id': 19, 'type': 'Lanzallamas'},
#                                         {'id': 34, 'type': 'Analisis'},
#                                         {'id': 35, 'type': 'Whisky'},
#                                         {'id': 36, 'type': 'Infeccion'}]}
    
#     #check with get player status 3
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
#     assert data.status_code == 200
#     assert data.json() == {"id": 3, "name": "test_player3", "position": -1, "status": "dead",
#                             'cards': []}
    
#     #check with get player status 4
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 4})
#     assert data.status_code == 200
#     assert data.json() == {"id": 4, "name": "test_player4", "position": 2, "status": "human",
#                             'cards': [  {'id': 25, 'type': 'Analisis'},
#                                         {'id': 26, 'type': 'Whisky'},
#                                         {'id': 27, 'type': 'Infeccion'},
#                                         {'id': 28, 'type': 'Lanzallamas'}]}
    
#     #check with get player status 5
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
#     assert data.status_code == 200
#     assert data.json() == {"id": 5, "name": "test_player5", "position": 3, "status": "human",
#                             'cards': [  {'id': 21, 'type': 'Sospecha'},
#                                         {'id': 22, 'type': 'CambioDeLugar'},
#                                         {'id': 23, 'type': 'VigilaTusEspaldas'},
#                                         {'id': 24, 'type': 'MasValeQueCorras'}]}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
#                                         {"id": 3, "name": "test_player3", "position": -1, "alive": False}, 
#                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True}, 
#                                         {"id": 5, "name": "test_player5", "position": 3, "alive": True}],
#                             "gameInfo": {"sentido": "derecha",
#                                             "jugadorTurno": 2,
#                                             "faseDelTurno": 3,
#                                             "siguienteJugador": 4}}
    
# #test change card, but player is dead
# @pytest.mark.end2end_test
# def test_change_card_dead(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for change card, but player is dead")

#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 2, "player_to_id": 3, "card_id": 34})
#     assert data.status_code == 400
#     assert data.json() == {"detail": "El jugador 3 está muerto"}

#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 2, "player_to_id": 4, "card_id": 34})
#     assert data.status_code == 200
#     assert data.json() == {'id': 25, 'type': 'Analisis', 'number': 25, 'description': 'Ask for a total of cards'}

# #test play card, Analisis
# @pytest.mark.end2end_test
# def test_play_card_Analisis(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for play card, Analisis")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/4")
#     assert data.status_code == 200
#     assert data.json() == {'id': 18, 'type': 'Infeccion', 'number': 18, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}

#     #play card
#     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 4, "id_player_to": 5, "id_card": 34})
#     assert data.status_code == 200
#     assert data.json() == {'succes': True, 'message': 'Cartas del jugador mostradas', 
#                            'cards': [{'name': 'CambioDeLugar', 'description': 'Change the place physically with a player that you have next to you'}, 
#                                      {'name': 'MasValeQueCorras', 'description': 'Change the place physically with a player'}, 
#                                      {'name': 'Sospecha', 'description': 'Ask for a card'}, 
#                                      {'name': 'VigilaTusEspaldas', 'description': 'Invert the order of the game'}]}

#     #check with get player status 4
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 4})
#     assert data.status_code == 200
#     assert data.json() == {"id": 4, "name": "test_player4", "position": 2, "status": "human",
#                             'cards': [  {'id': 18, 'type': 'Infeccion'},
#                                         {'id': 26, 'type': 'Whisky'},
#                                         {'id': 27, 'type': 'Infeccion'},
#                                         {'id': 28, 'type': 'Lanzallamas'}]}
    
#     #check with get player status 5
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
#     assert data.status_code == 200
#     assert data.json() == {"id": 5, "name": "test_player5", "position": 3, "status": "human",
#                             'cards': [  {'id': 21, 'type': 'Sospecha'},
#                                         {'id': 22, 'type': 'CambioDeLugar'},
#                                         {'id': 23, 'type': 'VigilaTusEspaldas'},
#                                         {'id': 24, 'type': 'MasValeQueCorras'}]}


# # test change card infeccion but player is human
# @pytest.mark.end2end_test
# def test_change_card_infeccion_human(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for change card infeccion but player is human")
    
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 4, "player_to_id": 5, "card_id": 18})
#     assert data.status_code == 400
#     assert data.json() == {"detail": "No se puede intercambiar una carta de infeccion si eres humano"}

#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 4, "player_to_id": 5, "card_id": 26})
#     assert data.status_code == 200
#     assert data.json() == {'id': 21, 'type': 'Sospecha', 'number': 21, 'description': 'Ask for a card'}



#---------------------------- usar Whisky o vigila tus espaldas ----------------------------

# #test play card, vigila tus espaldas
# @pytest.mark.end2end_test
# def test_play_card_vigila_tus_espaldas(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for play card, vigila tus espaldas")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/5")
#     assert data.status_code == 200
#     assert data.json() == {'id': 17, 'type': 'Whisky', 'number': 17, 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}

#     #play card
#     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 5, "id_player_to": 1, "id_card": 23})
#     assert data.status_code == 200
#     assert data.json() == {'succes': True, 'message': 'Carta vigila tus espaldas aplicada'}

#     #check with get player status 5
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
#     assert data.status_code == 200
#     assert data.json() == {'id': 5, 'name': 'test_player5', 'position': 3, 'status': 'human',
#                            'cards': [{'type': 'Whisky', 'id': 17}, 
#                                      {'type': 'CambioDeLugar', 'id': 22}, 
#                                      {'type': 'MasValeQueCorras', 'id': 24}, 
#                                      {'type': 'Whisky', 'id': 26}]}
    
#     #check with game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {'gameStatus': 'INIT',
#                             'name': 'test_game',
#                             'players': [{'id': 1, 'name': 'test_player1', 'position': 0, 'alive': True}, 
#                                         {'id': 2, 'name': 'test_player2', 'position': 1, 'alive': True}, 
#                                         {'id': 3, 'name': 'test_player3', 'position': -1, 'alive': False}, 
#                                         {'id': 4, 'name': 'test_player4', 'position': 2, 'alive': True}, 
#                                         {'id': 5, 'name': 'test_player5', 'position': 3, 'alive': True}],
#                             'gameInfo': {'sentido': 'izquierda', 
#                                          'jugadorTurno': 5, 
#                                          'faseDelTurno': 3,
#                                          'siguienteJugador': 4}}
    
#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 5, "player_to_id": 4, "card_id": 22})
#     assert data.status_code == 200
#     assert data.json() == {'id': 21, 'type': 'Sospecha', 'number': 21, 'description': 'Ask for a card'}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {'gameStatus': 'INIT',
#                             'name': 'test_game',
#                             'players': [{'id': 1, 'name': 'test_player1', 'position': 0, 'alive': True},
#                                         {'id': 2, 'name': 'test_player2', 'position': 1, 'alive': True},
#                                         {'id': 3, 'name': 'test_player3', 'position': -1, 'alive': False},
#                                         {'id': 4, 'name': 'test_player4', 'position': 2, 'alive': True},
#                                         {'id': 5, 'name': 'test_player5', 'position': 3, 'alive': True}],
#                             'gameInfo': {'sentido': 'izquierda',
#                                             'jugadorTurno': 4,
#                                             'faseDelTurno': 1,
#                                             'siguienteJugador': 2}}
    
    
#--------------------------------------- Whisky ------------------------------------------

# #test play card, with no player objetive
# @pytest.mark.end2end_test
# def test_play_card_whisky(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for play card, with no player objetive")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/5")
#     assert data.status_code == 200
#     assert data.json() == {'id': 17, 'type': 'Whisky', 'number': 17, 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}

#     #play card
#     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 5, "id_player_to": 1, "id_card": 26})
#     assert data.status_code == 200
#     assert data.json() == {'succes': True, 'message': 'Cartas del jugador mostradas', 
#                            'cards': [{'name': 'CambioDeLugar', 'description': 'Change the place physically with a player that you have next to you'}, 
#                                      {'name': 'MasValeQueCorras', 'description': 'Change the place physically with a player'}, 
#                                      {'name': 'VigilaTusEspaldas', 'description': 'Invert the order of the game'}, 
#                                      {'name': 'Whisky', 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}, 
#                                      {'name': 'Whisky', 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}]}

#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 5, "player_to_id": 1, "card_id": 22})
#     assert data.status_code == 200
#     assert data.json() == {'id': 33, 'type': 'MasValeQueCorras', 'number': 33, 'description': 'Change the place physically with a player'}

# #test play card cambio de lugar en el sentido de juego
# @pytest.mark.end2end_test
# def test_play_card_cambio_de_lugar(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for play card cambio de lugar en el sentido de juego")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/1")
#     assert data.status_code == 200
#     assert data.json() == {'id': 16, 'type': 'Analisis', 'number': 16, 'description': 'Ask for a total of cards'}

#     #check with get player status 1
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
#     assert data.status_code == 200
#     assert data.json() == {'id': 1, 'name': 'test_player1', 'position': 0, 'status': 'theThing',
#                            'cards': [{'type': 'Analisis', 'id': 16}, 
#                                      {'type': 'CambioDeLugar', 'id': 22}, 
#                                      {'type': 'Empty', 'id': 38}, 
#                                      {'type': 'Sospecha', 'id': 39}, 
#                                      {'type': 'LaCosa', 'id': 40}]}
    
#     #play card
#     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 1, "id_player_to": 2, "id_card": 22})
#     assert data.status_code == 200
#     assert data.json() == {'succes': True, 'message': 'Carta cambio de lugar aplicada'}

#     #check with get player status 1
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
#     assert data.status_code == 200
#     assert data.json() == {'id': 1, 'name': 'test_player1', 'position': 1, 'status': 'theThing',
#                            'cards': [{'type': 'Analisis', 'id': 16},
#                                      {'type': 'Empty', 'id': 38},
#                                      {'type': 'Sospecha', 'id': 39},
#                                      {'type': 'LaCosa', 'id': 40}]}

#     #check with get player status 2
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
#     assert data.status_code == 200
#     assert data.json() == {'id': 2, 'name': 'test_player2', 'position': 0, 'status': 'human',
#                            'cards': [{'type': 'Lanzallamas', 'id': 19}, 
#                                      {'type': 'Analisis', 'id': 25}, 
#                                      {'type': 'Whisky', 'id': 35}, 
#                                      {'type': 'Infeccion', 'id': 36}]}

#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {'gameStatus': 'INIT',
#                            'name': 'test_game',
#                            'players': [{'id': 1, 'name': 'test_player1', 'position': 1, 'alive': True},
#                                        {'id': 2, 'name': 'test_player2', 'position': 0, 'alive': True},
#                                        {'id': 3, 'name': 'test_player3', 'position': -1, 'alive': False},
#                                        {'id': 4, 'name': 'test_player4', 'position': 2, 'alive': True},
#                                        {'id': 5, 'name': 'test_player5', 'position': 3, 'alive': True}],
#                            'gameInfo': {'sentido': 'derecha',
#                                         'jugadorTurno': 1,
#                                         'faseDelTurno': 3,
#                                         'siguienteJugador': 2}}
    
#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 1, "player_to_id": 4, "card_id": 38})
#     assert data.status_code == 200
#     assert data.json() == {'id': 21, 'type': 'Sospecha', 'number': 21, 'description': 'Ask for a card'}

#     #check next player is 2
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {'gameStatus': 'INIT',
#                             'name': 'test_game',
#                             'players': [{'id': 1, 'name': 'test_player1', 'position': 1, 'alive': True},
#                                         {'id': 2, 'name': 'test_player2', 'position': 0, 'alive': True},
#                                         {'id': 3, 'name': 'test_player3', 'position': -1, 'alive': False},
#                                         {'id': 4, 'name': 'test_player4', 'position': 2, 'alive': True},
#                                         {'id': 5, 'name': 'test_player5', 'position': 3, 'alive': True}],
#                             'gameInfo': {'sentido': 'derecha',
#                                          'jugadorTurno': 2,
#                                          'faseDelTurno': 1,
#                                          'siguienteJugador': 1}}
    

#------------------------------------------------------------------------------------------------------------------------
