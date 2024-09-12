from pony.orm import db_session, select, commit
from .models import Estado_de_juego
from ..game.models import Game, GameStatus
from fastapi import HTTPException, status
from ..player.models import *
from ..player.utils import *
from ..player.utils import change_status
from ..deckCards.models import GameCards
from ..deckCards.utils import delete_deck
from ..card.models import CartaObstaculo

@db_session
def cantidad_players_para_iniciar(game):
    if len(game.players) < game.Min_players:
        raise ValueError("No hay suficientes jugadores para iniciar la partida.")
    return len(game.players)

    
@db_session  
def verify_game_exists(game_id):
    game = Game.get(id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="La partida no existe.")
    return game


@db_session
def verify_game_state_exists(game_id):
    estadoJuego = Estado_de_juego.get(IdGame=game_id)
    #verificamos que exista el estado de la partida, pero no que este en INIT
    if not estadoJuego :
        raise HTTPException(status_code=404, detail="El estado de la partida no existe.")
    return estadoJuego

@db_session
def verify_player_exists(id_game, id_player):
    game = verify_game_exists(id_game)
    players = game.players.filter(id=id_player)
    player = players.first()
    if not player:
        raise HTTPException(
            status_code=404, detail="El jugador no existe en esta partida.")
    return player

@db_session
def is_player_admin(game_id, player_id):
    """Verifica si un jugador es el administrador de la partida."""
    game = Game.get(id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="La partida no existe.")
    return game.admin == player_id

# funtion that takes a player out of the round
def take_out_of_round(id_player):
    """
    Take out of the round the player.

    """
    with db_session:
        player_target = Player.get(id=id_player)
        position = player_target.position
        game = player_target.game

        #actualizar el estado de la partida
        state = select(e for e in Estado_de_juego if e.IdGame == game.id).first()
        state.players_alive -= 1
        state.flush()
        
        update_next_player(game.id)
        #actualizar la posicion de los jugadores que estan despues del jugador eliminado
        for p in game.players:
            if p.position > position:
                p.position -= 1
                p.flush()
        

        #cambiar posicion del jugador a -1
        player_target.position = -1
        player_target.flush()
        
@db_session
def sit_the_players(game_id):
    i = 0
    game = Game.get(id=game_id)
    # sienta los players en orden de id, Se puede cambiar para que sea random
    players = game.players.order_by(Player.id)
    for player in players:
        player.position = i
        i += 1

#funtion to associate a deck with a game status
def associate_deck_with_game_status(deck_id, game_status_id):
    """
    Associate a deck with a game status.

    """
    with db_session:
        deck = select(d for d in GameCards if d.id == deck_id).first()
        deck.game_status = game_status_id
        game_status = select(e for e in Estado_de_juego if e.IdGame == game_status_id).first()
        game_status.deck = deck
        game_status.flush()

# funtion to change the estatus of the player to human
def change_all_status(id_game):
    """
    Change the estatus of all the players in a game to human.

    """
    with db_session:
        game = Game[id_game]
        for player in game.players:
            change_status(player.id, PlayerStatus.human)

# funtion to delete the game status
def delete_game_status(id_game):
    """
    Delete the game status.

    """
    
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        if not game_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game status {id_game} not exists",
            )
        if Game.get(id=id_game).Estado_Partida == GameStatus.FINISH:
            try:
                delete_deck(game_status.game_deck.id)
            except HTTPException as e:
                raise e
        game_status.delete()
        game_status.flush()
        
    return "Game status deleted"

# function to check if game is over
@db_session
def is_game_over(game_id: int):
    # Obtener el juego por su ID
    game = Game.get(id=game_id)

    # Contadores para los diferentes estados de los jugadores
    human_count = 0
    the_thing_count = 0

    # Iterar a través de los jugadores en el juego
    for player in game.players:
        print(f"Player {player.id} - Status: {player.status}")
        if player.status == PlayerStatus.human:
            human_count += 1
        elif player.status == PlayerStatus.theThing:
            the_thing_count += 1

    # Verificar las condiciones para determinar si el juego ha terminado
    if the_thing_count == 0:
        # Cambiar estado del juego
        change_status_game_to_finish(game_id)
        print(f"Game {game_id} is over!")
        return True

    return False


