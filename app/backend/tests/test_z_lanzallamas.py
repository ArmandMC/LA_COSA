import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest
from pony.orm import db_session, select

from game.player.models import Player, PlayerStatus
from game.player.utils import change_status
from game.game_status.utils import take_out_of_round
from game.game_status.models import Estado_de_juego

#test for change player status
@pytest.mark.integration_test
def test_change_player_status(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for change player status")
    
    response = change_status(1, PlayerStatus.dead)
    with db_session:
        player = select(p for p in Player if p.id == 1).first()
        assert player.status == PlayerStatus.dead

# test for take out of round
@pytest.mark.integration_test
def test_take_out_of_round(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest for take out of round")

    take_out_of_round(1)
    with db_session:
        state = select(e for e in Estado_de_juego if e.IdGame == 1).first()
        assert state.players_alive == 1

# falta test para disassociate_cards que tengo q esperar que armen test para discard_card