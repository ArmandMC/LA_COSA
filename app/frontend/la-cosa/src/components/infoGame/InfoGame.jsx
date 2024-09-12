import React from 'react'
import "./InfoGame.css"

const InfoGame = ({name,turno,rol}) => {
  return (
        <div className="player-turn">
        Partida:
        {name}
        <br></br> Turno del jugador:
        {turno}
        <br></br>
        Tu rol de jugador:
        {rol}
        <br></br>
      </div>
  )
}

export default InfoGame
