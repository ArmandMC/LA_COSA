import { useState } from "react";
import { Alert, Snackbar, Box, CircularProgress, FormControl, MenuItem, TextField, Button, Select } from "@mui/material";
import "./FormCreateGame.css";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import sleep from "../slepp";


const buttonStyles = {
  width: '200px', fontSize: '24px',
  background: '#1dad00', // Dark red color
  color: '#ffffff', // White text color
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
  marginTop: '16px',
  marginBottom: '16px',
};

const LoadingStyles = {
  marginTop: '22px',
  marginBottom: '24px',
}

const formStyles = {
  fontFamily: 'KCWaxMuseum, sans-serif',
  color: '#ffffff', // White text color
};

function FormCreateGame() {
  const [name, setName] = useState(null);
  const [password, setPassword] = useState(null);
  const [minPlayer, setMinPlayer] = useState(4);
  const [maxPlayer, setMaxPlayer] = useState(12);
  const [open, setOpen] = useState(false);
  const [open2, setOpen2] = useState(false);
  const [error, setError] = useState("Error Crear Partida");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const sendData = async (e) => {
    e.preventDefault();
    const url = "http://127.0.0.1:8000/game/";

    const form = {
      name: name,
      min_players: minPlayer,
      max_players: maxPlayer,
      has_password: password ? true : false,
      password: password,
    };

    if (maxPlayer < minPlayer) {
      setError("El Max de jugadores es menor al Min");
      setOpen2(true);
      return 0;
    }
    setLoading(true);
    axios
      .post(url, form)
      .then((response) => {
        console.log(response.status);
        if (response.status === 201) {
          sessionStorage.setItem("id_game", response.data.id);
          setOpen(true);
          sleep(3000).then(() => { navigate('/unirsepartida') })
        }
      })
      .catch((error) => {
        if (error.response.status === 400) {
          setOpen2(true);
          setError("Nombre de partida repetida");
          setLoading(false);
        } else {
          setOpen2(true);
          setLoading(false);
        }
      });
  };
  const handleClose = () => {
    setOpen(false);
  };
  const handleClose2 = () => {
    setOpen2(false);
  };

  return (
    <Box className='container'>
      <h1 className="headerGame">Crear Partida</h1>
      <form onSubmit={sendData} className="form" >
        <h3>Nombre Partida</h3>
        <TextField
          required
          onChange={(e) => setName(e.target.value)}
          InputProps={{
            style: { color: '#ffffff' }, // Set text color to white
          }}

        />
        <h3>Contraseña (Opcional)</h3>
        <TextField
          label="Contraseña"
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          InputProps={{
            style: { color: '#ffffff' }, // Set text color to white
          }}
        />
        <h3>Minimo de Jugadores</h3>
        <FormControl sx={{ m: -1, minWidth: 150, backgroundColor: '#ffff' }} size="small">
          <Select
            labelId="demo-select-small-label"
            id="demo-select-small"
            defaultValue={4}
            onChange={(e) => setMinPlayer(e.target.value)}
          >
            <MenuItem value={4} >4</MenuItem>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={6}>6</MenuItem>
            <MenuItem value={7}>7</MenuItem>
            <MenuItem value={8}>8</MenuItem>
            <MenuItem value={9}>9</MenuItem>
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={11}>11</MenuItem>
            <MenuItem value={12}>12</MenuItem>
          </Select>
        </FormControl>
        <h3>Maximo de Jugadores</h3>
        <FormControl sx={{ marginTop: -1, minWidth: 150, backgroundColor: '#ffff' }} size="small">
          <Select
            labelId="demo-select-small-label"
            id="demo-select-small"
            defaultValue={12}
            onChange={(e) => setMaxPlayer(e.target.value)}
          >
            <MenuItem value={4}>4</MenuItem>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={6}>6</MenuItem>
            <MenuItem value={7}>7</MenuItem>
            <MenuItem value={8}>8</MenuItem>
            <MenuItem value={9}>9</MenuItem>
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={11}>11</MenuItem>
            <MenuItem value={12}>12</MenuItem>
          </Select>
        </FormControl>
        {loading ?
          <CircularProgress color='success' sx={LoadingStyles} />
          :
          <Button type="submit" variant="contained" sx={buttonStyles}>
            Crear
          </Button>
        }
        <br />
      </form>
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={handleClose} severity="success">
          Partida Creada
        </Alert>
      </Snackbar>
      <Snackbar
        open={open2}
        autoHideDuration={6000}
        onClose={handleClose2}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={handleClose2} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default FormCreateGame;
