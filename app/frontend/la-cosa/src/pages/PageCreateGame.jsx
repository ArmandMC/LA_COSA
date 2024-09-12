import { Button, Box } from "@mui/material";
import FormCreateGame from "../components/createGame/FormCreateGame";
import "./PageCreateGame.css";

const buttonStyles = {
  width: '200px', fontSize: '24px',
  background: '#8B0000', // Dark red color
  color: '#ffffff', // White text color
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
};

function PageCreateGame() {
  return (
    <Box className='container'>
      <Box className="pageForm">
        <FormCreateGame></FormCreateGame>
      </Box>
      <Box className="button">
        <Button variant="contained" href="/" sx={buttonStyles}>Menu</Button>
      </Box>
    </Box>
  );
}

export default PageCreateGame;
