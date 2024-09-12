from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
from game.models.db import db
from game.models.converter import EnumConverter
from api import api_router
from constants import DB_PROVIDER, PROJECT_DESCRIPTION, PROJECT_NAME
from settings import settings
from version import __API__VERSION
from utils import manager
import os

app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=__API__VERSION,
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG_MODE,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/version")
async def version():
    """
    gets api version

    Returns
    -------
    Dict
        returns api version
    """
    return {"version": __API__VERSION}


# Including routers
app.include_router(api_router)


@app.websocket("/ws/{gameID}/{userID}")
async def websocket_endpoint(websocket: WebSocket, gameID: int, userID: int):
    await manager.connect_player(websocket, gameID, userID)
    try: 
        while True:
            received_message = await websocket.receive_json()
            received_message_type = received_message.get("type")

            if received_message_type == "exchangeResponse":
                # Handle the exchange response
                await manager.handle_exchange_response(
                    received_message["data"]["player_to_id"],
                    received_message["data"]["card_id"]
                )
    except WebSocketDisconnect:
        manager.disconnect_player(gameID, userID)



# Connecting to DB and creating tables
if (os.getenv('ENVIRONMENT') == 'test'):
    db.bind(provider=DB_PROVIDER, filename=settings.Db_TEST_FILEANAME, create_db=True)
else:    
    db.bind(provider=DB_PROVIDER, filename=settings.DB_FILEANAME, create_db=True)
db.provider.converter_classes.append((Enum, EnumConverter))
db.generate_mapping(create_tables=True)