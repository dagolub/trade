import './App'
import './utils/ThemeContext'
import 'react'
import 'react-dom/client'
import 'react-router-dom'
import App
import React
import ReactDOM
import ThemeProvider
import { BrowserRouter as Router }

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <ThemeProvider>
        <App />
      </ThemeProvider>
    </Router>
  </React.StrictMode>
);
