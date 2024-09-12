from pony.orm import db_session, select, commit 

from game.player.utils import change_status
from game.card.utils import disassociate_cards
from game.game_status.utils import take_out_of_round , are_adjacent_players, update_next_player, update_next_player_no_change, hay_puerta_atrancada
from game.player.models import PlayerStatus , Player
from game.game_status.models import Estado_de_juego 
from game.card.models import *

import sys



#aplicar efecto de la carta
@db_session
def apply_efect(card, game, player, player_to):
    function_name = f"{card.type.replace(' ', '_')}"
    
    effect_function = getattr(sys.modules[__name__], function_name, None)
    
    if effect_function:
        return effect_function(card, player, player_to)  # Devuelve el resultado aquí
    else:
        raise Exception(f"No se encontró una función de efecto para la carta: {card.type}")



# efects of the card lanzallamas
# that eliminate the player, it change the estatus in Player
# no hago chequeos porque se supone que para este punto no habria problemas
def Lanzallamas(card, player_id, player_to_id):
    """
    Eliminate the player, it change the estatus in Player.

    """

    #checkeamos que no este en cuarentena el jugador que quiere jugar el lanzallamas o que no haya puerta atrancada entre los 2 players
    if Player.get(id=player_id).in_quarantine:
        return {"succes": False , "message": "No se puede jugar lanzallamas estando en cuarentena"}
    if hay_puerta_atrancada(Player.get(id=player_id), Player.get(id=player_to_id)):
        return {"succes": False , "message": "No se puede jugar lanzallamas con una puerta atrancada entre los jugadores"}
    
    #change the estatus of the player to eliminated
    change_status(player_to_id, PlayerStatus.dead)
    #disassociate all the cards of the player
    disassociate_cards(player_to_id)
    #take out of the round the player
    take_out_of_round(player_to_id)
    return {"succes": True , "message": "Carta lanzallamas aplicada"}

def Empty(card, player, player_to):
    return {"succes": True , "message": "Carta en blanco aplicada"}

def VigilaTusEspaldas(card, player, player_to):
    """
    Invert the order of the game. So if the turn passed to the left, now it does to the right.
    This affects both the order of turns and the exchanges of cards.

    """
    #cambiar el orden del juego con el metodo de game_status
    player_obj = Player.get(id=player)
    game_status = Estado_de_juego.get(IdGame=player_obj.game.id)
    game_status.Sentido = not game_status.Sentido
    update_next_player_no_change(card.player.game.id)
    return {"succes": True , "message": "Carta vigila tus espaldas aplicada"}



def CambioDeLugar(card, player, player_to):
    """
    Change the place physically with a player that you have next to you,
    unless an obstacle like "Quarantine" or "Locked door" prevents you from doing so,
    Take your hand of cards when you change places. Then, exchange 1 card with the
    next player from your new location and end your turn. The next turn
    begins with the player with whom you have made the exchange, following the 
    active game order.

    """
    player1 = Player.get(id=player)
    player2 = Player.get(id=player_to)

    #verificamos que el jugador player_to no este en cuarentena
    if player2.in_quarantine or player1.in_quarantine:
        return {"succes": False , "message": "No se puede cambiar de lugar con alguien en cuarentena"}
    #verificamos que no haya puerta atrancada entre los 2 players
    if hay_puerta_atrancada(player1, player2):
        return {"succes": False , "message": "No se puede cambiar de lugar con una puerta atrancada entre los jugadores"}

    #cambiar el lugar fisicamente con una persona que este al lado 
    if are_adjacent_players(player1, player2): 
        player1.position, player2.position = player2.position, player1.position

        with db_session:
            game_status = Estado_de_juego.get(IdGame=player1.game.id)
            game_status.next_player = player2.id

        return {"succes": True , "message": "Carta cambio de lugar aplicada"}
    else:
        return {"succes": False ,"message": "No se puede cambiar de lugar con esa persona"} #aca ver que no se juege la carta!
    


def MasValeQueCorras(card, player, player_to):
    """
    Change the place physically with a player ,
    unless an obstacle like "Quarantine" or "Locked door" prevents you from doing so,
    Take your hand of cards when you change places. Then, exchange 1 card with the
    next player from your new location and end your turn. The next turn
    begins with the player with whom you have made the exchange, following the  fer posicion 3 y yo 2, id fer 3 id yo 1
    active game order.

    """
    player1 = Player.get(id=player)
    player2 = Player.get(id=player_to)

    #verificamos que no el player_to y player no este en cuarentena
    if player2.in_quarantine or player1.in_quarantine:
        return {"succes": False , "message": "No se puede cambiar de lugar con alguien en cuarentena"}

    #cambiar el lugar fisicamente con cualquier persona
    player1.position, player2.position = player2.position, player1.position

    with db_session:
        game_status = Estado_de_juego.get(IdGame=player1.game.id)
        game_status.next_player = player2.id
    
    return {"succes": True ,"message": "Carta mas vale que corras aplicada"}


