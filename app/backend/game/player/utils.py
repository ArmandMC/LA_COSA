"""Player utilities."""

from fastapi import HTTPException, status
from pony.orm import db_session, select, commit

from game.game.models import *
from game.player.models import *
from game.player.schemas import JoinResponse, PlayerResponse


# function to check if exist the game
def check_game(gameId):
    with db_session:
        game = select(g for g in Game if g.id == gameId).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game {gameId} not exists",
            )

# function to check if game is full
def check_full(gameId):
    with db_session:
        game = select(g for g in Game if g.id == gameId).first()
        if game.players.count() >= game.Max_players:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Game {gameId} is full",
            )

# function to check if name is already taken
def check_name(name, gameId):
    with db_session:
        player = select(p for p in Player if p.name == name and (p.game).id == gameId).first()
        if player:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Name {name} is already taken",
            )

# function to create a new player
def create_player(name, gameId):
    with db_session:
        #create player
        admin = check_admin(gameId)
        P = Player(name=name, game=gameId, admin=admin)
        P.flush()
        if (admin):
            assign_admin(gameId, P.id)
        #change status of game if there is enough players to start
        change_status_game_to_ready(gameId)

    return JoinResponse(playerId=P.id, admin=admin)

# function to check if player is the first in the game
def check_admin(gameId):
    with db_session:
        game = select(g for g in Game if g.id == gameId).first()
        if game.players.count() == 0:
            return True
        else:
            return False
        
# function to assign admin to game
def assign_admin(gameId, playerId):
    with db_session:
        game = select(g for g in Game if g.id == gameId).first()
        game.admin = playerId

# function to get all players in a game
def fetch_players(gameId):
    p = []
    with db_session:
        players = select(p for p in Player if (p.game).id == gameId)[:]
        for player in players:
            p.append(PlayerResponse(playerId=player.id, name=player.name, admin=player.admin))
    return p

#funtion that change the estatus of the player to eliminated
def change_status(id_player, status):
    """
    Change the estatus of the player to eliminated.

    """
    with db_session:
        player = select(p for p in Player if p.id == id_player).first()
        player.status = status

#funtion that change the estatus of the game if there is enough players to start
def change_status_game_to_ready(id_game):
    """
    Change the estatus of the game if there is enough players to start.

    """
    with db_session:
        game = select(g for g in Game if g.id == id_game).first()
        if game.players.count() >= game.Min_players:
            game.Estado_Partida = GameStatus.READY


#funtion to delete a player
def delete_player(id_player):
    """
    Delete a player.

    """
    with db_session:
        player = select(p for p in Player if p.id == id_player).first()
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Player {id_player} not exists",
            )
        player.delete()
        commit()
    return "Player deleted"

#funtion to dissasociate a player from a game
def dissasociate_player(id_player):
    """
    Dissasociate a player from a game.

    """
    from game.game.utils import delete_game
    with db_session:
        player = select(p for p in Player if p.id == id_player).first()
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Player {id_player} not exists",
            )
        if player.game.Estado_Partida != GameStatus.NOTREADY and player.game.Estado_Partida != GameStatus.READY:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Game {player.game.id} has already started",
            )
        if player.admin:
            return delete_game(player.game.id)
        else:
            return delete_player(id_player)