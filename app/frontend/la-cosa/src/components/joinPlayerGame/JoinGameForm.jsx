import { useState } from "react";
// import { useHistory } from "react-router-dom";
import {TextField, Box, Button} from "@mui/material";
import axios from "axios";
import "./JoinGameForm.css";
import { useNavigate } from 'react-router-dom'

const buttonStyles = {
  width: '490px', fontSize: '20px', marginTop: '-250px',
  background: '#8B0000', // Dark red color
  color: '#ffffff', // White text color
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
};


function JoinGameForm() {
  const navigate = useNavigate();

  // Obtengo los datos del almacenamiento local
  const gameId = sessionStorage.getItem("id_game");
  const has_password = sessionStorage.getItem("has_password");

  // Estados para almacenar los valores de los campos
  //const [gameId, setGameId] = useState(4);
  const [name, setName] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [password] = useState(has_password == true);

  // Manejadores de cambios para los campos
  const handleNombreChange = (event) => {
    setName(event.target.value);
  };

  const handleContrasenaChange = async (event) => {
    setContrasena(event.target.value);
  };

  // Aquí enviamos los datos al servidor o realizamos alguna lógica con los valores ingresados.
  // Manejador de envío del formulario
  const handleSubmit = async (event) => {
    event.preventDefault(); // Evitar el comportamiento de envío predeterminado

    // Realiza una solicitud POST al servidor con los datos del formulario
    try {
      const form = {
        name: name,
        gameId: gameId,
      };

      const response = await axios.post("http://127.0.0.1:8000/player/join", form);
      console.log(response.status);
      if (response.status === 200) {
        // Operación exitosa, mostrar un mensaje de éxito
        console.log(response.data.playerId);
        console.log(response.data.admin);
        sessionStorage.setItem("playerId", response.data.playerId);
        sessionStorage.setItem("isAdmin", response.data.admin);
        navigate("/saladeespera"); // Para cambiar de pagina

      } else if (response.status === 404) {
        // Partida no encontrada
        console.log("404: No se encontró la partida.");
      } else if (response.status === 400) {
        // Partida llena
        console.log("400: La partida está llena")
        alert("La partida está llena.");
      } else if (response.status === 406) {
        // Nombre de jugador repetido
        alert("El nombre de jugador ya está en uso en la partida.")
        console.log("406: El nombre de jugador ya está en uso en la partida.");
      } else {
        // Otro tipo de error, muestra un mensaje de error genérico en la consola
        console.log("Ha ocurrido un error al unirse a la partida. Inténtalo más tarde.");
      }
    } catch (error) {
      // Captura cualquier error inesperado y muestra un mensaje de error en la consola
      console.log("Error al unirse a la partida:", error);
      alert("Ha ocurrido un error al unirse a la partida. Inténtalo más tarde.");
    }
  };

  return (
    <Box className='containerFormJoin'>
      <h1 className="title">Unirse a una partida</h1>
      <div className="centered-formulario">
        <form onSubmit={handleSubmit}>
          <TextField
            label="Nombre de jugador"
            variant="outlined"
            fullWidth
            required
            value={name}
            onChange={handleNombreChange}
            sx={{ backgroundColor: '#fff', marginTop: '-200px' }}
          />
          {password && (
            <TextField
              label="Contraseña"
              type="password"
              variant="outlined"
              fullWidth
              required
              value={contrasena}
              onChange={handleContrasenaChange}
              sx={{ backgroundColor: '#fff', marginTop: '-200px' }}
            />
          )}
          <Button
            variant="contained"
            color="primary"
            type="submit"
            fullWidth
            sx={buttonStyles}
          >
            Unirse a la partida
          </Button>
        </form>
      </div>
    </Box>
  );
}

export default JoinGameForm;