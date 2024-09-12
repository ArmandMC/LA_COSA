import requests
import pytest

SERVICE_URL = "http://127.0.0.1:8000"

#test the thing finish the game, and it is worng
@pytest.mark.end2end_test
def test_finish_game_1(capsys):
    with capsys.disabled():
            print("\n")
            print("\ttest for finish game, wrong")

    cards_id = []
    for i in range(1, 138):
        cards_id.append(i + 135)

    #create a game
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_2", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 5}
    game_id = data.json()["id"]

    #create gameId
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 13, "admin": True}
    player_1_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 14, "admin": False}
    player_2_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 15, "admin": False}
    player_3_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 16, "admin": False}
    player_4_id = data.json()["playerId"]

    #start game
    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"id": game_id, "cantidad de jugadores": 4, "jugador de turno": player_1_id, "fase de turno": 1, "sentido": True}

    #TRY finish game
    data = requests.post(f"{SERVICE_URL}/game/finish", json={"game_id": game_id, "player_id": player_2_id})
    assert data.status_code == 400
    assert data.json() == {"detail": "Player is not the thing"}

    #finish game
    data = requests.post(f"{SERVICE_URL}/game/finish", json={"game_id": game_id, "player_id": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"message": "Game finished successfully"}

    #check with get game status
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    #check with get game status

    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "FINISH",
                            "name": "test_game_2",
                            "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                            "gameInfo": {"sentido": "derecha",
                                            "obstaculos": [],
                                            "jugadorTurno": player_1_id,
                                            "faseDelTurno": 1,
                                            "siguienteJugador": player_2_id}}

    #check winners
    data = requests.get(f"{SERVICE_URL}/game/{game_id}/winners")
    assert data.status_code == 200
    assert data.json() == {'name': 'test_game_2', 'team': 'Humanos', 
                           'players': [{'id': player_2_id, 'name': 'test_player2', 'role': 'human'}, 
                                       {'id': player_3_id, 'name': 'test_player3', 'role': 'human'}, 
                                       {'id': player_4_id, 'name': 'test_player4', 'role': 'human'}]}
    
    #delete game
    data = requests.delete(f"{SERVICE_URL}/game/{game_id}")
    assert data.status_code == 200
    assert data.json() == {"message": "Game deleted successfully"}
    
