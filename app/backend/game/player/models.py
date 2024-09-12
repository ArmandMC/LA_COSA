"""Player Models."""
from pony.orm import PrimaryKey, Required, Set, Optional
from enum import Enum

from game.card.models import Card
from game.models.db import db

# Definir una enumeración para los estados del jugador
class PlayerStatus(Enum):
    human = "human"
    infected = "infected"
    dead = "dead"
    theThing = "theThing"
    notDefined = "notDefined"

class Player(db.Entity):
    """
    Represent a Player.

    """

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    game = Required("Game")
    admin = Required(bool, default=False)
    cards = Set(Card)
    status = Required(PlayerStatus, default=PlayerStatus.notDefined)
    position = Required(int, default=0)
    card_to_steal = Optional(int)
    card_to_change = Optional(int)
    card_to_play = Optional(int)
    in_quarantine = Required(bool, default=False)
    quarantine_shifts = Required(int, default=0)
    change_with = Optional(int, default=-1)
    player_to = Optional(int, default=-1)