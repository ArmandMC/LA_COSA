from pydantic import BaseModel
from typing import Optional , List

class StartGame(BaseModel):
    id_game: int
    id_player: int
    
    
class CardInfo(BaseModel):
    type: str
    number: int

class PlayerInfo(BaseModel):
    id: int
    name: str
    cards: List[CardInfo]
    position: int

class GameInfo(BaseModel):
    sentido: str
    jugadorTurno: int
    faseDelTurno: int
    deckTopCard: CardInfo

class GameResponse(BaseModel):
    gameStatus: str
    players: List[PlayerInfo]
    gameInfo: GameInfo