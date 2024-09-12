import * as React from "react";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import Avatar from "@mui/material/Avatar";
import monsterImage from '../../images/monster.jpeg';


export default function BasicList({ players }) {
  return (
    <Box sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}>
      <h2 style={{ fontFamily: 'KCWaxMuseum, sans-serif', textAlign: 'center', color:'#8B0000', fontSize: '30px', marginBottom:'-1px' }}> 
      Jugadores</h2>
      <nav aria-label="game list">
        <List>
          {players.map((player, index) => (
            <div key={index}>
              <ListItem disablePadding>
                <ListItemButton>
                  <ListItemIcon>
                    <Avatar src={monsterImage} />
                  </ListItemIcon>
                  {/* If it's admin, concatenate "(admin)" to the name */}
                  <ListItemText
                    primary={
                      player.admin ? (
                        <span style={{ fontFamily: 'KCWaxMuseum, sans-serif', fontSize: '16px' }}>
                          {player.name} (admin)
                        </span>
                      ) : (
                        <span style={{ fontFamily: 'KCWaxMuseum, sans-serif', fontSize: '16px' }}>
                          {player.name}
                        </span>
                      )
                    }
                    secondary={
                      <span style={{ fontFamily: 'KCWaxMuseum, sans-serif', fontSize: '14px' }}>
                        playerId: {player.playerId}
                      </span>
                    }
                  />
                </ListItemButton>
              </ListItem>
              {index < players.length - 1 && <Divider />}{" "}
              {/* Add Divider for all items except the last one */}
            </div>
          ))}
        </List>
      </nav>
    </Box>
  );
}
