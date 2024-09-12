
# #---------------------------------------------------descartar carta y intercambiar: player 1---------------------------------------------------------

# #test discard card
# @pytest.mark.end2end_test
# def test_discard_card_1(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for discard card, empty")

#     data = requests.post(f"{SERVICE_URL}/card/discard_card/1/20")
#     assert data.status_code == 200
#     assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

#     #check with get player status
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
#     assert data.status_code == 200
#     assert data.json() == {"id": 1, "name": "test_player1", "position": 0, "status": "theThing",
#                             'cards': [{'id': 37, 'type': 'Lanzallamas'},
#                                         {'id': 38, 'type': 'Empty'},
#                                         {'id': 39, 'type': 'Sospecha'},
#                                         {'id': 40, 'type': 'LaCosa'}]}

#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}], 
#                             "gameInfo": {"sentido": "derecha", 
#                                             "jugadorTurno": 1, 
#                                             "faseDelTurno": 3,
#                                             "siguienteJugador": 2}}

# #test change card, but player is not next
# @pytest.mark.end2end_test
# def test_change_card_not_next(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for change card, but player is not next")

#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 1, "player_to_id": 3, "card_id": 38})
#     assert data.status_code == 400
#     assert data.json() == {"detail": "El jugador con el que se quiere intercambiar no es el siguiente jugador"}

# #test change card
# @pytest.mark.end2end_test
# def test_change_card(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for change card")
    
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 1, "player_to_id": 2, "card_id": 38})
#     assert data.status_code == 200
#     assert data.json() == {'id': 33, 'type': 'MasValeQueCorras', 'number': 33, 'description': 'Change the place physically with a player'}

#     #check with get player status 1
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
#     assert data.status_code == 200
#     assert data.json() == {"id": 1, "name": "test_player1", "position": 0, "status": "theThing",
#                             'cards': [{'id': 33, 'type': 'MasValeQueCorras'},
#                                         {'id': 37, 'type': 'Lanzallamas'},
#                                         {'id': 39, 'type': 'Sospecha'},
#                                         {'id': 40, 'type': 'LaCosa'}]}
    
#     #check with get player status 2
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
#     assert data.status_code == 200
#     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
#                             'cards': [  {'id': 34, 'type': 'Analisis'},
#                                         {'id': 35, 'type': 'Whisky'},
#                                         {'id': 36, 'type': 'Infeccion'},
#                                         {'id': 38, 'type': 'Empty'}]}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() == {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
#                             "gameInfo": {"sentido": "derecha",
#                                             "jugadorTurno": 2,
#                                             "faseDelTurno": 1,
#                                             "siguienteJugador": 3}}


# #---------------------------------------------------Sospecha---------------------------------------------------------

    # #test play card, sospecha to right

    # data = requests.post(f"{SERVICE_URL}/card/play_card1", json={"id_game": game_id, "id_player": player_1_id, "id_player_to": player_2_id, "id_card": cards_id[25]})
    # assert data.status_code == 200
    # assert (data.json() == {'succes': True, 'message': 'Carta del jugador mostrada', 
    #                         'card': {'id': cards_id[37], 'name': 'Analisis', 'description': 'Ask for a total of cards'}}) or (
    #         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
    #                         'card': {'id': cards_id[36], 'name': 'MasValeQueCorras', 'description': 'Change the place physically with a player'}}) or (
    #         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
    #                         'card': {'id': cards_id[35], 'name': 'VigilaTusEspaldas', 'description': 'Invert the order of the game'}}) or (
    #         data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
    #                         'card': {'id': cards_id[34], 'name': 'CambioDeLugar', 'description': 'Change the place physically with a player that you have next to you'}})

                                     
    # #check with get player status 1
    # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_1_id})
    # assert data.status_code == 200
    # assert data.json() ==  {'id': player_1_id, 'name': 'test_player1', 'position': 0, 'status': 'theThing',
    #                         'cards': [{'type': 'Whisky', 'id': cards_id[38]},
    #                                     {'type': 'Infeccion', 'id': cards_id[39]},
    #                                     {'type': 'Lanzallamas', 'id': cards_id[40]},
    #                                     {'type': 'LaCosa', 'id': cards_id[41]}]}
    
    # #check with get player status 2
    # data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": game_id, "id_player": player_2_id})
    # assert data.status_code == 200
    # assert data.json() == {"id": player_2_id, "name": "test_player2", "position": 1, "status": "human",
    #                         'cards': [{'type': 'CambioDeLugar', 'id': cards_id[34]},
    #                                     {'type': 'VigilaTusEspaldas', 'id': cards_id[35]},
    #                                     {'type': 'MasValeQueCorras', 'id': cards_id[36]},
    #                                     {'type': 'Analisis', 'id': cards_id[37]}]}
    
    
