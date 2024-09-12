"""Deck of cards Models."""
from pony.orm import PrimaryKey, Optional, Set

from game.models.db import db

class GameCards(db.Entity):
    """
    Represent a Deck of the Cards that are in Game.

    """

    id = PrimaryKey(int) #same as Game
    quantity_card = Optional(int)
    cards = Set("Card")
    game_status = Optional("Estado_de_juego")

class DiscardCards(db.Entity):
    """
    Represent a Deck of the Cards that are in Discard.

    """

    id = PrimaryKey(int) #same as Game
    quantity_card = Optional(int)
    cards = Set("Card")
    game_status = Optional("Estado_de_juego")


