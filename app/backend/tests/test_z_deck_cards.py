import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import pytest

from game.models.db import db
from pony.orm import Database, db_session
from game.deckCards.models import GameCards
from game.deckCards.utils import *
from game.card.utils import *
from game.card.models import Card
from game.player.models import *
from game.game.models import Game

@pytest.mark.integration_test
@db_session
def test_create_deck_cards():
    # Prueba la creación de un conjunto de cartas de mazo
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = GameCards(id = game.id ,quantity_card=30)
    assert isinstance(deck, GameCards)
    assert deck.quantity_card == 30

@pytest.mark.integration_test
@db_session
def test_assign_cards_to_deck():
    # Prueba la asignación de cartas a un conjunto de cartas de mazo
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = GameCards(id = game.id ,quantity_card=30)
    card1 = Card(type="CardType1", number=1, description="Description 1")
    card2 = Card(type="CardType2", number=2, description="Description 2")

    # Asigna las cartas al mazo
    deck.cards.add(card1)
    deck.cards.add(card2)

    # Guarda el conjunto de cartas de mazo en la base de datos
    db.commit()

    # Recupera el conjunto de cartas de mazo y verifica que tenga las cartas asignadas
    retrieved_deck = GameCards.get(id=deck.id)
    assert isinstance(retrieved_deck, GameCards)
    assert retrieved_deck.quantity_card == 30
    assert card1 in retrieved_deck.cards
    assert card2 in retrieved_deck.cards

@pytest.mark.integration_test
@db_session
def test_retrieve_cards_from_deck():
    # Prueba la recuperación de cartas de un conjunto de cartas de mazo
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = GameCards(id = game.id ,quantity_card=30)
    card1 = Card(type="CardType1", number=1, description="Description 1")
    card2 = Card(type="CardType2", number=2, description="Description 2")

    # Asigna las cartas al mazo
    deck.cards.add(card1)
    deck.cards.add(card2)

    # Guarda el conjunto de cartas de mazo en la base de datos
    db.commit()

    # Recupera las cartas del mazo y verifica que estén presentes
    retrieved_deck = GameCards.get(id=deck.id)
    retrieved_cards = list(retrieved_deck.cards)
    assert len(retrieved_cards) == 2
    assert card1 in retrieved_cards
    assert card2 in retrieved_cards

