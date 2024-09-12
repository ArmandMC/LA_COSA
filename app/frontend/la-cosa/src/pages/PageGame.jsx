// Main game interface
import { Button, Box } from "@mui/material";
import "./PageGame.css";
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import deckimg from "../images/dorso.jpeg";
import Table from "../components/Table";
import Card from "../components/Card";
import ShiftsGames from "../components/shiftGame/ShiftsGames";
import webSocketManager from "../utils/WebSocketUtil";
import Notification from "../components/Notification";
import { useNavigate } from "react-router-dom";
import { Snackbar } from "@mui/material";
import ButtonFinishGame from "../components/buttonFinishGame/ButtonFinishGame";
import InfoGame from "../components/infoGame/InfoGame";
import Sentido from "../components/senseGame/Sentido";

const buttonStyles = {
  width: "120px",
  background: "#8B0000", // Dark red color
  color: "#ffffff", // White text color
  marginRight: 2,
  fontSize: "15px",
  padding: "15px 30px",
  fontFamily: "KCWaxMuseum, sans-serif",
  "&:hover": {
    background: "#610101", // Darker red color on hover
  },
};

function PageGame() {
  const [gameStatus, setGameStatus] = useState({
    gameStatus: null,
    players: [],
    gameInfo: {},
  });
  const [showSelectPlayerButtons, setShowSelectPlayerButtons] = useState(false);
  const [showNotificationBox, setShowNotificationBox] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState("");
  const [playerStatus, setPlayerStatus] = useState({});
  const [playerCards, setPlayerCards] = useState([]);
  const [otherPlayers, setOtherPlayers] = useState([]);
  const [selectedCard, setSelectedCard] = useState({});
  const [currentPlayerId, setCurrentPlayerId] = useState(0); // State variable to store the current player ID
  const [leftPlayerPosition, setLeftPlayerPosition] = useState({}); // State variable to store the left player ID
  const [rightPlayerPosition, setRightPlayerPosition] = useState({}); // State variable to store the right player ID
  const [leftPlayer, setLeftPlayer] = useState({}); // State variable to store the left player object
  const [rightPlayer, setRightPlayer] = useState({}); // State variable to store the right player object
  const [playerAlive, setPlayerAlive] = useState(true);
  const [phase, setPhase] = useState(0); // State variable to store the phase of the turn [1,2,3
  const userID = sessionStorage.getItem("playerId");
  const gameID = sessionStorage.getItem("id_game");
  // JSON websocket message
  const [wsMessage, setWsMessage] = useState({}); // State variable to store the websocket message
  const [showCardsDeck, setShowCardsDeck] = useState(false);
  const [showWhiskeyCards, setShowWhiskeyCards] = useState(false); // State variable to store the cards of the whiskey
  const [whiskeyCards, setWhiskeyCards] = useState([]); // State variable to store the cards of the whiskey
  const [exchangableCards, setExchangableCards] = useState([]); // State variable to store the exchangable cards
  const [inExchange, setInExchange] = useState(false); // State variable to store if the player is in exchange
  const [inExchangeWith, setInExchangeWith] = useState(0); // State variable to store the player in exchange with
  const [cardInExchange, setCardInExchange] = useState(0); // State variable to store the card in exchange
  const [showPlayOrDiscardOption, setShowPlayOrDiscardOption] = useState(false); // State variable to store Play or Discard
  const [showPlayerCards, setShowPlayerCards] = useState(true);
  const [showSelectPlayersButtons, setShowSelectPlayersButtons] =
    useState(false);
  const [showInfoCardsPlayers, setShowInfoCardsPlayers] = useState([]); // State variable to store the cards of other's players
  const [showResponseCards, setShowResponseCards] = useState(false); // State variable to store habilited show cards
  const [showMessengeCardStolen, setShowMessengeCardStolen] = useState(false);
  const [showSelectDefenseButtons, setShowSelectDefenseButtons] =
    useState(false); // State variable to store the card of defense
  const [cardDefense, setCardDefense] = useState([]); // State variable to store the card of defense
  const [playerAttack, setPlayerAttack] = useState();
  const [defense, setDefense] = useState(false);
  const [inSeduccion, setInSeduccion] = useState(false);

  // function to wait n seconds
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  // Handle notifications from the server
  const handleWebSocketMessage = (event) => {
    const data = JSON.parse(event.data);
    setWsMessage(data);
    console.log("WebSocket message received:");
    console.log(data);
    if (data.type === "gameStatus") {
      console.log("gameStatus notification received");
      fetchGameStatus();
    }
    if (data.type === "playerStatus") {
      console.log("playerStatus notification received");
      fetchPlayerStatus();
    }
    if (
      data.type === "exchangeSolicitude"
    ) {
      console.log("exchangeSolicitude notification received");
      getExchangableCards();
      wait(1000); // Wait 1 second
      const payload = data.payload;
      console.log(payload);
      setInExchangeWith(payload.player);
      setCardInExchange(payload.card_id);
      setInExchange(true);
    }
    if (data.type === "Whisky") {
      // Recibimos notificacion para mostrar las cartas a todos los jugadores
      console.log("Whisky notification received");
      const payload = data.payload;
      console.log(payload);
      handleWhiskey(payload.player);
      setShowWhiskeyCards(true);
      // Luego, hacer una funcion para hacer un get del nuevo endpoint donde obtengo las cartas
      // luego mostrarlas en la pantalla para los id diferentes al que recibio la notificacion
    }
    if (data.type === "defenseSolicitude") {
      console.log("defense notification received");
      setShowPlayerCards(false);
      // Mostramos los botones para defenderse
      setShowSelectDefenseButtons(true);
      // Si recibo el id de la carta de defensa, lo guardo en una variable para poder usarlo
      setCardDefense(data.payload.cards);
      setPlayerAttack(data.payload.player);
      setDefense(true);
    }
    if (data.type === 'Seduccion'){
      console.log('Seduccion notification received')
      const payload = data.payload;
      getExchangableCards();
      wait(1000); // Wait 1 second
      setShowPlayerCards(false);
      setShowPlayOrDiscardOption(false);
      setInExchange(true);
      setInSeduccion(true);
      setInExchangeWith(payload.player_to);
      setCardInExchange(0);
    }
    if (data.type == 'exchangeSolicitude_Seduccion' ){
      console.log('exchangeSolicitude seduccion notification received')
      getExchangableCards();
      wait(1000); // Wait 1 second
      const payload = data.payload;
      console.log(payload);
      setInExchangeWith(payload.player);
      //setCardInExchange(payload.card_id);
      setInExchange(true);
      setInSeduccion(true);
    }
    if(data.type == 'playAgain'){
      console.log("no se defendio");
      const payload = data.payload;
      playCard(payload.card_to_play,payload.player_to);
    }
  };

  // Connect to the WebSocket server
  const socket = webSocketManager({ handleWebSocketMessage, gameID, userID });

  // fetch game status
  const fetchGameStatus = async () => {
    try {
      // Make a GET request to fetch game status based on the game ID
      const response = await axios.get(
        `http://localhost:8000/game/status?id_game=${gameID}`
      );

      // Set the players state with the data from the response
      setGameStatus(response.data);
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  // fetch player status
  const fetchPlayerStatus = async () => {
    try {
      // Make a get request to fetch player status based on the game ID and user ID /status/player
      const response = await axios.get(
        `http://127.0.0.1:8000/game/playerstatus?id_game=${gameID}&id_player=${userID}`
      );
      // Set the players state with the data from the response
      setPlayerStatus(response.data);
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  // Get initial game status and player status
  useEffect(() => {
    fetchGameStatus();
    fetchPlayerStatus();
  }, []);

  // Get initial player status
  useEffect(() => {
    fetchPlayerStatus();
    fetchGameStatus();
  }, [gameID, userID]);

  // Update player cards and alive status
  useEffect(() => {
    const playerObject = playerStatus;
    console.log(playerObject);
    setPlayerStatus(playerObject);
    if (playerStatus?.cards) {
      setPlayerCards(playerStatus.cards);
    }
    if (playerStatus?.alive) {
      setPlayerAlive(playerStatus.alive);
    }
  }, [playerStatus]);

  // fetch exchangable cards
  const getExchangableCards = async () => {
    try {
      // Make a get request to fetch exchangable cards based on the game ID and user ID
      const response = await axios.get(
        `http://127.0.0.1:8000/card/change/${userID}`
      );
      // Set the players state with the data from the response
      setExchangableCards(response.data);
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  const handleWhiskey = async (playerW) => {
    try {
      const response = await axios.get(
        `http://localhost:8000/card/cards/${playerW}`
      );
      console.log(response.data);
      if (response.status === 200) {
        console.log(response);
        setWhiskeyCards(response.data);
      }
    } catch (error) {
      console.error("Error getting cards:", error);
    }
  };

  const drawCard = async () => {
    try {
      // Make a POST request to draw a card
      const response = await axios.post(
        `http://localhost:8000/card/steal_card/${userID}`
      );
      // Check if the post return success
      if (response.status === 200) {
        console.log("Card drawn successfully!");
        setShowCardsDeck(false);
        setShowMessengeCardStolen(true);
      } else {
        console.log("Error drawing card!");
      }
    } catch (error) {
      console.error("Error drawing card:", error);
    }
  };

  // exchange cards 1
  const exchangeCards1 = async (player_to_id, card_id) => {
    try {
      // Hide elements until the exchange is done
      setShowPlayerCards(false);
      setShowSelectPlayerButtons(false);
      setShowPlayOrDiscardOption(false);
      setShowCardsDeck(false);
      setNotificationMessage(
        "Espere mientras se realiza el intercambio de cartas"
      );
      setShowNotificationBox(true);
      // if(gameStatus.gameInfo.faseDelTurno == 2){
      //   const response = await axios.post(
      //     `http://localhost:8000/card/change1_all`,
      //     {
      //       player_id: userID,
      //       player_to_id: player_to_id,
      //       card_id: card_id,
      //     }
      //   );
      // } else if (gameStatus.gameInfo.faseDelTurno == 3) {
      // Make post request to exchange cards
      const response = await axios.post(`http://localhost:8000/card/change1`, {
        player_id: userID,
        player_to_id: player_to_id,
        card_id: card_id,
      });

      // Check if the post return success and show notification
      if (response.status === 200) {
        console.log("Cards exchanged successfully!");
        // setNotificationMessage("Cartas intercambiadas con éxito");
        // setShowNotificationBox(true);
        setShowCardsDeck(true);
        setShowPlayerCards(true);
        setInExchange(false);
        setInExchangeWith(0);
        setCardInExchange(0);
        setSelectedCard({});
      } else {
        console.log("Error exchanging cards!");
      }
    } catch (error) {
      console.error("Error exchanging cards:", error);
    }
  };

  // exchange cards 2
  const exchangeCards2 = async (
    inExchangeWith,
    userID,
    cardInExchange,
    selectedCard
  ) => {
    try {
      console.log("inExchangeWith", inExchangeWith);
      console.log("userID", userID);
      console.log("cardInExchange", cardInExchange);
      console.log("selectedCard", selectedCard);

      // Make post request to exchange cards
      const response = await axios.post(`http://localhost:8000/card/change2`, {
        player_id: inExchangeWith,
        player_to_id: userID,
        card_id1: cardInExchange,
        card_id2: selectedCard,
      });

      // Check if the post return success and show notification
      if (response.status === 200) {
        console.log("Cards exchanged successfully!");
        // setNotificationMessage("Cartas intercambiadas con éxito");
        // setShowNotificationBox(true);
        setInExchange(false);
        setShowPlayerCards(true);
        setInExchangeWith(0);
        setCardInExchange(0);
        setSelectedCard({});
        setShowPlayOrDiscardOption(false);
        setShowSelectPlayerButtons(false);
      } else {
        console.log("Error exchanging cards!");
      }
    } catch (error) {
      console.error("Error exchanging cards:", error);
    }
  };

  const handleSeduccion = async (player_to_id, card_id) => {
    try {
      const response = await axios.post(
        `http://localhost:8000/card/change_in_play_1`,
        {
          player_id: userID,
          player_to_id: player_to_id,
          card_id: card_id,
        }  
      );
      // Check if the post return success and show notification
      if (response.status === 200) {
        console.log("Seduccion cards exchanged successfully!");
        setShowPlayerCards(true);
        setInExchange(false);
        setInExchangeWith(0);
        setCardInExchange(0);
        setSelectedCard({});
      } else {
        console.log("Error exchanging cards!");
      }  
      

    }  
    catch (error) {
      console.error("Error exchanging cards:", error);
    }  
  }  

  const handleSeduccion2 = async (inExchangeWith, userID, selectedCard) => {
    try {
      console.log("inExchangeWith", inExchangeWith);
      console.log("userID", userID);
      console.log("cardInExchange", cardInExchange);
      console.log("selectedCard", selectedCard);

      // Make post request to exchange cards 
      const response = await axios.post(
        `http://localhost:8000/card/change_in_play_2`
        , {
          player_id: inExchangeWith,
          player_to_id: userID,
          card_id2: selectedCard,
        }  
      );  


      // Check if the post return success and show notification
      if (response.status === 200) {
        console.log("Cards exchanged successfully!");
        // setNotificationMessage("Cartas intercambiadas con éxito");
        // setShowNotificationBox(true);
        setInExchange(false);
        setShowPlayerCards(true);
        setInExchangeWith(0);
        setCardInExchange(0);
        setSelectedCard({});
        setShowPlayOrDiscardOption(false);
        setShowSelectPlayerButtons(false);
      } else {
        console.log("Error exchanging cards!");
      }  


    }  
    catch (error) {
      console.error("Error exchanging cards:", error);
    }  
  }  


  // Check if the game is finished
  const navigate = useNavigate();

  useEffect(() => {
    console.log(gameStatus.gameStatus);
    if (gameStatus.gameStatus === "FINISH") {
      //Cambia a la pagina de resultados
      navigate(`/resultados/${gameID}`);
    }
  }, [gameStatus, gameID]);

  // Update players on table (otherPlayers) and current player (currentPlayerId)
  useEffect(() => {
    // CAMBIO LA CONDICIÓN DE QUE PLAYER STATUS != HUMAN YA QUE ESO NO LLEGA MAS POR EL GAME STATUS
    const otherPlayersObject = gameStatus.players
      .filter((player) => player.id !== userID && player.alive)
      .sort((a, b) => a.position - b.position) // Sort based on player IDs
      .map((player) => player.name);

    setOtherPlayers(otherPlayersObject);
    setCurrentPlayerId(gameStatus.gameInfo.jugadorTurno);
    setPhase(gameStatus.gameInfo.faseDelTurno);
    //check the phase of the turn
    if (currentPlayerId == userID) {
      if (phase == 1) {
        setShowCardsDeck(true);
        setShowPlayerCards(true);
        setShowPlayOrDiscardOption(false);
        setShowSelectPlayerButtons(false);
      } else if (phase == 2) {
        setShowPlayerCards(true);
        setShowPlayOrDiscardOption(false);
        setShowSelectPlayerButtons(false);
        setShowCardsDeck(false);
      } else if (phase == 3) {
        setShowPlayerCards(false);
        setShowPlayOrDiscardOption(false);
        getExchangableCards();
        wait(1000); // Wait 1 second
        setInExchange(true);
        setInExchangeWith(
          gameStatus.gameInfo.sentido === "derecha"
            ? leftPlayer.id
            : rightPlayer.id
        );
        setCardInExchange(0);
      }
    } else {
      setShowPlayerCards(true);
    }
  }, [gameStatus, phase, userID, playerStatus]);

  // Update leftPlayer and rightPlayer according to user.position
  useEffect(() => {
    if (playerStatus !== undefined) {
      const leftPlayerPos =
        (playerStatus.position + 1) % gameStatus.players.length;

      const rightPlayerPos =
        playerStatus.position > 0
          ? playerStatus.position - 1
          : gameStatus.players.length - 1;

      setRightPlayerPosition(rightPlayerPos);
      setLeftPlayerPosition(leftPlayerPos);

      const leftPlayerObject = gameStatus.players.find(
        (player) => player.position === leftPlayerPos
      );

      const rightPlayerObject = gameStatus.players.find(
        (player) => player.position === rightPlayerPos
      );

      if (leftPlayerObject) {
        setLeftPlayer(leftPlayerObject);
      }
      if (rightPlayerObject) {
        setRightPlayer(rightPlayerObject);
      }
    }
  }, [playerStatus, userID, gameStatus]);

  // Define a function to handle deck click
  const handleDeckClick = () => {
    console.log("Deck clicked");
    if (phase == 1 && currentPlayerId == userID) {
      drawCard();
    }
    //setShowCardsDeck(false);
  };

  // Define a function to handle card click
  const handleCardClick = (clickedCard) => {
    // Check if it is the player's turn and the phase of playing
    if (currentPlayerId == userID) {
      // DRAW FROM DECK
      if (phase == 1) {
        //NOTHING
      }
      // PLAY OR DISCARD
      else if (phase == 2) {
        // Enables and disables the play or discard button.
        if (selectedCard.id === clickedCard) {
          setSelectedCard({});
          setShowPlayOrDiscardOption(false);
        } else {
          // Otherwise, update the selected card.
          setSelectedCard(clickedCard);
          // Displays the option to play or discard
          setShowPlayOrDiscardOption(true);
        }
        // IT DO NOT HAVE TO ENTER HERE
      } else if (phase == 3) {
        if (inExchange) {
          setShowNotificationBox(false);
          setNotificationMessage("");
        }
      }
    } else if (defense) {
      if (selectedCard.id === clickedCard) {
        setSelectedCard({});
      } else {
        setSelectedCard(clickedCard);
      }
    }
  };

  // Define a function to handle play card click
  const handlePlayCardClick = async (clickedCard) => {
    // Check if it is the player's turn and the phase of playing
    if (currentPlayerId == userID && phase == 2) {
      switch (clickedCard.type) {
        case "Lanzallamas":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayerButtons(true);
          break;
        case "Empty":
          // chequear que esté ok pasar null como id_player_target
          setShowSelectPlayerButtons(false);
          setShowPlayOrDiscardOption(false);

          // No colgar en borrar el userID
          playCard(clickedCard.id, userID);
          break;
        case "VigilaTusEspaldas":
          setShowSelectPlayerButtons(false);
          setShowPlayOrDiscardOption(false);
          playCard(clickedCard.id, userID);
          break;
        case "CambioDeLugar":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayerButtons(true);
          break;
        case "MasValeQueCorras":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayersButtons(true);
          break;
        case "Seduccion":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayersButtons(true);
          break;
        case "Analisis":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayerButtons(true);
          break;
        case "Sospecha":
          setShowPlayOrDiscardOption(false);
          setShowSelectPlayerButtons(true);
          break;
        case "Whisky":
          setShowPlayOrDiscardOption(false);
          playCard(clickedCard.id, userID);
          break;
        // case "Determinacion":
        //   setShowPlayOrDiscardOption(false);
        //   setShowSelectPlayersButtons(true);
        //   break;
        // case "hacha":
        //   setShowPlayOrDiscardOption(false);
        //   setShowSelectPlayersButtons(true);
        //   break;
        default:
          console.log("Card type not recognized!");
      }
    } else {
      console.log("Not your turn or not the phase of playing!");
    }
  };

  // Enables to display response cards
  useEffect(() => {
    if (showInfoCardsPlayers && showInfoCardsPlayers.length > 0) {
      setShowResponseCards(true);
    } else {
      console.log("No letters to display");
    }
  }, [showInfoCardsPlayers]);

  // Set the game to continue after viewing the card
  const handleContinueGame = () => {
    // Seteamos para dejar de mostrar las cartas
    setShowResponseCards(false);
    setShowWhiskeyCards(false);
    setShowInfoCardsPlayers([]);
  };

  // Define a function to handle Discard card click
  const handleDiscardCard = async (selectedCard) => {
    if (currentPlayerId == userID && showPlayOrDiscardOption) {
      try {
        console.log("Enviando solicitud de descarte de carta...");
        console.log("gameID:", gameID);
        console.log("userID:", userID);
        console.log("selectedCard.id:", selectedCard.id);

        //Make a POST request to discard the card
        const response = await axios.post(
          `http://localhost:8000/card/discard_card/${userID}/${selectedCard.id}`,
          {
            id_game: gameID,
          }
        );

        if (response.status === 200) {
          //if (true) {
          console.log("Card discarded successfully!");
          setShowPlayOrDiscardOption(false);

          // Delete the Discard Card of the state playerCards
          const updatedPlayerCards = playerCards.filter(
            (card) => card.id !== selectedCard.id
          );
          setPlayerCards(updatedPlayerCards);
        }
      } catch (error) {
        console.error("Error discarding card:", error);
      }
    }
  };

  // Define a function to handle card play
  const playCard = async (id_cardD, id_player_target) => {
    try {
      // Make a POST request to play a card
      // Chequear que se esté haciendo bien el post
      const response = await axios.post(
        `http://localhost:8000/card/play_card1`,
        {
          id_game: gameID,
          id_player: userID,
          id_player_to: id_player_target,
          id_card: id_cardD,
        }
      );
      console.log(response.data);
      // Check if the post return success
      if (response.status === 200) {
        console.log("Card played successfully!");
        setShowSelectPlayerButtons(false);
        console.log("card: ", response.data.card);
        console.log("cards: ", response.data.cards);
        // Setea si recibe las cartas del caso Analisis o Whisky
        if (response.data.cards) {
          console.log("CASO ANALISIS O WHISKY");
          setShowInfoCardsPlayers(response.data.cards); // Me envian en [{},{},{}...]
        }
        // Setea si recibe una carta del caso "Sospecha"
        else if (response.data.card) {
          console.log("CASO SOSPECHA");
          setShowInfoCardsPlayers([response.data.card]); // Me envian {} entonces los guardamos asi [{}]
        }
      } else {
        console.log("Error playing card!");
      }
    } catch (error) {
      console.error("Error playing card:", error);
    }
  };

  // Si recibo como parametro el id de la carta que debo jugar, entonces hago un post
  // el id de la carta de defensa es lo que recibo como parametro por websockets
  const PlayDefenseCards = async (card, condicionDef) => {
    try {
      // Make a get request to fetch defense cards based on the game ID and user ID
      console.log(card, condicionDef, Number(userID), playerAttack);
      const response = await axios.post(
        `http://127.0.0.1:8000/card/play_card2`,
        {
          // los datos que tengo que enviar al back son: id_game, id_player, id_card
          id_player: playerAttack,
          id_player_to: Number(userID),
          id_card_2: card, // id de la carta de defensa
          defense: condicionDef, // booleano que indica si me quiero defender o no
        }
      );
      console.log(response.data);
      // Set the players state with the data from the response
      if (response.status === 200) {
        setShowSelectDefenseButtons(false);
        console.log("card: ", response.data.card);
        console.log("Card played successfully!");
        // si la carta de defensa es "Defensa Aterradora" entonces recibo una carta
        if (response.data.card) {
          console.log("CASO DEFENSA ATERRADOR");
          setShowInfoCardsPlayers([response.data.card]); // Me envian {} entonces los guardamos asi [{}]
        }
      } else {
        console.log("Error playing card!");
      }
    } catch (error) {
      console.error("Error playing card:", error);
    }
  };

  // Define a function to handle player selection
  const handlePlayerSelection = async (targetPlayerId) => {
    // Process the player selection here
    console.log(`Player selected: ${targetPlayerId}`);
    console.log(`Card selected: ${selectedCard.id}`);
    console.log(`target id: ${targetPlayerId}`);
    playCard(selectedCard.id, targetPlayerId);
    setShowSelectPlayerButtons(false);
    setShowSelectPlayersButtons(false);
    setSelectedCard({});
  };

  // Define a function to handle notification OK click
  const handleNotificationOKClick = () => {
    // Check if it is the player's turn and the phase
    if (currentPlayerId == userID && inExchange) {
      //NOTHING, WAIT FOR THE OTHER PLAYER TO EXCHANGE
      // chequear que sea necesario setear o si ya vienen seteados
      setShowCardsDeck(false);
      setShowPlayerCards(false);
    } else if (inExchange) {
      // Here if player is not in turn but received a solicitude to exchange
      // We allow the player to close the notification box so he can select a card to exchange
      setNotificationMessage("");
      setShowNotificationBox(false);
    } else {
      setNotificationMessage("");
      setShowNotificationBox(false);
    }
  };

  // Handle exchange solicitude
  const handleExchangeSolicitude = (exchangeCard) => {
    console.log("inExchangeWith", inExchangeWith);
    console.log("userID", userID);
    console.log("leftPlayer.id", leftPlayer.id);
    if (inExchange && inSeduccion && currentPlayerId == userID) {
      handleSeduccion(inExchangeWith, exchangeCard);
      setInSeduccion(false);
    }
    if (currentPlayerId != userID && inExchange && inSeduccion) {
      handleSeduccion2(inExchangeWith, userID, exchangeCard);
      setInSeduccion(false);
    }
    // Here when player is not in turn and received a solicitude to exchange
    // In this case we send the response through the websocket
    if (currentPlayerId != userID && inExchange && !inSeduccion) {
      exchangeCards2(inExchangeWith, userID, cardInExchange, exchangeCard);
      // Here when player is in turn and in phase of exchanging
      // In this case we call the exchangeCards function that touches the /change endpoint
    } else if (currentPlayerId == userID && inExchange && !inSeduccion) {
      exchangeCards1(inExchangeWith, exchangeCard);
    }
  };

  const findUserNameById = (id) => {
    const player = gameStatus.players.find((player) => player.id === id);
    return player ? player.name : "Usuario no encontrado";
  };

  //Draw card automatically
  useEffect(() => {
    if (
      gameStatus.gameInfo.jugadorTurno == userID &&
      gameStatus.gameInfo.faseDelTurno == 1
    ) {
      const timeOut = setTimeout(() => {
        axios
          .post(`http://localhost:8000/card/steal_card/${userID}`)
          .then((res) => {
            console.log(res);
            setShowMessengeCardStolen(true);
          })
          .catch((error) => {
            console.log(error);
          });
      }, 40000);
      return () => clearTimeout(timeOut);
    }
  });

  console.log(gameStatus);

  return (
    <Box className="containerGame">
      {playerStatus && playerStatus.status == "theThing" && (
        <ButtonFinishGame gameID={gameID} playerID={userID}></ButtonFinishGame>
      )}
      <InfoGame
        name={gameStatus.name}
        turno={findUserNameById(gameStatus.gameInfo.jugadorTurno)}
        rol={playerStatus.status}
      ></InfoGame>
      <div className="cardDeck">
        {showCardsDeck && (
          <div>
            <img src={deckimg} alt="Deck" onClick={handleDeckClick} />
          </div>
        )}
      </div>
      <div className="pageGameTable">
        <div className="tablegame">
        <Sentido sentido={gameStatus.gameInfo.sentido}></Sentido>
          <Table players={otherPlayers} currentPlayer={playerStatus} />
        </div>
      </div>
      <div className="playerCards">
        {/* acá van las cartas del jugador */}
         {/* acá van las cartas del jugador */}
        {!showNotificationBox && !inExchange && !showSelectDefenseButtons &&<h3>Tus cartas</h3>}
        {!inExchange &&
          showPlayerCards &&
          playerCards &&
          !showSelectDefenseButtons &&
          playerCards
            .slice() // Create a shallow copy to avoid mutating the original array
            .sort((a, b) => a.id - b.id) // Sort based on card IDs
            .map((card) => (
              <Card
                key={card.id}
                id={card.id}
                type={card.type}
                number={card.number}
                selectedCard={selectedCard.id ?? null}
                //image={gallardoImage}
                onClick={() => handleCardClick(card)} // Add onClick handler
              />
            ))}
        <div>
          {showNotificationBox && (
            <Notification
              text={notificationMessage}
              handleOKClick={handleNotificationOKClick}
            />
          )}
        </div>
      </div>
      <div className="playerCards">
        {/* acá van las cartas intercambiables del jugador */}
        {!showNotificationBox && inExchange && exchangableCards && <h3>Tus cartas intercambiables</h3>}
        {!showNotificationBox &&
          inExchange &&
          exchangableCards &&
          exchangableCards.map((exchangeableCardId) =>
            playerCards.find((card) => card.id === exchangeableCardId) ? (
              <Card
                id={exchangeableCardId}
                type={
                  playerCards.find((card) => card.id === exchangeableCardId)
                    .type
                }
                number={
                  playerCards.find((card) => card.id === exchangeableCardId)
                    .number
                }
                // image={gallardoImage}
                onClick={() => handleExchangeSolicitude(exchangeableCardId)}
              />
            ) : null
          )}
      </div>
      <div className="playerCards">
        {/* acá van las cartas de Defensa */}
        {cardDefense && showSelectDefenseButtons && (
        <>
          <h3>Tus cartas de defensa</h3>
          {cardDefense.map((IdCardDefense) =>
          playerCards.find((card) => card.id === IdCardDefense) ? (
          <Card
            id={IdCardDefense}
            type={playerCards.find((card) => card.id === IdCardDefense).type}
            number={playerCards.find((card) => card.id === IdCardDefense).number}
            selectedCard={selectedCard.id  ?? null}
            onClick={() => handleCardClick(IdCardDefense)}
          />
          ) : null
          )}
        </>
        )}
      </div>
      <div className="SelectPlayOrDiscardOption">
        {showPlayOrDiscardOption && (
          <div>
            <h2>¿Qué deseas hacer?</h2>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handlePlayCardClick(selectedCard)}
              style={buttonStyles}
            >
              Jugar
            </Button>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleDiscardCard(selectedCard)}
              style={buttonStyles}
            >
              Descartar
            </Button>
          </div>
        )}
      </div>
      <div className="SelectPlayerButtons">
        {showSelectPlayerButtons && (
          <div>
            <h2>Seleccionar jugador</h2>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handlePlayerSelection(leftPlayer.id)}
              style={buttonStyles}
            >
              {leftPlayer.name}
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handlePlayerSelection(rightPlayer.id)}
              style={buttonStyles}
            >
              {rightPlayer.name}
            </Button>
          </div>
        )}
      </div>
      <div className="SelectPlayerButtons">
        {showSelectPlayersButtons && (
          <div>
            <h2>Seleccionar jugador</h2>
            {gameStatus.players.map((playerName) => (
              <Button
                key={playerName.id} // Usar un identificador único para la clave
                variant="contained"
                color="primary"
                onClick={() => handlePlayerSelection(playerName.id)}
                style={buttonStyles}
                disabled={!(playerName.id != userID)}
              >
                {playerName.name}
              </Button>
            ))}
          </div>
        )}
      </div>
      {/* Muestra la cartas de respuesta de sospecha, Analisis, Whisky o Aterrador */}
      <div className="showResponseCards">
        {showResponseCards && (
          <div>
            <h2>Cartas del rival:</h2>
            <div
              style={{
                position: "relative",
                display: "flex",
                flexDirection: "row",
                justifyItems: "center",
              }}
            >
              {showInfoCardsPlayers.map((card, index) => (
                <Card
                  id={index + 1}
                  type={card.name}
                  number={index + 1}
                  onClick={() => {}}
                />
              ))}
            </div>
            {/* Botón para continuar el juego */}
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleContinueGame()}
              style={buttonStyles}
            >
              Continuar
            </Button>
          </div>
        )}
      </div>
      <div className="showWhiskeyCards">
        {showWhiskeyCards && (
          <div>
            <h2>Cartas del rival:</h2>
            <div
              style={{
                position: "relative",
                display: "flex",
                flexDirection: "row",
                justifyItems: "center",
              }}
            >
              {whiskeyCards.map((card) => (
                <Card
                  id={card.id}
                  type={card.type}
                  number={card.number}
                  onClick={() => {}}
                />
              ))}
            </div>
            {/* Botón para continuar el juego */}
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleContinueGame()}
              style={buttonStyles}
            >
              Continuar
            </Button>
          </div>
        )}
      </div>
      {/* Muestra la opcion para defenderse */}
      <div className="SelectPlayOrDiscardOption">
        {showSelectDefenseButtons && (
          <div>
            <h3 style={{color:"white"}}> Decide si quieres defenderte </h3>
            <Button
              variant="contained"
              color="primary"
              onClick={() => PlayDefenseCards(selectedCard, true)} // Una funcion para defenderse
              style={buttonStyles}
            >
              ¡Aplicar defensa!
            </Button>
            <Button
              variant="contained"
              color="primary"
              onClick={() => PlayDefenseCards(selectedCard, false)} // Una funcion para no defenderse
              style={buttonStyles}
            >
              ¡No me quiero defender!
            </Button>
          </div>
        )}
      </div>
      {gameStatus.gameInfo.jugadorTurno == userID && (
        <ShiftsGames
          phaseShift={gameStatus.gameInfo.faseDelTurno}
        ></ShiftsGames>
      )}
      <div>
        <Snackbar
          open={showMessengeCardStolen}
          anchorOrigin={{ vertical: "button", horizontal: "center" }}
          message={`Carta Robada`}
          autoHideDuration={4000}
          onClose={() => setShowMessengeCardStolen(false)}
        />
      </div>
    </Box>
  );
}

export default PageGame;
