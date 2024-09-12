# chat/models/chat_models.py
from pony.orm import PrimaryKey, Required, Optional, Set
from game.models.db import db
import datetime

class ChatMessage(db.Entity):
    id = PrimaryKey(int, auto=True)
    game_id = Required(int)
    player_id = Required(int)
    text = Required(str)
    timestamp = Required(datetime.datetime, default=datetime.datetime.utcnow)
