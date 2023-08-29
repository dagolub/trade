import React from 'react'; // Import React properly
import ReactDOM from 'react-dom'; // Import ReactDOM properly
import { BrowserRouter as Router } from 'react-router-dom'; // Import BrowserRouter properly
import ThemeProvider from './utils/ThemeContext'; // Import ThemeProvider properly
import App from './App'; // Import App properly

// Use ReactDOM.render instead of ReactDOM.createRoot().render
ReactDOM.render(
  <React.StrictMode>
    <Router>
      <ThemeProvider>
        <App />
      </ThemeProvider>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
);