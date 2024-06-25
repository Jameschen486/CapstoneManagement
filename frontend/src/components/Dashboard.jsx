import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear any stored user information (e.g., token)
    localStorage.removeItem('token'); // Assuming you're storing the token in localStorage
    navigate('/');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>
      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Projects</h2>
          <p>Here you can manage your projects.</p>
        </div>
        <div className="dashboard-section">
          <h2>Messages</h2>
          <p>Here you can view your messages.</p>
        </div>
        <div className="dashboard-section">
          <h2>Notifications</h2>
          <p>Here you can view your notifications.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
