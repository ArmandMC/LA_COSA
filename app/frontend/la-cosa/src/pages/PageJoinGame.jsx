import { Button, Box } from "@mui/material";
import JoinGameForm from "../components/joinPlayerGame/JoinGameForm";
import "./PageJoinGame.css";

const buttonStyles = {
  width: '200px', 
  fontSize: '24px',
  background: '#8B0000', // Dark red color
  color: '#ffffff', // White text color
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
};

function PageJoinGame() {
  return (
    <Box className='containerJoin'>
      <div className="pageJoinForm">
        <JoinGameForm></JoinGameForm>
      </div>
      <div className="buttonContainer">
          <Button variant="contained" href="/crearpartida" sx={buttonStyles}> Atras </Button>
          <Button variant="contained" href="/" sx={buttonStyles}> Home </Button>
      </div>
    </Box>
  );
}

export default PageJoinGame;