import { useEffect, useState, useRef } from "react";
import { Button } from "@mui/material";
import AudiotrackIcon from '@mui/icons-material/Audiotrack';
import './PageGameResult.css'; // Importa el archivo CSS
import { Link } from "react-router-dom"
import axios from "axios";
import trompetas from '../others/trumpets.mp3';


function PageGameResult({ gameID }) {

  // State variable to store the winner game
  const [gameWinners, setGameWinners] = useState(false, {});
  const [isAudioPlaying, setIsAudioPlaying] = useState(true);
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;

    if (isAudioPlaying) {
      audio.play();
    } else {
      audio.pause();
      audio.currentTime = 0; // Reset audio to the beginning
    }
    const fetchGameResultInfo = async () => {
      try {        
        // Get game winners data from the API
        const gameResultResponse = await axios.get(`http://localhost:8000/game/${gameID}/winners`);
        console.log("Respuesta de la API:", gameResultResponse);
  
        // Extract the winners' information from the game result.
        const gameWinners = gameResultResponse.data;
        setGameWinners(gameWinners);
        console.log("Información de los ganadores:", gameWinners);
  
        // Wait 2 seconds before deleting the game
        setTimeout(async () => {
          try {
            console.log("Sending a request to delete the game");
            // Make a DELETE request to the backend to delete the game
            await axios.delete(`http://localhost:8000/game/${gameID}`);
            
            console.log("Game successfully eliminated");

          } catch (error) {
            console.error("Error when deleting the game:", error);
          }
        }, 2000);
  
      } catch (error) {
        console.error("Error when obtaining the results of the game:", error);
      }
    };
  
    // Call function on component load or when gameID changes
    fetchGameResultInfo();
  }, [gameID, isAudioPlaying]);
  
  const toggleAudio = () => {
    setIsAudioPlaying(!isAudioPlaying);
  };
  
  return (
    <>
    <h2 className="header">Partida: {gameWinners.name}</h2>
    <div className="gameWinners">
      <h2>Ganador/es: {gameWinners.team}</h2>
      <ul>
        {gameWinners.players && gameWinners.players.map((winners, index) => (
          <li key={index}> Name: {winners.name} - Role: {winners.role}</li>
        ))}
      </ul>
      <Link to="/" className="custom-button">Home</Link>
    </div>
    <Button onClick={toggleAudio} startIcon={<AudiotrackIcon />} sx={{  width: '120px'}}>trumpets</Button>
    <audio ref={audioRef} src={trompetas} loop />
    </>
  );
}

export default PageGameResult;

  // // Simulación de respuesta de ganadores
  // const fakeGameWinners = {
  //   name_partida: 'FamafyC',
  //   team_winner: 'La Cosa y los Infectados',
  //   winners_players: [
  //     { id: 1, name: 'Armand', role: 'La Cosa' },
  //     { id: 2, name: 'facu', role: 'Infectado' },
  //     { id: 3, name: 'ivan', role: 'Infectado' },
  //     { id: 4, name: 'gonza', role: 'Infectado' },
  //   ],
  // };

  //   <div className="gameWinners">
  //     <h2>Partida: {fakeGameWinners.name_partida}</h2>
  //     <h2>Ganador/es: {fakeGameWinners.team_winner}</h2>
  //     <ul>
  //       {fakeGameWinners.winners_players.map((winner, index) => (
  //       <li key={index}> Name: {winner.name} - Role: {winner.role}</li>
  //       ))}
  //     </ul>
  //     <Link to="/" className="custom-button">Home</Link>
  // </div>

    // <div className="gameWinners">
    //   <h2>Partida: {gameWinners.name_partida}</h2>
    //     <h2>Ganador/es: {gameWinners.team_winner}</h2>
    //     <ul>
    //       {gameWinners && gameWinners.winners_players && gameWinners.winners_players.map((winner, index) => (
    //       <li key={index}> Name: {winner.name} - Role: {winner.role}</li>
    //       ))}
    //     </ul>
    // </div>
