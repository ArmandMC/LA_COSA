"""Defines Card endpoints."""
from typing import List
from pony.orm import db_session, select
from game.card.models import Card
from game.player.models import Player
from .schemas import *
from game.game.models import Game
from game.game_status.models import Estado_de_juego
from .efects import apply_efect
from .utils import *
from game.deckCards.utils import  take_card_from_deck, discard_card
from game.game_status.utils import next_turn_phase , check_turn_and_phase , is_game_over , hay_puerta_atrancada
from game.deckCards.models import GameCards
from utils import manager



from fastapi import APIRouter, HTTPException, status

Card_router = APIRouter()

@Card_router.post('/discard_card/{player_id}/{card_id}', status_code=status.HTTP_200_OK)
async def discard_card_end(player_id: int, card_id: int):

    with db_session:
        # Verificar si la tarjeta y el jugador existen
        card = Card.get(id=card_id)
        player = Player.get(id=player_id)

        if not card or not player:
            raise HTTPException(status_code=404, detail='Carta o jugador no encontrados')

        # Verificar si la tarjeta está asociada al jugador
        if card.player != player:
            raise HTTPException(status_code=400, detail='La Carta no pertenece al jugador')

        # Verificar que sea el turno del jugador y su fase
        check_turn_and_phase(Player.get(id=player_id).game.id, player_id, 2)

        #verificar que la carta sea descartable
        change_verification = verify_card_discard(card, player)
        if change_verification.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification.description)

        discard_card(card)

        #guardamos la carta que jugamos
        player.card_to_play = card.id

        #checkeamos si esta en cuarentena, si esta en cuarentena aplicamos el trigger_quarantine
        if player.in_quarantine:
            await manager.trigger_quarantine(player.game.id, player.id)


        #posible cambio de fase
        next_turn_phase(player.game.id)

        await manager.trigger_game_status(player.game.id)
        await manager.trigger_player_status(player.game.id , player.id)
        
        return  {"message": "Carta desligada y marcada como descartada"}

@Card_router.post("/play_card1", status_code=status.HTTP_200_OK)
async def play_card1(play_card: PlayCard):

    with db_session:
        # Buscar la partida, el jugador y la carta en la base de datos
        game = Game.get(id=play_card.id_game).id
        player = Player.get(id=play_card.id_player)
        
        status = Estado_de_juego.get(IdGame=game)

        if not game or not player or not status:
            raise HTTPException(status_code=404, detail="Partida o jugador no encontrado")
        
        if status.no_defense and play_card.id_card != player.card_to_play:
            raise HTTPException(status_code=400, detail="No se jugo la carta que se debia jugar")
        
        card = Card.get(id=play_card.id_card)
        if not card:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        
        # Verificar si es el turno del jugador y su phase
        check_turn_and_phase(game, player.id, 2)

        # Verifica que el jugador tenga la carta
        if card not in player.cards:
            raise HTTPException(status_code=400, detail="El jugador no tiene la carta")
        
        # verificar que la carta sea jugable
        
        #si es carta de hacha se pasa el id del obstaculo a destruir como player to
        if card.type == "Hacha":
            obstaculo = player_to
        elif status.in_defense and play_card.id_player_to != player.player_to:
            raise HTTPException(status_code=400, detail="No se le jugo la carta al jugador que se debia jugar")
        else:
            player_to = Player.get(id=play_card.id_player_to)
            
            if not player_to:
                raise HTTPException(status_code=404, detail="Jugador no encontrado")
            
            
        #fijarse que el player to este vivo
        if player_to.status == PlayerStatus.dead or player_to.status == PlayerStatus.notDefined:
            raise HTTPException(status_code=400, detail=f"El jugador {player_to.id} está muerto")


        #guardamos que carta se juega
        player.card_to_play = card.id

        #checkeamos si esta en cuarentena, si esta en cuarentena aplicamos el trigger_quarantine
        if player.in_quarantine:
            await manager.trigger_quarantine(player.game.id, player.id)

        #si el jugador no se defendio, no se vuelve a hacer el chequeo
        if not status.no_defense:
            # verificar que si el player to tiene una carta de defensa
            def_cards = get_defenseable_cards(player_to, card)
            if def_cards != [] and player.id != player_to.id and not card.change:
                # mandar notificacion al player to
                print("se setea el in defense en play card 1")
                status.in_defense = True
                await manager.send_defense_solicitude(game, player.id, player_to.id, def_cards)
                return {"message": "se esta esperando la respuesta del jugador 2"}

        #Aplica el efecto de la carta
        effect_result = apply_efect(card, game, play_card.id_player, play_card.id_player_to)

        #falta descartar carta si es que se aplico el efecto
        if not effect_result["succes"]:
            return effect_result

        #aca vamos a checkear si la carta jugada es Whisky 
        if card.type == "Whisky":
            await manager.trigger_whisky(game, player.id)

        #si el jugador no se defendio, y se jugo una carta de seduccion, no deberia de estar en esta parte
        if not status.no_defense:
            #se corta la ejecucion para que el jugador activo pueda seleccionar que carta intercambiar
            #aca vamos a checkear si es Seduccion
            if card.type == "Seduccion":
                discard_card(card)
                #guardo con quien se va a intercambiar
                player.change_with = player_to.id
                await manager.trigger_seduccion(game, player.id, player_to.id)
                return effect_result
        else:
            if card.type == "Seduccion":
                raise HTTPException(status_code=400, detail="No deberia entrar nunca aca")

        game_over = is_game_over(game)
        if game_over:
            print("El juego ha terminado.")
        
        #ver la forma de descartar la carta cuando se juegue aunque se juegue o no la carta de defensa
        discard_card(card)
        next_turn_phase(player.game.id)

        #resetear el in_defense del estado de juego
        status.no_defense = False
        #resetear player to del player
        player.player_to = -1


        await manager.trigger_game_status(player.game.id)
        if player.id != player_to.id:
            await manager.trigger_player_status(player.game.id , player_to.id)
        await manager.trigger_player_status(player.game.id , player.id)

        return effect_result

