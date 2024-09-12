
from game.deckCards.models import GameCards, DiscardCards
from game.card.models import Card
from game.player.models import Player , PlayerStatus
from pony.orm import db_session, select, commit, delete
from ..card.utils import assign_card_to_player, constraint_check
from ..models.db import db
from game.card.utils import delete_card
from fastapi import HTTPException, status
import os
import random

@db_session
def init_deck_of_cards(quantity_of_players: int, game_id: int):

    if (os.getenv('ENVIRONMENT') == 'test'):
    # Crea un nuevo conjunto de cartas de mazo
        cards = [
            #tengo que modificar el orden del mazo para hacaer que funcionen los test
            
            #agregamos cartas creadas en el sprint 3
            #panico
            {"name": "SoloEntreNosotros", "description": "Muestra todas las cartas de tu mano a un jugador adyacente de tu eleccion",
                    "cards": [4,6,8,11], "change": False},
            
            {"name": "Revelaciones", "description": "Empezando por ti, y siguiendo el orden del juego,"
                    "cada jugador elige si revela o no su mano."
                    "La ronda de 'revelaciones' termina cuando un jugador muestre una carta, 'infeccion',"
                    "sin que tenga que revelar el resto de su mano","cards": [4,6,8,11], "change": False},
            
            {"name": "CitaACiegas", "description": "Intercambia una carta de tu mano con la primera carta del mazo,"
                    "descartando cualquier carta de 'panico' robada. Tu turno termina","cards": [4,6,8,11], "change": False},
            
            {"name": "Oops!", "description": "Muestrales todas las cartas de tu mano a todos los jugadores",
                    "cards": [4,6,8,11], "change": False},
            
            {"name": "CadenasPodridas", "description": "solo para tests","cards": [4,6,8,11], "change": False},
            
            {"name": "RondaYRonda", "description": "solo para tests","cards": [4,6,8,11], "change": False},
            
            {"name": "PodemosSerAmigos?", "description": "solo para tests","cards": [4,6,8,11], "change": False},
            
            {"name": "Olvidadizo", "description": "solo para tests","cards": [4,6,8,11], "change": False},
            
            {"name": "Carta1,2", "description": "solo para tests","cards": [4,6,8,11], "change": False},
            
            {"name": "Carta3,4", "description": "solo para tests","cards": [4,6,8,11], "change": False},

            #obstaculo
            {"name": "Cuarentena","description": "You are in quarantine for 2 turns", "cards": [4,4,4,4,4,4], "change": False},
            {"name": "PuertaAtrancada", "description": "You can't exchange cards with any player for 2 turns",
             "cards": [4,4,4,4], "change": False},
            {"name": "Hacha", "description": "Kill puerta", "cards": [4,4,4,4,4,4,6,9,11], "change": False},

            #defensa
            {"name": "Aterrador", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                 "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta. Mira la carta que te has negado a coger y devuélvesela a su dueño.", "cards": [5,6,8,11], "change": False},
            {"name": "NoGracias", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                 "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta", "cards": [4,6,8,11], "change": False},
            {"name": "Fallaste", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                 "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta."
                 "El siguiente jugador después de ti (siguiendo el orden de juego) debe intercambiar cartas en lugar de hacerlo tú."
                 "Si este jugador recibe una carta '¡Infectado!' durante el intercambio, no queda Infectado, ¡pero sabrá que ha recibido una carta de La Cosa o de un jugador Infectado!"
                 "Si hay 'obstáculos' en el camino, como una 'Puerta atrancada' o 'Cuarentena', no se produce ningún intercambio, y el siguiente turno lo jugará el jugador siguiente a aquel que inició el intercambio", "cards": [4,6,11], "change": False},
            {"name": "AquíEstoyBien", "description": "Sólo puedes jugar esta carta como respuesta a una carta '¡Cambio de lugar!'' o '¡Más vale que corras!'' para cancelar su efecto.", "cards": [4,6,11], "change": False},
            {"name": "NadaDeBarbacoas", "description": "Sólo puedes jugar esta carta como respuesta a una carta 'Lanzallamas' para evitar ser eliminado de la partida.", "cards": [4,6,11], "change": False},

            #agregamos cartas creadas en el sprint 2
            {"name": "Seduccion","description": "Exchange 1 card with any player who is not in Quarantine and then end your turn.", "cards": [4,4,4,4], "change": True},
            {"name": "Sospecha", "description": "Ask for a card", "cards": [4,4,4,4,7,9,10], "change": False},
            {"name": "CambioDeLugar", "description": "Change the place physically with a player that you have next to you", "cards": [4,4,7,9,11], "change": False},
            {"name": "VigilaTusEspaldas", "description": "Invert the order of the game", "cards": [4,9], "change": False},
            {"name": "MasValeQueCorras", "description": "Change the place physically with a player " , "cards": [4,4,7,9,11], "change": False},
            {"name": "Analisis", "description": "Ask for a total of cards", "cards": [5,6,9], "change": False},
            {"name": "Whisky", "description": "Show all your cards to the other players. This card can only be played on yourself." , "cards":[4,6,10], "change": False},
            {"name": "Infeccion", "description": "Esta carta te infecta, solo si la recibes luego de un intercambio de cartas" , "cards": [4,4,4,4,4,4,4,4,6,6,7,7,8,9,9,10,10,11,11,11], "change": False},

            {"name": "Lanzallamas", "description": "Kill player", "cards": [4,4,6,9,11], "change": False},
        ]
    
        #--------------para testeo, sin azarosidad-----------------
        quantity_card = len(cards) * 5 + 1

        la_cosa_card = {"name": "LaCosa", "description": "Tu eres LA COSA", "change": False}
        deck = []

        for i in range(quantity_card - 1):
            deck.append(cards[i % len(cards)])

        deck.append(la_cosa_card)
    else:
    #---------------para jugar con azarosidad------------------
        cards = [
                #tengo que modificar el orden del mazo para hacaer que funcionen los test
                
                #agregamos cartas creadas en el sprint 3
                {"name": "Aterrador", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                    "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta."
                    "Mira la carta que te has negado a coger y devuélvesela a su dueño.", "cards": [5,6,8,11], "change": False},
                {"name": "NoGracias", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                    "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta", "cards": [4,6,8,11], "change": False},
                {"name": "Fallaste", "description": "Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas."
                    "Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta."
                    "El siguiente jugador después de ti (siguiendo el orden de juego) debe intercambiar cartas en lugar de hacerlo tú."
                    "Si este jugador recibe una carta '¡Infectado!' durante el intercambio, no queda Infectado,"
                    "¡pero sabrá que ha recibido una carta de La Cosa o de un jugador Infectado!"
                    "Si hay 'obstáculos' en el camino, como una 'Puerta atrancada' o 'Cuarentena', no se produce ningún intercambio,"
                    "y el siguiente turno lo jugará el jugador siguiente a aquel que inició el intercambio", "cards": [4,6,11], "change": False},
                {"name": "AquíEstoyBien", "description": "Sólo puedes jugar esta carta como respuesta a una carta '¡Cambio de lugar!' o '¡Más vale que corras!'"
                    "para cancelar su efecto.", "cards": [4,6,11], "change": False},
                {"name": "NadaDeBarbacoas", "description": "Sólo puedes jugar esta carta como respuesta a una carta 'Lanzallamas' para evitar ser eliminado de la partida.",
                    "cards": [4,6,11], "change": False},

                #obstaculo
                {"name": "Seduccion", "description": "Exchange 1 card with any player who is not in Quarantine and then end your turn.", "cards": [4,4,4,4], "change": True},
                {"name": "Cuarentena", "description": "You are in quarantine for 2 turns", "cards": [4,4,4,4,4,4], "change": False},
                {"name": "Hacha", "description": "Kill puerta", "cards": [4,4,4,4,4,4,6,9,11], "change": False},
                {"name": "PuertaAtrancada", "description": "You can't exchange cards with any player for 2 turns", "cards": [4,4,4,4,4,4,4,4], "change": False},

                #agregamos cartas creadas en el sprint 2
                {"name": "Sospecha", "description": "Ask for a card", "cards": [4,4,4,4,7,9,10], "change": False},
                {"name": "CambioDeLugar", "description": "Change the place physically with a player that you have next to you", "cards": [4,4,7,9,11], "change": False},
                {"name": "VigilaTusEspaldas", "description": "Invert the order of the game", "cards": [4,9], "change": False},
                {"name": "MasValeQueCorras", "description": "Change the place physically with a player " , "cards": [4,4,7,9,11], "change": False},
                {"name": "Analisis", "description": "Ask for a total of cards", "cards": [5,6,9], "change": False},
                {"name": "Whisky", "description": "Show all your cards to the other players. This card can only be played on yourself." , "cards":[4,6,10], "change": False},
                {"name": "Infeccion", "description": "Esta carta te infecta, solo si la recibes luego de un intercambio de cartas" , "cards": [4,4,4,4,4,4,4,4,6,6,7,7,8,9,9,10,10,11,11,11], "change": False},

                {"name": "Lanzallamas", "description": "Kill player", "cards": [4,4,6,9,11], "change": False},
            ]
        quantity_card = 1
        deck = []
        for card in cards:
            for c in card["cards"]:
                if c <= quantity_of_players:
                    deck.append({"name": card["name"], "description": card["description"], "change": card["change"]})
                    quantity_card += 1

        # Mezcla las cartas
        random.shuffle(deck)

        # Insertamos la carta "La_Cosa" en una de las últimas 4 posiciones
        la_cosa_card = {"name": "LaCosa", "description": "Tu eres la cosa", "change": False}
        # Número total de cartas repartidas al principio
        cards_dealt_at_start = 4 * quantity_of_players

        # Elije una posición aleatoria dentro de las últimas 'cards_dealt_at_start' cartas
        position = random.randint(len(deck) - cards_dealt_at_start, len(deck) - 1)

        deck.insert(position, la_cosa_card)
    #----------------------------------------------------------

    deck_game = GameCards(id = game_id, quantity_card=quantity_card)
    discard_deck = DiscardCards(id = game_id, quantity_card=0)

    # Crea N cartas y las asocia al mazo
    for i, card_info in enumerate(deck):
        card = Card(
            type=card_info["name"],
            number=i+1,
            description=card_info["description"],
            player=None,
            game_deck=deck_game,
            change=card_info["change"]
        )

    # Guarda los cambios en la base de datos
    db.commit()
    return deck_game



