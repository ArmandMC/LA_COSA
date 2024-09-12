import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest
#-------------------------------------------------------------------------------------
#this section of code should be in the first file to be executed in the integration test
from game.models.converter import EnumConverter
from settings import settings
from constants import DB_PROVIDER
from game.models.db import db
from enum import Enum

db.bind(provider=DB_PROVIDER, filename=settings.DB_FILEANAME, create_db=True)
db.provider.converter_classes.append((Enum, EnumConverter))
db.generate_mapping(create_tables=True)
#-----------------------------------------------------------------------------------------

from pony.orm import db_session, select
from game.card.models import Card
from game.card.utils import *


@pytest.mark.integration_test
@db_session
def test_create_card():
    # Prueba la creación de una carta
    card = db.Card(type="Lanzallamas", number=42, description="A description")
    assert isinstance(card, Card)
    assert card.type == "Lanzallamas"
    assert card.number == 42
    assert card.description == "A description"

@pytest.mark.integration_test
@db_session
def test_card_save_and_retrieve():
    # Prueba guardar una carta en la base de datos y luego recuperarla
    card = db.Card(type="SomeType", number=42, description="A description")

    # Guarda la carta en la base de datos
    db.commit()

    # Recupera la carta de la base de datos por su ID
    retrieved_card = db.Card.get(id=card.id)
    assert isinstance(retrieved_card, Card)
    assert retrieved_card.type == "SomeType"
    assert retrieved_card.number == 42
    assert retrieved_card.description == "A description"

@pytest.mark.integration_test
@db_session
def test_invalid_card_creation():
    # Prueba crear una carta sin algunos atributos obligatorios
    with pytest.raises(ValueError):
        invalid_card = db.Card(type="SomeType")  # Falta 'number' y 'description'

#test assign a card to a player
@pytest.mark.integration_test
@db_session
def test_assign_card_to_player(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest assign a card to a player")

    card = db.Card(type="SomeType", number=42, description="A description")
    game = db.Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player = db.Player(name="test", game=game.id)
    commit()
    response = assign_card_to_player(player, card)
    assert card.player == player
    assert card in player.cards
    assert response == {f"Carta asignada a test"}