# #                                    -------------------------------------

# # #test play card, sospecha to left
# # @pytest.mark.end2end_test
# # def test_play_card_sospecha_left(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, sospecha to left")

# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 1, "id_player_to": 5, "id_card": 39})
# #     assert data.status_code == 200
# #     assert (data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
# #                             'card': {'id': 21, 'name': 'Sospecha', 'description': 'Ask for a card'}}) or (
# #             data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
# #                             'card': {'id': 22, 'name': 'CambioDeLugar', 'description': 'Change the place physically with a player'}}) or (
# #             data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
# #                             'card': {'id': 23, 'name': 'VigilaTusEspaldas', 'description':  'Invert the order of the game'}}) or (
# #             data.json() == {'succes': True, 'message': 'Carta del jugador mostrada',
# #                             'card': {'id': 24, 'name': 'MasValeQueCorras', 'description': 'Change the place physically with a player'}})
    

# #     #check with get player status 1
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {'id': 1, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 
# #                             'cards': [{'type': 'Empty', 'id': 20}, 
# #                                       {'type': 'Lanzallamas', 'id': 37}, 
# #                                       {'type': 'Empty', 'id': 38}, 
# #                                       {'type': 'LaCosa', 'id': 40}]}
    
# #     #check with get player status 5
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 5, 'name': 'test_player5', 'position': 4, 'status': 'human', 
# #                            'cards': [{'type': 'Sospecha', 'id': 21}, 
# #                                      {'type': 'CambioDeLugar', 'id': 22}, 
# #                                      {'type': 'VigilaTusEspaldas', 'id': 23}, 
# #                                      {'type': 'MasValeQueCorras', 'id': 24}]}
    


# #---------------------------------------------------lanzallama para la izquierda---------------------------------------------------------

# # #test play card, lanzallamas to left
# # @pytest.mark.end2end_test
# # def test_play_card_lanzallamas_left(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, lanzallamas to left")

# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 1, "id_player_to": 5, "id_card": 37})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}

# #     #check with get player status 1
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 1, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 
# #                            'cards': [{'type': 'Empty', 'id': 20}, 
# #                                      {'type': 'Empty', 'id': 38}, 
# #                                      {'type': 'Sospecha', 'id': 39}, 
# #                                      {'type': 'LaCosa', 'id': 40}]}

# #     #check with get player status 5
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 5, 'name': 'test_player5', 'cards': [], 'position': -1, 'status': 'dead'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
# #                                         {"id": 5, "name": "test_player5", "position": -1, "alive": False}], 
# #                             "gameInfo": {"sentido": "derecha", 
# #                                             "jugadorTurno": 1, 
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 2}}

# #     #change card
# #     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 1, "player_to_id": 2, "card_id": 38})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 33, 'type': 'MasValeQueCorras', 'number': 33, 'description': 'Change the place physically with a player'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
# #                                         {"id": 5, "name": "test_player5", "position": -1, "alive": False}], 
# #                             "gameInfo": {"sentido": "derecha", 
# #                                             "jugadorTurno": 2, 
# #                                             "faseDelTurno": 1,
# #                                             "siguienteJugador": 3}}
    
# #-------------------------------------------- lanzallamas para la derecha--------------------------------------------

# # #test play card, lanzallamas to right
# # @pytest.mark.end2end_test
# # def test_play_card_lanzallamas_right(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, lanzallamas to right")

# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 1, "id_player_to": 2, "id_card": 37})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Carta lanzallamas aplicada'}

# #     #check with get player status 1
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 1, 'name': 'test_player1', 'position': 0, 'status': 'theThing', 
# #                            'cards': [{'type': 'Empty', 'id': 20}, 
# #                                      {'type': 'Empty', 'id': 38}, 
# #                                      {'type': 'Sospecha', 'id': 39}, 
# #                                      {'type': 'LaCosa', 'id': 40}]}

