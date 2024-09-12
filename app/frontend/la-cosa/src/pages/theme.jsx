import React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#000000',
    },
    text: {
      primary: '#ffffff',
    },
    primary: {
      main: '#ff0000',
    },
    secondary: {
      main: '#800080',
    },
  },
  typography: {
    fontFamily: 'Creepster, cursive',
  },
});
