"""Game Models."""
from pony.orm import PrimaryKey, Set, Optional, Required
from enum import Enum


from game.models.db import db
from game.player.models import Player

class GameStatus(Enum):
    NOTREADY = "NOTREADY"
    READY = "READY"
    INIT = "INIT"
    FINISH = "FINISH"
class Game(db.Entity):
    """
    Represent a Game.

    """

    id = PrimaryKey(int, auto=True)
    ID_creador = Optional(int)
    Name = Required(str)
    players = Set(Player)
    Estado_Partida = Required(GameStatus, default=GameStatus.NOTREADY)
    # mazo = Optional('Mazo')
    #estado_de_juego = Optional('Estado_de_juego')
    # chat = Optional('Chat')
    Max_players = Optional(int)
    Min_players = Optional(int)
    Has_password = Optional(bool)
    Password = Optional(str)
    admin = Optional(int)