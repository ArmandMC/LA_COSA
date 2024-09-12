import { Box, Button } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import axios from "axios";
import { useState, useEffect } from "react";
import "./PageHome.css";

const buttonStyles = {
  width: '200px', minHeight: '170px', fontSize: '24px', 
  background: '#8B0000', // Dark red color
  color: '#ffffff', // White text color
  fontFamily: 'KCWaxMuseum, sans-serif',
  '&:hover': {
    background: '#610101', // Darker red color on hover
  },
};

const dataGridStyles = {
  fontFamily: 'KCWaxMuseum, sans-serif', 
  background: '#000000', // Dark background color
  color: '#ffffff', // White text color
  letterSpacing: '1px', 
};

const columns = [
  {
    field: "id",
    headerName: "ID",
    width: 50,
    sortable: false,
  },
  {
    field: "name",
    headerName: "Nombre Partida",
    width: 400,
    sortable: false,
  },
  {
    field: "cantidad de jugadores",
    headerName: "Jugadores",
    width: 120,
  },
  {
    field: "has_password",
    headerName: "Contraseña",
    width: 120,
    sortable: false,
  },
];

function PageHome() {
  const [games, setGames] = useState([]);
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);
  const [selectedRow, setSelectedRow] = useState(null);

  useEffect(() => {
    // Define la función que realiza la petición GET
    const actData = async () => {
      const url = "http://127.0.0.1:8000/game/";
      axios.get(url).then((res) => {
        console.log(res.data);
        setGames(res.data);
      });
    };

    // Establece un intervalo para ejecutar actData cada 3 segundos
    const intervalId = setInterval(actData, 3000);

    // Limpia el intervalo cuando el componente se desmonta
    return () => clearInterval(intervalId);
  }, []);

  const handleRowClick = (params) => {
    setSelectedRow(params.row.id);
    sessionStorage.setItem("id_game", params.row.id);
    setIsButtonDisabled(false);
  };
  return (
    <Box className='containerHome'>
      <h1 className="title">LA COSA</h1>

      <Box
        sx={{
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'flex-start', // CAMBIO
          '& > :not(style)': {
            m: 5,
            width: 200,
            height: 150,
          },
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Button
            variant="contained"
            href="/crearpartida"
            sx={buttonStyles}
          >
            Crear Partida
          </Button>
          <Button
            variant="contained"
            disabled={selectedRow === null}
            href="/unirsepartida"
            style={{ marginTop: '60px' }}
            sx={buttonStyles}
          >
            Unir Partida
          </Button>
        </div>
        <div
          style={{
            height: 400,
            width: '59%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <DataGrid
            rows={games}
            columns={columns}
            sx={dataGridStyles}
            initialState={{
              pagination: {
                paginationModel: { page: 0, pageSize: 5 },
              },
            }}
            pageSizeOptions={[5, 10]}
            checkboxSelection={false}
            onRowClick={handleRowClick}
            selectionModel={selectedRow ? [selectedRow] : []}
            disableColumnMenu
          />
        </div>
      </Box>
    </Box>
  );
}

export default PageHome;