def build_game_status(id_game: int):
    with db_session:
        game = verify_game_exists(id_game)
        estadodeJuego = verify_game_state_exists(id_game)
        players_info = []
        obstacles_puertaatrancada = []  # Inicializa la lista de obstáculos aquí
        obstacles_cuarentena = []

        for obstacle in estadodeJuego.obstaculos:
            #crear una lista con usuarios en cuaretena
            if obstacle.cuarentena:
                obstacles_cuarentena.append({
                    "id": obstacle.id,
                    "jugador_izquierda": obstacle.jugador_izquierda,
                    "jugador_derecha": obstacle.jugador_derecha,
                })

            #crear una lista con puerta atracada con sus posiciones
            if obstacle.nombre == "Puerta Atrancada":
                obstacles_puertaatrancada.append({
                    "id": obstacle.id,
                    "jugador_izquierda": obstacle.jugador_derecha,
                    "jugador_derecha": obstacle.jugador_izquierda,
                })

        for player in sorted(game.players, key=lambda p: p.id):
            #verificamos si la posicion de un jugador coincide con la de un obstaculo
            obstaculo_izquierda = False
            obstaculo_derecha = False

            for obstacle in estadodeJuego.obstaculos:
                if player.position == obstacle.jugador_izquierda:
                    obstaculo_izquierda = True
                if player.position == obstacle.jugador_derecha:
                    obstaculo_derecha = True

            players_info.append({
                "id": player.id,
                "name": player.name,
                "position": player.position,
                "alive": player.status != PlayerStatus.dead,
                "obstaculo_izquierda": obstaculo_izquierda,
                "obstaculo_derecha": obstaculo_derecha,
                "cuarentena": player.in_quarantine,
            })


        response = {
            "gameStatus": game.Estado_Partida,
            "players": players_info,
            "name": game.Name,
            "gameInfo": {
                "sentido": "derecha" if estadodeJuego.Sentido else "izquierda",
                "jugadoresVivos": estadodeJuego.players_alive,
                "jugadorTurno": estadodeJuego.jugador_de_turno,
                "faseDelTurno": estadodeJuego.Fase_de_turno,
                "siguienteJugador": estadodeJuego.next_player,
                "obstaculosCuarentena": obstacles_cuarentena,
                "obstaculosPuertaAtrancada": obstacles_puertaatrancada,
            }
        }

        return response

# Local method to build player status
def build_player_status(id_game: int, id_player: int):
    with db_session:
        # CHEQUEAR SI NO ES DEMASIADO INEFICIENTE
        player = verify_player_exists(id_game, id_player)
        player_cards = [{"type": card.type, "id": card.id}
                        for card in sorted(player.cards, key=lambda c: c.id)]
        # borrar algunos atributos que no son necesarios ya que vienen por el game status
        response = {
            "id": player.id,
            "name": player.name,
            "cards": player_cards,
            "position": player.position,
            "status": player.status,
            "in_quarantine": player.in_quarantine,
            "quarantine_shifts": player.quarantine_shifts
        }
        return response
    

# # Trigger update of game status to all players in the game
# async def trigger_game_status(id_game: int):
#     manager.broadcast_to_game(id_game, {"type": "gameStatus", "data": ""})


# # Trigger update of player status specific player in the game
# async def trigger_player_status(id_game: int, id_player: int):
#     manager.send_to_player(id_game, id_player, {"type": "message", "data": "Has sido infectado"})
    

    return "Game status deleted"

# proximo fase de turno de cada jugador

def next_turn_phase(id_game):
    """
    Change the turn phase of the player.

    """
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        if not game_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game status {id_game} not exists",
            )
        if game_status.Fase_de_turno == 1:
            game_status.Fase_de_turno = 2
        elif game_status.Fase_de_turno == 2:
            game_status.Fase_de_turno = 3
        elif game_status.Fase_de_turno == 3:
            discount_quarantine(game_status.jugador_de_turno)
            next_turn_player(id_game)
            game_status.Fase_de_turno = 1
        game_status.flush()

    #printear el turno y la fase del jugador
    print("turno del jugador: " + str(game_status.jugador_de_turno))
    print("fase de turno: " + str(game_status.Fase_de_turno))

    return "game status updated"

# proximo turno de cada jugador

def next_turn_player(id_game):
    """
    Change the turn of the player based on position.

    """
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        if not game_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game status {id_game} not exists",
            )
        
        current_player = Player.get(id=game_status.jugador_de_turno)
        if not current_player:
            raise HTTPException(status_code=404, detail="Jugador actual no encontrado.")
        
        total_players = game_status.players_alive #jugadores vivos
        
        next_player_id = game_status.next_player
        
        next_player = Player.get(id=next_player_id)
        
        while True:
            # update de game_status.next_player
            next_next_position = (next_player.position + 1) % total_players if game_status.Sentido else (next_player.position - 1) % total_players
            
            next_next_player = select(p for p in Player if p.game.id == id_game and p.position == next_next_position).first()
            if not next_next_player:
                raise HTTPException(status_code=404, detail="Próximo jugador no encontrado.")
            
            if (next_next_player.status != PlayerStatus.dead):
                break
            else:
                next_player = next_next_player
            
        
        game_status.next_player = next_next_player.id
        
        game_status.jugador_de_turno = next_player_id
        game_status.flush()
    return "game status updated"

#update de game_status.next_player
def update_next_player(id_game):
    """
    Update the next player of the game status.

    """
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        if not game_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game status {id_game} not exists",
            )
        
        current_player = Player.get(id=game_status.jugador_de_turno)
        if not current_player:
            raise HTTPException(status_code=404, detail="Jugador actual no encontrado.")
        
        total_players =  game_status.players_alive #jugadores vivos
        
        next_player_id = game_status.next_player
        
        next_player = Player.get(id=next_player_id)
        
        if (next_player.status == PlayerStatus.dead):
            while True:
                # update de game_status.next_player
                next_next_position = (next_player.position + 1) % total_players if game_status.Sentido else (next_player.position - 1) % total_players
                
                next_next_player = select(p for p in Player if p.game.id == id_game and p.position == next_next_position).first()
                if not next_next_player:
                    raise HTTPException(status_code=404, detail="Próximo jugador no encontrado.")
                
                if (next_next_player.status != PlayerStatus.dead):
                    break
                else:
                    next_player = next_next_player
                
            
            game_status.next_player = next_next_player.id
            game_status.flush()
    return "game status updated"

