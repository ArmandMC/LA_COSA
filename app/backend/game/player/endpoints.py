"""Defines Player endpoints."""
from typing import List

from fastapi import APIRouter, HTTPException, status

from game.player.schemas import PlayerJoin, JoinResponse, PlayerResponse
from game.player.utils import *
from utils import manager

#/player
Player_router = APIRouter()

# endpoint to join a player to a game
@Player_router.post(path="/join", status_code=status.HTTP_200_OK)
async def join_game(info: PlayerJoin) -> JoinResponse:
    """
    create a new player, and add it to a game

    Parameters
    ----------
    PlayerJoin
        Player name and game id

    Returns
    -------
    PlayerResponse
        Player id and admin status

    Raises
    ------
    HTTPException
        400 -> When game is full
        404 -> When game is not found
        406 -> When name is already taken
    """ """"""

    #check if game exists
    try:
        check_game(info.gameId)
    except HTTPException as e:
        raise e
    #check if game is full
    try:
        check_full(info.gameId)
    except HTTPException as e:
        raise e
    
    #check if name is already taken
    try:
        check_name(info.name, info.gameId)
    except HTTPException as e:
        raise e
    
    #create player
    player_response = create_player(info.name, info.gameId)
    #trigger game status
    await manager.trigger_game_status(info.gameId)


    return player_response

# endpoint to get all players in a game
@Player_router.get(path="", status_code=status.HTTP_200_OK)
def get_players(game_id: int) -> List[PlayerResponse]:
    """
    get all players in a game

    Parameters
    ----------
    game_id : int
        game id

    Returns
    -------
    List[PlayerResponse]
        list of players in the game

    Raises
    ------
    HTTPException
        404 -> When game is not found
    """ """"""

    #check if game exists
    try:
        check_game(game_id)
    except HTTPException as e:
        raise e

    #get all players in the game
    players = fetch_players(game_id)

    return players

# endpoint to dissociate a player from a game
@Player_router.delete(path="/{player_id}", status_code=status.HTTP_200_OK)
async def dissociate_player(player_id: int):
    """
    dissociate a player from a game

    Parameters
    ----------
    player_id : int

    Returns
    -------
    "Player deleted" -> if player is not admin
    "Game deleted" -> if player is admin

    Raises
    ------
    HTTPException
        404 -> When player is not found
        406 -> When game started
    """ """"""

    #delete player
    try:
        with db_session:
            player = Player.get(id=player_id)
            gameId = player.game.id
            result = dissasociate_player(player_id)
            await manager.trigger_game_status(gameId)
            return result 
    except HTTPException as e:
        raise e