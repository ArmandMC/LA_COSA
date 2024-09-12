# game_status/models.py

from pony.orm import PrimaryKey, Required, Optional, Set
from game.models.db import db
from game.deckCards.models import GameCards, DiscardCards


class Estado_de_juego(db.Entity):
    IdGame = PrimaryKey(int)  # Hacemos de IdGame la clave primaria
    jugador_de_turno = Required(int)
    Fase_de_turno = Required(int)
    Sentido = Required(bool)
    players_alive = Required(int)
    game_deck = Optional(GameCards)
    discard_deck = Optional(DiscardCards)
    next_player = Optional(int) #es el id del jugador que sigue en el turno
    apply_infection = Required(bool, default=True)
    obstaculos = Set('CartaObstaculo')
    seduccion = Optional(bool, default=False)
    in_defense = Optional(bool, default=False)
    no_defense = Optional(bool, default=False)