#update game_status.next_player when there is no change in position
def update_next_player_no_change(id_game):
    """
    Update the next player of the game status.

    """
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        if not game_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game status {id_game} not exists",
            )
        
        current_player = Player.get(id=game_status.jugador_de_turno)
        if not current_player:
            raise HTTPException(status_code=404, detail="Jugador actual no encontrado.")
        
        total_players =  game_status.players_alive #jugadores vivos
         
        while True:
            # update de game_status.next_player
            next_position = (current_player.position + 1) % total_players if game_status.Sentido else (current_player.position - 1) % total_players
            
            next_player = select(p for p in Player if p.game.id == id_game and p.position == next_position).first()
            if not next_player:
                raise HTTPException(status_code=404, detail="Próximo jugador no encontrado.")
            
            if (next_player.status != PlayerStatus.dead):
                game_status.next_player = next_player.id
                game_status.flush()
                break
            else:
                current_player = next_player
    return "game status updated"

                

# funcion para checkear que sea tu turno por su posicion en el juego

def check_turn_and_phase(id_game, id_player, phase):
    """
    Check if it is the turn of the player.

    """
    with db_session:
        game_status = Estado_de_juego.get(IdGame=id_game)
        
        # Obtener la posición del jugador basada en id_player
        current_player_position = Player.get(id=id_player).position

        # Obtener la posición del jugador al que le corresponde el turno
        current_turn_player_position = Player.get(id=game_status.jugador_de_turno).position
        
        # Comparar las posiciones
        if current_player_position != current_turn_player_position:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"It is not your turn",
            )
            
        if game_status.Fase_de_turno != phase:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"It is not the phase of the turn",
            )

    return "It is your turn"





#funcion para checkear que esta al lado
def are_adjacent_players(player1, player2):
    """
    Check if the players are adjacent to each other in the game order.

    Args:
    - player1: First player (ID or instance) to check.
    - player2: Second player (ID or instance) to check against the first player.

    Returns:
    - bool: True if the players are adjacent, otherwise False.
    """
    
    # If IDs are passed, get the player instances
    
    if isinstance(player1, int):
        player1 = Player.get(id=player1)
    
    if isinstance(player2, int):
        player2 = Player.get(id=player2)
    
    total_players = len(player1.game.players)
    print(f"Player1 ID: {player1.id}, Position: {player1.position}")
    print(f"Player2 ID: {player2.id}, Position: {player2.position}")
    print(f"Total Players: {total_players}")

    # Check if they are immediately next to each other
    if player1.position == (player2.position + 1) % total_players or \
       player1.position == (player2.position + total_players - 1) % total_players:
        print("Players are adjacent.")
        return True

    print("Players are not adjacent.")
    return False


#cambiamos el player status a theThing a quien le haya tocado la carta TheThing

def change_player_status_to_TheThing(id_game):
    """
    Change the status of the player to theThing.

    """
    with db_session:
        game = Game.get(id=id_game)
        for player in game.players:
            if player.cards.filter(type="LaCosa").first():
                change_status(player.id, PlayerStatus.theThing)
                break
    return "Player status updated"



#funcion para cambiar el estado a FINISH
def change_status_game_to_finish(id_game):
    """
    Change the estatus of the game to FINISH.

    """
    with db_session:
        game = select(g for g in Game if g.id == id_game).first()
        game.Estado_Partida = GameStatus.FINISH

#funcion para descontar cuarentena
def discount_quarantine(id_player):
    """
    Discount the quarantine shifts of the players.

    """
    with db_session:
        player = Player.get(id=id_player)
        if player.in_quarantine:
            player.quarantine_shifts -= 1
            player.flush()
            if player.quarantine_shifts == 0:
                player.in_quarantine = False
                player.flush()
    return "Quarantine shifts updated"


def hay_puerta_atrancada(jugador1, jugador2):
    obstaculo = CartaObstaculo.get(jugador_izquierda=jugador1.position, jugador_derecha=jugador2.position, nombre="Puerta Atrancada")
    if not obstaculo:
        obstaculo = CartaObstaculo.get(jugador_izquierda=jugador2.position, jugador_derecha=jugador1.position, nombre="Puerta Atrancada")
    return bool(obstaculo)


def eliminar_puerta_atrancada(jugador1, jugador2):
    with db_session:
        obstaculo = CartaObstaculo.get(jugador_izquierda=jugador1, jugador_derecha=jugador2, nombre="Puerta Atrancada")
        if not obstaculo:
            obstaculo = CartaObstaculo.get(jugador_izquierda=jugador2, jugador_derecha=jugador1, nombre="Puerta Atrancada")
        if obstaculo:
            obstaculo.delete()