def Seduccion(card, player, player_to):
    """
    Exchange 1 card with any player who is not in Quarantine and
    then end your turn.

    """
    
    # ACA IRIA LA VERIFICACION CUANDO HAGAMOS OBSTACULO
    player = Player.get(id=player)
    status = Estado_de_juego.get(IdGame=player.game.id)
    status.seduccion = True
    
    return {"succes": True , "message": "Carta seduccion aplicada"}


def Analisis(card, player, player_to):
    """
    If you play this card on an adjacent player, he must show you all the cards in his hand.
    """
    player = Player.get(id=player)
    player_to = Player.get(id=player_to)
    #verificamos que el jugador este al lado
    if not are_adjacent_players(player, player_to):
        return {"succes": False , "message": "El jugador no esta al lado"}

    #verificamos que no haya puerta atrancada entre los 2 players
    if hay_puerta_atrancada(player, player_to):
        return {"succes": False , "message": "No se puede jugar analisis con una puerta atrancada entre los jugadores"}

    # obtenemos las cartas del jugador
    cards = player_to.cards
    # Convertimos las cartas en un formato serializable
    serializable_cards = [{"name": card.type, "description": card.description} for card in cards]
    cards_order = sorted(serializable_cards, key=lambda x: x['name'])
    
    # mostramos las cartas del jugador
    return {"succes": True , "message": "Cartas del jugador mostradas", "cards": cards_order}


def Sospecha(card, player, player_to):
    """
    Take 1 random card from an adjacent player, look at it and return it.

    """
    target_player = Player.get(id=player_to)  # Cambiamos la variable a target_player

    # Verificamos que el jugador esté al lado
    if not are_adjacent_players(player, target_player):  # Pasamos player y target_player
        return {"succes": False , "message": "El jugador no esta al lado"}
    
    player_o = Player.get(id=player)
    player_to_o = Player.get(id=player_to)
    #checkeamos si hay una puerta atrancada entre los jugadores
    if hay_puerta_atrancada(player_o, player_to_o):
        return {"succes": False , "message": "No se puede jugar sospecha con una puerta atrancada entre los jugadores"}
    
    # Obtenemos las cartas del jugador objetivo
    cards = target_player.cards
    # Obtenemos una carta aleatoria del jugador y accedemos al primer elemento del resultado
    random_card = cards.random(1)[0]
    # Convertimos la carta a un diccionario serializable
    card_data = {
        "id": random_card.id,
         "name": random_card.type,
        "description": random_card.description
        # Agrega cualquier otro atributo que necesites aquí
    }
    # Mostramos la carta
    return {"succes": True , "message": "Carta del jugador mostrada", "card": card_data}



def Whisky(card, player, player_to):
    """
    Show all your cards to the other players. This card can only be played on yourself.
    """
    return {"succes": True, "message": "Cartas del jugador mostradas"}


def NadaDeBarbacoas(card, player, player_to):
    """
    Sólo puedes jugar esta carta como respuesta a una carta 'Lanzallamas' para evitar ser eliminado de la partida.
    """
    
    return {"succes": True , "message": "Carta nada de barbacoas aplicada"}

def AquíEstoyBien(card, player, player_to):
    """
    Sólo puedes jugar esta carta como respuesta a una carta '¡Cambio de lugar!'' o '¡Más vale que corras!'' para cancelar su efecto.
    """
    
    return {"succes": True , "message": "Carta aqui estoy bien aplicada"}

def NoGracias(card, player, player_to):
    """
    Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta
    """
    
    return {"succes": True , "message": "Carta no gracias aplicada"}

def Fallaste (card, player, player_to):
    """
    Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas.
    Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta.
    El siguiente jugador después de ti (siguiendo el orden de juego) debe intercambiar cartas en lugar de hacerlo tú.
    Si este jugador recibe una carta '¡Infectado!' durante el intercambio, no queda Infectado, ¡pero sabrá que ha recibido una carta de La Cosa o de un jugador Infectado!
    Si hay 'obstáculos' en el camino, como una 'Puerta atrancada' o 'Cuarentena', no se produce ningún intercambio, y el siguiente turno lo jugará el jugador siguiente a aquel que inició el intercambio
    """
    with db_session:
        player = Player.get(id=player)
        player_to = Player.get(id=player_to)
        game = player.game
        game_status = Estado_de_juego.get(IdGame=game.id)
        game_status.apply_infection = False
    
        #QUE PASA SI EL SIGUIENTE JUGADOR SOS VOS?

        #calculamos el siguiente jugador
        if game_status.Sentido:
            next_position = (player_to.position + 1) % game_status.players_alive
            next_player = select(p for p in game.players if p.position == next_position).first()
        else:
            next_position = (player_to.position - 1) % game_status.players_alive
            next_player = select(p for p in game.players if p.position == next_position).first()
        
        if next_player.id == player.id:
            raise Exception("El siguiente jugador no puede ser el mismo que el que jugo la carta")

    return {"succes": True , "message": "Carta fallaste aplicada", "next_player": next_player.id}

