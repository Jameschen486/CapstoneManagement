import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');

  useEffect(() => {
    // User role from localStorage
    const userRole = localStorage.getItem('role');
    if (userRole) {
      setRole(userRole);
    } else {
      // If no role is found, redirect to the home page or login page
      navigate('/');
    }
  }, [navigate]);

  const handleLogout = () => {
    // Clear any stored user information (e.g., token)
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/');
  };

  const renderDashboardContent = () => {
    switch (role) {
      case '0':
        return (
          <div className="dashboard-section">
            <div className='dashboard-header-row'>
                <h2>Student Dashboard</h2>
                <div className="dashboard-icons">
                    <div className="dashboard-icon notification-icon" title="Notifications">&#128276;</div>
                    <div className="dashboard-icon message-icon" title="Messages">&#128488;</div>
                    <div className="dashboard-icon profile-icon" title="Profile">&#128100;</div>
                </div>
            </div>
            <p>Here you can manage your projects, view messages, and notifications.</p>
          </div>
        );
      case '1':
        return (
          <div className="dashboard-section">
            <h2>Client Dashboard</h2>
            <p>Here you can manage your projects, view messages, student preferences, and notifications.</p>
          </div>
        );
      case '2':
        return (
          <div className="dashboard-section">
            <h2>Tutor Dashboard</h2>
            <p>Here you can manage your students, view messages, and notifications.</p>
          </div>
        );
      case '3':
        return (
          <div className="dashboard-section">
            <h2>Admin Dashboard</h2>
            <p>Here you can manage the system, view messages, and notifications.</p>
          </div>
        );
      default:
        return (
          <div className="dashboard-section">
            <h2>Dashboard</h2>
            <p>Here you can manage your projects, view messages, and notifications.</p>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>
      <div className="dashboard-content">
        {renderDashboardContent()}
      </div>
    </div>
  );
};

export default Dashboard;
