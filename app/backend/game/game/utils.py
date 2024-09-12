from pony.orm import db_session, select
from .models import Game
from ..player.utils import delete_player
from ..game_status.utils import delete_game_status
from fastapi import HTTPException, status


def validate_players(min_players, max_players):
    if min_players < 4 or max_players > 12:
        raise ValueError("Número de jugadores no válido.")
    if min_players > max_players:
        raise ValueError("El mínimo de jugadores no puede ser mayor que el máximo.")

@db_session
def check_game_name_exists(name):
    return select(g for g in Game if g.Name == name).exists()

# function to delete a game
def delete_game(game_id):
    """
    Delete a game.

    """
    
    with db_session:
        game = Game.get(id=game_id)
        if game is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game {game_id} not exists",
            )
        try:
            delete_game_status(game_id)
            for player in game.players:
                delete_player(player.id)
            game.delete()
            game.flush()
        except HTTPException as e:
            raise e
    return "Game deleted"