# #     #check with get player status 2
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 2, 'name': 'test_player2', 'cards': [], 'position': -1, 'status': 'dead'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": -1, "alive": False},
# #                                         {"id": 3, "name": "test_player3", "position": 1, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 3, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 1,
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 3}}
    
# #     #change card
# #     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 1, "player_to_id": 3, "card_id": 38})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 29, 'type': 'Empty', 'number': 29, 'description': 'Without effect'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": -1, "alive": False},
# #                                         {"id": 3, "name": "test_player3", "position": 1, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 3, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 3,
# #                                             "faseDelTurno": 1,
# #                                             "siguienteJugador": 4}}


# #----------------------------------------------------------------------------------------------------------------------------
# #                     para ejecutar tiene que estar descomentado descartar carta y intercambiar: player 1

# #--------------------------------------pasar turno: player 2------------------------------------------------------

# #pasar turno
# @pytest.mark.end2end_test
# def test_pasar_turno_2(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for pasar turno")
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/2")
#     assert data.status_code == 200
#     assert data.json() == {'id': 19, 'type': 'Lanzallamas', 'number': 19, 'description': 'Kill player'}
    
#     #check with get player status
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
#     assert data.status_code == 200
#     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
#                             'cards': [{'id': 19, 'type': 'Lanzallamas'},
#                                         {'id': 34, 'type': 'Analisis'},
#                                         {'id': 35, 'type': 'Whisky'},
#                                         {'id': 36, 'type': 'Infeccion'},
#                                         {'id': 38, 'type': 'Empty'}]}

#     #discard card
#     data = requests.post(f"{SERVICE_URL}/card/discard_card/2/36")
#     assert data.status_code == 200
#     assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

#     #check with get player status
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
#     assert data.status_code == 200
#     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
#                             'cards': [{'id': 19, 'type': 'Lanzallamas'},
#                                         {'id': 34, 'type': 'Analisis'},
#                                         {'id': 35, 'type': 'Whisky'},
#                                         {'id': 38, 'type': 'Empty'}]}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() ==  {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}], 
#                             "gameInfo": {"sentido": "derecha", 
#                                             "jugadorTurno": 2, 
#                                             "faseDelTurno": 3,
#                                             "siguienteJugador": 3}}
    
#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 2, "player_to_id": 3, "card_id": 38})
#     assert data.status_code == 200
#     assert data.json() == {'id': 29, 'type': 'Empty', 'number': 29, 'description': 'Without effect'}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() ==  {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True}, 
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True}, 
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
#                             "gameInfo": {"sentido": "derecha",
#                                             "jugadorTurno": 3,
#                                             "faseDelTurno": 1,
#                                             "siguienteJugador": 4}}
    
# #--------------------------------------Whisky------------------------------------------------------

# # #test play card, whisky
# # @pytest.mark.end2end_test
# # def test_play_card_whisky(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, whisky")

# #     #draw card
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/2")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 19, 'type': 'Lanzallamas', 'number': 19, 'description': 'Kill player'}

# #     #check with get player status
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
# #                             'cards': [{'id': 19, 'type': 'Lanzallamas'},
# #                                         {'id': 34, 'type': 'Analisis'},
# #                                         {'id': 35, 'type': 'Whisky'},
# #                                         {'id': 36, 'type': 'Infeccion'},
# #                                         {'id': 38, 'type': 'Empty'}]}

# #     #play card
# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 2, "id_player_to": 2, "id_card": 35})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Cartas del jugador mostradas', 
# #                            'cards': [{'name': 'Analisis', 'description': 'Ask for a total of cards'}, 
# #                                      {'name': 'Empty', 'description': 'Without effect'}, 
# #                                      {'name': 'Infeccion', 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}, 
# #                                      {'name': 'Lanzallamas', 'description': 'Kill player'}, 
# #                                      {'name': 'Whisky', 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}]}

# #     #check with get player status 2
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 2, "name": "test_player2", "position": 1, "status": "human",
# #                             'cards': [{'id': 19, 'type': 'Lanzallamas'},
# #                                         {'id': 34, 'type': 'Analisis'},
# #                                         {'id': 36, 'type': 'Infeccion'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 2,
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 3}}
    
# #     #change card
# #     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 2, "player_to_id": 3, "card_id": 38})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 29, 'type': 'Empty', 'number': 29, 'description': 'Without effect'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True}, 
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True}, 
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 3,
# #                                             "faseDelTurno": 1,
# #                                             "siguienteJugador": 4}}

