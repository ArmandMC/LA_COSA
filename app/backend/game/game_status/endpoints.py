from fastapi import APIRouter, HTTPException, status, WebSocket , WebSocketDisconnect
from pony.orm import db_session
from .schemas import StartGame
from .utils import *
from ..deckCards.utils import init_deck_of_cards, deal_cards_to_players
from ..game.models import GameStatus
from utils import manager


# REVISAR COMENTARIOS PARA PULIR EL CODIGO


# /game
Game_start = APIRouter()
Game_status = APIRouter()


# Endpoint to get game status by id_game
@Game_status.get("/status", status_code=status.HTTP_200_OK)
def get_game_status(id_game: int):
    response = build_game_status(id_game)
    return response

# Endpoint to get player status by id_game and id_player
@Game_status.get("/playerstatus", status_code=status.HTTP_200_OK)
def get_player_status(id_game: int, id_player: int):
    response = build_player_status(id_game, id_player)
    print("response:", response)
    return response

# Endpoint to start game
@Game_start.post("/start", status_code=status.HTTP_200_OK)
async def start_game(start_game_data: StartGame):
    print("start_game_data.id_game:", start_game_data.id_game)
    print("start_game_data.id_player:", start_game_data.id_player)

    if start_game_data.id_game and start_game_data.id_player:
        with db_session:
            # seleccionamos la partida
            game = verify_game_exists(start_game_data.id_game)

            # Verificar si el jugador es administrador
            if not is_player_admin(start_game_data.id_game, start_game_data.id_player):
                raise HTTPException(
                    status_code=403, detail="No eres el administrador de esta partida.")

            try:
                # verificamos si hay suficientes jugadores para iniciar la partida, ya que game ahora tiene los atributos de GameSettings
                cantidad_players_para_iniciar(game)
            except ValueError as e:
                raise HTTPException(status_code=400, detail="No hay suficientes jugadores para iniciar la partida.")
            
            mazo = init_deck_of_cards(len(game.players), start_game_data.id_game) #inicializamos el mazo de cartas

            associate_deck_with_game_status(mazo.id, start_game_data.id_game) #asociamos el mazo con el estado de la partida
            
            deal_cards_to_players(game.players, mazo) #repartimos las cartas a los jugadores
            
            change_all_status(start_game_data.id_game) #cambiamos el estado de los jugadores a humanos
            
            sit_the_players(start_game_data.id_game) #sentamos a los jugadores
               
            #cambiamos el player status a theThing a quien le haya tocado la carta TheThing
            change_player_status_to_TheThing(start_game_data.id_game)

            estadodeJuego = verify_game_state_exists(start_game_data.id_game) # Utilizamos el id_game directamente
            initial_player = select(p for p in Player if p.game.id == start_game_data.id_game and p.position == 0).first()
            if not initial_player:
                raise HTTPException(status_code=404, detail="Jugador inicial no encontrado.")
            estadodeJuego.jugador_de_turno = initial_player.id
            

            estadodeJuego.Fase_de_turno = 1
            estadodeJuego.Sentido = True
            estadodeJuego.players_alive = len(game.players)
            
            next_player_id = select(p for p in Player if p.game.id == start_game_data.id_game and p.position == 1).first().id 
            estadodeJuego.next_player = Player.get(id=next_player_id).id

            game.Estado_Partida = GameStatus.INIT

            #printear fase de juego y jugador de turno
            print("Fase de juego:", estadodeJuego.Fase_de_turno)
            print("Jugador de turno:", estadodeJuego.jugador_de_turno)
            

            await manager.trigger_game_status(game.id)
            await manager.trigger_all_players_status(game.id)


            return {
                "id": estadodeJuego.IdGame,
                "cantidad de jugadores": len(game.players),
                "jugador de turno": estadodeJuego.jugador_de_turno,
                "fase de turno": estadodeJuego.Fase_de_turno,
                "sentido": estadodeJuego.Sentido
            }

    else:
        raise HTTPException(status_code=404, detail="La partida no existe.")