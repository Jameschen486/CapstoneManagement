import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../css/Home.css';

const Home = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    alert(`Logged in with email: ${email}`);
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Capstone Compass</h1>
      </header>
      <div className="home-content">
        <div className="home-info">
          <img src="sailboat.png" alt="Sailboat" className="home-image" />
          <p>Capstone Compass guides you through your projects, connecting you with opportunities and collaboration</p>
        </div>
        <div className="login-form">
          <form onSubmit={handleLogin}>
            <input type="email" placeholder="Email address" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <button type="submit">Log In</button>
            <Link to="/forgot-password">Forgotten password?</Link>
          </form>
          <button className="register-button">
            <Link to="/register">Create New Account</Link>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
