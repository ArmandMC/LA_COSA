import React, { useEffect, useState } from 'react';
import './Table.css';
import Avatar from '@mui/material/Avatar';

function Table({ players, currentPlayer}) {
  const [currentPlayerName, setCurrentPlayerName] = useState('');
  const playerCount = players.length;
  const angle = 360 / playerCount;
  const parentRadius = 180;
  const childRadius = 40;

  useEffect(() => {
    if (currentPlayer) setCurrentPlayerName(currentPlayer.name);
  }, [currentPlayer])
  const totalOffset = parentRadius - childRadius;
  console.log(players, currentPlayerName);
  return (
    <div className="table">
      {players.map((player, index) => {
        const childStyle = {
          position: 'absolute',
          boxShadow: currentPlayerName === player ? '0 0 20px 5px rgba(225, 216, 24, 5)': '0 0 40px 0 rgba(166, 21, 39, 0)',
          transform: `rotate(${index * angle}deg) translate(${totalOffset}px)`,
          borderRadius: '20px',
        };

        const playerNameStyle = {
          position: 'absolute',
          left: '95%',
          transform: 'translate(-50%, -50%)', // Center the text inside the circle,
          textAlign: 'center',
          color: '#fff',
          transform: 'rotate(90deg)',
          backgroundColor:'black',
          borderRadius: '10px',
          padding:'4px'
        };

        return (
          <div key={index} className="player" style={childStyle}>
            <Avatar alt="Remy Sharp" src='https://avataaars.io/?avatarStyle=Circle&topType=Hat&accessoriesType=Sunglasses&facialHairType=BeardLight&facialHairColor=Brown&clotheType=BlazerShirt&eyeType=Surprised&eyebrowType=FlatNatural&mouthType=Sad&skinColor=Pale' sx={{ width: 56, height: 56 }}/>
            <div className="player-name" style={playerNameStyle}>
              {player}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Table;