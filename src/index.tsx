import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ReactDOM from "react-dom/client";
import React from "react";
import App from './App';


const theme = createTheme({
  palette: {
    primary: {
      main: '#0033a0', // KRA blue
    },
    secondary: {
      main: '#ff6d00', // Accent orange
    },
    background: {
      default: '#f9f9f9',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});


const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
   <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

