import { Box, Button } from "@mui/material";
import "./PageWaitingRoom.css";
import BasicList from "../components/waitingRoom/BasicList";
import Chat from "../components/waitingRoom/Chat";
import { useEffect } from "react";
import { useState } from "react";
import axios from "axios";
import Stack from "@mui/material/Stack";
import { useNavigate } from 'react-router-dom'
import webSocketManager from "../utils/WebSocketUtil";


const buttonStyles = {
  width: '200px', fontSize: '24px', 
  background: '#8B0000', // Dark red color
  color: '#ffffff', // White text color
  marginRight: 2,
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
};
const buttonStyles2 = {
  width: '200px', fontSize: '24px', 
  background: '#3cff00',
  color: '#ffffff', // White text color
  marginRight: 2,
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#249c00', 
  },
};


function PageWaitingRoom() {
  const [players, setPlayers] = useState([]); // array of players
  const [Admin, setIsAdmin] = useState(false);
  const [gameInfo, setGameInfo] = useState([]);
  const [isGameReady, setIsGameReady] = useState(false);
  const navigate = useNavigate();
  
  const gameID = sessionStorage.getItem("id_game");
  const userID = sessionStorage.getItem("playerId");
  const isAdmin = sessionStorage.getItem("isAdmin");
  
  // Handle notifications from the server
  const handleWebSocketMessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'gameStatus') {
      console.log('gameStatus waiting room notification received')
      fetchGameInfo();
      fetchPlayers();
    }
  };

  // Connect to the WebSocket server
  const socket = webSocketManager({handleWebSocketMessage, gameID, userID });
  
  const fetchPlayers = async () => {
    try {
      // Make a GET request to fetch players based on the game ID
      const response = await axios.get(
        `http://localhost:8000/player?game_id=${gameID}`
      );

      // Set the players state with the data from the response
      setPlayers(response.data);
    } catch (error) {
      console.error("Error fetching players:", error);
    }
  };

  const fetchGameInfo = async () => {
    try {
      // Make a GET request to fetch game info
      const response = await axios.get(
        `http://localhost:8000/game/status?id_game=${gameID}`
      );

      // Set the gameInfo state with the data from the response
      setGameInfo(response.data);
    } catch (error) {
      console.error("Error fetching game info:", error);
      navigate("/");
    }
  };


  useEffect(() => {    
    // Initial fetch of players and game info
    fetchGameInfo();
    fetchPlayers();   
  }, [gameID]);

  // Update is game ready from game info
  useEffect(() => {
    setIsGameReady(gameInfo.gameStatus == "READY");
  }, [gameInfo]);

  // Update is admin from players
  useEffect(() => {
    setIsAdmin(isAdmin);
  }, [isAdmin]);

  const handleInitClick = async () => {
    try {
      // Make a POST request to start the game
      const response = await axios.post(`http://localhost:8000/game/start`, {
        id_game: gameID,
        id_player: userID,
      });

      // Handle the response if needed
      console.log(response.data); // Log the response data

      // Check if the response is OK
      if (response.status === 200) {
        // Navigate to the PageGame component with the appropriate props
        navigate("/juego");
      }

      // You can update the state or perform other actions based on the response
    } catch (error) {
      console.error("Error starting the game:", error);
    }
  };

  const exitGame = async () =>{
    axios.delete(`http://localhost:8000/player/${userID}`)
    .then(
      navigate("/")
    ).catch((error) => {
      console.log(error)
    })
  }
  console.log(Admin)
  useEffect(()=>{
    if(gameInfo.gameStatus == "INIT"){
        navigate("/juego")
    }
  })

  return (
    <div className="pageContainer">
      <div className="header">
        <h1>Sala de Espera</h1>
      </div>
      <div className="gameListContainer">
        <BasicList players={players} />
        <Box className="ChatBox">
          <div className="chatContainer">
            <Chat />
          </div>
        </Box>
      </div>

      <div className="Buttons">
        <Stack direction="row" spacing={4}>
          {/* //if admin and game is ready, show start game button */}
          {isAdmin=="true" && isGameReady && (
            <Button
              onClick={handleInitClick}
              variant="outlined"
              color="success"
              sx={buttonStyles2}
            >
              Iniciar Partida
            </Button>
          )}
            <Button variant="outlined" color="error" sx={buttonStyles} onClick={exitGame}>
              Salir Partida
            </Button>
        </Stack>
      </div>
    </div>
  );
}

export default PageWaitingRoom;