def Aterrador (card, player, player_to):
    """
    Sólo puedes jugar esta carta como respuesta a un ofrecimiento de intercambio de cartas.
    Niégate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta. 
    Mira la carta que te has negado a coger y devuélvesela a su dueño.
    """
    with db_session:
        player = Player.get(id=player)
        card = Card.get(id=player.card_to_change)
        
        #reseteo el change card del player
        player.card_to_change = -1
    
    return {"succes": True , "message": "Carta aterrador aplicada", "card": {"card": card.type, "description": card.description}}

def Cuarentena(card, player, player_to):
    """
    Aplica el efecto de la carta Cuarentena a un jugador adyacente.
    """
    player = Player.get(id=player)
    target_player = Player.get(id=player_to)
    #sacar el estado de juego
    game_status = Estado_de_juego.get(IdGame=player.game.id)

    # Verifica que el jugador esté al lado
    if not are_adjacent_players(player, target_player):
        return {"succes": False, "message": "El jugador no está al lado"}
    
    #verificar que no tenga cuarentena ya
    if target_player.in_quarantine:
        return {"succes": False , "message": "No se puede jugar cuarentena con alguien en cuarentena"}
    
    #verificamos que no haya puerta atrancada entre los 2 players
    if hay_puerta_atrancada(player, target_player):
        return {"succes": False , "message": "No se puede jugar cuarentena con una puerta atrancada entre los jugadores"}

    # Aplica el efecto de cuarentena
    with db_session:
        #se crea la carta osbtaculo cuarentena
        CartaObstaculo(nombre='Cuarentena', jugador_izquierda=target_player.id, jugador_derecha=target_player.id, estado_juego=game_status, cuarentena=True)
        target_player.in_quarantine = True
        target_player.quarantine_shifts = 2
        commit()

    return {"succes": True, "message": "El jugador ha sido puesto en cuarentena"}



def PuertaAtrancada(card, player_id, player_to_id):
    """
    Aplica el efecto de la carta Puerta Atrancada entre el jugador y un adyacente.
    """
    player = Player.get(id=player_id)
    player_to = Player.get(id=player_to_id)

    # Verifica que el jugador esté al lado
    if not are_adjacent_players(player, player_to):
        return {"succes": False, "message": "El jugador no está al lado"}

    with db_session:
        game_status = Estado_de_juego.get(IdGame=player.game.id)

        # Decide la dirección de la "Puerta Atrancada" en función de las posiciones de manera circular
        player_positions = [p.position for p in player.game.players]
        player_index = player_positions.index(player.position)
        player_to_index = player_positions.index(player_to.position)
        if player_index < player_to_index:
            # Se juega de izquierda a derecha
            CartaObstaculo(nombre='Puerta Atrancada', jugador_izquierda=player.position, jugador_derecha=player_to.position, estado_juego=game_status, cuarentena=False)
        else:
            # Se juega de derecha a izquierda
            CartaObstaculo(nombre='Puerta Atrancada', jugador_izquierda=player_to.position, jugador_derecha=player.position, estado_juego=game_status, cuarentena=False)

    return {"succes": True, "message": "Puerta Atrancada ha sido colocada entre los jugadores"}


def Hacha(card, player_id, player_to_id=None):
    """
    Aplica el efecto de la carta Hacha para retirar un obstáculo ('Puerta Atrancada' o 'Cuarentena') 
    sobre el jugador o un jugador adyacente.
    """
    player = Player.get(id=player_id)
    
    # Si no se especifica un jugador adyacente, la carta se aplica al propio jugador
    target_player = Player.get(id=player_to_id) if player_to_id else player

    # Verificar si el jugador es adyacente si se proporcionó un jugador adyacente
    if player_to_id and not are_adjacent_players(player, target_player) and not player == target_player:
        return {"succes": False, "message": "El jugador no está al lado"}

    with db_session:
        # Intentar encontrar y eliminar la carta 'Puerta Atrancada' que afecta al jugador objetivo
        obstaculo = CartaObstaculo.get(
            lambda o: 
            (o.jugador_izquierda == target_player.position or o.jugador_derecha == target_player.position) 
            and o.nombre == "Puerta Atrancada"
        )
        
        if obstaculo:
            obstaculo.delete()
            return {"succes": True, "message": "Puerta Atrancada ha sido eliminada por la Hacha"}
        
        # Si no se encontró una 'Puerta Atrancada', intenta retirar el efecto 'Cuarentena' 
        # Nota: Esto asume que tienes un atributo 'in_quarantine' en tu modelo Player. Ajusta según sea necesario.
        elif target_player.in_quarantine:
            target_player.in_quarantine = False
            target_player.quarantine_shifts = 0
            return {"succes": True, "message": "Cuarentena ha sido retirada por la Hacha"}
        else:
            return {"succes": False, "message": "No hay obstáculos para retirar con la Hacha"}