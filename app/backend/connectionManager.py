from typing import List, Dict, Tuple
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import time

class ConnectionManager():
    def __init__(self):
        self.lobby_connections: List[WebSocket] = []
        self.player_connections: Dict[Tuple[int, int], WebSocket] = {}
        self.initialized: bool = False

    async def connect_lobby(self, websocket: WebSocket):
        await websocket.accept()
        self.lobby_connections.append(websocket)

    def disconnect_lobby(self, websocket: WebSocket):
        self.lobby_connections.remove(websocket)

    async def connect_game(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        self.lobby_connections.append(websocket)

    def disconnect_game(self, websocket: WebSocket, game_id: int):
        self.lobby_connections.remove(websocket)

    async def connect_player(self, websocket: WebSocket, game_id: int, player_id: int):
        await websocket.accept()
        key = (game_id, player_id)
        if key not in self.player_connections:
            self.player_connections[key] = websocket
            print("Player connected: ", key)
            if (not self.initialized):
                self.initialized = True

    def disconnect_player(self, game_id: int, player_id: int):
        key = (game_id, player_id)
        if key in self.player_connections:
            self.player_connections[key].close()
            self.player_connections.pop(key, None)
            print("Player disconnected: ", key)

    async def broadcast_json(self, message: any, dst: List[WebSocket]):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        for connection in dst:
            await connection.send_json(message)

    async def send_to_player(self, game_id: int, player_id: int, message: any):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        key = (game_id, player_id)
        if key in self.player_connections:
            await self.player_connections[key].send_json(message)
        else :
            print(f"Error in player connection. Player {player_id} not found in websocket dict: ", key)

    async def broadcast_to_game(self, game_id: int, message: any):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Broadcast a message to all players in a game
        connections = [conn for key, conn in self.player_connections.items() if key[0] == game_id]
        for connection in connections:
            await connection.send_json(message)
        print(f"Broadcasted message to game {game_id}")

    async def trigger_game_status(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "gameStatus"}
        # Get all player connections for the specified game
        connections_to_notify = [ws for (g_id, _), ws in self.player_connections.items() if g_id == game_id]
        # Send the message to each player's WebSocket connection
        for connection in connections_to_notify:
            await connection.send_json(message)
        print(f"Triggered game status update for game {game_id}")


    async def trigger_player_status(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "playerStatus"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        print(f"Triggered player status update for player {player_id} in game {game_id}")

    async def send_exchange_solicitude(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        
        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "exchangeSolicitude", "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_to_id, message)
        print(f"Sending exchange solicitude for player {player_to_id} in game {game_id}")

    async def send_exchange_solicitude_seduccion(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}  
        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "exchangeSolicitude_Seduccion", "payload": {"player": player_id}}
        await self.send_to_player(game_id, player_to_id, message)
        print(f"Sending exchange seduccion solicitude for player {player_to_id} in game {game_id}")

    
    async def trigger_seduccion(self, game_id, player_id, player_to_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        # Create the JSON message, "cards" is a list of card ids that can be exchanged by player_to_id
        message = {"type": "Seduccion", "payload": {"player_to": player_to_id}}
        await self.send_to_player(game_id, player_id, message)
        print(f"Sending notification of seduccion to change player {player_id} and player {player_to_id} in game {game_id}")


    async def trigger_whisky(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        
        message = {"type": "Whisky", "payload": {"player": player_id}}
        await self.broadcast_to_game(game_id, message)
        print(f"Sending whisky message for player {player_id} in game {game_id}")

    async def trigger_play_again(self, game_id, player_id, player_to_id, card_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}} 
        # Create the JSON message, 
        message = {"type": "playAgain", "payload": {"player_to": player_to_id, "card_to_play": card_id}}
        await self.send_to_player(game_id, player_id, message)
        print(f"Sending message to play again for player {player_id} in game {game_id}")


    async def trigger_all_players_status(self, game_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "playerStatus"}
        # Get all player connections for the specified game
        connections_to_notify = [ws for (g_id, _), ws in self.player_connections.items() if g_id == game_id]
        # Send the message to each player's WebSocket connection
        for connection in connections_to_notify:
            await connection.send_json(message)
        print(f"Triggered all players status update for game {game_id}")

    async def send_defense_solicitude(self, game_id, player_id, player_to_id, def_cards):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        
        message = {"type": "defenseSolicitude", "payload": {"player": player_id, "cards": def_cards}}
        await self.send_to_player(game_id, player_to_id, message)
        print(f"Sending defense solicitude for player {player_to_id} in game {game_id}")

    async def trigger_exchange_fished(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "exangeFished"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        print(f"Triggered exchange finished for player {player_id} in game {game_id}")

    async def trigger_turn_finished(self, game_id, player_id):
        if (not self.initialized):
            return {"type": "error", "payload": {"message": "Game not initialized"}}
        # Create the JSON message
        message = {"type": "turnFinished"}
        # Send the message to the player's WebSocket connection
        await self.send_to_player(game_id, player_id, message)
        print(f"Triggered turn finished for player {player_id} in game {game_id}")

    # async def wait_change_response(self, player_to_id, game_id):
    #     print(f"Waiting for response from player {player_to_id}")
    #     # Wait for response in websocket
    #     key = (game_id, player_to_id)
    #     if key in self.player_connections:
    #         ws = self.player_connections[key]
    #         while True:
    #             data = await ws.receive_json()
    #             print("Dentro del WhileTrue")
    #             if data["type"] == "exchangeResponse":
    #                 return data["data"]["card_id"]
    #     else:
    #         print(f"Error in key, not found in websocket dict: ", key)