#play card 2
@Card_router.post("/play_card2", status_code=status.HTTP_200_OK)
async def play_card2(play_card: PlayCard2):
    """
    Play a card as response of other card played

    Parameters
    ----------
    PlayCard2
        id_player: int
        id_player_to: int
        id_card_2: int
        defense: bool

    Returns
    -------

    Raises
    ------
    HTTPException

    """ """"""
    with db_session:
        # Buscar la partida, el jugador y la carta en la base de datos
        player = Player.get(id=play_card.id_player)
        player_to = Player.get(id=play_card.id_player_to)
        card_1 = Card.get(id=player.card_to_play)
        status = Estado_de_juego.get(IdGame=player.game.id)

        if status.no_defense or not status.in_defense:
            raise HTTPException(status_code=400, detail="No se puede jugar una carta de defensa en este momento")
        
        
        try:
            card_2 = Card.get(id=play_card.id_card_2)
        except Exception:
            card_2 = None

        game = Game.get(id=player.game.id)
        game_status = Estado_de_juego.get(IdGame=player.game.id)

        if not game or not player or not player_to or not card_1 or not game_status:
            raise HTTPException(status_code=404, detail="Partida, jugador o carta no encontrado")
        # Verificar si es el turno del jugador y su phase
        check_turn_and_phase(game.id, player.id, 2)

        #caso que el player to no quiera defenderse
        if (not play_card.defense):
            if card_1.type == "seduccion":
                response = await manager.send_exchange_solicitude_seduccion(player.game.id, player.id, player_to.id)
                return {"exchange": "solicitude sent"}
            else:
                status.in_defense = False
                status.no_defense = True
                player.player_to = player_to.id
                await manager.trigger_play_again(game.id, player.id, player_to.id, card_1.id)
                return {"message": "El jugador no se defendio"}

        # Verifica que el jugador tenga la carta
        if card_2 not in player_to.cards:
            raise HTTPException(status_code=400, detail="El jugador 2 no tiene la carta")

        # verificar si el player to esta vivo

        # verificar que la defensa sea valida
        if(not verify_card_defense(card_1, card_2)):
            raise HTTPException(status_code=400, detail="La carta no es valida para defenderse")

        #Aplica el efecto de la carta
        effect_result = apply_efect(card_2, game, play_card.id_player, play_card.id_player_to)

        #take a card from the deck
        deck = GameCards.get(id=game.id)
        last_card = take_card_from_deck(deck)

        #assign the card to the player
        assign_card_to_player(player_to, last_card)


        #CARTA DE FALLASTE
        #se jugo una carta de defensa que hace que no se aplique la infeccion
        if not game_status.apply_infection:
            #chequear si hay una carta de obstaculo en la siguiente posicion
            #
            #
            #
            #
            #
            
            #caso hay obstaculos
            if not (False):
                #triger para que el player to haga intercambio con siguiente jugador del player to
                #le pasamos el id del siguiente al player to
                discard_card(card_2)
                
                next_player = effect_result["next_player"]
                player_to = Player.get(id=next_player)
                if not player_to:
                    raise HTTPException(status_code=404, detail="Jugador no encontrado")
                
                player.change_with = player_to.id
                # verificar que si el player to tiene una carta de defensa
                def_cards = get_defenseable_cards(player_to, card_1)
                if def_cards != []:
                    print("se setea el in defense en play card 2")
                    # mandar notificacion al player to
                    status.in_defense = True
                    await manager.send_defense_solicitude(game, player.id, player_to.id, def_cards)
                    return effect_result
                
                #si no tiene seguimos con el intercambio
                else:
                    status.in_defense = False
                    await manager.send_exchange_solicitude(game, player.id, player_to.id)
                return effect_result



        #finalizo el turno si se juega una carta de seduccion
        if card_1.type == "Seduccion":
            status.Fase_de_turno = 3
            status.seduccion = False

        #MEJORAR ESTO---------------------------------------------------------------
        #falta descartar carta si es que se aplico el efecto
        if effect_result["succes"]:
            if card_1.type != "Seduccion":
                discard_card(card_1)
            discard_card(card_2)
        #-----------------------------------------------------------------------------

        next_turn_phase(game.id)

        
        #resetear el in_defense del estado de juego
        status.in_defense = False
        #resetear card to play del player
        player.card_to_play = -1
        #resetear in change with del player
        player.change_with = -1
        
        await manager.trigger_game_status(player.game.id)
        if player.id != player_to.id:
            await manager.trigger_player_status(player.game.id , player_to.id)
        await manager.trigger_player_status(player.game.id , player.id)

        if card_1.type == "seduccion":
            await manager.trigger_turn_finished(player.game.id , player.id)

        return effect_result

