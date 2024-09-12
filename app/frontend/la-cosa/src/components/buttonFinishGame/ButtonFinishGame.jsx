import React from "react";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import axios from "axios";

const ButtonFinishGame = ({gameID,playerID}) => {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const finishGame = () => {
    const url = "http://127.0.0.1:8000/game/finish";
    const form = {
      game_id: gameID,
      player_id: playerID,
    };
    console.log(gameID,playerID)
    axios
      .post(url,form)
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <div style={{width:"20%"}}>
      <Button variant="contained" color="error" onClick={handleClickOpen} size="small">
        Finalizar Partida
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title"   style={{backgroundColor:"white",zIndex:"999"}}>
          {"Estas seguro de finalizar la partida?"}
        </DialogTitle>
        <DialogContent 
         style={{backgroundColor:"white"}}>
          <DialogContentText id="alert-dialog-description" >
            Si todos los jugadores no estan infectados.Pierdes la partida.
          </DialogContentText>
        </DialogContent>
        <DialogActions  style={{backgroundColor:"white"}}>
          <Button onClick={handleClose}>Atras</Button>
          <Button onClick={finishGame} autoFocus>
            Finalizar
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default ButtonFinishGame;
