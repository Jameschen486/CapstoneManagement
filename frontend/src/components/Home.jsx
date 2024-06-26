import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';
import '../css/Home.css';

const Home = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    try {
      const response = await fetch('http://localhost:5001/login', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Login successful:', data);
        // Store the token in localStorage
        localStorage.setItem('token', data.token);

        // Decode the token to get the role
        const decodedToken = jwt_decode(data.token);
        const userRole = decodedToken.role;
        console.log('Decoded role:', userRole);
        localStorage.setItem('role', userRole);

        navigate('/dashboard');
      } else {
        const errorData = await response.json();
        alert(errorData.error || 'Invalid login credentials');
      }
    } catch (error) {
      console.error('Error logging in:', error);
      alert('An error occurred during login. Please try again.');
    }
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
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
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
