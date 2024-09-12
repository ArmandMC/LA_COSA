from pydantic import BaseModel
from typing import Optional


class PartidaCreate(BaseModel):
    name: str
    min_players: int
    max_players: int
    has_password: bool
    password: Optional[str] = None

class FinishGame(BaseModel):
    game_id: int
    player_id: int