#endpoint to steal a card for a player
@Card_router.post("/steal_card/{player_id}", status_code=status.HTTP_200_OK)
async def steal_card(player_id: int):
    """
    Steal a card for a player

    Parameters
    ----------
    player_id : int

    Returns
    -------
    CardResponse
        id: int
        type: str
        number: int
        description: str

    Raises
    ------
    HTTPException
        403 -> When player is not the turn player or is not the phase
        404 -> When player is not found
    """
    with db_session:
        player = Player.get(id=player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        # Check if it's the turn of the player and their phase
        check_turn_and_phase(player.game.id, player.id, 1)

        # Take a card from the deck
        deck = GameCards.get(id=player.game.id)
        last_card = take_card_from_deck(deck)

        # Assign the card to the player
        assign_card_to_player(player, last_card)

        card = CardResponse(id=last_card.id, type=last_card.type, number=last_card.number, description=last_card.description)

        player.card_to_steal = last_card.id

        #checkeamos si esta en cuarentena, si esta en cuarentena aplicamos el trigger_quarantine
        if player.in_quarantine:
            await manager.trigger_quarantine(player.game.id, player.id)
        
        
        # Possible change of phase
        next_turn_phase(player.game.id)

        await manager.trigger_game_status(player.game.id)
        await manager.trigger_player_status(player.game.id, player.id)
        
        return card


# endpoint to get all cards of a player that can be changed
@Card_router.get("/change/{player_id}", status_code=status.HTTP_200_OK)
def get_cards_to_change(player_id: int) -> List[int]:
    """
    Get all cards of a player that can be changed

    Parameters
    ----------
    player_id : int

    Returns
    -------
    List[int]
        list of cards id

    Raises
    ------
    HTTPException
        404 -> When player is not found
    """ """"""
    with db_session:
        player = Player.get(id=player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        #devolver las cartas disponibles
        cards = get_changeable_cards(player)
        return cards


# endpoint to change a card whit other player
@Card_router.post("/change1", status_code=status.HTTP_200_OK)
async def change_card_1(ChangeC: ChangeCard1):
    """
    Change a card with another player

    Parameters
    ----------
    player_id : int
    player_to_id : int
    card_id : int

    Returns
    -------

    Raises
    ------
    HTTPException
        400 -> When some card is not valid or player is not valid
        403 -> When player is not the turn player or is not the phase
        404 -> When player is not found or card is not found
    """ """"""

    with db_session:
        print(f"el jugador {ChangeC.player_id} quiere cambiar la carta {ChangeC.card_id} con el jugador {ChangeC.player_to_id}")
        player = Player.get(id=ChangeC.player_id)
        player_to = Player.get(id=ChangeC.player_to_id)

        if not player or not player_to:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        card = Card.get(id=ChangeC.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        
        #fijarse que el player to este vivo
        if player_to.status == PlayerStatus.dead or player_to.status == PlayerStatus.notDefined:
            raise HTTPException(status_code=400, detail=f"El jugador {player_to.id} está muerto")
        
        #fijarse que sea la fase del turno y el turno del jugador
        check_turn_and_phase(player.game.id, player.id, 3)

        #checkeamos si hay puerta atrancada entre los jugadores y pasamos a la proxima fase
        # if hay_puerta_atrancada(player, player_to):
        #     next_turn_phase(player.game.id)
        #     raise HTTPException(status_code=400, detail="Hay una puerta atrancada entre los jugadores")
        

        estado = Estado_de_juego.get(IdGame=player.game.id)
        #fijarse que sea el siguente jugador
        if estado.Sentido:
            if (player.position + 1) % estado.players_alive != player_to.position:
                raise HTTPException(status_code=400, detail="El jugador con el que se quiere intercambiar no es el siguiente jugador")
        else:
            if (player.position - 1) % estado.players_alive != player_to.position:
                raise HTTPException(status_code=400, detail="El jugador con el que se quiere intercambiar no es el siguiente jugador")
        
        #fijarse que sea valida la carta
        change_verification = verify_card_change(card, player)

        if change_verification.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification.description)

        #guardamos en el player la carta que quiere cambiar
        player.card_to_change = card.id

        #checkeamos si esta en cuarentena, si esta en cuarentena aplicamos el trigger_quarantine
        if player.in_quarantine:
            await manager.trigger_quarantine(player.game.id, player.id)

        response = await manager.send_exchange_solicitude(player.game.id, player.id, player_to.id)
        return {"exchange": "solicitude sent"}



 
# endpoint to change a card whit other player
@Card_router.post("/change2", status_code=status.HTTP_200_OK)
async def change_card_2(ChangeC2: ChangeCard2):
    """
    Change a card with player who proposed the change

    Parameters
    ----------
    player_id : int
    player_to_id : int
    card_id2 : int
    
    Returns
    -------

    Raises
    ------
    HTTPException
        400 -> When some card is not valid or player is not valid
        403 -> When player is not the turn player or is not the phase
        404 -> When player is not found or card is not found
    """ """"""
    with db_session:
        player = Player.get(id=ChangeC2.player_id)
        player_to = Player.get(id=ChangeC2.player_to_id)


        if not player or not player_to:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        
        #busco del player la carta que quiere cambiar
        card1 = Card.get(id=player.card_to_change)
        card2 = Card.get(id=ChangeC2.card_id2)

        if not card1 or not card2:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        
        #fijarse que el player to este vivo
        if player_to.status == PlayerStatus.dead or player_to.status == PlayerStatus.notDefined:
            raise HTTPException(status_code=400, detail=f"El jugador {player_to.id} está muerto")
        
        #fijarse que sea la fase del turno y el turno del jugador
        check_turn_and_phase(player.game.id, player.id, 3)

        estado = Estado_de_juego.get(IdGame=player.game.id)
        #fijarse que sea el siguente jugador
        if estado.Sentido:
            if (player.position + 1) % estado.players_alive != player_to.position:
                raise HTTPException(status_code=400, detail="El jugador con el que se quiere intercambiar no es el siguiente jugador")
        else:
            if (player.position - 1) % estado.players_alive != player_to.position:
                raise HTTPException(status_code=400, detail="El jugador con el que se quiere intercambiar no es el siguiente jugador")
        
        #fijarse que sea valida la carta
        change_verification1 = verify_card_change(card1, player)
        change_verification2 = verify_card_change(card2, player_to)

        if change_verification1.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification1.description)
        if change_verification1.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification2.description)
        
        ## chequeado
        change_data = ChangeCardResponse (  id_player_1 = player.id,
                                    id_player_2 = player_to.id,
                                    id_card1 = card1.id,
                                    id_card2= card2.id)
        
        #si el jugador esta infectado y intenta intercambiar una carta de infeccion, solo puede intercambiar con la cosa
        if player.status == PlayerStatus.infected and card1.type == "Infeccion" and player_to.status != PlayerStatus.theThing:
            raise HTTPException(status_code=400, detail="intentar hacer el cambio de nuevo")
        elif player_to.status == PlayerStatus.infected and card2.type == "Infeccion" and player.status != PlayerStatus.theThing:
            raise HTTPException(status_code=400, detail="intentar hacer el cambio de nuevo")
        
        #realizar el intercambio
        impact_change(player_from=player, player_to=player_to, card=card1) #asigna la carta 1 a player 2 y la saca de player 1
        impact_change(player_from=player_to, player_to=player, card=card2) #asigna la carta 2 a player 1 y la saca de player 2

        #cambiar el estado del player si se realizo una infeccion
        verify_infection(player, card2)
        verify_infection(player_to, card1)

        #realizar el cambio de fase
        next_turn_phase(player.game.id)

        #reseteo el change card del player
        player.card_to_change = -1

        #ejecutar el trigger
        await manager.trigger_game_status(player.game.id)
        await manager.trigger_player_status(player.game.id , player.id)
        await manager.trigger_exchange_fished(player.game.id , player.id)
        await manager.trigger_player_status(player.game.id , player_to.id)

        await manager.trigger_turn_finished(player.game.id , player.id)
        
        return {"exchange": "succes"}

