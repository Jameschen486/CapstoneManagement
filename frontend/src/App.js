import React from 'react';
import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Groups from './components/Groups';
import CreateGroup from './components/CreateGroup';
import Profile from './components/Profile';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile/>} />
          <Route path="/" exact element={<Home />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/create-group" element={<CreateGroup />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
