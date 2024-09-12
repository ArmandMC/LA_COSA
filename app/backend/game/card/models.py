"""Card Models."""
from pony.orm import PrimaryKey, Set, Required, Optional

from game.models.db import db

class Card(db.Entity):
    """
    Represent a Card.

    """

    id = PrimaryKey(int, auto=True)
    type = Required(str)
    number = Required(int)
    description = Required(str)
    player = Optional("Player")
    game_deck = Optional("GameCards")
    discard_deck = Optional("DiscardCards")
    change = Required(bool, default=False)

class CartaObstaculo(db.Entity):
    id = PrimaryKey(int, auto=True)
    nombre = Required(str)
    jugador_izquierda = Optional(int)
    jugador_derecha = Optional(int)
    cuarentena = Required(bool, default=False)
    estado_juego = Required('Estado_de_juego')