# endpoint to change a card whit other player
@Card_router.post("/change_in_play_1", status_code=status.HTTP_200_OK)
async def change_in_play_1(ChangeC: ChangeCard1):
    """
    Change a card with another player

    Parameters
    ----------
    player_id : int
    player_to_id : int
    card_id : int

    Returns
    -------

    Raises
    ------
    HTTPException
        400 -> When some card is not valid or player is not valid
        403 -> When player is not the turn player or is not the phase
        404 -> When player is not found or card is not found
    """ """"""

    with db_session:
        print(f"el jugador {ChangeC.player_id} quiere cambiar la carta {ChangeC.card_id} con el jugador {ChangeC.player_to_id}")
        player = Player.get(id=ChangeC.player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        
        if player.change_with != ChangeC.player_to_id:
            raise HTTPException(status_code=400, detail="No se esta cambiando con el jugador correcto")
        
        status = Estado_de_juego.get(IdGame=player.game.id)

        if status.no_defense:
            raise HTTPException(status_code=400, detail="No se puede hacer esto en este momento")
        
        if status.in_defense:
            raise HTTPException(status_code=400, detail=f"Se esta esperando la respuesta del jugador")
        
        player_to = Player.get(id=ChangeC.player_to_id)
        if not player_to:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")
        
        card = Card.get(id=ChangeC.card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        
        #fijarse que el player to este vivo
        if player_to.status == PlayerStatus.dead or player_to.status == PlayerStatus.notDefined:
            raise HTTPException(status_code=400, detail=f"El jugador {player_to.id} está muerto")
        
        #fijarse que sea la fase del turno y el turno del jugador
        check_turn_and_phase(player.game.id, player.id, 2)

        #checkeamos si hay puerta atrancada entre los jugadores y pasamos a la proxima fase
        # if hay_puerta_atrancada(player, player_to):
        #     next_turn_phase(player.game.id)
        #     raise HTTPException(status_code=400, detail="Hay una puerta atrancada entre los jugadores")

        #fijarse que sea valida la carta
        change_verification = verify_card_change(card, player)

        if change_verification.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification.description)

        #guardamos en el player la carta que quiere cambiar
        player.card_to_change = card.id

        #checkeamos si esta en cuarentena, si esta en cuarentena aplicamos el trigger_quarantine
        if player.in_quarantine:
            await manager.trigger_quarantine(player.game.id, player.id)
        

        #verificar que si el player to tiene una carta de defensa
        card_played = Card.get(id=player.card_to_play)
        def_cards = get_defenseable_cards(player_to, card_played)
        if def_cards != [] :
            print("se setea el in defense en cange in play 1")
            # mandar notificacion al player to
            status.in_defense = True
            await manager.send_defense_solicitude(player.game.id, player.id, player_to.id, def_cards)
            return {"message": f"se esta esperando la respuesta del jugador"}
        




        #se deberia de guardar el player to id para hacer chequeos en el play card 2
        
        response = await manager.send_exchange_solicitude_seduccion(player.game.id, player.id, player_to.id)

        return {"exchange": "solicitude sent"}



 
# endpoint to change a card whit other player
@Card_router.post("/change_in_play_2", status_code=status.HTTP_200_OK)
async def change_in_play_2(ChangeC2: ChangeCard2):
    """
    Change a card with player who proposed the change

    Parameters
    ----------
    player_id : int
    player_to_id : int
    card_id2 : int
    
    Returns
    -------

    Raises
    ------
    HTTPException
        400 -> When some card is not valid or player is not valid
        403 -> When player is not the turn player or is not the phase
        404 -> When player is not found or card is not found
    """ """"""
    with db_session:
        player = Player.get(id=ChangeC2.player_id)

        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        status = Estado_de_juego.get(IdGame=player.game.id)

        if status.in_defense:
            raise HTTPException(status_code=400, detail="Se esta esperando la respuesta del jugador")
        
        # if status.no_defense:
        #     raise HTTPException(status_code=400, detail="No se puede hacer esto en este momento")
        #     return {"message": "No se puede hacer esto en este momento"}
        
        if player.change_with != ChangeC2.player_to_id:
            raise HTTPException(status_code=400, detail="No se esta cambiando con el jugador correcto")
        
        player_to = Player.get(id=ChangeC2.player_to_id)
        
        #busco del player la carta que quiere cambiar
        card1 = Card.get(id=player.card_to_change)
        card2 = Card.get(id=ChangeC2.card_id2)

        if not card1 or not card2:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        
        #fijarse que el player to este vivo
        if player_to.status == PlayerStatus.dead or player_to.status == PlayerStatus.notDefined:
            raise HTTPException(status_code=400, detail=f"El jugador {player_to.id} está muerto")
        
        #fijarse que sea la fase del turno y el turno del jugador
        check_turn_and_phase(player.game.id, player.id, 2)

        #fijarse que sea valida la carta
        change_verification1 = verify_card_change(card1, player)
        change_verification2 = verify_card_change(card2, player_to)

        if change_verification1.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification1.description)
        if change_verification1.type != TipeEnum.tipe_1:
            raise HTTPException(status_code=400, detail=change_verification2.description)
        
        ## chequeado
        change_data = ChangeCardResponse (id_player_1 = player.id,
                                    id_player_2 = player_to.id,
                                    id_card1 = card1.id,
                                    id_card2= card2.id)
        
        #si el jugador esta infectado y intenta intercambiar una carta de infeccion, solo puede intercambiar con la cosa
        if player.status == PlayerStatus.infected and card1.type == "Infeccion" and player_to.status != PlayerStatus.theThing:
            raise HTTPException(status_code=400, detail="intentar hacer el cambio de nuevo")
        elif player_to.status == PlayerStatus.infected and card2.type == "Infeccion" and player.status != PlayerStatus.theThing:
            raise HTTPException(status_code=400, detail="intentar hacer el cambio de nuevo")
        
        #realizar el intercambio
        impact_change(player_from=player, player_to=player_to, card=card1) #asigna la carta 1 a player 2 y la saca de player 1
        impact_change(player_from=player_to, player_to=player, card=card2) #asigna la carta 2 a player 1 y la saca de player 2

        #cambiar el estado del player si se realizo una infeccion
        verify_infection(player, card2)
        verify_infection(player_to, card1)

        
        # chequear que sea una carta de seduccion para finalizar el turno del player
        status = Estado_de_juego.get(IdGame=player.game.id)
        if (status.seduccion):
            status.Fase_de_turno = 3
            status.seduccion = False
    
        #realizar el cambio de fase
        next_turn_phase(player.game.id)
        
        #reseteo el change card del player
        player.card_to_change = -1
        #reseteo el change with del player
        player.change_with = -1

        #ejecutar el trigger
        await manager.trigger_game_status(player.game.id)
        await manager.trigger_player_status(player.game.id , player.id)
        await manager.trigger_exchange_fished(player.game.id , player.id)
        await manager.trigger_player_status(player.game.id , player_to.id)

        return {"exchange": "succes"}



