"""Card Schemas."""

from pydantic import BaseModel
from enum import Enum
    
class PlayCard(BaseModel):
    """
    Schema for representing a inbound card
    """

    id_game: int
    id_player: int
    id_player_to: int
    id_card: int

class PlayCard2(BaseModel):
    id_player: int
    id_player_to: int
    id_card_2: int
    defense: bool

class CardResponse(BaseModel):
    """
    Schema for representing a outbound card
    """
    id: int
    type: str
    number: int
    description: str

class TipeEnum(int, Enum):
    tipe_1 = 1
    tipe_2 = 2
    tipe_3 = 3
    tipe_4 = 4

class ChangeValidation(BaseModel):
    """
    Schema for representing the validation of a change
    """
    type: TipeEnum
    description: str
    
class ChangeCard1(BaseModel):
    """
    Schema for representing a change card
    """
    player_id: int
    player_to_id: int
    card_id: int

class ChangeCard2(BaseModel):
    """
    Schema for representing a change card
    """
    player_id: int
    player_to_id: int
    card_id2: int

class ChangeCardResponse(BaseModel):
    """
    Schema for representing a change card
    """
    id_player_1: int
    id_player_2: int
    id_card1: int
    id_card2: int