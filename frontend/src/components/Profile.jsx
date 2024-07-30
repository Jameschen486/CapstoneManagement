import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';
import Modal from './Modal';

const Dashboard = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [hasData, setHasData] = useState(false);
  const [user, setUser] = useState({});
  const [showNotificationModal, setShowNotificationModal] = useState(false);
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");

  useEffect(() => {
    // User role from localStorage
    const userRole = localStorage.getItem('role');
    if (userRole) {
      setRole(userRole);
    } else {
      // If no role is found, redirect to the home page or login page
      navigate('/');
    }
    fetchUserData();
  }, [navigate]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      // Fetch user data
      const response = await fetch(`http://localhost:5001/user?id=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const Userdata = await response.json();
      setHasData(true)
      console.log('User data:', Userdata);
      setUser({
        first: Userdata.first_name,
        last: Userdata.last_name,
        email: Userdata.email,
      });
      setFirstName(Userdata.first_name);
      setLastName(Userdata.last_name);
      setEmail(Userdata.email);
    //   {"userid" : user.userid, "email" : user.email, "first_name" : user.first_name, "last_name" : user.last_name, "role" : user.role, "groupid" : user.groupid}
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
    return;
  };

  // console.log('User data:', userData);
  console.log("outside Async");
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');

      const formdata = new FormData();
      formdata.append('user_id', userId);
      formdata.append('firstName', firstName);
      formdata.append('lastName', lastName,);

      const response = await fetch(`http://localhost:5001/updateUserName`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formdata
      });
      const output = await response.json();
      console.log(output)
    }
    
    catch (error) {
      console.error('Error updating user data:', error);
    }
    // Add your form submission logic here
};
  const handleLogout = () => {
    // Clear any stored user information (e.g., token)
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('userId');
    localStorage.removeItem('groupId');
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
            <div className='dashboard-header-row'>
                <h2>Profile</h2>
                {console.log(user.first)}
                {/* <p>{user && user.map && user.map((data) => {
                  
                  return(
                    <p> {user.first}</p>
                  )
                })}</p> */}
                
                <p>Firstname:
                  <input type="text"  name="First" placeholder={firstName} onChange={(e) => setFirstName(e.target.value)}></input>
                </p>
                
                <p>LastName:
                <input type="text" name="Last" placeholder={lastName} onChange={(e) => setLastName(e.target.value)}></input>
                </p>
                
                <p>Email:
                <p>{email}</p>
                </p>
                <button onClick={(e) => handleSubmit(e)}> update </button>
                
            </div>
        </div>
      </div>
      <Modal show={showNotificationModal} handleClose={() => setShowNotificationModal(false)} title="Notifications">
        <p>No notifications yet.</p>
      </Modal>
      <Modal show={showMessageModal} handleClose={() => setShowMessageModal(false)} title="Messages">
        <p>No messages yet.</p>
      </Modal>
    </div>
  );
};

export default Dashboard;
