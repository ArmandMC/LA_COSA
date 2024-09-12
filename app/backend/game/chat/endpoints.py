# chat/routers/chat_router.py
from fastapi import APIRouter, HTTPException
from pony.orm import db_session, commit, select
from .models import ChatMessage
from .schemas import ChatMessageCreate, ChatMessageResponse
from utils import manager

Chat_router = APIRouter()

@db_session
def save_chat_message(chat_message: ChatMessageCreate):
    new_message = ChatMessage(**chat_message.dict())
    commit()  # Guardar el nuevo mensaje en la base de datos
    return new_message

@Chat_router.post("/send_message", response_model=ChatMessageResponse)
async def send_chat_message(chat_message: ChatMessageCreate):
    """
    Envia un nuevo mensaje de chat para el juego especificado.

    Args:
        chat_message (ChatMessageCreate): Datos del mensaje de chat.

    Returns:
        ChatMessageResponse: Información sobre el mensaje de chat enviado.
    """
    try:
        new_message = save_chat_message(chat_message)
        #usamos el trigger de chat para avisar que se mando un mensaje
        game_id = chat_message.game_id
        await manager.trigger_chat(game_id)
        return ChatMessageResponse(**new_message.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el mensaje: {str(e)}")
    

@Chat_router.get("/get_messages/{game_id}", response_model=list[ChatMessageResponse])
async def get_chat_messages(game_id: int):
    with db_session:
        messages = select(m for m in ChatMessage if m.game_id == game_id).order_by(ChatMessage.timestamp)
        print("Número de mensajes recuperados:", len(messages))
        #print("Mensajes recuperados:", [message.to_dict() for message in messages])
        return [ChatMessageResponse(**message.to_dict()) for message in messages]



@Chat_router.get("/get_messages_from/{game_id}/{message_id}", response_model=list[ChatMessageResponse])
async def get_chat_messages_from(game_id: int, message_id: int):
    """
    Obtiene todos los mensajes de chat para el juego especificado a partir de un cierto ID.

    Args:
        game_id (int): ID del juego para el cual obtener mensajes de chat.
        message_id (int): ID del mensaje a partir del cual obtener los mensajes.

    Returns:
        list[ChatMessageResponse]: Lista de mensajes de chat ordenados por timestamp.
    """
    with db_session:
        messages = select(m for m in ChatMessage if m.game_id == game_id and m.id >= message_id).order_by(ChatMessage.timestamp)
        return [ChatMessageResponse(**message.to_dict()) for message in messages]