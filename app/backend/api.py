"""Defines Agenda API."""
from fastapi import APIRouter

from game.player.endpoints import Player_router
from game.card.endpoints import Card_router
from game.game.endpoints import Game_router
from game.game_status.endpoints import Game_start , Game_status
from game.chat.endpoints import Chat_router

api_router = APIRouter()
api_router.include_router(Player_router, prefix="/player", tags=["player"])
api_router.include_router(Card_router, prefix="/card", tags=["card"])
api_router.include_router(Game_router, prefix="/game", tags=["game"])
api_router.include_router(Game_start, prefix="/game", tags=["game"])
api_router.include_router(Game_status, prefix="/game", tags=["game"])
api_router.include_router(Chat_router, prefix="/chat", tags=["chat"])