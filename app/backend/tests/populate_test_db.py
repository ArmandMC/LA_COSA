import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from pony.orm import db_session, commit
from enum import Enum

from settings import settings
from constants import DB_PROVIDER
from game.models.db import db
from game.models.converter import EnumConverter

from game.game.models import GameStatus
from game.player.models import Player, PlayerStatus
from game.card.models import Card
from game.deckCards.models import *
from game.game_status.models import Estado_de_juego

# Connecting to DB and creating tables
db.bind(provider=DB_PROVIDER, filename=settings.DB_FILEANAME, create_db=True)
# Register the type converter with the database
db.provider.converter_classes.append((Enum, EnumConverter))
db.generate_mapping(create_tables=True)

@db_session
def load_data_for_test():
    
    #game id = 1
    db.Game(Max_players=2, Name="test1", Min_players=2)
    commit()
    #player id = 1
    db.Player(name="test", game=1)
    #player id = 2
    db.Player(name="test2", game=1)

    #game id = 2
    db.Game(Max_players=2, Name="test2", Min_players=2)
    commit()
    #player id = 3
    db.Player(name="test", game=2)

    #game id = 3
    db.Game(Max_players=2, Name="test3", Min_players=2)
    commit()

    #game id = 4
    db.Game(Max_players=2, Name="test4", Min_players=2)
    commit()

    #game id = 5
    db.Game(Max_players=2, Name="test5", Min_players=2)
    commit()
    db.Player(name='Player test',game=5,status=PlayerStatus.theThing)
    db.Player(name='Player test2',game=5,status=PlayerStatus.infected)
    
    #game id = 6
    db.Game(Max_players=4, Name="test6", Min_players=4)
    commit()
    for id in range(3):
        db.Player(name='Player test {id}',game=6,status=PlayerStatus.human)
    db.Player(name='Player test 4',game=6,status=PlayerStatus.dead)

    #game id = 7
    db.Game(Max_players=4, Name="test7", Min_players=4, Estado_Partida=GameStatus.FINISH)
    commit()
    for id in range(4):
        db.Player(name='Player test {id}',game=7,status=PlayerStatus.human)

    #game id = 8
    db.Game(Max_players=4, Name="test8", Min_players=4)
    commit()
    for id in range(3):
        db.Player(name='Player test {id}',game=8,status=PlayerStatus.human)
    db.Player(name='Player test 4',game=8,status=PlayerStatus.theThing)

    #game id = 9
    db.Game(Max_players=4, Name="test9", Min_players=4)
    commit()
    for id in range(4):
        db.Player(name='Player test {id}',game=9,status=PlayerStatus.human)

    #state game id = 1
    db.Estado_de_juego(IdGame=1, jugador_de_turno=1, Fase_de_turno=1, Sentido=True, players_alive=2, next_player=2)

if __name__ == '__main__':
    load_data_for_test()