@db_session
def deal_cards_to_players(players, deck):

    #esta lista tiene un orden aleatorio, no siempre es el mismo
    #players_list = list(players)  # Convertimos el PlayerSet a una lista

    #esta lista tiene un orden fijo, siempre es el mismo
    players_list = sorted(list(players), key=lambda player: player.id)  # Sort by a unique identifier, like player ID
    len_players = len(players_list)
    #repartimos 4 cartas para cada uno de los jugadores
    for i in range(len_players):
        for j in range(4):
            last_card = take_card_from_deck(deck)
            assign_card_to_player(players_list[i], last_card)

    return {"message": "Cartas asignadas a los jugadores"}

#funtion to take a card from the deck
def take_card_from_deck(deck):
    """
    Take a card from the deck.

    """
    # se entregan primero las cartas con mayor numero
    last_card = deck.cards.select().order_by(Card.number.desc()).first()
    # is important to check the constraint before remove the card
    constraint_check(last_card)
    if last_card:
        deck.cards.remove(last_card)
        # Guarda los cambios en la base de datos
        db.commit()
    else:
        #falta agregar funtion que vuelva a poner las cartas del discard deck en el deck
        raise ValueError("No hay más cartas en el mazo.")
    return last_card

#funtion to discard a card
def discard_card(card):
    """
    Discard a card.

    """
    with db_session:
        if(card.game_deck == None and card.player == None):
            raise ValueError("The card is not in the deck or in the player")
        elif(card.game_deck != None and card.player != None):
            raise ValueError("The card is in the deck and in the player")

        #case when the card comes from the deck
        if (card.game_deck != None):
            discard_deck = DiscardCards.get(id=card.game_deck.id)
            card.game_deck = None

        #case when the card comes from the player
        elif (card.player != None):
            player = Player.get(id=card.player.id)
            discard_deck = DiscardCards.get(id=player.game.id)
            card.player = None
            player.cards.remove(card)

        # es suficiente hacer uno solo de las 2 asignaciones, pony se encarga de linkear las 2, pero por las dudas
        card.discard_deck = discard_deck
        discard_deck.cards.add(card)

        discard_deck.quantity_card += 1
        commit()
        constraint_check(card)
    return "Card discarded"


#funtion to delete all cards of a deck, and the deck
def delete_deck(deck_id):
    """
    Delete all cards of a deck.

    """
    with db_session:
        deck = select(d for d in GameCards if d.id == deck_id).first()
        discard_deck = select(d for d in DiscardCards if d.id == deck_id).first()
        if not deck or not discard_deck:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck {deck_id} not exists",
            )
        for card in deck.cards:
            delete_card(card.id)
        for card in discard_deck.cards:
            delete_card(card.id)
        deck.delete()
        discard_deck.delete()
        commit()
    return "Deck deleted"