# #--------------------------------------Analisis------------------------------------------------------








# #----------------------------------------------------------------------------------------------------------------
# #                 para ejecutar tiene que estar descomentado descartar carta y intercambiar: player 2

# #--------------------------------------pasar turno: player 3------------------------------------------------------

# #pasar turno
# @pytest.mark.end2end_test
# def test_pasar_turno_3(capsys):
#     with capsys.disabled():
#         print("\n")
#         print("\ttest for pasar turno")
    
#     #draw card
#     data = requests.post(f"{SERVICE_URL}/card/steal_card/3")
#     assert data.status_code == 200
#     assert data.json() == {'id': 18, 'type': 'Infeccion', 'number': 18, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}
    
#     #check with get player status
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
#     assert data.status_code == 200
#     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
#                             'cards': [{'id': 18, 'type': 'Infeccion'},
#                                         {'id': 30, 'type': 'Sospecha'},
#                                         {'id': 31, 'type': 'CambioDeLugar'},
#                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
#                                         {'id': 38, 'type': 'Empty'}]}

#     #discard card
#     data = requests.post(f"{SERVICE_URL}/card/discard_card/3/18")
#     assert data.status_code == 200
#     assert data.json() == {'message': 'Carta desligada y marcada como descartada'}

#     #check with get player status
#     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
#     assert data.status_code == 200
#     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
#                             'cards': [{'id': 30, 'type': 'Sospecha'},
#                                         {'id': 31, 'type': 'CambioDeLugar'},
#                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
#                                         {'id': 38, 'type': 'Empty'}]}
    
#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() ==  {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
#                             "gameInfo": {"sentido": "derecha",
#                                             "jugadorTurno": 3,
#                                             "faseDelTurno": 3,
#                                             "siguienteJugador": 4}}
    
#     #change card
#     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 3, "player_to_id": 4, "card_id": 38})
#     assert data.status_code == 200
#     assert data.json() == {'id': 25, 'type': 'Analisis', 'number': 25, 'description': 'Ask for a total of cards'}

#     #check with get game status
#     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
#     assert data.status_code == 200
#     assert data.json() ==  {"gameStatus": "INIT",
#                             "name": "test_game",
#                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
#                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
#                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
#                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
#                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
#                             "gameInfo": {"sentido": "derecha",
#                                             "jugadorTurno": 4,
#                                             "faseDelTurno": 1,
#                                             "siguienteJugador": 5}}
    
# #--------------------------------------vigila tus espaldas------------------------------------------------------

# # #test play card, vigila tus espaldas
# # @pytest.mark.end2end_test
# # def test_play_card_vigila_tus_espaldas(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, vigila tus espaldas")
    
# #     #draw card
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/3")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 18, 'type': 'Infeccion', 'number': 18, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}
    
# #     #check with get player status
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 31, 'type': 'CambioDeLugar'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #play card
# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 3, "id_player_to": 3, "id_card": 32})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Carta vigila tus espaldas aplicada'}

# #     #check with get player status 3
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 31, 'type': 'CambioDeLugar'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "izquierda",
# #                                             "jugadorTurno": 3,
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 2}}
    
# #     #change card
# #     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 3, "player_to_id": 2, "card_id": 38})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 19, 'type': 'Lanzallamas', 'number': 19, 'description': 'Kill player'}

# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 2, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "izquierda",
# #                                             "jugadorTurno": 2,
# #                                             "faseDelTurno": 1,
# #                                             "siguienteJugador": 1}}
    
# #     #draw card player 2
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/2")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 17, 'type': 'Whisky', 'number': 17, 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}


# #--------------------------------------cambio de lugar------------------------------------------------------

# # #test play card, cambio de lugar, to right
# # @pytest.mark.end2end_test
# # def test_play_card_cambio_de_lugar_right(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, cambio de lugar, to right")
    
# #     #draw card
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/3")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 18, 'type': 'Infeccion', 'number': 18, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}
    
# #     #check with get player status
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 31, 'type': 'CambioDeLugar'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #play card
# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 3, "id_player_to": 4, "id_card": 31})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Carta cambio de lugar aplicada'}