#test finish game, humans kill the thing
@pytest.mark.end2end_test
def test_finish_game_2(capsys):
    with capsys.disabled():
            print("\n")
            print("\ttest for finish game, humans kill the thing")

    cards_id = []
    for i in range(1, 138):
        cards_id.append(i + 407)

    #create a game
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_3", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 6}
    game_id = data.json()["id"]

    #create gameId
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 17, "admin": True}
    player_1_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 18, "admin": False}
    player_2_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 19, "admin": False}
    player_3_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 20, "admin": False}
    player_4_id = data.json()["playerId"]

    #start game
    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"id": game_id, "cantidad de jugadores": 4, "jugador de turno": player_1_id, "fase de turno": 1, "sentido": True}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[120], 'type': 'PuertaAtrancada', 'number': 120, 'description': "You can't exchange cards with any player for 2 turns"}

    #discard card player 1
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[120]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[129]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[119], 'type': 'Cuarentena', 'number': 119, 'description': 'You are in quarantine for 2 turns'}

    #play card
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_2_id, "id_player_to": player_1_id, "id_card": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}
                                       
    #check with get player status 1
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200
    assert data.json() ==  {'id': player_1_id, 'name': 'test_player1', 'position': -1, 'status': 'dead', 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': []}
    
    #check with get game status
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "FINISH",
                            "name": "test_game_3",
                            "players": [{"id": player_1_id, "name": "test_player1", "position": -1, "alive": False, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_3_id, "name": "test_player3", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                            "gameInfo": {"sentido": "derecha",
                                            "obstaculos": [],
                                            "jugadorTurno": player_2_id,
                                            "faseDelTurno": 3,
                                            "siguienteJugador": player_3_id}}
    
    #check winners
    data = requests.get(f"{SERVICE_URL}/game/{game_id}/winners")
    assert data.status_code == 200
    assert data.json() == {'name': 'test_game_3', 'team': 'Humanos',
                            'players': [{'id': player_2_id, 'name': 'test_player2', 'role': 'human'},
                                        {'id': player_3_id, 'name': 'test_player3', 'role': 'human'},
                                        {'id': player_4_id, 'name': 'test_player4', 'role': 'human'}]}
    
    #delete game
    data = requests.delete(f"{SERVICE_URL}/game/{game_id}")
    assert data.status_code == 200
    assert data.json() == {"message": "Game deleted successfully"}

#test finish game, the thing and infected kill the humans
@pytest.mark.end2end_test
def test_finish_game_3(capsys):
    with capsys.disabled():
            print("\n")
            print("\ttest for finish game, the thing and infected kill the humans")

    cards_id = []
    for i in range(1, 138):
        cards_id.append(i + 543)

    #create a game
    data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_4", "min_players": 4, "max_players": 5, "has_password": False})
    assert data.status_code == 201
    assert data.json() == {"id": 7}
    game_id = data.json()["id"]

    #create gameId
    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 21, "admin": True}
    player_1_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 22, "admin": False}
    player_2_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 23, "admin": False}
    player_3_id = data.json()["playerId"]

    data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
    assert data.status_code == 200
    assert data.json() == {"playerId": 24, "admin": False}
    player_4_id = data.json()["playerId"]

    #start game
    data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
    assert data.status_code == 200

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() ==  {'id': cards_id[120], 'type': 'PuertaAtrancada', 'number': 120, 'description': "You can't exchange cards with any player for 2 turns"}

    #play card
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_4_id, "id_card": cards_id[135]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[134]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[132]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[119], 'type': 'Cuarentena', 'number': 119, 'description': 'You are in quarantine for 2 turns'}
    
    #discard card player 2
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[119]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[128]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[118], 'type': 'Carta3,4', 'number': 118, 'description': 'solo para tests'}
    
    #discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[118]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[133]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[117], 'type': 'Carta1,2', 'number': 117, 'description': 'solo para tests'}

    #discard card player 1
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[117]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[130]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[116], 'type': 'Olvidadizo', 'number': 116, 'description': 'solo para tests'}
    
    #discard card player 2
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[116]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[127]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[115], 'type': 'PodemosSerAmigos?', 'number': 115, 'description': 'solo para tests'}
    
    #discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[115]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[132]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[114], 'type': 'RondaYRonda', 'number': 114, 'description': 'solo para tests'}

    #discard card player 1
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[114]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[129]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

    #discard card player 2
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[113]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[126]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[112], 'type': 'Oops!', 'number': 112, 'description': 'Muestrales todas las cartas de tu mano a todos los jugadores'}

    #discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[112]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[130]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[111], 'type': 'CitaACiegas', 'number': 111, 'description':  "Intercambia una carta de tu mano con la primera carta del mazo,descartando cualquier carta de 'panico' robada. Tu turno termina"}

    #discard card player 1
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[111]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[128]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 2
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[110], 'type': 'Revelaciones', 'number': 110, 'description': "Empezando por ti, y siguiendo el orden del juego,cada jugador elige si revela o no su mano.La ronda de 'revelaciones' termina cuando un jugador muestre una carta, 'infeccion',sin que tenga que revelar el resto de su mano"}

    #discard card player 2
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[110]}")
    assert data.status_code == 200

    #change card player 2
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[131]})
    assert data.status_code == 200

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[133]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 3
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[109], 'type': 'SoloEntreNosotros', 'number': 109, 'description': 'Muestra todas las cartas de tu mano a un jugador adyacente de tu eleccion'}

    #discard card player 3
    data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_3_id}/{cards_id[109]}")
    assert data.status_code == 200
    assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

    #change card player 3
    data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id": cards_id[131]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "solicitude sent"}

    #change card player 1
    data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[129]})
    assert data.status_code == 200
    assert data.json() == {"exchange": "succes"}

    #draw card player 1
    data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
    assert data.status_code == 200
    assert data.json() == {'id': cards_id[108], 'type': 'Lanzallamas', 'number': 108, 'description': 'Kill player'}

    #TRY play card
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_4_id, "id_card": cards_id[108]})
    assert data.status_code == 400
    assert data.json() ==  {'detail': f'El jugador {player_4_id} está muerto'}

    #play card
    data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_3_id, "id_card": cards_id[108]})
    assert data.status_code == 200
    assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}

    #check with get player status 3
    data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
    assert data.status_code == 200
    assert data.json() ==  {'id': player_3_id, 'name': 'test_player3', 'position': -1, 'status': 'dead', 'in_quarantine': False, 'quarantine_shifts': 0,
                            'cards': []}
    
    #check with get game status
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "INIT",
                            "name": "test_game_4",
                            "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_3_id, "name": "test_player3", "position": -1, "alive": False, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_4_id, "name": "test_player4", "position": -1, "alive": False, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                            "gameInfo": {"sentido": "derecha",
                                            "obstaculos": [],
                                            "jugadorTurno": player_1_id,
                                            "faseDelTurno": 3,
                                            "siguienteJugador": player_2_id}}
    
    #finish game
    data = requests.post(f"{SERVICE_URL}/game/finish", json={"game_id": game_id, "player_id": player_1_id})
    assert data.status_code == 200
    assert data.json() == {"message": "Game finished successfully"}

    #check with get game status
    data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
    assert data.status_code == 200
    assert data.json() == {"gameStatus": "FINISH",
                            "name": "test_game_4",
                            "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_3_id, "name": "test_player3", "position": -1, "alive": False, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                        {"id": player_4_id, "name": "test_player4", "position": -1, "alive": False, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                            "gameInfo": {"sentido": "derecha",
                                            "obstaculos": [],
                                            "jugadorTurno": player_1_id,
                                            "faseDelTurno": 3,
                                            "siguienteJugador": player_2_id}}
    
    #check winners
    data = requests.get(f"{SERVICE_URL}/game/{game_id}/winners")
    assert data.status_code == 200
    assert data.json() == {'name': 'test_game_4', 'team': 'La Cosa y los infectados',
                            'players': [{'id': player_1_id, 'name': 'test_player1', 'role': 'theThing'},
                                        {'id': player_2_id, 'name': 'test_player2', 'role': 'infected'}]}
    
    #delete game
    data = requests.delete(f"{SERVICE_URL}/game/{game_id}")
    assert data.status_code == 200
    assert data.json() == {"message": "Game deleted successfully"}