# endpoint to view all cards of a player
@Card_router.get("/cards/{player_id}", status_code=status.HTTP_200_OK)
def get_cards(player_id: int) -> List[CardResponse]:
    """
    Get all cards of a player

    Parameters
    ----------
    player_id : int

    Returns
    -------
    List[CardResponse]
        list of cards

    Raises
    ------
    HTTPException
        404 -> When player is not found
    """ """"""
    with db_session:
        player = Player.get(id=player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        card_played = Card.get(id=player.card_to_play)
        if not card_played:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
        if card_played.type != "Whisky":
            raise HTTPException(status_code=400, detail="La carta que se jugo no es Whisky")

        cards = []
        for card in player.cards:
            cards.append(CardResponse(id=card.id, type=card.type, number=int(card.number), description=card.description))

    return cards

#endpoint para mostrar una carta dependiendo de la fase del turno (en la primera fase, mostrar que carta robo, en la segunda fase
# que carta jugo o descarto y en la tercera fase que carta cambio)
@Card_router.get("/show_card/{player_id}", status_code=status.HTTP_200_OK)
def get_card(player_id: int) -> CardResponse:
    """
    Get the card of a player depending on the phase

    Parameters
    ----------
    player_id : int

    Returns
    -------
    CardResponse
        card

    Raises
    ------
    HTTPException
        404 -> When player is not found
    """ """"""
    with db_session:
        player = Player.get(id=player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Jugador no encontrado")

        #corroborar en que fase esta el jugador para ver que carta mostrar
        status = Estado_de_juego.get(IdGame=player.game.id)
        #fase uno, mostrar la carta que robo
        if status.Fase_de_turno == 1:
            card = Card.get(id=player.card_to_steal)
        #fase 2, mostrar que carta jugo o descarto
        elif status.Fase_de_turno == 2:
            card = Card.get(id=player.card_to_play)
        #fase 3, mostrar que carta cambio
        elif status.Fase_de_turno == 3:
            card = Card.get(id=player.card_to_change)
        else:
            raise HTTPException(status_code=400, detail="No se puede mostrar la carta en este momento")
    
        if not card:
            raise HTTPException(status_code=404, detail="Carta no encontrada")
    
        card_response = CardResponse(id=card.id, type=card.type, number=int(card.number), description=card.description)

    return card_response