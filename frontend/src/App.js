import React from 'react';
import './css/App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Register from './components/Register';
import Reset from './components/Reset';
import Dashboard from './components/Dashboard';
import Groups from './components/Groups';
import CreateGroup from './components/CreateGroup';
import Profile from './components/Profile';
import Projects from './components/Projects';
import CreateProject from './components/CreateProject';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile/>} />
          <Route path="/reset" element={<Reset/>} />
          <Route path="/" exact element={<Home />} />
          <Route path="/groups" element={<Groups />} />
          <Route path="/create-group" element={<CreateGroup />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/create" element={<CreateProject />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
