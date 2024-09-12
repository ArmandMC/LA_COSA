import requests
import pytest

SERVICE_URL = "http://127.0.0.1:8000"

#test draw card, discad card theThing, discard card, change card infectado
@pytest.mark.end2end_test
def test_integral_1(capsys):
   with capsys.disabled():
      print("\n")
      print("\tIntegral test: draw card, discad card theThing, play card sospecha to right, change card infectado")
   cards_id = []
   for i in range(1, 138):
      cards_id.append(i + 135)

   #create a game
   data = requests.post(f"{SERVICE_URL}/game/", json={"name": "test_game_1", "min_players": 4, "max_players": 5, "has_password": False})
   assert data.status_code == 201
   assert data.json() == {"id": 4}
   game_id = data.json()["id"]

   #create gameId
   data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player1", "gameId": game_id})
   assert data.status_code == 200
   assert data.json() == {"playerId": 9, "admin": True}
   player_1_id = data.json()["playerId"]

   data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player2", "gameId": game_id})
   assert data.status_code == 200
   assert data.json() == {"playerId": 10, "admin": False}
   player_2_id = data.json()["playerId"]

   data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player3", "gameId": game_id})
   assert data.status_code == 200
   assert data.json() == {"playerId": 11, "admin": False}
   player_3_id = data.json()["playerId"]

   data = requests.post(f"{SERVICE_URL}/player/join", json={"name": "test_player4", "gameId": game_id})
   assert data.status_code == 200
   assert data.json() == {"playerId": 12, "admin": False}
   player_4_id = data.json()["playerId"]

   #start game
   data = requests.post(f"{SERVICE_URL}/game/start", json={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": game_id, "cantidad de jugadores": 4, "jugador de turno": player_1_id, "fase de turno": 1, "sentido": True}

   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
   assert data.status_code == 200
   assert data.json() ==  {'id': cards_id[120], 'type': 'PuertaAtrancada', 'number': 120, 'description': "You can't exchange cards with any player for 2 turns"}

   #check with get player status
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {'id': player_1_id, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'PuertaAtrancada', 'id': cards_id[120]},
                                    {'type': 'Whisky', 'id': cards_id[133]}, 
                                    {'type': 'Infeccion', 'id': cards_id[134]}, 
                                    {'type': 'Lanzallamas', 'id': cards_id[135]}, 
                                    {'type': 'LaCosa', 'id': cards_id[136]}]}

   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                          "obstaculos": [],
                                          "jugadorTurno": player_1_id,
                                          "faseDelTurno": 2,
                                          "siguienteJugador": player_2_id}}
   
   #-----------------------------------
   #test discard card, LaCosa
   data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[136]}")
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede descartar la carta de la cosa'}

   #------------------------------------
   #test discard card
   data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_1_id}/{cards_id[120]}")
   assert data.status_code == 200
   assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

   #check with get player status
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 0, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [{'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'Infeccion', 'id': cards_id[134]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}

   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha", 
                                       "obstaculos": [],
                                       "jugadorTurno": player_1_id, 
                                       "faseDelTurno": 3,
                                       "siguienteJugador": player_2_id}}
   

   #------------------------------------
   #test change card, infectado
   
   #change card player 1
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[134]})
   assert data.status_code == 200
   assert data.json() == {"exchange": "solicitude sent"}
   
   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[129]})
   assert data.status_code == 200
   assert data.json() == {"exchange": "succes"}


   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 0, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'CambioDeLugar', 'id': cards_id[129]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'VigilaTusEspaldas', 'id': cards_id[130]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Analisis', 'id': cards_id[132]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                       "obstaculos": [],
                                          "jugadorTurno": player_2_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_3_id}}
   
   #------------------------------------
   #test play card, analisis

   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[119], 'type': 'Cuarentena', 'number': 119, 'description': 'You are in quarantine for 2 turns'}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'VigilaTusEspaldas', 'id': cards_id[130]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Analisis', 'id': cards_id[132]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_2_id, "id_player_to": player_1_id, "id_card": cards_id[132]})
   assert data.status_code == 200
   assert data.json() == {'succes': True, 'message': 'Cartas del jugador mostradas',
                           'cards': [{'name': 'CambioDeLugar','description': 'Change the place physically with a player that you have next to you'},
                                       {'name': 'LaCosa', 'description': 'Tu eres LA COSA'},
                                       {'name': 'Lanzallamas', 'description': 'Kill player'},
                                       {'name': 'Whisky', 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}]}
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'VigilaTusEspaldas', 'id': cards_id[130]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                       "obstaculos": [],
                                          "jugadorTurno": player_2_id,
                                          "faseDelTurno": 3,
                                          "siguienteJugador": player_3_id}}
   
   #------------------------------------
   #test change card, Infeccion

   #try to change card Infeccion
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[134]})
   assert data.status_code == 400
   assert data.json() == {"detail": "No se puede intercambiar la unica carta de infeccion que tiene"}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'VigilaTusEspaldas', 'id': cards_id[130]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}

   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]},
                                       {'type': 'Sospecha', 'id': cards_id[128]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                       "obstaculos": [],
                                          "jugadorTurno": player_2_id,
                                          "faseDelTurno": 3,
                                          "siguienteJugador": player_3_id}}
   
   #------------------------------------
   #test play card, vigila tus espaldas

   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id": cards_id[130]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 3
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_3_id, "card_id2": cards_id[125]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]},
                                       {'type': 'Sospecha', 'id': cards_id[128]},
                                       {'type': 'VigilaTusEspaldas', 'id': cards_id[130]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "derecha",
                                       "obstaculos": [],
                                          "jugadorTurno": player_3_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_4_id}}

   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[118],  'type': 'Carta3,4', 'number': 118, 'description': 'solo para tests'}

   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta3,4', 'id': cards_id[118]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]},
                                       {'type': 'Sospecha', 'id': cards_id[128]},
                                       {'type': 'VigilaTusEspaldas', 'id': cards_id[130]}]}
   
   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_3_id, "id_card": cards_id[130]})
   assert data.status_code == 200
   assert data.json() == {'succes': True, 'message': 'Carta vigila tus espaldas aplicada'}

   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta3,4', 'id': cards_id[118]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]},
                                       {'type': 'Sospecha', 'id': cards_id[128]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_3_id,
                                          "faseDelTurno": 3,
                                          "siguienteJugador": player_2_id}})
   
   #change card player 3
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_3_id, "player_to_id": player_2_id, "card_id": cards_id[128]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_3_id, "player_to_id": player_2_id, "card_id2": cards_id[119]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta3,4', 'id': cards_id[118]},
                                       {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]}]}
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'Sospecha', 'id': cards_id[128]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_2_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_1_id}})

   #------------------------------------
   #test play card, sospecha

   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[117], 'type': 'Carta1,2', 'number': 117, 'description': 'solo para tests'}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'Sospecha', 'id': cards_id[128]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}

   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_2_id, "id_player_to": player_1_id, "id_card": cards_id[128]})
   assert data.status_code == 200
   assert (data.json() == {'succes': True, 'message': 'Carta del jugador mostrada', 
                           'card': {'id': cards_id[136], 'name': 'LaCosa', 'description': 'Tu eres LA COSA'}}) or (
         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
                           'card': {'id': cards_id[135], 'name': 'Lanzallamas', 'description': 'Kill player'}}) or (
         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
                           'card': {'id': cards_id[133], 'name': 'Whisky', 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}}) or (
         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
                           'card': {'id': cards_id[129], 'name': 'CambioDeLugar', 'description': 'Change the place physically with a player that you have next to you'}})
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #------------------------------------
   #test play card, mas vale que corras en sentido contrario al de la ronda

   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_1_id, "card_id": cards_id[131]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 1
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_1_id, "card_id2": cards_id[129]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'CambioDeLugar', 'id': cards_id[129]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 0, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'MasValeQueCorras', 'id': cards_id[131]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_1_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[116], 'type': 'Olvidadizo', 'number': 116, 'description': 'solo para tests'}

   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[131]})
   assert data.status_code == 200
   assert data.json() == {'message': 'se esta esperando la respuesta del jugador 2'}

   #------------------------
   #TRY play card again
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se le jugo la carta al jugador que se debia jugar'}

   #TRY change in play
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #TRY change in play 2
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'Se esta esperando la respuesta del jugador'}

   #------------------------

   #RESPONSE from player 2
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_1_id, "id_player_to": player_2_id, "id_card_2": -1, "defense": False})
   assert data.status_code == 200
   assert data.json() == {'message': 'El jugador no se defendio'}

   #------------------------
   #TRY RESPONSE from player 2 again
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_1_id, "id_player_to": player_2_id, "id_card_2": -1, "defense": False})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   #TRY change in play
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #TRY change in play 2
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #------------------------

   #play card again
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[131]})
   assert data.status_code == 200
   assert data.json() == {'succes': True, 'message': 'Carta mas vale que corras aplicada'}

   #------------------------
   #TRY play card again
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[131]})
   assert data.status_code == 403
   assert data.json() == {'detail': 'It is not the phase of the turn'}

   #TRY RESPONSE from player 2 again
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_1_id, "id_player_to": player_2_id, "id_card_2": -1, "defense": False})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   #TRY change in play
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #TRY change in play 2
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[131]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #------------------------

   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 1, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Olvidadizo', 'id': cards_id[116]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 0, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'CambioDeLugar', 'id': cards_id[129]},
                                       {'type': 'Infeccion', 'id': cards_id[134]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_1_id,
                                          "faseDelTurno": 3,
                                          "siguienteJugador": player_2_id}})
   
   #change card player 1
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id": cards_id[135]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_1_id, "player_to_id": player_2_id, "card_id2": cards_id[117]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 1, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Olvidadizo', 'id': cards_id[116]},
                                       {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 0, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'CambioDeLugar', 'id': cards_id[129]},
                                       {'type': 'Infeccion', 'id': cards_id[134]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_2_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_4_id}})
   
   #------------------------------------
   #test descartar carta de infectado                            

   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_2_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[115], 'type': 'PodemosSerAmigos?', 'number': 115, 'description': 'solo para tests'}

   #discard card
   data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[134]}")
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede descartar la unica carta de infeccion que tiene'}

   #discard card
   data = requests.post(f"{SERVICE_URL}/card/discard_card/{player_2_id}/{cards_id[115]}")
   assert data.status_code == 200
   assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

   #change card player 2
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_2_id, "player_to_id": player_4_id, "card_id": cards_id[129]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 4
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_2_id, "player_to_id": player_4_id, "card_id2": cards_id[121]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 2
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 0, "status": "infected", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Hacha', 'id': cards_id[121]},
                                       {'type': 'AquíEstoyBien', 'id': cards_id[125]},
                                       {'type': 'Infeccion', 'id': cards_id[134]},
                                       {'type': 'Lanzallamas', 'id': cards_id[135]}]}
   
   #check with get player status 4
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Aterrador', 'id': cards_id[122]},
                                       {'type': 'NoGracias', 'id': cards_id[123]},
                                       {'type': 'Fallaste', 'id': cards_id[124]},
                                       {'type': 'CambioDeLugar', 'id': cards_id[129]},]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_4_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_3_id}})
   
   #------------------------------------
   #test play card, cambio de lugar en el sentido de la ronda
   
   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_4_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[114], 'type': 'RondaYRonda', 'number': 114, 'description': 'solo para tests'}

   #----------------

   #TRY response from player 3
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_4_id, "id_player_to": player_3_id, "id_card_2": cards_id[126], "defense": True})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   #TRY change card in play player 4
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_4_id, "player_to_id": player_3_id, "card_id": cards_id[124]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #TRY change card in play player 3
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_4_id, "player_to_id": player_3_id, "card_id2": cards_id[126]})
   assert data.status_code == 400
   assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   #----------------

   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_4_id, "id_player_to": player_3_id, "id_card": cards_id[129]})
   assert data.status_code == 200
   assert data.json() == {'succes': True, 'message': 'Carta cambio de lugar aplicada'}

   #----------------

   #TRY response from player 3
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_4_id, "id_player_to": player_3_id, "id_card_2": cards_id[126], "defense": True})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   #TRY change card in play player 4
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_4_id, "player_to_id": player_3_id, "card_id": cards_id[124]})
   assert data.status_code == 400
   assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   #TRY change card in play player 3
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_4_id, "player_to_id": player_3_id, "card_id2": cards_id[126]})
   assert data.status_code == 400
   assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   #----------------

   #check with get player status 4
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'RondaYRonda', 'id': cards_id[114]},
                                       {'type': 'Aterrador', 'id': cards_id[122]},
                                       {'type': 'NoGracias', 'id': cards_id[123]},
                                       {'type': 'Fallaste', 'id': cards_id[124]}]}
   
   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta3,4', 'id': cards_id[118]},
                                       {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]},
                                       {'type': 'Seduccion', 'id': cards_id[127]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_4_id,
                                          "faseDelTurno": 3,
                                          "siguienteJugador": player_3_id}})
   
   #change card player 4
   data = requests.post(f"{SERVICE_URL}/card/change1", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id": cards_id[114]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'solicitude sent'}

   #change card player 1
   data = requests.post(f"{SERVICE_URL}/card/change2", json={"player_id": player_4_id, "player_to_id": player_1_id, "card_id2": cards_id[116]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 4
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Olvidadizo', 'id': cards_id[116]},
                                       {'type': 'Aterrador', 'id': cards_id[122]},
                                       {'type': 'NoGracias', 'id': cards_id[123]},
                                       {'type': 'Fallaste', 'id': cards_id[124]}]}
   
   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 1, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'RondaYRonda', 'id': cards_id[114]},
                                       {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_3_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_4_id}})
   
   # #------------------------------------
   # #test play card, seduccion

   # #draw card
   # data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   # assert data.status_code == 200
   # assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

   # #play card
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_1_id, "id_card": cards_id[127]})
   # assert data.status_code == 200
   # assert data.json() == {'succes': True, 'message': 'Carta seduccion aplicada'}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_3_id,
   #                                        "faseDelTurno": 2,
   #                                        "siguienteJugador": player_4_id}})

   # #change card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id": cards_id[113]})
   # assert data.status_code == 200
   # assert data.json() ==  {'exchange': 'solicitude sent'}

   # #change card in play player 1
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[117]})
   # assert data.status_code == 200
   # assert data.json() ==  {'exchange': 'succes'}

   # #check with get player status 3
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
   #                                     {'type': 'Carta3,4', 'id': cards_id[118]},
   #                                     {'type': 'Cuarentena', 'id': cards_id[119]},
   #                                     {'type': 'NadaDeBarbacoas', 'id': cards_id[126]}]}

   # #check with get player status 1
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 1, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'CadenasPodridas', 'id': cards_id[113]},
   #                                     {'type': 'RondaYRonda', 'id': cards_id[114]},
   #                                     {'type': 'Whisky', 'id': cards_id[133]},
   #                                     {'type': 'LaCosa', 'id': cards_id[136]}]}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_4_id,
   #                                        "faseDelTurno": 1,
   #                                        "siguienteJugador": player_1_id}})

   # #------------------------------------
   # #test play card, seduccion y el jugador no se defiende

   # #draw card
   # data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   # assert data.status_code == 200
   # assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

   # #play card
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 200
   # assert data.json() == {'succes': True, 'message': 'Carta seduccion aplicada'}

   # #----------------
   
   # #TRY play card player 3
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'El jugador no tiene la carta'}

   # #TRY response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[123]})
   # assert data.status_code == 404
   # assert data.json() ==  {'detail': 'Carta no encontrada'}

   # #----------------

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_3_id,
   #                                        "faseDelTurno": 2,
   #                                        "siguienteJugador": player_4_id}})

   # #CHANGE card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 200
   # assert data.json() ==  {'message': f'se esta esperando la respuesta del jugador'}


   # #----------------
   # #TRY change card in play player 3 again
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': f'Se esta esperando la respuesta del jugador'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[116]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': f'Se esta esperando la respuesta del jugador'}

   # #TRY play card player 3
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'El jugador no tiene la carta'}

   # #----------------

   # #RESPONSE from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": False})
   # assert data.status_code == 200
   # assert data.json() == {'message': 'El jugador no se defendio'}

   # #----------------

   # #TRY response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   # #TRY play card player 3
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'El jugador no tiene la carta'}

   # #TRY change card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'No se puede hacer esto en este momento'}

   # #----------------

   # #CHANGE card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[123]})
   # assert data.status_code == 200
   # assert data.json() ==  {'exchange': 'succes'}

   # #----------------
   
   # #TRY play card player 3
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 403
   # assert data.json() == {'detail': 'It is not your turn'}

   # #TRY response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   # #TRY change card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[123]})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'No se esta cambiando con el jugador correcto'}

   # #----------------
   

   # #check with get player status 3
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'Carta3,4', 'id': cards_id[118]},
   #                                     {'type': 'Cuarentena', 'id': cards_id[119]},
   #                                     {'type': 'NoGracias', 'id': cards_id[123]},
   #                                     {'type': 'NadaDeBarbacoas', 'id': cards_id[126]}]}

   # #check with get player status 4
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'CadenasPodridas', 'id': cards_id[113]},
   #                                     {'type': 'Olvidadizo', 'id': cards_id[116]},
   #                                     {'type': 'Aterrador', 'id': cards_id[122]},
   #                                     {'type': 'Fallaste', 'id': cards_id[124]}]}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_4_id,
   #                                        "faseDelTurno": 1,
   #                                        "siguienteJugador": player_1_id}})
   

   # #------------------------------------
   # #test play card, seduccion y el jugador se defiende con no gracias

   # #draw card
   # data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   # assert data.status_code == 200
   # assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

   # #play card
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 200
   # assert data.json() == {'succes': True, 'message': 'Carta seduccion aplicada'}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_3_id,
   #                                        "faseDelTurno": 2,
   #                                        "siguienteJugador": player_4_id}})

   # #change card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 200
   # assert data.json() ==  {'message': 'se esta esperando la respuesta del jugador'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[116]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'Se esta esperando la respuesta del jugador'}

   # #response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
   # assert data.status_code == 200
   # assert data.json() == {'succes': True, 'message': 'Carta no gracias aplicada'}

   # #TRY change card in play player 1
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[117]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   # #TRY response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[123], "defense": True})
   # assert data.status_code == 400
   # assert data.json() == {'detail': 'No se puede jugar una carta de defensa en este momento'}

   # #check with get player status 3
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'CadenasPodridas', 'id': cards_id[113]},
   #                                     {'type': 'Carta3,4', 'id': cards_id[118]},
   #                                     {'type': 'Cuarentena', 'id': cards_id[119]},
   #                                     {'type': 'NadaDeBarbacoas', 'id': cards_id[126]}]}

   # #check with get player status 4
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'Oops!', 'id': cards_id[112]},
   #                                     {'type': 'Olvidadizo', 'id': cards_id[116]},
   #                                     {'type': 'Aterrador', 'id': cards_id[122]},
   #                                     {'type': 'Fallaste', 'id': cards_id[124]}]}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_4_id,
   #                                        "faseDelTurno": 1,
   #                                        "siguienteJugador": player_1_id}})
   

   # #------------------------------------
   # #test play card, seduccion a jugador que se defiende con aterrador

   # #draw card
   # data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   # assert data.status_code == 200
   # assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

   # #play card
   # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   # assert data.status_code == 200
   # assert data.json() == {'succes': True, 'message': 'Carta seduccion aplicada'}

   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_3_id,
   #                                        "faseDelTurno": 2,
   #                                        "siguienteJugador": player_4_id}})

   # #change card in play player 3
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   # assert data.status_code == 200
   # assert data.json() ==  {'message': 'se esta esperando la respuesta del jugador'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[114]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'Se esta esperando la respuesta del jugador'}

   # #response from player 4
   # data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[122], "defense": True})
   # assert data.status_code == 200
   # assert data.json() ==  {'succes': True, 'message': 'Carta aterrador aplicada', 'card': {'card': 'CadenasPodridas', 'description': 'solo para tests'}}

   # #TRY change card in play player 2
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_2_id, "card_id2": cards_id[121]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   # #TRY change card in play player 4
   # data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[114]})
   # assert data.status_code == 400
   # assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   # #check with get player status 3
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'CadenasPodridas', 'id': cards_id[113]},
   #                                     {'type': 'Carta3,4', 'id': cards_id[118]},
   #                                     {'type': 'Cuarentena', 'id': cards_id[119]},
   #                                     {'type': 'NadaDeBarbacoas', 'id': cards_id[126]}]}

   # #check with get player status 4
   # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   # assert data.status_code == 200
   # assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
   #                         'cards': [  {'type': 'Oops!', 'id': cards_id[112]},
   #                                     {'type': 'Olvidadizo', 'id': cards_id[116]},
   #                                     {'type': 'NoGracias', 'id': cards_id[123]},
   #                                     {'type': 'Fallaste', 'id': cards_id[124]}]}
   
   # #check with get game status
   # data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   # assert data.status_code == 200
   # assert (data.json() == {"gameStatus": "INIT",
   #                         "name": "test_game_1",
   #                         "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
   #                                     {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
   #                         "gameInfo": {"sentido": "izquierda",
   #                                     "obstaculos": [],
   #                                        "jugadorTurno": player_4_id,
   #                                        "faseDelTurno": 1,
   #                                        "siguienteJugador": player_1_id}})

   #------------------------------------
   #test play card, seduccion a jugador que se defiende con fallaste y el siguiente jugador no tiene para defenderse

   #draw card
   data = requests.post(f"{SERVICE_URL}/card/steal_card/{player_3_id}")
   assert data.status_code == 200
   assert data.json() == {'id': cards_id[113], 'type': 'CadenasPodridas', 'number': 113, 'description': 'solo para tests'}

   #play card
   data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_3_id, "id_player_to": player_4_id, "id_card": cards_id[127]})
   assert data.status_code == 200
   assert data.json() == {'succes': True, 'message': 'Carta seduccion aplicada'}

   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_3_id,
                                          "faseDelTurno": 2,
                                          "siguienteJugador": player_4_id}})

   #change card in play player 3
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_1", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id": cards_id[113]})
   assert data.status_code == 200
   assert data.json() ==  {'message': 'se esta esperando la respuesta del jugador'}

   #TRY change card in play player 4
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_4_id, "card_id2": cards_id[116]})
   assert data.status_code == 400
   assert data.json() ==  {'detail': 'Se esta esperando la respuesta del jugador'}

   #response from player 4
   data = requests.post(f"{SERVICE_URL}/card/play_card2", json={"id_player": player_3_id, "id_player_to": player_4_id, "id_card_2": cards_id[124], "defense": True})
   assert data.status_code == 200
   assert data.json() ==  {'succes': True, 'message': 'Carta fallaste aplicada', 'next_player': player_1_id}

   #TRY change card in play player 2
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_2_id, "card_id2": cards_id[121]})
   assert data.status_code == 400
   assert data.json() ==  {'detail': 'No se esta cambiando con el jugador correcto'}

   #cambiar carta en juego player 1
   data = requests.post(f"{SERVICE_URL}/card/change_in_play_2", json={"player_id": player_3_id, "player_to_id": player_1_id, "card_id2": cards_id[117]})
   assert data.status_code == 200
   assert data.json() ==  {'exchange': 'succes'}

   #check with get player status 3
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_3_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_3_id, "name": "test_player3", "position": 3, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Carta1,2', 'id': cards_id[117]},
                                       {'type': 'Carta3,4', 'id': cards_id[118]},
                                       {'type': 'Cuarentena', 'id': cards_id[119]},
                                       {'type': 'NadaDeBarbacoas', 'id': cards_id[126]}]}

   #check with get player status 4
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_4_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_4_id, "name": "test_player4", "position": 2, "status": "human", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'Oops!', 'id': cards_id[112]},
                                       {'type': 'Olvidadizo', 'id': cards_id[116]},
                                       {'type': 'Aterrador', 'id': cards_id[122]},
                                       {'type': 'NoGracias', 'id': cards_id[123]}]}
   
   #check with get player status 1
   data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
   assert data.status_code == 200
   assert data.json() == {"id": player_1_id, "name": "test_player1", "position": 1, "status": "theThing", 'in_quarantine': False, 'quarantine_shifts': 0,
                           'cards': [  {'type': 'CadenasPodridas', 'id': cards_id[113]},
                                       {'type': 'RondaYRonda', 'id': cards_id[114]},
                                       {'type': 'Whisky', 'id': cards_id[133]},
                                       {'type': 'LaCosa', 'id': cards_id[136]}]}
   
   #check with get game status
   data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": game_id})
   assert data.status_code == 200
   assert (data.json() == {"gameStatus": "INIT",
                           "name": "test_game_1",
                           "players": [{"id": player_1_id, "name": "test_player1", "position": 1, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_2_id, "name": "test_player2", "position": 0, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_3_id, "name": "test_player3", "position": 3, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False},
                                       {"id": player_4_id, "name": "test_player4", "position": 2, "alive": True, 'obstaculo_derecha': False, 'obstaculo_izquierda': False}],
                           "gameInfo": {"sentido": "izquierda",
                                       "obstaculos": [],
                                          "jugadorTurno": player_4_id,
                                          "faseDelTurno": 1,
                                          "siguienteJugador": player_1_id}})