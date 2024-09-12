from fastapi import APIRouter, HTTPException, status 
from .models import *
from .schemas import *
from .utils import *
from pony.orm import db_session , select
from ..game_status.models import Estado_de_juego
from ..game.models import db
from ..player.models import PlayerStatus
from utils import manager

#/game
Game_router = APIRouter()

@Game_router.get("/")
@db_session
def get_all_games():
    games = select(g for g in Game)[:]
    game_dicts = [{
        "id": game.id,
        "name": game.Name,  # Suponiendo que tienes un campo 'name' en tu modelo Game
        "cantidad de jugadores": len(game.players),
    } for game in games]
    return game_dicts

#/game/
@Game_router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_partida(partida: PartidaCreate):
    # Verificación de cantidad de jugadores
    try:
        validate_players(partida.min_players, partida.max_players)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    with db_session:
        if check_game_name_exists(partida.name):
            raise HTTPException(status_code=400, detail="El nombre de partida ya existe.")

        password = partida.password if partida.has_password else "None"

        new_game = Game(
            Name=partida.name,
            Max_players=partida.max_players,
            Min_players=partida.min_players,
            Has_password=partida.has_password,
            Password=password
        )
         # Guarda la partida en la base de datos
        db.commit()
        
        # Verifica el valor de new_game.id
        game_id = new_game.id
        if game_id:
            Estado_de_juego(IdGame=game_id, jugador_de_turno=1, Fase_de_turno=1, Sentido=True , players_alive=0)
        else:
            raise ValueError("new_game.id is None!")

    return {"id": new_game.id}

#endpoint to delete a game
@Game_router.delete("/{game_id}", status_code=status.HTTP_200_OK)
def delete_game_end(game_id: int):
    """
    delete a game

    Parameters
    ----------
    game_id : int

    Returns
    -------
    message

    Raises
    ------
    HTTPException
        404 -> When game is not found
        400 -> When game is not finished
    """ """"""
    with db_session:
        game = select(g for g in Game if g.id == game_id).first()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.Estado_Partida != GameStatus.FINISH:
            raise HTTPException(status_code=400, detail="Game is not finished")
        delete_game(game_id)

    return {"message": "Game deleted successfully"}

# Ruta para obtener los datos de los jugadores que ganaron
@Game_router.get("/{game_id}/winners", status_code=status.HTTP_200_OK)
def get_game_winners(game_id: int):
    with db_session:
        game = select(g for g in Game if g.id == game_id).first()

        if game.Estado_Partida != GameStatus.FINISH:
            return HTTPException(status_code=400, detail="Game is not finished")
        
        # Verificamos si hay un jugador con el rol 'human' o 'La Cosa' para determinar al equipo ganador
        humans = 0
        theThing = 0

        for player in game.players:
            if player.status == PlayerStatus.human:
                humans += 1
            elif player.status == PlayerStatus.theThing:
                theThing += 1

        if humans > 0 and theThing == 1:
            team_winner = "Humanos"
            human_winner = True
            la_cosa_winner = False
            infected_winner = False
        elif theThing == 1 and humans == (len(game.players) - 1):
            team_winner = "La Cosa"
            human_winner = False
            la_cosa_winner = True
            infected_winner = False
        elif theThing == 1 and humans == 0:
            team_winner = "La Cosa y los infectados"
            human_winner = False
            la_cosa_winner = True
            infected_winner = True
        elif humans > 0:
            team_winner = "Humanos"
            human_winner = True
            la_cosa_winner = False
            infected_winner = False
        else:
            raise HTTPException(status_code=400, detail="Condicion no considerada")

        # Recopilamos los datos de los jugadores ganadores
        winners = []
        for player in game.players:
            if human_winner and player.status == PlayerStatus.human:
                winner_info = {"id": player.id,"name": player.name, "role": player.status.value}
                winners.append(winner_info)
            elif la_cosa_winner and player.status == PlayerStatus.theThing:
                winner_info = {"id": player.id,"name": player.name, "role": player.status.value}
                winners.append(winner_info)
            elif infected_winner and player.status == PlayerStatus.infected:
                winner_info = {"id": player.id,"name": player.name, "role": player.status.value}
                winners.append(winner_info)

        winners.sort(key=lambda x: x["id"])
        
        result = {
            "name": game.Name,
            "team": team_winner,
            "players": winners,
        }
    return result

#enpoint to finish a game, when the Thing wants to finish the game
@Game_router.post("/finish", status_code=status.HTTP_200_OK)
async def finish_game(schema: FinishGame):
    """
    finish a game

    Parameters
    ----------
    schema : FinishGame
        game_id : int
        player_id : int

    Returns
    -------
    message

    Raises
    ------
    HTTPException
        404 -> When game is not found
        400 -> When game is already finished
    """
    with db_session:
        game = select(g for g in Game if g.id == schema.game_id).first()
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")
        
        player = select(p for p in game.players if p.id == schema.player_id).first()
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        
        if player.status != PlayerStatus.theThing:
            raise HTTPException(status_code=400, detail="Player is not the thing")
        
        game.Estado_Partida = GameStatus.FINISH
        
        await manager.trigger_game_status(game.id)
    return {"message": "Game finished successfully"}