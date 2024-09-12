import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest

from game.models.db import db

from game.game_status.utils import is_game_over
from game.game.models import GameStatus

@pytest.mark.integration_test
def test_no_humans(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest game is over, no humans")

    assert is_game_over(5) is False

@pytest.mark.integration_test
def test_thing_eliminated(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest game is over, thing eliminated")

    assert is_game_over(6) is True

@pytest.mark.integration_test
def test_only_humans(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest game is over, only humans")

    assert is_game_over(7) is True

@pytest.mark.integration_test
def test_game_not_over(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest game is over, game not over")

    assert is_game_over(8) is False

@pytest.mark.integration_test
def test_game_over(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest game is over, game over")

    assert is_game_over(9) is True
