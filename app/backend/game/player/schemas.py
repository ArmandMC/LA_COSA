"""Player Schemas."""

from pydantic import BaseModel


class PlayerJoin(BaseModel):
    """
    Schema for representing a inbound player
    """

    name: str
    gameId: int


class JoinResponse(BaseModel):
    """Class for retriving Game info after Player joining response."""

    playerId: int
    admin: bool

class PlayerResponse(BaseModel):
    """Class for retriving Player info response."""

    playerId: int
    name: str
    admin: bool