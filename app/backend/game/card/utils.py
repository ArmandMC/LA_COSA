from pony.orm import db_session, select, commit
from fastapi import HTTPException, status

from game.player.models import *
from game.card.models import *
from game.card.schemas import ChangeValidation, TipeEnum

import sys

#funtion to check if the card belongs to a deck or to a discard deck
def constraint_check(card):

    """Check that a card belongs to a deck or to a discard deck, but not to both."""

    if card.game_deck is None and card.discard_deck is None and card.player is None:
        raise ValueError("A card must belong to a deck or to a discard deck or to a player")
    elif card.game_deck is not None and card.discard_deck is not None:
        raise ValueError("A card can't belong to both a deck and a discard deck")      
    elif card.game_deck is not None and card.player is not None:
        raise ValueError("A card can't belong to both a deck and a player")
    elif card.discard_deck is not None and card.player is not None:
        raise ValueError("A card can't belong to both a discard deck and a player")  

def assign_card_to_player(player, card):
    # Asigna la carta al jugador
    player.cards.add(card)
    card.player = player
    commit()
    # its important to check the constraint after assign the card
    constraint_check(card)
    return {f"Carta asignada a {player.name}"}

#funtion that disassociate all the cards of the player
def disassociate_cards(id_player):
    from game.deckCards.utils import discard_card
    """
    Disassociate all the cards of the player.

    """
    #obtengo todas los id card del jugador
    with db_session:
        cards = select(c for c in Player[id_player].cards)
        #desasocio las cartas del jugador
        for card in cards:
            discard_card(card)

#funtion to delete a card
def delete_card(id_card):
    """
    Delete a card.

    """
    with db_session:
        card = select(c for c in Card if c.id == id_card).first()
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Card {id_card} not exists",
            )
        card.delete()
        commit()
    return "Card deleted"

#funtion to verify if the card is valid for a discard
def verify_card_discard(card, player):
    """
    Verify if the card is valid for a discard.

    return:
    1 if the card is valid
    2 if the card is the thing
    4 if the player is infected and have only one infection card

    raise:
    400 if there is a ploblem with the card and the player

    """
    if card.player != player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Card {card.id} not belongs to player {player.id}",
        )
    #caso si si intentan descartar la carta de la cosa
    if card.type == "LaCosa":
        return ChangeValidation(type= TipeEnum.tipe_2, description="No se puede descartar la carta de la cosa")
    
    #caso si el jugador esta infectado
    elif player.status == PlayerStatus.infected and card.type == "Infeccion":
        count = 0
        for card in player.cards:
            if card.type == "Infeccion":
                count += 1

        if count == 1:
            return ChangeValidation(type = TipeEnum.tipe_4, description="No se puede descartar la unica carta de infeccion que tiene")
        
        elif count >= 2:
            return ChangeValidation(type = TipeEnum.tipe_1, description="Se puede descartar la carta")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Player {player.id} have negative infection cards",
            )
    
    return ChangeValidation(type= TipeEnum.tipe_1, description="Se puede descartar la carta")

#funtion to verify if the card is valid for a change
def verify_card_change(card, player):
    """
    Verify if the card is valid for a change.

    return:
    1 if the card is valid
    2 if the card is the thing
    3 if the player is human and the card is infection
    4 if the player is infected and have only one infection card

    raise:
    400 if there is a ploblem with the card and the player

    """
    if card.player != player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Card {card.id} not belongs to player {player.id}",
        )
    #caso si intentan intercambiar la carta de la cosa
    if card.type == "LaCosa":
        return ChangeValidation(type= TipeEnum.tipe_2, description="No se puede intercambiar la carta de la cosa")
    
    #caso si el jugador es humano y intenta intercambiar una carta de infeccion
    elif player.status == PlayerStatus.human and card.type == "Infeccion":
        return ChangeValidation(type = TipeEnum.tipe_3, description="No se puede intercambiar una carta de infeccion si eres humano")
    
    #caso si el jugador esta infectado
    elif player.status == PlayerStatus.infected and card.type == "Infeccion":
        count = 0
        for card in player.cards:
            if card.type == "Infeccion":
                count += 1

        if count == 1:
            return ChangeValidation(type = TipeEnum.tipe_4, description="No se puede intercambiar la unica carta de infeccion que tiene")
        
        elif count >= 2:
            return ChangeValidation(type = TipeEnum.tipe_1, description="Se puede intercambiar la carta")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Player {player.id} have negative infection cards",
            )
    
    return ChangeValidation(type= TipeEnum.tipe_1, description="Se puede intercambiar la carta")

#funtion to get all the cards of a player that are changeable
def get_changeable_cards(player):
    """
    Get all the cards of a player that are changeable.

    """
    changeable_cards = []
    for card in player.cards:
        change_verification = verify_card_change(card, player)
        if change_verification.type == TipeEnum.tipe_1:
            changeable_cards.append(card.id)
    return sorted(changeable_cards)

#funtion to verify if there is a infection during a change
def verify_infection(player, card):
    """
    Verify if there is a infection during a change.

    """
    if player.status == PlayerStatus.human and card.type == "Infeccion":
        player.status = PlayerStatus.infected
        return True
    return False

#funtion to impact the change of a card
def impact_change(player_from, player_to, card):
    """
    Impact the change of a card.

    """
    #desasocio la carta del jugador
    card.player = None
    player_from.cards.remove(card)
    #asocio la carta al jugador
    assign_card_to_player(player_to, card)
    constraint_check(card)
    return {f"Carta {card.id} cambiada con exito"}

#funtion to veryfy if the card is valid for defense
def verify_card_defense(card1, card2):
    """
    Verify if the card is valid for defense.
    """

    if card1.type == "Lanzallamas" and card2.type == "NadaDeBarbacoas":
        return True
    elif (card1.type == "MasValeQueCorras" or card1.type == "CambioDeLugar") and card2.type == "AquíEstoyBien":
        return True
    elif card1.type == "Seduccion" and (card2.type == "Aterrador" or card2.type == "NoGracias" or card2.type == "Fallaste"):
        return True

    return False

#funtion to get all the cards of a player that are defenseable
def get_defenseable_cards(player, card):
    """
    Get all the cards of a player that are defenseable.

    """
    defenseable_cards = []
    for card2 in player.cards:
        defense_verification = verify_card_defense(card, card2)
        if defense_verification:
            defenseable_cards.append(card2.id)
    return sorted(defenseable_cards)