# #     #check with get player status 3
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 3, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #check with get player status 4
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 4})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 4, "name": "test_player4", "position": 2, "status": "human",
# #                             'cards': [{'id': 25, 'type': 'Analisis'},
# #                                         {'id': 26, 'type': 'Whisky'},
# #                                         {'id': 27, 'type': 'Infeccion'},
# #                                         {'id': 28, 'type': 'Lanzallamas'}]}
    
# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 3, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 3,
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 4}}
    
# #     #change card
# #     data = requests.post(f"{SERVICE_URL}/card/change", json={"player_id": 3, "player_to_id": 5, "card_id": 38})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 21, 'type': 'Sospecha', 'number': 21, 'description': 'Ask for a card'}

# #     #check with get player status 3
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 3, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 21, 'type': 'Sospecha'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'}]}
    
# #     #check with get player status 5
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 5})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 5, "name": "test_player5", "position": 4, "status": "human",
# #                             'cards': [{'id': 22, 'type': 'CambioDeLugar'},
# #                                         {'id': 23, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 24, 'type': 'MasValeQueCorras'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 3, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 4,
# #                                             "faseDelTurno": 1,
# #                                             "siguienteJugador": 3}}
    
# #     #draw card player 4
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/4")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 17, 'type': 'Whisky', 'number': 17, 'description': 'Show all your cards to the other players. This card can only be played on yourself.'}

# #     #check with game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() == {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 1, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 3, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 2, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 4,
# #                                             "faseDelTurno": 2,
# #                                             "siguienteJugador": 3}}
    
# #                               --------------------------------------------------

# # #test play card, cambio de lugar, to left
# # @pytest.mark.end2end_test
# # def test_play_card_cambio_de_lugar_left(capsys):
# #     with capsys.disabled():
# #         print("\n")
# #         print("\ttest for play card, cambio de lugar, to left")
    
# #     #draw card
# #     data = requests.post(f"{SERVICE_URL}/card/steal_card/3")
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 18, 'type': 'Infeccion', 'number': 18, 'description': 'Esta carta te infecta, solo si la recibes luego de un intercambio de cartas'}
    
# #     #check with get player status
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 2, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 31, 'type': 'CambioDeLugar'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #play card
# #     data = requests.post(f"{SERVICE_URL}/card/play_card", json={"id_game": 1, "id_player": 3, "id_player_to": 2, "id_card": 31})
# #     assert data.status_code == 200
# #     assert data.json() == {'succes': True, 'message': 'Carta cambio de lugar aplicada'}

# #     #check with get player status 3
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 3})
# #     assert data.status_code == 200
# #     assert data.json() == {"id": 3, "name": "test_player3", "position": 1, "status": "human",
# #                             'cards': [{'id': 18, 'type': 'Infeccion'},
# #                                         {'id': 30, 'type': 'Sospecha'},
# #                                         {'id': 32, 'type': 'VigilaTusEspaldas'},
# #                                         {'id': 38, 'type': 'Empty'}]}
    
# #     #check with get player status 2
# #     data = requests.get(f"{SERVICE_URL}/game/playerstatus", params={"id_game": 1, "id_player": 2})
# #     assert data.status_code == 200
# #     assert data.json() == {'id': 2, 'name': 'test_player2', 'position': 2, 'status': 'human', 
# #                            'cards': [{'id': 19, 'type': 'Lanzallamas'},
# #                                         {'id': 29, 'type': 'Empty'},
# #                                         {'id': 34, 'type': 'Analisis'},
# #                                         {'id': 35, 'type': 'Whisky'}]}
    
    
# #     #check with get game status
# #     data = requests.get(f"{SERVICE_URL}/game/status", params={"id_game": 1})
# #     assert data.status_code == 200
# #     assert data.json() ==  {"gameStatus": "INIT",
# #                             "name": "test_game",
# #                             "players": [{"id": 1, "name": "test_player1", "position": 0, "alive": True},
# #                                         {"id": 2, "name": "test_player2", "position": 2, "alive": True},
# #                                         {"id": 3, "name": "test_player3", "position": 1, "alive": True},
# #                                         {"id": 4, "name": "test_player4", "position": 3, "alive": True},
# #                                         {"id": 5, "name": "test_player5", "position": 4, "alive": True}],
# #                             "gameInfo": {"sentido": "derecha",
# #                                             "jugadorTurno": 3,
# #                                             "faseDelTurno": 3,
# #                                             "siguienteJugador": 2}}