#test take a card from the deck
@pytest.mark.integration_test
@db_session
def test_take_card_from_deck(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest take a card from the deck")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = GameCards(id = game.id ,quantity_card=30)
    card1 = Card(type="CardType1", number=1, description="Description 1")
    card2 = Card(type="CardType2", number=2, description="Description 2")

    # Asigna las cartas al mazo
    deck.cards.add(card1)
    deck.cards.add(card2)

    # Guarda el conjunto de cartas de mazo en la base de datos
    db.commit()

    # Take a card from the deck
    last_card = take_card_from_deck(deck)
    assert last_card == card2
    assert card2 not in deck.cards
    assert card1 in deck.cards

#test discard a card, when the discard comes from the deck
@pytest.mark.integration_test
@db_session
def test_discard_card(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest discard a card, when the discard comes from the deck")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    deck = GameCards(id = game.id, quantity_card=30)
    discard_deck = DiscardCards(id = game.id, quantity_card= 0)
    commit()
    card1 = Card(type="CardType1", number=1, description="Description 1", game_deck=deck)
    card2 = Card(type="CardType2", number=2, description="Description 2", game_deck=deck)
    deck.cards.add(card1)
    deck.cards.add(card2)
    db.commit()
    response = discard_card(card1)

    assert discard_deck.quantity_card == 1
    assert card1 not in deck.cards
    assert card1 in discard_deck.cards
    assert card2 in deck.cards
    assert card2 not in discard_deck.cards
    assert card1.game_deck == None
    assert card1.player == None
    assert card1.discard_deck == discard_deck
    assert card2.game_deck == deck
    assert card2.player == None
    assert card2.discard_deck == None
    assert response == "Card discarded"

#test discard a card, when the discard comes from the player
@pytest.mark.integration_test
@db_session
def test_discard_card_from_player(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest discard a card, when the discard comes from the player")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player = Player(name="test", game=game)
    discard_deck = DiscardCards(id = game.id, quantity_card= 0)
    commit()
    card1 = Card(type="CardType1", number=1, description="Description 1", player=player)
    card2 = Card(type="CardType2", number=2, description="Description 2", player=player)
    player.cards.add(card1)
    player.cards.add(card2)
    commit()

    response = discard_card(card1)

    assert discard_deck.quantity_card == 1
    assert card1 not in player.cards
    assert card1 in discard_deck.cards
    assert card2 in player.cards
    assert card2 not in discard_deck.cards
    assert card1.discard_deck == discard_deck
    assert card1.game_deck == None
    assert card1.player == None
    assert card2.player == player
    assert card2.game_deck == None
    assert card2.discard_deck == None
    assert response == "Card discarded"

#test to veryfy if the card is valid for a change, when the card is valid
@pytest.mark.integration_test
@db_session
def test_verify_card_change_valid(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to veryfy if the card is valid for a change, when the card is valid")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = Player(name="test", game=game, status = PlayerStatus.human)
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    player3 = Player(name="test3", game=game, status = PlayerStatus.theThing)
    commit()
    card1 = Card(type="Lanzallamas", number=1, description="Description 1", player=player1)
    card2 = Card(type="Empty", number=2, description="Description 2", player=player1)

    card3 = Card(type="Lanzallamas", number=3, description="Description 3", player=player2)
    card4 = Card(type="Empty", number=4, description="Description 4", player=player2)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player2)

    card5 = Card(type="Lanzallamas", number=5, description="Description 5", player=player3)
    card6 = Card(type="Empty", number=6, description="Description 6", player=player3)
    commit()

    response = verify_card_change(card1, player1)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(card2, player1)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(card3, player2)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(card4, player2)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(card5, player3)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(card6, player3)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"


#test to veryfy if the card is valid for a change, when the card is the thing
@pytest.mark.integration_test
@db_session
def test_verify_card_change_thing(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to veryfy if the card is valid for a change, when the card is the thing")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player3 = Player(name="test3", game=game, status = PlayerStatus.theThing)
    commit()

    card5 = Card(type="Lanzallamas", number=5, description="Description 5", player=player3)
    card6 = Card(type="Empty", number=6, description="Description 6", player=player3)
    card7 = Card(type="LaCosa", number=7, description="Description 7", player=player3)
    commit()

    response = verify_card_change(card7, player3)
    assert response.type == TipeEnum.tipe_2
    assert response.description == "No se puede intercambiar la carta de la cosa"

#test to veryfy if the card is valid for a change, when the player is human and the card is infection
@pytest.mark.integration_test
@db_session
def test_verify_card_change_human(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to veryfy if the card is valid for a change, when the player is human and the card is infection")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = Player(name="test", game=game, status = PlayerStatus.human)
    commit()

    card1 = Card(type="Lanzallamas", number=1, description="Description 1", player=player1)
    card2 = Card(type="Empty", number=2, description="Description 2", player=player1)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player1)
    commit()

    response = verify_card_change(cardinf, player1)
    assert response.type == TipeEnum.tipe_3
    assert response.description == "No se puede intercambiar una carta de infeccion si eres humano"

#test to veryfy if the card is valid for a change, when the player is infected and have only one infection card
@pytest.mark.integration_test
@db_session
def test_verify_card_change_infected(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to veryfy if the card is valid for a change, when the player is infected and have only one infection card")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    commit()

    card3 = Card(type="Lanzallamas", number=3, description="Description 3", player=player2)
    card4 = Card(type="Empty", number=4, description="Description 4", player=player2)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player2)
    commit()

    response = verify_card_change(cardinf, player2)
    assert response.type == TipeEnum.tipe_4
    assert response.description == "No se puede intercambiar la unica carta de infeccion que tiene"

#test to veryfy if the card is valid for a change, when the player is infected and have more than one infection card
@pytest.mark.integration_test
@db_session
def test_verify_card_change_infected2(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to veryfy if the card is valid for a change, when the player is infected and have more than one infection card")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    commit()

    card3 = Card(type="Lanzallamas", number=3, description="Description 3", player=player2)
    card4 = Card(type="Empty", number=4, description="Description 4", player=player2)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player2)
    cardinf2 = Card(type="Infeccion", number=8, description="Description 8", player=player2)

    commit()

    response = verify_card_change(cardinf, player2)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

    response = verify_card_change(cardinf2, player2)
    assert response.type == TipeEnum.tipe_1
    assert response.description == "Se puede intercambiar la carta"

#test to get all the cards of a player that are changeable, when the player is human
@pytest.mark.integration_test
@db_session
def test_get_changeable_cards_human(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to get all the cards of a player that are changeable, when the player is human")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = Player(name="test", game=game, status = PlayerStatus.human)
    commit()

    card1 = Card(type="Lanzallamas", number=1, description="Description 1", player=player1)
    card2 = Card(type="Empty", number=2, description="Description 2", player=player1)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player1)
    cardthing = Card(type="LaCosa", number=8, description="Description 8", player=player1)
    commit()

    response = get_changeable_cards(player1)

    assert len(response) == 2
    assert card1.id in response
    assert card2.id in response
    assert cardinf.id not in response
    assert cardthing.id not in response

#test to get all the cards of a player that are changeable, when the player is infected
@pytest.mark.integration_test
@db_session
def test_get_changeable_cards_infected(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to get all the cards of a player that are changeable, when the player is infected")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    commit()

    card3 = Card(type="Lanzallamas", number=3, description="Description 3", player=player2)
    card4 = Card(type="Empty", number=4, description="Description 4", player=player2)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player2)
    cardthing = Card(type="LaCosa", number=8, description="Description 8", player=player2)
    commit()

    response = get_changeable_cards(player2)

    assert len(response) == 2
    assert card3.id in response
    assert card4.id in response
    assert cardinf.id not in response
    assert cardthing.id not in response

#test to get all the cards of a player that are changeable, when the player is the thing
@pytest.mark.integration_test
@db_session
def test_get_changeable_cards_thing(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to get all the cards of a player that are changeable, when the player is the thing")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player3 = Player(name="test3", game=game, status = PlayerStatus.theThing)
    commit()

    card5 = Card(type="Lanzallamas", number=5, description="Description 5", player=player3)
    card6 = Card(type="Empty", number=6, description="Description 6", player=player3)
    cardinf = Card(type="Infeccion", number=7, description="Description 7", player=player3)
    cardthing = Card(type="LaCosa", number=8, description="Description 8", player=player3)
    commit()

    response = get_changeable_cards(player3)

    assert len(response) == 3
    assert card5.id in response
    assert card6.id in response
    assert cardinf.id in response
    assert cardthing.id not in response

#test to verify infection in change, when the player is human
@pytest.mark.integration_test
@db_session
def test_verify_infection_change_human(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to verify infection in change, when the player is human and the card is not infection")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = Player(name="test", game=game, status = PlayerStatus.human)
    commit()

    card1 = Card(type="Lanzallamas", number=1, description="Description 1")
    card2 = Card(type="Empty", number=2, description="Description 2")
    cardinf = Card(type="Infeccion", number=7, description="Description 7")
    commit()

    response = verify_infection(player1, card1)
    assert response == False
    assert player1.status == PlayerStatus.human

    response = verify_infection(player1, card2)
    assert response == False
    assert player1.status == PlayerStatus.human

    response = verify_infection(player1, cardinf)
    assert response == True
    assert player1.status == PlayerStatus.infected

#test to verify infection in change, when the player is infected
@pytest.mark.integration_test
@db_session
def test_verify_infection_change_infected(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to verify infection in change, when the player is infected and the card is not infection")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    commit()

    card3 = Card(type="Lanzallamas", number=3, description="Description 3")
    card4 = Card(type="Empty", number=4, description="Description 4")
    cardinf = Card(type="Infeccion", number=7, description="Description 7")
    commit()

    response = verify_infection(player2, card3)
    assert response == False
    assert player2.status == PlayerStatus.infected

    response = verify_infection(player2, card4)
    assert response == False
    assert player2.status == PlayerStatus.infected

    response = verify_infection(player2, cardinf)
    assert response == False
    assert player2.status == PlayerStatus.infected

#test to verify infection in change, when the player is the thing
@pytest.mark.integration_test
@db_session
def test_verify_infection_change_thing(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to verify infection in change, when the player is the thing and the card is not infection")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player3 = Player(name="test3", game=game, status = PlayerStatus.theThing)
    commit()

    card5 = Card(type="Lanzallamas", number=5, description="Description 5")
    card6 = Card(type="Empty", number=6, description="Description 6")
    cardinf = Card(type="Infeccion", number=7, description="Description 7")
    commit()

    response = verify_infection(player3, card5)
    assert response == False
    assert player3.status == PlayerStatus.theThing

    response = verify_infection(player3, card6)
    assert response == False
    assert player3.status == PlayerStatus.theThing

    response = verify_infection(player3, cardinf)
    assert response == False
    assert player3.status == PlayerStatus.theThing

#test to verify impact in the db of the exchange of cards
@pytest.mark.integration_test
@db_session
def test_exchange_cards(capsys):
    with capsys.disabled():
        print("\n")
        print("\ttest to verify impact in the db of the exchange of cards")
    
    game = Game(Max_players=4, Name="test5", Min_players=4)
    commit()
    player1 = Player(name="test", game=game, status = PlayerStatus.human)
    player2 = Player(name="test2", game=game, status = PlayerStatus.infected)
    commit()

    card1 = Card(type="Lanzallamas", number=1, description="Description 1", player=player1)
    card2 = Card(type="Empty", number=2, description="Description 2", player=player1)

    card3 = Card(type="Lanzallamas", number=3, description="Description 3", player=player2)
    card4 = Card(type="Empty", number=4, description="Description 4", player=player2)
    commit()

    response = impact_change(player1, player2, card1)
    assert response == {f"Carta {card1.id} cambiada con exito"}
    assert card1.player == player2
    assert card2.player == player1
    assert card3.player == player2
    assert card4.player == player2
    assert player1.cards.count() == 1
    assert player2.cards.count() == 3

    response = impact_change(player2, player1, card4)
    assert response == {f"Carta {card4.id} cambiada con exito"}
    assert card1.player == player2
    assert card2.player == player1
    assert card3.player == player2
    assert card4.player == player1
    assert player1.cards.count() == 2
    assert player2.cards.count() == 2


