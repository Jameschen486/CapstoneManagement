import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';
import Modal from './Modal';
import { BackButton } from './utils';

const Dashboard = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('userId');
  const [code, setCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    fetchUserData();
  }, [navigate]);

  const fetchUserData = async () => {
    console.log(userId);
    if (userId != null && token != null) {
      try {
        const response = await fetch(`http://localhost:5001/user?id=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const Userdata = await response.json();
        console.log('User data:', Userdata);
        setEmail(Userdata.email);
      } 
      catch (error) {
        console.error('Error fetching user data:', error);
      }
    }
  };

  const handleSubmitEmail = async (e) => {
    try {
      const formdata = new FormData();
      formdata.append('email', email);

      const response = await fetch(`http://localhost:5001/auth_reset_request`, {
        method: 'POST',
        body: formdata
      });
      const output = await response.json();
      console.log(output)
    }
    catch (error) {
      console.error('Error Sending Email:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');

      const formdata = new FormData();
      formdata.append('email', email);
      formdata.append('reset_code', code);
      formdata.append('new_password', newPassword);

      const response = await fetch(`http://localhost:5001/auth_password_reset`, {
        method: 'POST',
        headers: {
          // Authorization: `Bearer ${token}`,
        },
        body: formdata
      });
      const output = await response.json();
      console.log(output)
    }
    
    catch (error) {
      console.error('Error', error);
    }
    // useLogout(navigate);
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <BackButton />
      </header>
      <div className="dashboard-content">
        <div className="dashboard-section">
            <div className='dashboard-header-row'>
                <h2>Reset</h2>
                <p>Type your email here to recieve reset code:</p>
                <input type="text"  name="Email" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                <button onClick={(e) => handleSubmitEmail(e)}> Submit </button>
            </div>
            <div className='dashboard-header-row'>
                <p>Code:
                  <input type="text"  name="Code" onChange={(e) => setCode(e.target.value)}></input>
                </p>
                <p>New Password:
                  <input type="text" name="Password" onChange={(e) => setNewPassword(e.target.value)}></input>
                </p>
                <button onClick={(e) => handleSubmit(e)}> Update </button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
